import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.express as px
import plotly.graph_objects as go

#Input variables
file_path = input("Enter the file path to the Hiking data (csv): ")
output_path = input("Enter the directory where you want to save the analysis: ")

# Load csv into a Pandas DataFrame
data = pd.read_csv(file_path)

# Calculations for labels and plotting below
max_elevation = data.Elevation.max()
min_elevation = data.Elevation.min()
start_elevation = data.iloc[0].Elevation
total_elevation = max_elevation - min_elevation
half_way = data.shape[0] / 2
first_quarter = data.shape[0] / 4
third_quarter = first_quarter * 3
thirdQ_elevation = data.iloc[int(third_quarter)].Elevation
firstQ_elevation = data.iloc[int(first_quarter)].Elevation

# Elevation Line Chart
fig, ax = plt.subplots(figsize=(10,8))

ax.plot(data.Elevation, color='orange', linestyle="-")
ax.axvline(half_way, color='blue', linestyle=":")
ax.axvline(first_quarter, color='red', linestyle=":")
ax.axvline(third_quarter, color='green', linestyle=":")

ax.text(half_way + (first_quarter*0.1), min_elevation + 20, 'Q2', color='blue', ha='center')
ax.text(first_quarter - (first_quarter*0.1), min_elevation + 20, 'Q1', color='red', ha='center')
ax.text(third_quarter + (first_quarter*0.1), min_elevation + 20, 'Q3', color='green', ha='center')

ax.set_title(f"Hike Elevation Overview: {total_elevation} meters Total Elevation Gain")
ax.set_xlabel("Coordinate Snapshots (1 every 3-5 seconds)")
ax.set_ylabel("Elevation (meters)")

plt.savefig(f"{output_path}/Hike_Analysis.png")
plt.close()

# 2D Scatter Plot
latitude = data['Latitude']
longitude = data['Longitude']
elevation = data['Elevation']

fig, ax = plt.subplots(figsize=(10,8))
scatter = ax.scatter(longitude, latitude, c=elevation, cmap='viridis')
plt.colorbar(scatter, label='Elevation (m)')
ax.set_title('Latitude, Longitude, and Elevation - 2D Scatter Plot')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
plt.savefig(f"{output_path}/Scatterplot_2d.png")
plt.close()

# 3D Scatter Plot
fig = px.scatter_3d(data, x='Longitude', y='Latitude', z='Elevation', color='Elevation')
fig.update_layout(
    title='Latitude, Longitude, and Elevation - 3D Scatter Plot',
    scene=dict(xaxis_title='Longitude', yaxis_title='Latitude', zaxis_title='Elevation')
)
fig.write_html(f"{output_path}/scatterplot_3d.html")

# Google Map Plot
center_lat = data['Latitude'].mean()
center_lon = data['Longitude'].mean()

fig = px.scatter_mapbox(data, lat='Latitude', lon='Longitude',
                        height=600, zoom=12, hover_name='Elevation')
fig.update_layout(
    mapbox_style='open-street-map',
    mapbox_center={'lat': center_lat, 'lon': center_lon},
    title='Google Earth Hike Overview'
)
fig.write_html(f"{output_path}/google_map.html")
