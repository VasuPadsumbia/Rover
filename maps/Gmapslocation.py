import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import osmnx as ox

# Your Google Map image file path
google_map_image_path = "/home/outdoor/Rover/maps/sample.png"

# Load the Google Map image
google_map_img = mpimg.imread(google_map_image_path)

# Define the specific point (latitude, longitude) you're interested in
point = (53.54036, 8.58139)  # Bremerhaven, Germany

# Get the OSMnx network for the specific point
graph = ox.graph_from_point(point, network_type="all", dist=200, dist_type='bbox')

# Plot the OSMnx network
fig, ax = ox.plot_graph(ox.project_graph(graph), show=False, close=False)

# Set the bounding box directly
north, south, east, west = bbox = (53.54040, 53.53938, 8.58198, 8.58451)

# Create an OffsetImage to superimpose the Google Map image
imagebox = OffsetImage(google_map_img, zoom=1.5, resample=True)

# Create an AnnotationBbox to add the OffsetImage
ab = AnnotationBbox(imagebox, (west, south), (east, north), pad=0, frameon=False)
ax.add_artist(ab)

# Display the map
plt.show()

