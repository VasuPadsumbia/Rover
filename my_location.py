import os, json
from Layers.L1_App.navigation.create_map_network import MapHandler
from Layers.L1_App.sensor.dgps.DGPS import connect_pksi_dgps 
from json.decoder import JSONDecodeError
import helper as helper

coordinates_path = helper.gps_path()
#coordinates_path = f'{os.path.abspath(os.path.join(os.path.dirname(__file__),))}\Layers\L2_Data\gps_data.json'
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
print(centre_point)
Destination = (53.540966, 8.585301) 
print(Destination)
map = MapHandler(type='all', destination=Destination, coordinates=centre_point)
print(f'Getting map data: {map.get_map()}')
