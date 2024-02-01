from Layers.L1_App.sensor.dgps.DGPS import connect_pksi_dgps
from json.decoder import JSONDecodeError
import helper as helper
import json
import math
import matplotlib.pyplot as plt
from geopy.distance import geodesic
from matplotlib.animation import FuncAnimation

coordinates_path = helper.gps_path()
config_file_path = helper.config_path()
try:
    gps = connect_pksi_dgps(config_file_path)
    print(f'Getting Longitudenal and Latitude data: {gps.get_data()}')
    print(f'Logging Longitudenal and Latitude data: {gps.log()}')
except KeyboardInterrupt:
    pass 

try:
    with open(coordinates_path, "r") as config_file:
        data = json.load(config_file)
        lat = data['lat']
        lon = data['lon']
        config_file.close()
        
except JSONDecodeError as e:
    print("Failed to read JSON, return code %d\n", e)

centre_point = (lat, lon)
def distance(point1, point2):
    ''' Returns the distance between two points in kilometers'''
    lat1, lon1 = point1
    lat2, lon2 = point2

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = 6371 * c  # Radius of the Earth in kilometers

    return distance*1000
# # Initialize the plot
# plt.figure()
# plt.plot(lon, lat, 'ro', label='GPS Data')
# plt.plot(lon, lat, 'b-', label='Path')
# plt.plot(lon, lat, 'go', label='Initial Center Point')
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.title('GPS Data')
# plt.legend()

# Initialize list to store distances
distances = []
counter = 0
while True:
    # Import the necessary modules
    # ...

    # Initialize the plot
    plt.figure()
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('GPS Data')
    plt.legend()

    # Initialize list to store distances
    distances = []

    def update_plot(frame):
        # Get new GPS data
        new_lat, new_lon, height = gps.get_data()
        new = (new_lat, new_lon)
        print(new)
        # Calculate distance from initial point
        calculated_distance = ((geodesic((lat, lon), (new_lat, new_lon)).kilometers)*1000)
        print(calculated_distance)
        distances.append(calculated_distance)
        
        # Update the plot
        plt.plot(new_lon, new_lat, 'ro')
        #plt.plot(new_lon, new_lat, 'b-')    
        # Plot distance
        #plt.plot(distances, 'g-', label='Distance from initial point')
        
        # Draw box indicating distance from centre point and new coordinates
        plt.text(new_lon, new_lat, f'Distance: {calculated_distance:.2f} m', ha='center', va='bottom', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
        
        # Draw connecting line as the coordinates change
        plt.plot([lon, new_lon], [lat, new_lat], 'k--')

    # Create the animation
    animation = FuncAnimation(plt.gcf(), update_plot,frames=100, interval=100,repeat=False)
    # Show the plotq
    #plt.show()
    
    # Save the animation as a GIF
    animation.save('animation.gif', writer='pillow')
    counter += 1  # Increment the counter

    if counter == 100:
        animation.event_source.stop()  # Stop the animation
        plt.close()  # Close the plot window
    # Show the plot
    plt.show()
