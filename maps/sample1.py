import folium

# Define a location (latitude, longitude)
location_point = (53.540559, 8.5836)  # Example: San Francisco

# Create a folium map centered around the location
map_osm = folium.Map(location=location_point, zoom_start=15)

# Add a marker to the map
folium.Marker(location=location_point, popup='Location Point').add_to(map_osm)

# Display the map
map_osm.save('map_osm.html')  # Save the map as an HTML file
map_osm
