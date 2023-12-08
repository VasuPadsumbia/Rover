from numpy import True_
import osmnx as ox
import matplotlib.pyplot as plt
import folium
import json

# Specify the name that is used to seach for the data
place_name = "Hochschule Bremerhaven, Bremerhaven, Germany"

# Fetch OSM street network from the location
graph = ox.graph_from_point((53.540559, 8.5836),dist=150,network_type = 'all')
# Create a street network graph for the specified area

#nodes, edges = ox.graph_to_gdfs(graph)
#fig, ax = ox.plot_graph(graph, show=False)
#graph=ox.features_from_point((53.540559, 8.5836), tags={'building':True,'highway':'road'}, dist=200)
#ox.plot_footprints(graph,edge_color="blue", edge_linewidth=1, show=False)
footprint = json.dumps(wkt.loads(products[key]["footprint"]))
ubc_footprint = folium.Map(location=(53.540559, 8.5836), zoom_start=15)
folium.GeoJson(footprints).add_to(ubc_footprint)
ox.plot_graph_folium(G=graph, edge_color='black', edge_width=0.00005, 
                     node_size=0,bgcolor='lightgray',
                     tiles='OpenStreetMap',zoom=12,center=(53.540559, 8.5836))
