import osmnx as ox
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define a central point (latitude, longitude)
central_point = (53.540559, 8.5836)  # Example: New York City

# Create a street network graph within a specified distance (in meters) from the central point
G = ox.graph_from_point(central_point, dist=500, network_type="all", simplify=True)

# Extract node coordinates
nodes, edges = ox.graph_to_gdfs(G)

# Generate random elevation data for demonstration purposes
nodes['elevation'] = np.random.uniform(0, 100, len(nodes))

# Set the threshold for ground level (adjust as needed)
ground_threshold = 10

# Filter points for ground level only
ground_points = nodes[nodes['elevation'] <= ground_threshold]

# Save point cloud data to a JSON file
json_file_path = 'point_cloud_data.json'
ground_points[['x', 'y', 'elevation']].to_json(json_file_path, orient='records', lines=True)

print(f"Point cloud data saved to {json_file_path}")

# Create a 3D scatter plot
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(ground_points['x'], ground_points['y'], ground_points['elevation'], c=ground_points['elevation'], cmap='viridis', s=1)

# Set axis limits
ax.set_xlim(ground_points['x'].min(), ground_points['x'].max())
ax.set_ylim(ground_points['y'].min(), ground_points['y'].max())
ax.set_zlim(ground_points['elevation'].min(), ground_points['elevation'].max())

# Set axis labels
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Elevation')

# Add colorbar
cbar = fig.colorbar(scatter, label='Elevation')

plt.title('Point Cloud Visualization')
plt.show()