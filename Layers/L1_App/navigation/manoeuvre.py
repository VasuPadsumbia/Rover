import os, math, sys, numpy as np, matplotlib.pyplot as plt
from turtle import position
from matplotlib.pylab import f
from re import L
from json.decoder import JSONDecodeError
import json, time

class Target_manoeuvre():
    def __init__(self, speed, map_path):
        self.speed = speed
        self.path = map_path
        self.map_coordinates = self.get_coordinates()
        self.target_position = self.get_target_position()
        self.current_position = self.get_current_position()
        self.heading = self.get_heading()
        #self.update_position = self.update_current_position()

        #self.heading = self.calculate_heading() #add heading from magnetometer
    def get_coordinates(self):    
            try:
                with open(self.path, "r") as config_file:
                    data = json.load(config_file)
                    config_file.close()
                    return data
            except JSONDecodeError as e:
                print("Failed to read JSON, return code %d\n", e) 
                return None
            
    def get_target_position(self):
        if self.map_coordinates is not None:
            target_position = [round(self.map_coordinates["Point 2"]["Latitude"],6), round(self.map_coordinates["Point 2"]["Longitude"],6)]
            print(f"target_position: {target_position}")
            return target_position
        else:
            return None, None
    
    def get_current_position(self):
        if self.map_coordinates is not None:
            current_position = [round(self.map_coordinates["Point 1"]["Latitude"],6), round(self.map_coordinates["Point 1"]["Longitude"],6)]
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
    
    def get_heading(self):
        """Returns the heading to the target"""

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
            turning_angle = self.heading - self.get_heading()
            return turning_angle
        else:
            return None
        
    def calculate_heading(magnetometer_x, magnetometer_y):
        """Returns the heading based on magnetometer data
        Should be used with sensor data"""
        heading = math.atan2(magnetometer_y, magnetometer_x)
        heading = math.degrees(heading)
        if heading < 0:
            heading += 360
        return heading
    
    def get_speed(self):
        return self.speed
    
    def update_current_position(self,position):
        # Simulate the new current position based on input speed
        position[0] += self.speed * math.cos(math.radians(self.heading))
        position[1] += self.speed * math.sin(math.radians(self.heading))
        position = [round(coord, 6) for coord in self.current_position]  # Round current position to 4 decimal place
        return position

    def manoeuvre(self):
        # Initialize the PID controller parameters
        Kp = 0.5
        Ki = 0.55
        Kd = 0.0

        integral = 0
        previous_error = 0

        current_position = self.get_current_position()

        while True:
            target_position = self.get_target_position()
            distance_to_target = round(self.distance(current_position[0], current_position[1], target_position[0], target_position[1]),6)
            print("Distance to target:", distance_to_target)
            if distance_to_target is not None:
                if distance_to_target <= 23:
                    print("Reached target position")
                    break
                
            # Calculate the bearing to the target position
            bearing_to_target = self.calculate_initial_compass_bearing(current_position, target_position)

            # Calculate the error as the difference between the target bearing and the current heading
            error = (bearing_to_target - self.heading + 180) % 360 - 180
            #if error > 180:
             #   error -= 360

            # Calculate the integral and derivative of the error
            integral += error
            derivative = error - previous_error

            # Use the PID controller to calculate the turning angle
            turning_angle = round((Kp * error + Ki * integral + Kd * derivative),6)
            print("Turning Angle:", turning_angle)

            # Update the heading
            self.heading += turning_angle
            self.heading = round(self.heading,6)
            print("Heading:", self.heading)

            # Calculate the step size based on the speed and the distance to the target
            step_size = min(self.speed, distance_to_target)
            print("Step Size:", step_size)

            # Update current position based on speed and heading
            current_position[0] += round((step_size * math.cos(math.radians(self.heading))), 6)
            current_position[1] += round((step_size * math.sin(math.radians(self.heading))), 6)
            current_position = [round(coord, 6) for coord in current_position]  # Round current position to 4 decimal places

            print("Current Position:", current_position)

            # Update the previous error
            previous_error = error
            #time.sleep(0.5)
            """ data_JSON =  {
                "lat": current_position[0],
                "lon": current_position[1],        
            }
            with open(f'{os.path.abspath(os.path.join(os.path.dirname(__file__),"../../.."))}/L2_Data/gps_dummy.json', "w") as write_file:
                json.dump(data_JSON, write_file) """
        return current_position

    def set_pid_parameters(self, Kp, Ki, Kd):
        # Set the PID controller parameters
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
