import osmnx as ox
import geopandas as gpd
import folium
from shapely.geometry import Point
import matplotlib.pyplot as plt

# Define a bounding box for the map
north, south, east, west = 37.8, 37.75, -122.4, -122.45

# Download street network data from OSM within the bounding box
graph = ox.graph_from_bbox(north, south, east, west, network_type='all_private')

# Plot the street network
ox.plot_graph(ox.project_graph(graph))

# Identify and mark obstacles on the map
# For demonstration purposes, let's assume obstacles are represented as points
obstacle_data = {
    'name': ['Obstacle1', 'Obstacle2', 'Obstacle3'],
    'latitude': [37.777, 37.755, 37.770],
    'longitude': [-122.415, -122.430, -122.405],
}

# Create a GeoDataFrame from the obstacle data
obstacle_gdf = gpd.GeoDataFrame(
    obstacle_data,
    geometry=gpd.points_from_xy(obstacle_data['longitude'], obstacle_data['latitude'])
)

# Plot the obstacles on the map
obstacle_gdf.plot(marker='o', color='red', markersize=50, alpha=0.7)

# Display the map with obstacles
plt.show()
