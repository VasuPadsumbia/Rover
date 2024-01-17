from calendar import c
from operator import ge
from turtle import hideturtle
import osmnx as ox
import networkx as nx
import os, json, matplotlib
import threading
import matplotlib.pyplot as plt
from scipy.datasets import face

from distutils.command import build
matplotlib.use('Qt5Agg')
from matplotlib.animation import FuncAnimation, PillowWriter
import Layers.L1_App.navigation.manoeuvre as manoeuvre
from helper import map_coordinate_path
from Layers.L1_App.sensor.dgps.DGPS import connect_pksi_dgps
import base64
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
        self.path = map_coordinate_path()
        self._network_type = type
        self._destination = destination
        self._animation = None
        self.nodes = 0
        self.coordinates = []
        self.start_point = None
        self.current = None
        self.initial_location = coordinates
        self._footprints = None
        self.shortest_path = None
        if coordinates:
            self._path_graphml = self.create_street_network_point(coordinates)
        elif place_name:
            self._path_graphml = self.create_street_network_place(place_name)
        self.gps = connect_pksi_dgps()
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
        
        #building = footprints[footprints['building'] == 'yes']
        #building.plot(ax=ax, facecolor='blue', alpha=0.7, label='building', aspect='equal')

        #highway = footprints[footprints['highway'] == 'road']
        #highway.plot(ax=ax, facecolor='white', alpha=0.7, label='highway', aspect='equal')
        #general_footprints = footprints[(footprints['building'].isnull()) & (footprints['highway'].isnull())]
        #general_footprints.plot(ax=ax, facecolor='orange' ,label='buildings', aspect='equal', alpha=0.7)
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
        
        tags = {'building':True,'highway':'road', 'natural': True }
        # Plot footprints on the same plot
        footprints = self.create_footprints(tags) 
        college = footprints[footprints['tourism'] == 'museum']
        college.plot(ax=ax, facecolor='red', alpha=0.7, label='museum', aspect='equal')

        tree = footprints[footprints['natural'] == 'tree']
        tree.plot(ax=ax, facecolor='green', alpha=0.7, label='tree', aspect='equal')
        
        footprints.plot(ax=ax, alpha=0.7)
        # Highlight your location node
        your_location_node = self._graph.nodes[69]
        self.start_point, = ax.plot(your_location_node['x'], your_location_node['y'], 'bo', markersize=10, label='Start Point')
        #ax.scatter(your_location_node["x"], your_location_node["y"], c="cyan", s=50, zorder=5, label="Your Location")
        
        #plot gps location marker
        #self.lat, self.lon, self.height = self.gps.get_data()
        #self.current, = ax.plot(self.lon, self.lat, 'bo', markersize=10, label='Current Location')
        
        ax.legend()
        #ox.plot_graph_route(self._graph, self.find_shortest_path_between_two_points(), route_color='r', route_linewidth=2, ax=ax, save=True,filepath=f'{os.path.abspath(os.path.join(os.path.dirname(__file__),"../../"))}/L2_Data/map.png')
        self.shortest_path=self.find_shortest_path_between_two_points()
        #self._map_navigator = MapNavigator(self._graph,self.shortest_path, self.start_point)
        #self._map_navigator.navigate()
        self.manoeuvre = manoeuvre.Target_manoeuvre(0.0001, self.path, self._graph, self.shortest_path, self.start_point)
        #print(len(self.shortest_path))
        path_png = f'{os.path.abspath(os.path.join(os.path.dirname(__file__),"../../"))}/L2_Data/map.png'
        def gps_update(i):
            self.lat, self.lon, self.height = self.gps.get_data()
            self.current.set_data(self.lon, self.lat)
            return self.current,        
        
        if self.shortest_path is not None:
            fig, ax = ox.plot_graph_route(self._graph, self.shortest_path,route_color='r',route_linewidth=2,
                                            ax=ax,save=True,filepath=path_png, node_size=0, show=False, close=False)
        
        # Animate the movement along the path
        self._animation = FuncAnimation(fig, self.manoeuvre.manoeuvre_simulation, frames=len(self.shortest_path), interval=1000, repeat=True)
        
        # Animate the current gps location
        #self._animation = FuncAnimation(fig, gps_update, frames=100, interval=200, repeat=False) 
        #self.manoeuvre.plot_route()
        self.show_plot()
        self.save_animation()
        
        # Create a lock
        #lock = threading.Lock()
        # Create and start the threads for saving the animation and showing the plot
        #save_thread = threading.Thread(target=self.save_animation, args = (lock,))
        #show_thread = threading.Thread(target=self.show_plot, args = (lock,))
        # Start the threads
        #save_thread.start()
        #show_thread.start()
        
        # Wait for both threads to finish
        #save_thread.join()
        #show_thread.join()

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

    def log_coordinates(self):
        try:
            #location = [{'Point': i // 2 + 1 'latitude': self.coordinates[i], 'longitude': self.coordinates[i+1]}]for i in range(0, len(self.cordinates), 2)
            data = [self.coordinates[i:i+2] for i in range(0, len(self.coordinates), 2)]
            data_JSON = { 'data' : data}
            print(data_JSON)
            path = f'{os.path.abspath(os.path.join(os.path.dirname(__file__),"../../"))}/L2_Data/coordinates.json'
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

    def get_gps_data(self):

        try:
            self.lat, self.lon, self.height = self.gps.get_data()
            return self.lat, self.lon, self.height
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def save_animation(self):
            try:
                # # Convert the animation to HTML5 video format
                # self.html5_video = self._animation.to_html5_video()
                # # Embed the video in an HTML string
                # self.html_string = f"""
                # <html>
                # <body>
                # <video width="320" height="240" controls>
                #   <source src="data:video/mp4;base64,{base64.b64encode(self.html5_video.encode()).decode()}" type="video/mp4">
                # </video>
                # </body>
                # </html>
                # """
                path_gif = f'{os.path.abspath(os.path.join(os.path.dirname(__file__),"../../../"))}/path_animation.gif'
                writer = PillowWriter(fps=30) 
                self._animation.save(path_gif, writer='pillow')
                # Write the HTML string to a file
                #path_html = f'{os.path.abspath(os.path.join(os.path.dirname(__file__),"../../../"))}/path_animation.html'
                #with open(path_html, 'w') as f:
                #    f.write(self.html_string)
            except Exception as e:
                print(f"An error occurred: {e}")
                return None
        
    def show_plot(self):
            try:
                plt.show()
            except Exception as e:
                print(f"An error occurred: {e}")
                return None