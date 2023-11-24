import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from maps.create_map_network import create_map_network
from sensor.dgps.DGPS import *
import json



config_path = f'{os.path.abspath(os.path.join(os.path.dirname(__file__),""))}/map_coordinates.json'

try:
    with open(config_path, "r") as config_file:
        data = json.load(config_file)
        lat = data['lat']
        lon = data['lon']
        config_file.close()
        
except JSONDecodeError as e:
    print("Failed to read JSON, return code %d\n", e)

centre_point = (lat, lon)
Destination = (53.517991, 8.60)

"""try:
    gps = connect_pksi_dgps()
    print(f'Getting Longitudenal and Latitude data: {gps.get_data()}')

except KeyboardInterrupt:
    pass
"""

map = create_map_network('Bremerhaven,Germany', 'walk', centre_point, Destination)

print(f'create street network(): {map.create_street_network()}')
print(f'create area graph(): {map.create_area_graph()}')
print(f'find shortest path between two points(): {map.find_shortest_path_between_two_points()}')
print(f'cartesian coordinates(): {map.cartesian_coordinates()}')
print(f'plot graph shortest route(): {map.plot_graph_shortest_route()}')
