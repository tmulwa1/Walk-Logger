from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    # Calculates the straight-line distance between two GPS points
    radius = 6731 
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    # Haversine formula accounts for Earth's curvy nature
    angle = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return radius * 2 * atan2(sqrt(angle), sqrt(1-angle))

def calculate_distance(df):
    # Loops through points and adds up total distance
    total = 0
    for i in range(1, len(df)):
        total += haversine(df['lat'].iloc[i-1], 
                           df['lon'].iloc[i-1], 
                           df['lat'].iloc[i], 
                           df['lon'].iloc[i])

    return round(total, 2)

def calculate_duration(df):
    # Subtracts timestamps to get total time
    delta = df['time'].iloc[-1] - df['time'].iloc[0]
    total_minutes = delta.total_seconds() / 60
    hours = int(total_minutes // 60)
    minutes = int(total_minutes % 60)
    return hours, minutes, round(total_minutes, 1)

def calculate_pace(distance_km, total_minutes):
    if distance_km == 0:
        return 0
    
    pace = total_minutes / distance_km
    mins = int(pace)
    secs = int((pace - mins) * 60)
    return f"{mins}:{secs:02d} min/km"

def calculate_elevation(df):
    # Counts uphill sections
    gain = 0
    for i in range(1, len(df)):
        diff = df['elevation'].iloc[i] - df['elevation'].iloc[i-1] 
        if diff > 0:
            gain += diff
    
    return round(gain, 1)

def get_stats(df):
    distance = calculate_distance(df)
    hours, minutes, total_minutes = calculate_duration(df)
    pace = calculate_pace(distance, total_minutes)
    elevation = calculate_elevation(df)

    return {'distance_km': distance,
            'duration': f"{hours}h {minutes}m",
            'pace': pace,
            'elevation': elevation,
            'total_points': len(df)}