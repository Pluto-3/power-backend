from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PowerReadingSerializer
from .services.alerts import check_alerts

class IngestReadingView(APIView):
    def post(self, request):
        serializer = PowerReadingSerializer(data=request.data)
        if serializer.is_valid():
            reading = serializer.save()
            check_alerts(reading.device, reading)
            return Response({'status': 'reading saved'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)