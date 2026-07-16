import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, redirect, request, url_for
from src.parser import parse_gpx, get_metadata
from src.stats import get_stats, haversine
from src.maps import create_heatmap, create_map, save_map
from src.database import initialise_db, save_walk, get_walks, get_walk_id

app = Flask(__name__)
upload_folder = os.path.join(os.path.dirname(__file__), 'data', 'uploads')

@app.route('/')
def dashboard():
    walks = get_walks
    
    # Calculating overall statistics for summary 
    total_walks = len(walks)
    total_distance = round(sum(walk.distance_km  for walk in walks), 2)
    total_minutes = 0

    for walk in walks:
        # Duration is stored in hours and minutes, so have to convert it
        parts = walk.duration.replace('h', '').replace('m', '').split()
        total_minutes += int(parts[0]) * 60 + int (parts[1])

    total_hours = total_minutes // 60
    total_mins = total_minutes % 60
    total_time = f"{total_hours}h {total_mins}m"

    return render_template('index.html', walks = walks, total_walks = total_walks, total_distance = total_distance, total_time = total_time)

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('gpx')

        # Validates that a file was submitted
        if not file or file.filename == '':
            return render_template('upload.html', error = 'Please choose a GPX file.')
        
        if not file.filename.endswith('.gpx'):
            return render_template('upload.html', error = 'File must be a .gpx file.')
        
        # Saves file to data/uploads
        filename = file.filename
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        # Parses data and saves to database
        df = parse_gpx(filepath)
        name = get_metadata(filepath)
        stats = get_stats(df)
        date = df['time'].iloc[0].strftime('%Y-%m-%d')

        return redirect(url_for('dashboard'))
    
    return render_template('upload.html')

@app.route('/walk/<int:walk_id')
def walk(walk_id):
    walk = get_walk_id(walk_id)
    if not walk:
        return "Walk not found", 404
    
    return render_template('walk.html', walk=walk)

@app.route('/map/<int:walk_id>')
def route_map(walk_id):
    walk = get_walk_id(walk_id)
    filepath = os.path.join(upload_folder, walk.filename)
    df = parse_gpx(filepath)
    m = create_map(df, walk.name)
    return m.get_root().render()

@app.route('/elevation/<int:walk_id>')
def elevation(walk_id):
    import plotly.express as px
    walk = get_walk_id(walk_id)
    filepath = os.path.join(upload_folder, walk.filename)
    df = parse_gpx(filepath)

    distances = [0]
    for i in range(1, len(df)):
        d = haversine(df['lat'].iloc[i-1], df['lon'].iloc[i-1], df['lat'].iloc[i], df['lon'].iloc[i])
        distances.append(distances[-1] + d)
    df['distance_km'] = distances

    figure = px.area(df, x='distance_km', y='elevation', labels={'distance_km': 'Distance (km)', 'elevation': 'Elevation (m)'}, color_discrete_sequence=['#1D9E75'])
    figure.update_layout(plot_bgcolor='white', showlegend=False, margin=dict(t=20, b=20))
    figure.update_traces(fill='tozeroy', fillcolor='rgba(29, 158, 117, 0.5)')
    return figure.to_html(full_html=False)

@app.route('/heatmap')
def heatmap():
    walks = get_walks()
    all_coords = []
    for walk in walks:
        filepath = os.path.join(upload_folder, walk.filename)
        if os.path.exists(filepath):
            df = parse_gpx(filepath)
            all_coords += list(zip(df['lat'], df['lon']))
    
    heatmap = create_heatmap(all_coords)
    return heatmap.get_root().render()
    
if __name__ == '__main__':
    initialise_db()
    app.run(debug=True)