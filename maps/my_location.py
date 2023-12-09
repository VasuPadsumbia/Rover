import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from create_map_network import MapHandler
import sys
#sys.path.append('/home/outdoor/Rover')
""" sys.path.append('/home/vasu/Rover')
from sensor.dgps.DGPS import connect_pksi_dgps """
import json
from json.decoder import JSONDecodeError
import os


config_path = f'{os.path.abspath(os.path.dirname(__file__))}/gps_data.json'

try:
    with open(config_path, "r") as config_file:
        data = json.load(config_file)
        lat = data['lat']
        lon = data['lon']
        config_file.close()
        
except JSONDecodeError as e:
    print("Failed to read JSON, return code %d\n", e) 


centre_point = (lat, lon)
Destination = (53.540966, 8.585301) 

""" try:
    gps = connect_pksi_dgps()
    print(f'Getting Longitudenal and Latitude data: {gps.get_data()}')

except KeyboardInterrupt:
    pass """


map = MapHandler(type='walk', destination=Destination, coordinates=centre_point)
print(f'create area graph(): {map.create_area_graph()}')
print(f'find shortest path between two points(): {map.find_shortest_path_between_two_points()}')
print(f'cartesian coordinates(): {map.cartesian_coordinates()}')
print(f'logging coordinates(): {map.log()}')
print(f'plot graph shortest route(): {map.plot_graph_shortest_route()}')
