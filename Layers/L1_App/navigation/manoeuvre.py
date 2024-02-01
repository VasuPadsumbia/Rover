import math, time, json
from json.decoder import JSONDecodeError
from tkinter import N
from Layers.L1_App.sensor.dgps.DGPS import connect_pksi_dgps
import matplotlib.pyplot as plt
from Layers.L1_App.sensor.imu.gyroscpe import connect_pksi_INS
class Target_manoeuvre():
    def __init__(self, speed, map_path, graph, shortest_path, start_point=None):
        self.speed = speed
        self.path = map_path
        self.map_coordinates = self.get_coordinates()
        self.target_position = None
        self.current_position = None
        self.heading = self.get_heading_virtual()
        self.start_point = start_point
        self._graph = graph
        self.shortest_path = shortest_path
        self.route = []
        #self.gps = connect_pksi_dgps()
        #self.ins = connect_pksi_INS()
        #self.heading = self.get_heading_from_sensor() #add heading from magnetometer
        self.distances = [self.distance(self._graph.nodes[u]['y'], self._graph.nodes[u]['x'],
                                                 self._graph.nodes[v]['y'], self._graph.nodes[v]['x'])
                          for u, v in zip(self.shortest_path[:-1], self.shortest_path[1:])]
    def get_coordinates(self):
            try:
                with open(self.path, "r") as config_file:
                    data = json.load(config_file)
                    coordinates = data['data'] 
                    config_file.close()
                    return coordinates
            except JSONDecodeError as e:
                print("Failed to read JSON, return code %d\n", e) 
                return None
            
    def get_target_position(self,i):
        if self.map_coordinates is not None:
            target_position = self.map_coordinates[i]
            print(f"target_position: {target_position}")
            return target_position
        else:
            return None, None
    
    def get_current_position(self,i):
        if self.map_coordinates is not None:
            current_position = self.map_coordinates[i]
            print(f"current_position: {current_position}")
            return current_position
        else:
            return None, None
        
    def get_distance(self):
        if self.target_position is not None and self.current_position is not None:
            distance = self.distance(self.target_position[0], self.target_position[1], self.current_position[0], self.current_position[1])
            print(f"distance: {distance}")
            return distance
        else:
            return None
        
    def distance(self, lat1, lon1, lat2, lon2):
        R = 6371.0 # Radius of the earth in km
        dLat = math.radians(lat2-lat1)
        dLon = math.radians(lon2-lon1)
        a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)      
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = R * c * 1000
        return d
    
    def get_heading_virtual(self):
        """Returns the simulated heading based on the current and target position"""

        if self.target_position is not None and self.current_position is not None:
            heading = self.calculate_initial_compass_bearing(self.current_position, self.target_position)
            print(f"heading: {heading}")
            return round(heading,6)
        else:
            return None
        
    def calculate_initial_compass_bearing(self, point1, point2):
        """Calculates the bearing between two points.
            compass bearing is the angle between north and the direction of interest.
            The bearing is the angle measured in degrees in a clockwise direction 
            from the north line."""
        lat1 = math.radians(point1[0])
        lon1 = math.radians(point1[1])
        lat2 = math.radians(point2[0])
        lon2 = math.radians(point2[1])

        diffLong = math.radians(lon2 - lon1)
        
        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                * math.cos(lat2) * math.cos(diffLong))
        
        initial_bearing = math.atan2(x, y)
        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360
        
        return round(compass_bearing,6)
    
    def get_turning_angle(self):
        """Returns the turning angle required to reach the target"""
        #should be used with sensor data
        if self.heading is not None:
            turning_angle = self.heading - self.get_heading_virtual()
            return turning_angle
        else:
            return None

    def get_heading_from_sensor(self):
        """Returns the heading based on magnetometer data
        Should be used with sensor data"""
        heading = self.ins.get_heading()
        return heading
    
    def get_speed(self):
        return self.speed

    def manoeuvre_simulation(self, frame):
        # Initialize the PID controller parameters
        Kp = 1.0
        Ki = 0.55
        Kd = 0.01

        integral = 0
        previous_error = 0

        #current_position = self.get_current_position()
        
        if frame < len(self.shortest_path)-1:

            current_node = self.shortest_path[frame]
            next_node = self.shortest_path[frame + 1]
            x_current, y_current = self._graph.nodes[current_node]['x'], self._graph.nodes[current_node]['y']
            x_next, y_next = self._graph.nodes[next_node]['x'], self._graph.nodes[next_node]['y']
            self.heading = self.calculate_initial_compass_bearing((x_current,y_current), (x_next,y_next))
            
            while True:
                #target_position = self.get_target_position()
                distance_to_target = round(self.distance(x_current, y_current, x_next, y_next))
                print("Distance to target:", distance_to_target)
                if distance_to_target <= 0.1:
                    print("Reached target position")
                    break
                    
                # Calculate the bearing to the target position
                bearing_to_target = self.calculate_initial_compass_bearing((x_current,y_current), (x_next,y_next))

                # Calculate the error as the difference between the target bearing and the current heading
                if self.heading is not None:
                    error = (bearing_to_target - self.heading + 180) % 360 - 180
                    #if error > 180:
                     #   error -= 360

                    # Calculate the integral and derivative of the error
                    integral += error
                    derivative = error - previous_error

                    # Use the PID controller to calculate the turning angle
                    turning_angle = round((Kp * error + Ki * integral + Kd * derivative))
                    print("Turning Angle:", turning_angle)

                    # Update the heading
                    self.heading += turning_angle
                    self.heading = round(self.heading,6)
                    print("Heading:", self.heading)

                    # Calculate the step size based on the speed and the distance to the target
                    step_size = min(self.speed, distance_to_target)
                    print("Step Size:", step_size)

                    # Update current position based on speed and heading
                    x_current += round((step_size * math.cos(math.radians(self.heading))))
                    y_current += round((step_size * math.sin(math.radians(self.heading))))
                    #current_position = [round(coord, 6) for coord in current_position]  # Round current position to 4 decimal places

                    print("Current Position:", x_current, y_current)
                    # Update the previous error
                    previous_error = error
                    #time.sleep(0.5)
                    """ data_JSON =  {
                        "lat": current_position[0],
                        "lon": current_position[1],        
                    }
                    with open(f'{os.path.abspath(os.path.join(os.path.dirname(__file__),"../../.."))}/L2_Data/gps_dummy.json', "w") as write_file:
                        json.dump(data_JSON, write_file) """
                    self.start_point.set_data(x_current, y_current)
                    return self.start_point,
    
    def manoeuvre_plot(self):
        # Initialize the PID controller parameters
        Kp = 0.5
        Ki = 0.5
        Kd = 0.0

        integral = 0
        previous_error = 0

        #current_position = self.get_current_position()
        
        for i in range(len(self.shortest_path) - 4):

            current_node = self.shortest_path[i]
            next_node = self.shortest_path[i + 1]
            x_current, y_current = self._graph.nodes[current_node]['x'], self._graph.nodes[current_node]['y']
            print("Current Position:", x_current, y_current)
            x_next, y_next = self._graph.nodes[next_node]['x'], self._graph.nodes[next_node]['y']
            print("Next Position:", x_next, y_next)
            self.heading = self.calculate_initial_compass_bearing((x_current,y_current), (x_next,y_next))   
            while True:
                #target_position = self.get_target_position()
                distance_to_target = round(self.distance(x_current, y_current, x_next, y_next))
                print("Distance to target:", distance_to_target)
            
                if distance_to_target <= 5:
                    print("Reached target position")
                    break                    
                # Calculate the bearing to the target position
                bearing_to_target = self.calculate_initial_compass_bearing((x_current,y_current), (x_next,y_next))

                # Calculate the error as the difference between the target bearing and the current heading
                error = (bearing_to_target - self.heading + 180) % 360 - 180
                #if error > 180:
                 #   error -= 360

                # Calculate the integral and derivative of the error
                integral += error
                derivative = error - previous_error

                # Use the PID controller to calculate the turning angle
                turning_angle = round((Kp * error + Ki * integral + Kd * derivative))
                print("Turning Angle:", turning_angle)

                # Update the heading
                self.heading += turning_angle
                self.heading = round(self.heading,6)
                print("Heading:", self.heading)

                # Calculate the step size based on the speed and the distance to the target
                step_size = min(self.speed, distance_to_target)
                print("Step Size:", step_size)

                # Update current position based on speed and heading
                x_current += (step_size * math.cos(math.radians(self.heading)))
                y_current += (step_size * math.sin(math.radians(self.heading)))
                #current_position = [round(coord, 6) for coord in current_position]
                self.route.append((x_current, y_current))
                print("Current Position:", x_current, y_current)
                time.sleep(0.1)
        print("Route:", self.route)        
    
    def hardware_manoeuvre(self):
        if self.map_coordinates is not None:    
            for i in range(len(self.map_coordinates) - 1):
                self.target_position = self.get_target_position(i+1)
                self.current_position = self.get_current_position(i)
                self.heading = self.get_heading_virtual()
                self.get_distance()
                self.get_turning_angle()
                self.get_heading_from_sensor()
                self.gps_data()
                goal_reached = False
                current_lat = self.current_position[0]
                current_lon = self.current_position[1]
                while goal_reached == False:            
                    # Calculate the distance to move based on speed and time
                    self.time_interval = 0.1
                    # Calculate the distance to move based on speed and time
                    distance = self.get_speed() * self.time_interval
                    # Calculate the change in latitude and longitude
                    delta_lat = distance * math.cos(math.radians(self.heading))#change the heading based on sensor data
                    delta_lon = distance * math.sin(math.radians(self.heading))#change the heading based on sensor data
                    # Update the current position
                    current_lat += delta_lat
                    current_lon += delta_lon
                    if self.distance(current_lat, current_lon, self.target_position[0], self.target_position[1]) <= 0.1:
                        goal_reached = True
                    # Print the updated location
                    print("Updated Location: Latitude =", current_lat, "Longitude =", current_lon)
                time.sleep(0.1)
                self.map_coordinates.pop(0)
        else:
            return None, None
        
        
    def plot_route(self):
        self.manoeuvre_plot()
        # Unzip the route into X and Y coordinates
        X, Y = zip(*self.route)

        # Create the plot
        plt.figure()
        plt.plot(X, Y, 'ro-')

        # Show the plot
        plt.show()

    def gps_data(self):
        try:
            self.lat, self.lon, self.height = self.gps.get_data()
        except JSONDecodeError as e:
            print("Failed to read JSON, return code %d\n", e) 
            return None
        
        
