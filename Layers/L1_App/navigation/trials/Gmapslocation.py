import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import osmnx as ox
import os
from PIL import Image
import matplotlib.patches as patches

# Your Google Map image file path
google_map_image_path = f'{os.path.abspath(os.path.join(os.path.dirname(__file__),""))}/sample_2.png'

# Load the Google Map image
google_map_img = Image.open(google_map_image_path)

# Set the bounding box directly
north, south, east, west = bbox = (53.54128, 53.53914, 8.58101, 8.58571)

# Define the specific point (latitude, longitude) you're interested in
point = (53.54036, 8.58139)  # Bremerhaven, Germany

# Get the OSMnx network for the specific point
graph = ox.graph_from_bbox(*bbox, network_type="all")

# Plot the OSMnx map
fig, ax = ox.plot_graph(graph, show=False, close=False, bgcolor='None')

# Superimpose bounding box on the OSMnx map
rect = patches.Rectangle(
    (bbox[0], bbox[1]),
    bbox[2] - bbox[0],
    bbox[3] - bbox[1],
    linewidth=2,
    edgecolor='r',
    facecolor='none'
)

""" # Create an OffsetImage to superimpose the Google Map image
imagebox = OffsetImage(google_map_img, zoom=1.5, resample=True)

# Create an AnnotationBbox to add the OffsetImage
ab = AnnotationBbox(imagebox, (west, south), (east, north), pad=0, frameon=False)
# Plot the OSMnx network
fig, ax = ox.plot_graph(ox.project_graph(graph), show=True, bbox=ab, close=False)"""

ax.add_artist(rect) 
ax.imshow(google_map_img, extent=(bbox[0], bbox[2], bbox[1], bbox[3]))

# Display the map
plt.show()

