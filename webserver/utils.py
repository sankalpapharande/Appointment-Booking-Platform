from datetime import datetime, timedelta, time


def generate_hours(start, end, delta):
    startRange = start + (datetime.min - start) % delta
    endRange = end
    
    times = []
    ts = startRange
    while ts <= endRange:
        times.append(time(ts.hour, ts.minute, ts.second))
        ts += timedelta(minutes=30)

    return sorted(times)