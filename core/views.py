from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PowerReadingSerializer
from .services.alerts import check_alerts
from .models import Device, PowerReading, Alert
from .services.analytics import calculate_drain_rate, calculate_efficiency, calculate_time_remaining

class IngestReadingView(APIView):
    def post(self, request):
        serializer = PowerReadingSerializer(data=request.data)
        if serializer.is_valid():
            reading = serializer.save()
            check_alerts(reading.device, reading)
            return Response({'status': 'reading saved'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeviceStatusView(APIView):
    def get(self, request, device_id):
        try:
            device = Device.objects.get(id=device_id)
            reading = PowerReading.objects.filter(device=device).latest('timestamp')
            recent = list(PowerReading.objects.filter(device=device).order_by('-timestamp')[:10])

            drain_rate = calculate_drain_rate(recent)
            time_remaining = calculate_time_remaining(reading.battery_level, drain_rate)
            efficiency = calculate_efficiency(reading.solar_input, reading.power_consumption)

            return Response({
                'device': device.name,
                'battery_level': reading.battery_level,
                'solar_input': reading.solar_input,
                'power_consumption': reading.power_consumption,
                'timestamp': reading.timestamp,
                'efficiency_pct': efficiency,
                'drain_rate_per_interval': drain_rate,
                'estimated_minutes_remaining': time_remaining,
            })
        except Device.DoesNotExist:
            return Response({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)
        except PowerReading.DoesNotExist:
            return Response({'error': 'No readings yet'}, status=status.HTTP_404_NOT_FOUND)
        
class DeviceHistoryView(APIView):
    def get(self, request, device_id):
        try:
            device = Device.objects.get(id=device_id)
            readings = PowerReading.objects.filter(device=device).order_by('-timestamp')[:50]
            data = [{
                'battery_level': r.battery_level,
                'solar_input': r.solar_input,
                'power_consumption': r.power_consumption,
                'timestamp': r.timestamp, 
            } for r in readings]
            return Response(data)
        except Device.DoesNotExist:
            return Response({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)
        
class DeviceAlertsView(APIView):
    def get(self, request, device_id):
        try:
            device = Device.objects.get(id=device_id)
            alerts = Alert.objects.filter(device=device).order_by('-created_at')[:20]
            data = [{
                'alert_type': a.alert_type,
                'message': a.message,
                'resolved': a.resolved,
                'created_at': a.created_at,
            } for a in alerts]
            return Response(data)
        except Device.DoesNotExist:
            return Response({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)