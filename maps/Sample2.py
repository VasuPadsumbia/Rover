import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt

# Define a central point (latitude, longitude)
central_point = (53.540559, 8.5836)  # Example: New York City

# Create a street network graph within a specified distance (in meters) from the central point
G = ox.graph_from_point(central_point, dist=500, network_type="all", simplify=True)

# Get the bounding box for the street network
bbox = ox.utils_geo.bbox_from_point(center_point=central_point, distance=500, project_utm=True)

# Retrieve building footprints within the bounding box
buildings = ox.footprints.footprints_from_bbox(bbox[1], bbox[0], bbox[3], bbox[2], footprint_type='building', simplify=True)

# Create a 2D scatter plot for ground-level coordinates
fig, ax = plt.subplots(figsize=(10, 10))

# Plot the street network
ox.plot_graph(G, node_size=0, ax=ax, show=False, close=False)

# Plot building footprints
buildings.plot(ax=ax, facecolor='khaki', alpha=0.7)

# Set axis labels
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

plt.title('Street Network with Building Footprints')
plt.show()
