import ast
import json
import time
import numpy as np
import json
import matplotlib.pyplot as plt


class GridGenerator:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.cartesian_coordinates = None
        self.norm_coord = self.normalize_coordinates()
    def normalize_coordinates(self):
        x = [float(point[0]) for point in self.coordinates]
        y = [float(point[1]) for point in self.coordinates]
        print(f'x: {x}, y: {y}')
        min_x = np.min(x)
        min_y = np.min(y)
        buf_x = (x - min_x) / (np.max(x) - min_x)
        buf_y = (y - min_y) / (np.max(y) - min_y)
        normalised_x = np.round(buf_x, 2)
        normalised_y = np.round(buf_y, 2)
        normalized_coordinates = [(x, y) for x, y in zip(normalised_x*100+1, normalised_y*100+1)]
        return normalized_coordinates
    def generate_grid(self):
        # Extract x and y coordinates from the JSON data
        x_coordinates = [float(point[0]) for point in self.norm_coord]
        y_coordinates = [float(point[1]) for point in self.norm_coord]
        # Generate grid from the points
        x_min = min(x_coordinates)
        x_max = max(x_coordinates)
        y_min = min(y_coordinates)
        y_max = max(y_coordinates)
        grid_y = int((y_max - y_min))+1
        grid_x = int((x_max - x_min))+1
        print(grid_y,grid_x)
        grid = np.zeros((grid_y , grid_x ), dtype=float)
        #grid = np.zeros((y_max - (y_min), x_max - (x_min)), dtype=float)
        for point in self.norm_coord:
            x = int(point[0] - x_min)
            y = int(point[1] - y_min)
            grid[y, x] = 1
        #print(grid)
        return grid
    
class AStar:
    def __init__(self, coordinates):
        self.grid_generator = GridGenerator(coordinates)
        self.grid = self.grid_generator.generate_grid()
        self.coordinates = self.grid_generator.norm_coord
    def find_path(self, start, goal):
        # A* pathfinding algorithm implementation
        open_set = [start]
        came_from = {}
        g_score = {start: 0.0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            current = self.get_lowest_f_score(open_set, f_score)
            if current == goal:
                print("Goal found!")
                return self.reconstruct_path(came_from, current)

            open_set.remove(current)
            closed_list = open_set
            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                tentative_g_score = g_score[current] + self.distance(current, neighbor)
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)

                    if neighbor not in open_set:
                        open_set.append(neighbor)
            # Inside your main A* loop
            #print(f"Current node: {current}")
            #print(f"Open list: {open_set}")
            #print(f"Closed list: {closed_list}")
        return None

    def get_lowest_f_score(self, open_set, f_score):
        lowest_f_score = float('inf')
        lowest_node = None
        for node in open_set:
            if f_score[node] < lowest_f_score:
                lowest_f_score = f_score[node]
                lowest_node = node
        return lowest_node

    def get_neighbors(self, node):
        x, y = node
        neighbors = []

        # Define the possible movements (up, down, left, right)
        movements = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for dx, dy in movements:
            neighbor_x = x + dx
            neighbor_y = y + dy
            neighbor_x = int((neighbor_x))
            neighbor_y = int((neighbor_y))
            # Check if the neighbor is within the grid boundaries
            if 0 <= neighbor_x < self.grid.shape[1] and 0 <= neighbor_y < self.grid.shape[0]:
                # Check if the neighbor is a valid node (not an obstacle)
                if self.grid[neighbor_y, neighbor_x] != 1:
                    neighbors.append((neighbor_x, neighbor_y))

        return neighbors
    def distance(self, node1, node2):
        x1, y1 = node1
        x2, y2 = node2
        return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    def heuristic(self, node, goal):
        x1, y1 = node
        x2, y2 = goal
        return abs(x2 - x1) + abs(y2 - y1)

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        path = [(float(x), float(y)) for x, y in path]  # Convert path coordinates to float
        print(path)
        return path


# Load the JSON file
with open('Layers/L2_Data/coordinates.json') as f:
    data = json.load(f)
    coordinates = data['data']


# Create an instance of AStar
astar = AStar(coordinates)
normalised = astar.coordinates
print(f'normalised: {normalised}')

# Find path using A* algorithm
start = normalised[0][0], normalised[0][1]
goal = normalised[1][0], normalised[1][1]
print(f'start: {start}, goal: {goal}')
path = astar.find_path(start, goal)
print(f'path: {path}')
grid = astar.grid
# Convert path to a NumPy array
path_array = np.array(path)

# Plot the grid
#plt.imshow(grid, cmap='binary', origin='lower')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Grid from Points')

# Plot the path
plt.plot(path_array[:, 0], path_array[:, 1], color='red', linewidth=2)

# Show the plot
plt.show()

