from math import dist
from numpy import save, short
import osmnx as ox
import networkx as nx
import os, sys, argparse
import json
import matplotlib.pyplot as plt
from scipy.__config__ import show
from matplotlib.patches import Patch
from sklearn import tree

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
        self.nodes = 0
        self.coordinates = []
        self.initial_location = coordinates
        self._footprints = None
        if coordinates:
            self._path_graphml = self.create_street_network_point(coordinates)
        elif place_name:
            self._path_graphml = self.create_street_network_place(place_name)


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
            ox.save_graphml(area_graph, path_graphml)
            #This will create streetnetwork.graphml equiv size = 277M
        return  path_graphml
    
    def create_area_graph(self):
        
        """
        Load graph from graphml file that we created in create_street_network_() function
        
        """
        if self._path_graphml:
            return ox.load_graphml(self._path_graphml)
        else:
            raise ValueError("No graph data available. Please create a street network first.")
    
    def plot_graph_map(self):
        
        """
        Generating graph map and plotting the graph of the desired location
        
        """

        # Plot the street network
        fig, ax = ox.plot_graph(self._graph, bgcolor="k", show=False, close=False)
        
        # Plot footprints on the same plot
        footprints = self.create_footprints({'building':True,'highway':'road', 'natural':'tree'})
        footprints.plot(ax=ax, facecolor='orange', alpha=0.7)

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
        node_point1 = ox.nearest_nodes(self._graph, self.initial_location[1], self.initial_location[0])
        node_point2 = ox.nearest_nodes(self._graph, self._destination[1], self._destination[0])
        route_point1_point2 = ox.shortest_path(self._graph, node_point1, node_point2, weight=self._network_type)
        return route_point1_point2
        

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
        footprints.plot(ax=ax, facecolor='orange', alpha=0.7)

        ox.plot_graph_route(self._graph, self.find_shortest_path_between_two_points(), route_color='r', route_linewidth=2, ax=ax,save=True,)

        # Show the plot
        plt.show()

    def log(self):
        try:
            #location = [{'Point': i // 2 + 1 'latitude': self.coordinates[i], 'longitude': self.coordinates[i+1]}]for i in range(0, len(self.cordinates), 2)
            data_JSON = [{
                f"Point {i // 2 + 1}": {
                            "Latitude": self.coordinates[i],
                            "Longitude": self.coordinates[i+1]
                            } 
                    } for i in range(0,len(self.coordinates),2)]
            print(data_JSON)
            path = f'{os.path.abspath(os.path.join(os.path.dirname(__file__),""))}/map_coordinates.json'
            #self.coordinates[['x', 'y', 'elevation']].to_json(path, orient='records', lines=True)
            with open(path, "w") as write_file:
                json.dump(data_JSON, write_file)

        except Exception as e:
            print(f"An error occurred: {e}")
