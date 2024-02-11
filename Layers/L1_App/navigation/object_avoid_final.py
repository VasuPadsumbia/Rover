from Layers.L1_App.sensor.Laser.sickpy.sick2 import SICK
import math
import Layers.L1_App.driver.rover as bot

class Object_avoid:
    def __init__(self, sick, target_distance, target_angle):
        self.sick = sick
        self.target_distance = target_distance
        self.target_angle_range = target_angle
        self.point = []
        self.angle = 0
        self.steps = 0
        self.left = False
        self.right = False
        self.side = True

    def object_detect(self):
        while True:
            bot.forward1()
            self.sick.get_frame()  # Update SICK data
            obstacles = [coord[1] for coord in self.sick.polar]

            # Check for obstacles in the specified angle range
            for i in range(len(obstacles)):
                distance, angle = obstacles[i]
                if self.target_angle_range[0] <= angle <= self.target_angle_range[1]:
                    if distance <= self.target_distance:
                        bot.stop()
                        print(f"Rover is stopped as Obstacle is detected at {self.target_distance} cm away")
                        self.steps = self.steps + 1
                        self.forward = True   
                elif 120<= angle <= 180:
                    self.left = True
                elif 0<= angle <= 60:
                    self.right = True
                elif (self.left and self.right == True) and self.forward == False:
                    bot.forward1()

            self.angle= (self.steps * 0.5)
            ob.object_avoid(self.angle,self.target_distance)

    def object_avoid(self, angle, target_distance):
        if self.right == False:
            bot.right(angle)
        elif self.left == False:
            bot.left(angle)

        bot.forward(target_distance + 5)

        if self.right == False:
            bot.left(angle)
        elif self.left == False:
            bot.right(angle)

        bot.forward1()

        obstacles = [coord[1] for coord in self.sick.polar]
        for i in range(len(obstacles)):
                distance, angle = obstacles[i]
                if (120 <= angle <= 180) and (distance == 0):
                    print("Rover Side is completed")
                    self.side == True

        bot.forward(10)

        self.object_back = math.sqrt((target_distance + 5)**2 - (target_distance)**2)

        if self.right == False:
            bot.left(90)
        elif self.left == False:
            bot.right(90)

        bot.forward(self.object_back)

        if self.right == False:
            bot.right(90)
        elif self.left == False:
            bot.left(90)

# sick = SICK(port="/dev/ttyUSB1")  # Replace with your actual port
# ob = Object_avoid(sick, target_distance=40, target_angle=(60, 120))
# ob.object_detect()