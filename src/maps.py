import folium
from folium.plugins import HeatMap

def create_map(df, name):
    # Calculate centre point of walk to focus map there
    centre_lat = df['lat'].mean()
    centre_lon = df['lon'].mean()

    m = folium.Map(location=[centre_lat, centre_lon], zoom_start=14)
    coordinates = list(zip(df['lat'], df['lon']))

    # Drawing route on map
    folium.PolyLine(coordinates, color = '#1D9E75', weight = 4, opacity = 0.8, tooltip = name).add_to(m)

    #Markers at the start and end of the walk
    folium.Marker(location=[df['lat'].iloc[0], df['lon'].iloc[0]], popup='Start', icon=folium.Icon(color='green', icon='play')).add_to(m)
    folium.Marker(location=[df['lat'].iloc[-1], df['lon'].iloc[-1]], popup='End', icon=folium.Icon(color='red', icon='stop')).add_to(m)

    return m

def create_heatmap(all_coordinates):
    if not all_coordinates:
        return None
    
    # Centre heatmap using average position
    centre_lat = sum(c[0] for c in all_coordinates) / len(all_coordinates)
    centre_lon = sum(c[1] for c in all_coordinates) / len(all_coordinates)

    # Takes list of [lat, lon] pairs
    m = folium.Map(location=[centre_lat, centre_lon], zoom_start=13)
    HeatMap(all_coordinates, radius=10, blur=15).add_to(m)
    return m

def save_map(m, filepath):
    # Saves map as HTML file 
    m.save(filepath)
    print(f"Map saved to {filepath}")