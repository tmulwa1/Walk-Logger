import gpxpy
import pandas as pd

def parse_gpx(filepath):
    with open(filepath, 'r') as file:
        gpx = gpxpy.parse(file)

    points = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append({'lat': point.latitude, 'lon': point.longitude, 'elevation': point.elevation, 'time': point.time})

    df = pd.DataFrame(points)
    df['time'] = pd.to_datetime(df['time'], utc=True)
    return df

def get_metadata(filepath):   
    with open(filepath, 'r') as file:
        gpx = gpxpy.parse(file)

    if gpx.tracks[0].name:
        name = gpx.tracks[0].name 
    else:
        name = "Unnamed Walk"

    return name