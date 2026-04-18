def calculate_efficiency(solar_input, power_consumption):
    if power_consumption == 0:
        return 0.0
    return round((solar_input / power_consumption) * 100, 2)

def calculate_drain_rate(readings):
    """
    Expects a list/queryset of PowerReading ordered by timestamp descending.
    Returns average battery drop per reading interval.
    """
    if len(readings) < 2:
        return None
    
    levels = [r.battery_level for r in readings]
    drops = [levels[i] - levels[i + 1] for i in range(len(levels) - 1)]
    avg_drain = sum(drops) / len(drops)
    return round(avg_drain, 2)

def calculate_time_remaining(battery_level, drain_rate, interval_seconds=3):
    """
    Estimates time remaining in minutes based on drain rate per interval.
    """
    if not drain_rate or drain_rate <= 0:
        return None
    
    intervals_remaining = battery_level / drain_rate
    seconds_remaining = intervals_remaining * interval_seconds
    minutes_remaining = seconds_remaining / 60
    return round(minutes_remaining, 2)