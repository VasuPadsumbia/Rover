from calendar import c
from math import dist
from numpy import save, short
import osmnx as ox
import networkx as nx
import os, sys, argparse
import json, matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
from scipy.__config__ import show
from matplotlib.patches import Patch
from matplotlib.animation import FuncAnimation
from matplotlib.path import Path
from IPython.display import HTML

class MapHandler():
    def __init__(self, type, destination, place_name=None, coordinates=[]) -> None:
        
        """_summary_

        Args:
            place (city,country): place of which you want to develop strret network.
            network type (Map): Type of network includes "walk", "drive", "cycle".
            graph : class variable created for graph of the aabove map.
            origin : Origin coordinates of the rover from piksi (Latitude,Longitude).
            destination : desired target location to which the rover need to go.
            nodes = number of turnes for rover to travel till destination
        """
        self._network_type = type
        self._destination = destination
        self._animation = None
        self.nodes = 0
        self.coordinates = []
        self.initial_location = coordinates
        self._footprints = None
        if coordinates:
            self._path_graphml = self.create_street_network_point(coordinates)
        elif place_name:
            self._path_graphml = self.create_street_network_place(place_name)

        self.dummy = self.get_coordinates_from_json()
        self._graph = self.create_area_graph()
        
    def create_street_network_place(self, place_name):
        
        """
        Generate graphml file for further transfer to GUI
        Location name formate shall be like for example STREET_GRAPH_PLACE = Bremerhaven,Germany
        and shall be saved as Bremerhaven_Germany.graphml
        
        """
        # Get the absolute path of the script's directory
        script_directory = os.path.dirname(os.path.realpath(__file__))

        # Set the current working directory to the script's directory
        os.chdir(script_directory)
        current_directory = os.getcwd()
        print("Current working directory:", current_directory)

        DATA_FOLDER = os.path.join(current_directory, "data")

        # Create the "data" folder if it doesn't exist
        if not os.path.exists(DATA_FOLDER):
            os.makedirs(DATA_FOLDER)

        if isinstance(place_name, str):
            # If place_info is a string, treat it as a location name
            STREETGRAPH_FILENAME = place_name.replace(' ','_').replace(',','_')+'.graphml'
        elif isinstance(place_name, tuple):
            # If place_info is a tuple, treat it as coordinates
            STREETGRAPH_FILENAME = f'{place_name[0]}_{place_name[1]}'.replace(' ','_').replace(',','')+'.graphml'
        else:
            raise ValueError("Invalid format for place_info")
        
        #STREETGRAPH_FILENAME = place_name.replace(' ','_').replace(',','_')+'.graphml'
        
        path_graphml = os.path.join(DATA_FOLDER, STREETGRAPH_FILENAME)
        FORCE_CREATE = True
        #This Checks if the Streetnetwork File exists(or creation is overwritten using FORCE_CREATE)
        if (not os.path.isfile(path_graphml)) or FORCE_CREATE:
            #There are many different ways to create the Network Graph. Please follow osmnx documentation for more details
            area_graph = ox.graph_from_place(place_name, buffer_dist=200,network_type = self._network_type)
            ox.save_graphml(area_graph, path_graphml)
            print(len(area_graph.nodes), len(area_graph.edges))
            #This will create streetnetwork.graphml equiv size = 277M
        return path_graphml
        
    
    def create_street_network_point(self, coordinates):
        
        """
        Generate graphml file for further transfer to GUI
        Location name formate shall be like for example STREET_GRAPH_PLACE = Bremerhaven,Germany
        and shall be saved as Bremerhaven_Germany.graphml
        
        """
        # Get the absolute path of the script's directory
        script_directory = os.path.dirname(os.path.realpath(__file__))

        # Set the current working directory to the script's directory
        os.chdir(script_directory)
        current_directory = os.getcwd()
        print("Current working directory:", current_directory)
        # Specify the relative path to the data folder
        DATA_FOLDER = os.path.join(current_directory, "data")

        # Create the "data" folder if it doesn't exist
        if not os.path.exists(DATA_FOLDER):
            os.makedirs(DATA_FOLDER)

        #STREETGRAPH_FILENAME = coordinates.replace(' ','_').replace(',','')+'.graphml'
        STREETGRAPH_FILENAME = f'{coordinates[0]}_{coordinates[1]}'.replace(' ','_').replace(',','')+'.graphml'

        path_graphml = os.path.join(DATA_FOLDER, STREETGRAPH_FILENAME)
        FORCE_CREATE = True
        #This Checks if the Streetnetwork File exists(or creation is overwritten using FORCE_CREATE)
        if (not os.path.isfile(path_graphml)) or FORCE_CREATE:
            #There are many different ways to create the Network Graph. Please follow osmnx documentation for more details
            area_graph = ox.graph_from_point(coordinates, network_type = self._network_type, dist=200)
            print(len(area_graph.nodes), len(area_graph.edges))
            start_edge  = ox.nearest_edges(area_graph, self.initial_location[1], self.initial_location[0], return_dist=True)
            end_edge  = ox.nearest_edges(area_graph, self._destination[1], self._destination[0], return_dist=True)
            # Add your location as a node to the graph
            area_graph.add_node("69", x=float(coordinates[1]), y=float(coordinates[0]))
            #area_graph.add_node("70", x=float(self._destination[1]), y=float(self._destination[0]))
            area_graph.add_edge("69", start_edge[0][0], length=start_edge[1])
            #area_graph.add_edge("70", end_edge[0][1], length=end_edge[1])
            ox.save_graphml(area_graph, path_graphml)
            #This will create streetnetwork.graphml equiv size = 277M
        return  path_graphml
    
    def create_area_graph(self):
        
        """
        Load graph from graphml file that we created in create_street_network_() function
        
        """
        try:
            return ox.load_graphml(self._path_graphml)
        except Exception as e:
            print(f"Error loading graph: {e}")
            return ValueError("No graph data available. Please create a street network first.")
    
    def plot_graph_map(self):
        
        """
        Generating graph map and plotting the graph of the desired location
        
        """

        # Plot the street network
        #fig, ax = ox.plot_graph(self._graph, bgcolor="k", show=False, close=False)
        #shortest_path, H = self.find_shortest_path_between_two_points()
        fig, ax = ox.plot_graph(self._graph, bgcolor="k", show=False, close=False)
        # Plot footprints on the same plot
        tags = {'building':True,'highway':'road', 'natural': True ,'tourism':'college'}
        # Plot footprints on the same plot
        footprints = self.create_footprints(tags) 
        college = footprints[footprints['tourism'] == 'museum']
        college.plot(ax=ax, facecolor='red', alpha=0.7, label='museum', aspect='equal')

        tree = footprints[footprints['natural'] == 'tree']
        tree.plot(ax=ax, facecolor='green', alpha=0.7, label='tree', aspect='equal')
        
        general_footprints = footprints[(footprints['tourism'].isnull()) & (footprints['natural'].isnull())]
        footprints.plot(ax=ax, alpha=0.7)
        # Highlight your location node
        your_location_node = self._graph.nodes[69]
        ax.scatter(your_location_node["x"], your_location_node["y"], c="red", s=50, zorder=5, label="Your Location")
        
        plt.savefig(f'{os.path.abspath(
                                     os.path.join(
                                         os.path.dirname(__file__),"../../"))}/L2_Data/map.png')
        # Show the plot
        plt.show()
        
    def create_footprints(self,tags):
        
        """
        Generating graph map and plotting the graph of the desired location
        
        """
        #bbox = ox.utils_geo.bbox_from_point(self._origin,dist=150)
        #ox.features_from_bbox(bbox[0],bbox[1],bbox[2],bbox[3],tags={'building':True,'highway':'road'})
        return ox.features_from_point(self.initial_location, tags=tags, dist=200)


    def find_shortest_path_between_two_points(self):
        
        """
        
        This function finds the best route for the desired destination. 
        Please specify the type of network depending on the ride
        
        """

        #start_node = ox.nearest_nodes(self._graph, self.initial_location[1], self.initial_location[0])
        target_node= ox.nearest_nodes(self._graph, self._destination[1], self._destination[0])
        
        shortest_path = nx.shortest_path(self._graph, source=69, target=target_node, weight="length")
        print(shortest_path)
        return shortest_path
        #route_point1_point2 = ox.shortest_path(self._graph, start_edge[1], end_edge[0], weight=self._network_type)
        #route_point1_point2 = nx.shortest_path(H, source="your_location", target="target_location", weight='length')
        #return H, route_point1_point2
        

    def cartesian_coordinates(self):
        
        """

        The data obtained from the find_shortest_path_between_two_points() function is in node ID form from OSMnx 
        and so to convert those data to latitudes and longitudes we have to get the status from OSMnx analysis.
        
        """
        
        g = self._graph
        node_id = self.find_shortest_path_between_two_points()
        self.nodes = len(node_id)
        for x in range(self.nodes):
            self.coordinates.append(g.nodes[node_id[x]]['y'])
            self.coordinates.append(g.nodes[node_id[x]]['x'])
        return self.coordinates
    
    def plot_graph_shortest_route(self):
        
        """

        This function develops the graph of shortest route and imposes on the original map of the location
        
        """
        
        fig, ax = ox.plot_graph(self._graph, bgcolor="k", show=False, close=False)
        
        tags = {'building':True,'highway':'road', 'natural': True ,'tourism':'college'}
        # Plot footprints on the same plot
        footprints = self.create_footprints(tags) 
        college = footprints[footprints['tourism'] == 'museum']
        college.plot(ax=ax, facecolor='red', alpha=0.7, label='museum', aspect='equal')

        tree = footprints[footprints['natural'] == 'tree']
        tree.plot(ax=ax, facecolor='green', alpha=0.7, label='tree', aspect='equal')
        
        general_footprints = footprints[(footprints['tourism'].isnull()) & (footprints['natural'].isnull())]
        footprints.plot(ax=ax, alpha=0.7)
        
        # Highlight your location node
        your_location_node = self._graph.nodes[69]
        start_point, = ax.plot(your_location_node['x'], your_location_node['y'], 'bo', markersize=10, label='Start Point')
        #ax.scatter(your_location_node["x"], your_location_node["y"], c="cyan", s=50, zorder=5, label="Your Location")
        #ax.scatter(y=current_position[0], x=current_position[1], c="orange", s=50, zorder=5, label="Current Location")
        ax.legend()
        #ox.plot_graph_route(self._graph, self.find_shortest_path_between_two_points(), route_color='r', route_linewidth=2, ax=ax, save=True,filepath=f'{os.path.abspath(os.path.join(os.path.dirname(__file__),"../../"))}/L2_Data/map.png')
        shortest_path=self.find_shortest_path_between_two_points()
        print(len(shortest_path))
        path_png = f'{os.path.abspath(os.path.join(os.path.dirname(__file__),"../../"))}/L2_Data/map.png'
        if shortest_path is not None:
            path_line = ox.plot_graph_route(self._graph, shortest_path,route_color='r',route_linewidth=2,ax=ax,save=True,filepath=path_png)
        # Get the LineString geometry for the edge
        #edge_linestring = ox.distance.get_route_edge_linestring(G, edge)

        # Extract individual points from the LineString
        #points = [(point.x, point.y) for point in edge_linestring.coords]

        # Function to update animation frames
        def update(frame):
            if frame < len(shortest_path):
                #print(f"Frame: {frame}")
                current_node = shortest_path[frame]
                x = self._graph.nodes[current_node]['x']
                y = self._graph.nodes[current_node]['y']
                # Update the position of the PathPatch
                start_point.set_data(x, y)
                return start_point,
            else:
                #print(f"Frame outside shortest_path: {frame}")
                return start_point,

        # Animate the movement along the path
        self._animation = FuncAnimation(fig, update, frames=len(shortest_path), interval=500, repeat=True)
        # Save the animation
        path_gif = f'{os.path.abspath(os.path.join(os.path.dirname(__file__),"../../../"))}/path_animation.gif'
        self._animation.save(path_gif, writer='Pillow')
        
        # Show the plot
        plt.show()


    def log(self):
        try:
            #location = [{'Point': i // 2 + 1 'latitude': self.coordinates[i], 'longitude': self.coordinates[i+1]}]for i in range(0, len(self.cordinates), 2)
            data_JSON = {
                f"Point {i // 2 + 1}": {
                    "Latitude": self.coordinates[i],
                    "Longitude": self.coordinates[i+1]
                } for i in range(0, len(self.coordinates), 2)
            }
            print(data_JSON)
            path = f'{os.path.abspath(os.path.join(os.path.dirname(__file__),"../../"))}/L2_Data/map_coordinates.json'
            #self.coordinates[['x', 'y', 'elevation']].to_json(path, orient='records', lines=True)
            with open(path, "w") as write_file:
                json.dump(data_JSON, write_file)

        except Exception as e:
            print(f"An error occurred: {e}")

    def get_coordinates_from_json(self):
        try:
            path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../L2_Data/gps_dummy.json"))
            with open(path, "r") as json_file:
                data = json.load(json_file)
                lat = data['lat']
                lon = data['lon']
                coordinates = [lat, lon]
                return coordinates
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
