import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from maps.create_map_network import create_map_network

centre_point = lat,lon = (53.540559, 8.5836)
Destination = (53.55, 8.59)
map = create_map_network('Bremerhaven,Germany', 'walk', centre_point, Destination)

print(f'create street network(): {map.create_street_network()}')
print(f'create area graph(): {map.create_area_graph()}')
print(f'find shortest path between two points(): {map.find_shortest_path_between_two_points()}')
print(f'plot graph shortest route(): {map.plot_graph_shortest_route()}')
print(f'cartesian coordinates(): {map.cartesian_coordinates()}')