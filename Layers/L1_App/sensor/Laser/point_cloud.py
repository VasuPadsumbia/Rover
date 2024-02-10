from re import L
import sickpy.sick as sick
import cv2
import time, json, os, math
from json.decoder import JSONDecodeError
#import helper as helper
class Laser():
    def __init__(self) -> None:
        #self.config_path = helper.config_path()
        self.x = None
        self.y = None
        self.d = None
        self.cartesian_data = None
        self.polar_coordinates = None
        self.config_path = f'{os.path.abspath(os.path.join(os.path.dirname(__file__),"../../../.."))}/Configure.json'
        try:
            with open(self.config_path, "r") as config_file:
                data = json.load(config_file)
                self.port = data['laser']['port']
                config_file.close()
        
        except JSONDecodeError as e:
            print("Failed to read JSON, return code %d\n", e)
        
        #self.polarMap_path = helper.polarMap_path()
        
        self.laser = self.connect()
        self.scan()

    def scan(self):
        ''' Scans the laser'''
        while True:
            self.get_data()
            #self.avoid_obstacle()

    def get_data(self):
        ''' Returns the laser data '''
        try:
            print(".")
            if self.laser.get_frame():
                print(f'cartesian: {self.laser.cartesian}')
                #print(f'Cartesian Coordinates: {self.get_cartesian()}')
                #self.polar_coordinates = self.cartesian_to_polar()
                #print(f'Polar Coordinates: {self.cartesian_to_polar()}')
                #if self.obstacle_within_range(self.d):
                #    print("Obstacle within range")
                #self.laser.make_image()
                
                #cv2.imshow("img", self.laser.image)
                #cv2.waitKey(3)
                #print(f'logging coordinates(): {self.log_polar()}')
                time.sleep(0.01)
        except KeyboardInterrupt:
            print("Disconnected")
            cv2.destroyAllWindows()
            return None
        
    def connect(self):
        ''' Creates Laser connection'''
        return sick.SICK(self.port)
    
    def log_polar(self):
        ''' Logs the laser data'''
        try:    
            with open(self.polarMap_path, "w") as polarMap_file:
                data = [self.polar_coordinates[i:i+2] for i in range(0, len(self.polar_coordinates), 2)]
                data_JSON = { 'laser' : data}
                json.dump(data_JSON, polarMap_file, indent=4)
                polarMap_file.close()
                
        except JSONDecodeError as e:
            print("Failed to read JSON, return code %d\n", e)
        
    
    def get_cartesian(self):
        ''' Returns the cartesian coordinates'''
        self.cartesian_data = self.laser.cartesian
        #print(f'cartesian_data: {self.cartesian_data[[0]]}')
        for x, y, d in self.cartesian_data:
            print(f'x: {x}')
            #self.x.append(x)
            #self.y.append(y)
            #self.d.append(d)

        return self.x, self.y, self.d

    def cartesian_to_polar(self):
        ''' Converts cartesian coordinates to polar coordinates'''
        self.cartesian_data()
        for x, y, d in self.cartesian_data:
            self.r.append(math.sqrt(x**2 + y**2))
            self.theta.append(math.atan2(y, x))
        return (self.r, self.theta)
    
    def obstacle_within_range(self, r):
        ''' Checks if obstacle is within range'''
        if r < 0.5:
            return True
        else:
            return False

    def avoid_obstacle(self):
        ''' Checks nearby obstacle coordinates and decides which direction to turn '''
        x, y, d = self.get_cartesian()
        rover_width = float('inf')
        obstacle_index = []
        distance = []
        # Find the nearest obstacle
        for i in range(len(d)):
            if self.obstacle_within_range(d[i]):
                #min_distance = d[i]
                obstacle_index.append(i)

        if len(obstacle_index) != 0:
            # Determine the direction to turn based on obstacle coordinates
            for i in range(len(obstacle_index)):
                distance_between_obstacles = math.sqrt((x[obstacle_index[i+1]] - x[obstacle_index[i]])**2 + (y[obstacle_index[i+1]] - y[obstacle_index[i]])**2)
                distance.append(distance_between_obstacles)
                if distance_between_obstacles > rover_width: # check is the rover can pass through the obstacle
                    theta_1 = math.degrees(math.atan2(y[obstacle_index[0]], x[obstacle_index[0]])) # angle from rover to first obstacle point
                    theta_2 = math.degrees(math.atan2(y[obstacle_index[i]], x[obstacle_index[i]])) # angle from rover to last obstacle point
                    theta_3 = math.degrees(math.atan2(y[obstacle_index[i+1]], x[obstacle_index[i+1]])) # angle from rover to the obstacle that is apart from the first obstacle
                    if theta_1 > 90:
                        print(f'move forward')    
                    elif theta_2 > 90:
                        print(f'turn angle: {(theta_3 - theta_2)/2}')
                        print("turn right")
                    elif theta_3 > 90 and theta_2 < 90:
                        print(f'turn angle: {(theta_3 - theta_2)/2}')
                        print("turn left")
                    else:
                        pass
                else:
                    continue
            

laser = Laser()
laser.scan()
        

        
    