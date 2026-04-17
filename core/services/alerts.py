from core.models import Alert

def check_alerts(device, reading):
    alerts = []

    if reading.battery_level < 20:
        alert = Alert.objects.create(
            device=device,
            alert_type='LOW_BATTERY',
            message=f"Battery critically low at {reading.battery_level}%"
        )
        alerts.append(alert)

    if reading.power_consumption > 150:
        alert = Alert.objects.create(
            device=device,
            alert_type='HIGH_USAGE',
            message=f"High power consumption detected: {reading.power_consumption}W"
        )
        alerts.append(alert)

    if reading.solar_input > 0 and (reading.power_consumption / reading.solar_input) > 1.5:
        alert = Alert.objects.create(
            device=device,
            alert_type='INEFFICIENCY',
            message=f"Consumption is {reading.power_consumption}W vs solar input {reading.solar_input}W"
        )
        alerts.append(alert)

    return alerts