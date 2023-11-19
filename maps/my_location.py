import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from maps.create_map_network import create_map_network

centre_point = lat,lon = (53.540559, 8.5836)
Destination = (53.55, 8.59)
map = create_map_network('Bremerhaven,Germany', Walk, centre_point, Destination)

print(f'create street network(): {map.create_street_network()}')
print(f'create area graph(): {map.create_area_graph()}')
print(f'find shortest path between two points(): {map.find_shortest_path_between_two_points()}')
print(f'plot graph shortest route(): {map.plot_graph_shortest_route()}')
print(f'cartesian coordinates(): {map.cartesian_coordinates()}')

"""ox.settings.log_console=True
ox.settings.use_cache=True

centre_point = lat,lon = (53.540559, 8.5836)
optimizer = 'time'        # 'length','time'# create graph from OSM within the boundaries of some 
graph = ox.graph_from_point(centre_point, dist=500, dist_type='bbox', 
                            network_type='walk')#, 
                            #simplify=True, 
                            #retain_all=False, 
                            #truncate_by_edge=False, 
                            #clean_periphery=None)# find the nearest node to the start location

graph_map=ox.plot_graph_folium(graph, popup_attribute='name', edge_width=1)
#fig, ax = ox.plot_graph(graph, show=False, close=False, 
#                       bgcolor='w',node_color='b', node_size=2)
plt.plot(lon, lat, marker="o", markersize=5, markeredgecolor="red", markerfacecolor="red", alpha=0.5)
plt.show()
"""