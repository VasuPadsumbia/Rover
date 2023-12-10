import osmnx as ox
import matplotlib.pyplot as plt

class MapHandler():
    def __init__(self, network_type, coordinates):
        self._network_type = network_type
        self._coordinates = coordinates
        self._graph = self.create_street_network_point()

    def create_street_network_point(self):
        # Generate graph from a point
        area_graph = ox.graph_from_point(self._coordinates, network_type=self._network_type, dist=200)
        return area_graph

    def create_footprints(self):
        # Generate footprints from OSMnx around the specified point
        footprints = ox.features_from_point(self._coordinates, tags={'building':True,'highway':'road'}, dist=200)
        return footprints

    def plot_graph_and_footprints(self):
        # Plot the street network graph
        fig, ax = ox.plot_graph(self._graph, bgcolor="k", show=False, close=False)

        # Plot footprints on the same plot
        footprints = self.create_footprints()
        footprints.plot(ax=ax, facecolor='orange', alpha=0.7)

        # Show the plot
        plt.show()

# Example usage
coordinates = (53.540559, 8.5836)  # Replace with your desired coordinates
network_type = 'all'  # Replace with your desired network type
map_handler = MapHandler(network_type, coordinates)
map_handler.plot_graph_and_footprints()
