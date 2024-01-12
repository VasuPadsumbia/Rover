import os, json
from Layers.L1_App.navigation.create_map_network import MapHandler
from Layers.L1_App.sensor.dgps.DGPS import connect_pksi_dgps 
from json.decoder import JSONDecodeError


""" try:
    gps = connect_pksi_dgps()
    print(f'Getting Longitudenal and Latitude data: {gps.get_data()}')
    print(f'Logging Longitudenal and Latitude data: {gps.log()}')
except KeyboardInterrupt:
    pass 
 """

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
print(f'plot graph shortest route(): {map.plot_graph_shortest_route()}')
