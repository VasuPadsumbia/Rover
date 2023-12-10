import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

ox.settings.log_console=True
ox.settings.use_cache=True# define the start and end locations in latlng
start_latlng = (53.540559, 8.5836)
end_latlng = (53.50, 8.50)# location where you want to find your route
place     = 'Hochschule Bremerhaven, Bremerhaven, Germany'# find shortest route based on the mode of travel
mode      = 'walk'        # 'drive', 'bike', 'walk'# find shortest path based on distance or time
optimizer = 'time'        # 'length','time'# create graph from OSM within the boundaries of some 
# geocodable place(s)
graph = ox.graph_from_place(place, network_type = mode)# find the nearest node to the start location

orig_node = ox.distance.nearest_nodes(graph, start_latlng[1],
                                      start_latlng[0])# find the nearest node to the end location

dest_node = ox.distance.nearest_nodes(graph, end_latlng[1],
                                      end_latlng[0])#  find the shortest path

shortest_route = nx.shortest_path(graph,
                                  orig_node,
                                  dest_node,
                                  weight=optimizer)
fig, ax = ox.plot_graph_route(graph,
                              shortest_route,
                              save=True)

#shortest_route_map = ox.utils_graph.graph_to_gdfs(graph, nodes=True, edges=True, node_geometry=True, fill_edge_geometry=True)
#ox.plot_graph(graph,node_color='r')
#bbox = ox.utils_geo.bbox_from_point(point=(37.78497, -122.43327), dist=700)
#fig, ax = ox.plot_graph_route(graph, route, bbox = bbox, route_linewidth=6, node_size=0, bgcolor='k')
#routes = ox.k_shortest_paths(graph, orig_node, dest_node, k=5, weight='length')
#bbox = ox.utils_geo.bbox_from_point(point=(37.78497, -122.43327), dist=700)
#fig, ax = ox.plot_graph_routes(graph, list(routes), bbox = bbox, route_colors='r', route_linewidth=2, node_size=0)
#origin_node = list(graph.nodes())[0]
#destination_node = list(graph.nodes())[-1]
#route = ox.shortest_path(graph, origin_node,destination_node)
#graph_map = ox.plot_graph_folium(graph, popup_attribute='name', edge_width=1)
#route_graph_map = ox.plot_route_folium(graph, route, route_map=graph_map, popup_attribute='length')
#route_graph_map.save('route.html')
#route_graph_map