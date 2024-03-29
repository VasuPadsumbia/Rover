import json, time, os
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt
from helper import *
from json.decoder import JSONDecodeError
from queue import Queue
from Layers.L2_Data.pub_data_handler import Pub_Handler
from Layers.L1_App.sensor.dgps.DGPS import connect_pksi_dgps
import Layers.L1_App.driver.rover as rover
from Layers.L1_App.navigation.create_map_network import MapHandler
from Layers.L1_App.sensor.Laser.point_cloud import Laser as ls
from Layers.L1_App.navigation.object_avoid_final import Object_avoid
class AppCommand:
    def __init__(self) -> None:
        """Init Roboclaw"""
        self.enableManual = 69
        #self.rover = rover()
        # check connection is working between Jetson and Roboclaw
    """ while True:
            if not self.spi.spiHandshake():
                print("SPI connection error, check wiring!")
                time.sleep(0.5)
            else:
                break """

    def worker(self, q1, q2):
        print("Connected to mqtt")
        while True:
            try:
                command = q1.get()
                # convert string to  object
                json_object = json.loads(command)
                print(json_object)
                # Check data type coming from APP
                if not (json_object.get("botCommand") is None):
                    print("botCommand received: {}".format(json_object["botCommand"]))
                    #self.rover.command(int(json_object["botcommand"]))
                    if json_object["botCommand"] == 17:
                        rover.forward(33)
                        print("Robot is moving forwardm1")
                    elif json_object["botCommand"] == 18:
                        rover.backward(33)
                        print("Robot is moving backward")
                    elif json_object["botCommand"] == 20:
                        rover.right(90)
                        print("Robot is moving right")
                    elif json_object["botCommand"] == 24:
                        rover.left(90)
                        print("Robot is moving left")
                    elif json_object["botCommand"] == 16:
                        rover.stop()
                        print("Robot is stopped")
                elif not (json_object.get("autoMode") is None):
                    print("autoMode received: {}".format(json_object["autoMode"]))
                    #self.rover.command(int(json_object["autoMode"]))

                elif not (json_object.get("manualMode") is None):
                    print("manualMode received: {}".format(json_object["manualMode"]))
                    #self.rover.command(int(json_object["manualMode"]))

                elif not (json_object.get("targetLocation") is None):
                    print("targetLocation received: {}".format(json_object["targetLocation"]))
                    q2.put(json_object["targetLocation"])

                else:
                    print("not a valid Json format!")

            except KeyboardInterrupt:
                print("exiting")


class AppData:
    def __init__(self) -> None:
        #Init MQTT & SPI
        self.mqtt = Pub_Handler()
        
        self.datarefreshRate = 30
        self.coordinates = (0, 0)
        self.config_path = config_path()
        self.gps = connect_pksi_dgps(self.config_path)
        # Data Log for autonomous mode
        print(f'Getting Longitudenal and Latitude data: {self.gps.get_data(type="rover")}')
        print(f'Logging Longitudenal and Latitude data: {self.gps.log()}')
    def uploader(self, dataList):
        print(dataList)

        if dataList[0] < 400:
            Ultrasonic1 = dataList[0]
        elif dataList[1] < 400:
            Ultrasonic2 = dataList[1]
        elif dataList[2] < 360:
            heading = dataList[2]

        '''
        # Dictionary
        msg_dict = {
            "topic": "/bot/data",
            "distance": Ultrasonic1,
            "direction": heading,
        }
        print(msg_dict)'''

        # send msg to MQTT broaker
        # time.sleep(self.datarefreshRate)
        # self.mqtt.data_handler(msg_dict)

    def worker(self):
        while True:
            try:
                """Establishing connection with GPS"""
                
                self.coordinates = self.gps.get_data(type="rover")
                print(f'Getting Longitudenal and Latitude data: {self.coordinates}')
                # print(f'Logging Longitudenal and Latitude data: {gps.log()}')
            except KeyboardInterrupt:
                print("GPS connection ended") 

            except Exception as e:
                print(e) 
            
            # Dictionary
            msg_dict = {
                "topic": "/bot/data",
                "latitude": str(self.coordinates[0]),
                "longitude": str(self.coordinates[1]),
            }
            print(msg_dict)
            # send msg to MQTT broaker
            time.sleep(self.datarefreshRate)
            self.mqtt.data_handler(msg_dict)
            
class Navigator:
    def __init__(self) -> None:
        #self.mqtt = Pub_Handler()
        self.laser = ls()
        # config_path = f'{os.path.abspath(os.path.dirname(__file__))}/Layers/L2_Data/gps_data.json'
        config_path = gps_path()
        try:
            with open(config_path, "r") as config_file:
                data = json.load(config_file)
                lat = data['lat']
                lon = data['lon']
                config_file.close()
        
        except JSONDecodeError as e:
            print("Failed to read JSON, return code %d\n", e) 

        self.coordinates = (lat, lon)

    def autonomousNavigator(self, q2):
        try:
            """Once set the target position, this function will receive
            the value and set it to algorithm to start."""
            targetLocation = q2.get()
            print(targetLocation)
            #print(self.coordinates)
            map = MapHandler(type='all', destination=targetLocation, coordinates=self.coordinates)
            # print(f'create area graph(): {map.create_area_graph()}')
            # print(f'find shortest path between two points():{map.find_shortest_path_between_two_points()}')
            # cartesian_coordinates = map.cartesian_coordinates()
            # print(f'cartesian coordinates(): {cartesian_coordinates}')
            # print(f'logging coordinates(): {map.log_coordinates()}')
            # print(f'plot graph shortest route(): {map.plot_graph_shortest_route()}')
            print(f'plot graph(): {map.get_map()}')
            # Publish the initial direction to app
            """ msg_dict = {
                "topic": '/navigation/data',
                "path": cartesian_coordinates,
                "coordinates": self.coordinates
            }

            self.mqtt.data_handler(msg_dict) """
        except Exception as e:
            print("error in navigator library!: {}".format(e))

    def worker(self, q2):
        while True:
            try:
                self.autonomousNavigator(q2)
                # print(f'Laser data: {self.laser.scan()}')

            except KeyboardInterrupt:
                print("exiting navigator with error!")

#Update the below code for point cloud from SICK laser sensor or camera object avoidance algorithm
class manoeuvre:
    def __init__(self) -> None:
        self.laser = ls()
        self.ob = Object_avoid(self.laser.laser, target_distance=40, target_angle=(60, 120))
    def worker(self):
        while True:
            try:    
                print(f'Laser data: {self.laser.scan()}')
                print(f'Object Avoidance: {self.ob.object_detect()}')
                time.sleep(0.1)
            except KeyboardInterrupt:
                print("exiting manoeuvre with error!")
