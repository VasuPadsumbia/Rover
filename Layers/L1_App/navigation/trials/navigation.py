from matplotlib.pylab import f

import geopy.distance
import math

class MapNavigator:
    def __init__(self, graph, shortest_path, start_point=None):
        self._graph = graph
        self._animation = None
        self._speed_kmph = 0.1  # Set your speed in km/h
        self.shortest_path = shortest_path
        self.start_point = start_point
    def calculate_distance(self, coord1, coord2):
        try:
            return geopy.distance.distance(coord1, coord2).km
        except ValueError:
            # Handle the case where latitude is out of range
            return 0
    
    def distance(self, lat1, lon1, lat2, lon2):
        R = 6371.0 # Radius of the earth in km
        dLat = math.radians(lat2-lat1)
        dLon = math.radians(lon2-lon1)
        a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)      
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = R * c * 1000
        return d
    
    def update_coordinates(self, frame):
        frames_between_nodes = 2  # Adjust this value for smoother animation
        if frame < len(self.shortest_path) -1:
            current_node = self.shortest_path[frame]
            next_node = self.shortest_path[frame + 1]

            # Check if the graph has an edge between the current and next nodes
            if self._graph.has_edge(current_node, next_node):
                distance_between_nodes = self.calculate_distance((self._graph.nodes[current_node]['y'],
                                                              self._graph.nodes[current_node]['x']),
                                                             (self._graph.nodes[next_node]['y'],
                                                              self._graph.nodes[next_node]['x']))

                # Calculate total distance on the path
                total_distance_on_path = sum(self.distances[:frame + 1])
                # Calculate time elapsed
                time_elapsed = total_distance_on_path / self._speed_kmph
                # Calculate fraction along the edge
                fraction_along_edge = min(1.0, time_elapsed / (distance_between_nodes / self._speed_kmph))
                #fraction_between_nodes = (frame % frames_between_nodes) / frames_between_nodes

                # Interpolate coordinates between current and next nodes
                x_current, y_current = self._graph.nodes[current_node]['x'], self._graph.nodes[current_node]['y']
                x_next, y_next = self._graph.nodes[next_node]['x'], self._graph.nodes[next_node]['y']
                x = x_current + fraction_along_edge * (x_next - x_current)
                y = y_current + fraction_along_edge * (y_next - y_current)
                
                self.start_point.set_data(x, y)
                return self.start_point,
     
        # If edge data is not available, use node positions directly
        elif frame < len(self.shortest_path):
            current_node = self.shortest_path[frame]
            x, y = self._graph.nodes[current_node]['x'], self._graph.nodes[current_node]['y']
            self.start_point.set_data(x, y)
            return self.start_point,
    
    def update(self, frame):
            if frame < len(self.shortest_path):
                #print(f"Frame: {frame}")
                current_node = self.shortest_path[frame]
                x = self._graph.nodes[current_node]['x']
                y = self._graph.nodes[current_node]['y']
                # Update the position of the PathPatch
                self.start_point.set_data(x, y)
                return self.start_point,
            else:
                #print(f"Frame outside shortest_path: {frame}")
                return self.start_point,

    def navigate(self):
        #self.shortest_path = nx.shortest_path(self._graph, source=start_node, target=end_node)
        self.distances = [self.calculate_distance((self._graph.nodes[u]['y'], self._graph.nodes[u]['x']),
                                                 (self._graph.nodes[v]['y'], self._graph.nodes[v]['x']))
                          for u, v in zip(self.shortest_path[:-1], self.shortest_path[1:])]

        #fig, ax = ox.plot_graph_route(self._graph, self.shortest_path, route_color='r', route_linewidth=2,
        #                              node_size=0, show=False, close=False)
        
        #your_location_node = self._graph.nodes[start_node]
        #self.start_point, = ax.plot(your_location_node['x'], your_location_node['y'], 'bo', markersize=10, label='Start Point')

        #self._animation = FuncAnimation(fig, self.update_coordinates, frames=len(self.shortest_path), interval=500, repeat=True)

        # Save the animation as a GIF
        #path_gif = 'path_animation.gif'
        #self._animation.save(path_gif, writer='pillow', fps=1)  # Adjust fps as needed

        #plt.show()

# Create a sample graph (replace this with your actual graph)
#G = ox.graph_from_place("Piedmont, California, USA", network_type="all")

# Instantiate MapNavigator
#navigator = MapNavigator(G)

# Choose start and end nodes for navigation
#start_node = list(G.nodes())[0]
#end_node = list(G.nodes())[-1]

# Start navigation
#navigator.navigate(start_node, end_node)
