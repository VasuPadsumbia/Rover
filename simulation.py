import Layers.L1_App.navigation.manoeuvre as manoeuvre
from helper import map_coordinate_path
from Layers.L1_App.navigation.create_map_network import MapHandler
import os, sys, json, time
from json.decoder import JSONDecodeError

import matplotlib.pyplot as plt

class Navigation:
    def __init__(self, speed):
        self.speed = speed
        self.path = map_coordinate_path()
        self.manoeuvre = manoeuvre.Target_manoeuvre(speed, self.path)
        
    
    def navigate(self):
        coordinates = self.manoeuvre.manoeuvre()
        return coordinates


simulation = Navigation(0.0001)
coordinates = simulation.navigate()
config_path = f'{os.path.abspath(os.path.dirname(__file__))}/Layers/L2_Data/gps_data.json'

try:
    with open(config_path, "r") as config_file:
        data = json.load(config_file)
        lat = data['lat']
        lon = data['lon']
        config_file.close()
        
except JSONDecodeError as e:
    print("Failed to read JSON, return code %d\n", e) 

centre_point = (lat, lon)
print(centre_point)
Destination = (53.540966, 8.585301) 
print(Destination)
map = MapHandler(type='all', destination=Destination, coordinates=centre_point)
print(f'create area graph(): {map.create_area_graph()}')
print(f'find shortest path between two points(): {map.find_shortest_path_between_two_points()}')
print(f'cartesian coordinates(): {map.cartesian_coordinates()}')
print(f'logging coordinates(): {map.log()}')
print(f'coordinates: {coordinates}')
print(f'plot graph shortest route(): {map.plot_graph_shortest_route(coordinates)}')
#time.sleep(3)
#print(f'plot graph shortest route(): {map.plot_graph_shortest_route()}')