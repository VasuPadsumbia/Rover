import osmnx as ox
import folium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Define a location (latitude, longitude)
location_point = (37.7749, -122.4194)  # Example: San Francisco

# Download the street network for the specified location within a distance of 500 meters
G = ox.graph_from_point(location_point, dist=500, network_type="all")

# Create a folium map centered around the location
map_osm = folium.Map(location=[location_point[0], location_point[1]], zoom_start=15)

# Plot the street network on the folium map
ox.plot_graph_folium(G, graph_map=map_osm, popup_attribute='name', edge_color='k', edge_width=2)

# Save the folium map as an HTML file
html_file_path = 'osmnx_folium_map.html'
map_osm.save(html_file_path)

# Set the path to the ChromeDriver executable
chrome_driver_path = '/path/to/chromedriver'

# Configure Chrome to run in headless mode
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration to prevent issues

# Start Chrome browser
driver = webdriver.Chrome(options=chrome_options, service_args=['--executable-path=' + chrome_driver_path])

# Open the HTML file in the browser
driver.get(f'file://{html_file_path}')

# Wait for some time to ensure that the map is loaded (you may need to adjust this)
driver.implicitly_wait(10)

# Take a screenshot and save it as an image
driver.save_screenshot('output_image.png')

# Close the browser
driver.quit()

print('Image saved: output_image.png')
