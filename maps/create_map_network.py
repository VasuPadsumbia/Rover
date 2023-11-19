import osmnx as ox
import networkx as nx
import os


class create_map_network():
    def __init__(self, STREET_GRAPH_PLACE, type, origin, destination) -> None:
        """_summary_

        Args:
            point_cloud_polar (list[any): Point Cloud.
            position_map (Map): Map of environment without forbidden areas.
            path_map (Map): Map of environment with forbidden areas.
            target (MetricPosition): Target position.
            stages (int, optional): Convolution stages. Defaults to 4.
            threshold (float, optional): Threshold for convolution. Defaults to 0.7.
        """
        self._palce = STREET_GRAPH_PLACE
        self._network_type = type
        self._graph = self.create_area_graph()
        self._origin = origin
        self._destination = destination

    def create_street_network(self):
        """
        Generate graphml file for further transfer to GUI
        Location name formate shall be like for example STREET_GRAPH_PLACE = Bremerhaven,Germany
        and shall be saved as Bremerhaven_Germany.graphml
        
        """
        STREETGRAPH_FILENAME = self._palce.replace(' ','_').replace(',','_')+'.graphml'
        STREETGRAPH_FILEPATH = ".//data//"+STREETGRAPH_FILENAME
        FORCE_CREATE = False
        #This Checks if the Streetnetwork File exists(or creation is overwritten using FORCE_CREATE)
        if (not os.path.isfile(STREETGRAPH_FILEPATH)) or FORCE_CREATE:
            #There are many different ways to create the Network Graph. Please follow osmnx documentation for more details
            area_graph = ox.graph_from_place(self._palce, network_type = self._network_type)
            ox.save_graphml(area_graph, STREETGRAPH_FILEPATH)
            #This will create streetnetwork.graphml equiv size = 277M
        return STREETGRAPH_FILEPATH

    def create_area_graph(self):
        """
        Load graph from graphml file that we created in create_street_network() function
        
        """
        return ox.load_graphml(self.create_street_network())
    
    def plot_graph_map(self):
        """
        Generating graph map and plotting the graph of the desired location
        
        """
        ec = ox.plot.get_edge_colors_by_sttr(self._graph, attr="length", num_bins=5)

        #otherwise, when num_bins is None (default), linearly map one color to each node/edge by value
        #ec = ox.plot.get_edge_colors_by_sttr(self._graph, attr="length")

        #plot the graph with colored edges
        fig, ax = ox.plot_graph(self._graph, node_size=5, edge_color = ec, bgcolor="k")


    def find_shortest_path_between_two_points(self):
        """
        
        This function finds the best route for the desired destination. 
        Please specify the type of network depending on the ride
        
        """
        node_point1 = ox.nearest_nodes(self._graph, self._origin[1], self._origin[0])
        node_point2 = ox.nearest_nodes(self._graph, self._destination[1], self._destination[0])
        route_point1_point2 = ox.shortest_path(self._graph, node_point1, node_point2, weight=self._network_type)
        return route_point1_point2
        

    def cartesian_coordinates(self):
        """

        The data obtained from the find_shortest_path_between_two_points() function is in node ID form from OSMnx 
        and so to convert those data to latitudes and longitudes we have to get the status from OSMnx analysis.
        
        """
        coordinates=[]
        g = self._graph
        node_id = self.find_shortest_path_between_two_points()
        for x in range(len(node_id)):
            coordinates.append(g.nodes[node_id[x]]['y'])
            coordinates.append(g.nodes[node_id[x]]['x'])
        return coordinates
    
    def plot_graph_shortest_route(self):
        """

        This function develops the graph of shortest route and imposes on the original map of the location
        
        """
        return ox.plot_graph_route(self._graph, self.find_shortest_path_between_two_points(), orig_dest_size = 0, node_size=0)

