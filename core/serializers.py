from rest_framework import serializers
from .models import PowerReading

class PowerReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerReading
        fields = ['device', 'battery_level', 'solar_input', 'power_consumption']