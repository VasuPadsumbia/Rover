import json, time
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt
from Layers.L2_Data.pub_data_handler import Pub_Handler
#from Layers.L1_App.driver.rover import
from helper import *


class AppCommand:
    def __init__(self) -> None:
        """Init Roboclaw"""
        self.enableManual = 69

        # check connection is working between Jetson and Roboclaw
    """ while True:
            if not self.spi.spiHandshake():
                print("SPI connection error, check wiring!")
                time.sleep(0.5)
            else:
                break """

    def worker(self, q1, q2):
        while True:
            try:
                command = q1.get()
                # convert string to  object
                json_object = json.loads(command)

                # Check data type coming from APP
                if not (json_object.get("botCommand") is None):
                    print("botCommand received: {}".format(json_object["botCommand"]))
                    self.rover(self.enableManual)
                    time.sleep(1)
                    self.rover(int(json_object["botcommand"]))

                elif not (json_object.get("autoMode") is None):
                    print("autoMode received: {}".format(json_object["autoMode"]))
                    self.rover(int(json_object["autoMode"]))

                elif not (json_object.get("manualMode") is None):
                    print("manualMode received: {}".format(json_object["manualMode"]))
                    self.rover(int(json_object["manualMode"]))

                elif not (json_object.get("targetPosition") is None):
                    q2.put(json_object["targetPosition"])

                else:
                    print("not a valid Json format!")

            except KeyboardInterrupt:
                print("exiting")


class AppData:
    def __init__(self) -> None:
        """Init MQTT & SPI"""
        self.mqtt = Pub_Handler()
        self.spi = SPI()
        self.datarefreshRate = 30

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
        flag = False
        counter = 0
        dataList = []
        while True:
            try:
                # Read data from SPI
                val = self.spi.rxpi()
                #print("val is: ")
                #print(val)
                if flag == True:
                    #print("flag = true!")
                    dataList.append(val)
                    if counter == 8:
                        #print("list full")
                        print(dataList)
                        int1 =  dataList[3]<<8
                        int1 |= dataList[2]
                        int2 =  dataList[5]<<8
                        int2 |= dataList[4]
                        int3 =  dataList[7]<<8
                        int3 |= dataList[6]
                        print(int1,int2,int3)
                        dataList = [int1,int2,int3]
                        self.uploader(dataList)
                        counter = 0
                        flag = False
                        dataList.clear()
                    counter+=1

                if val == 89:
                    #print("89 detected")
                    flag = True

                time.sleep(0.1)

            except Exception as e:
                print(e)


class Navigator:
    def __init__(self) -> None:
        self.mqtt = Pub_Handler()

    def autonomousNavigator(self, q2):
        try:
            """Once set the target position, this function will receive
            the value and set it to algorithm to start."""
            targetPosition = q2.get()
            print(targetPosition)

            """with open(smallMap_path(), "r") as f:
                mapData = json.load(f)['data']
                
            with open(polarMap_path(), "r") as f:
                jsonData = json.load(f)
                navigator = Navigator(point_cloud_polar, position_map, path_map, target) -> None:
                startTime = datetime.now()
                path = navigator.generate_path()
                stopTime = datetime.now()
                timeTaken = stopTime - startTime

                direction = navigator.get_orientation()

                # Publish the initial direction to app
                msg_dict = {
                    "topic": '/bot/data',
                    "direction": direction
                }

                self.mqtt.data_handler(msg_dict)"""

        except Exception as e:
            print("error in navigator library!: {}".format(e))

    def worker(self, q2):
        while True:
            try:
                self.autonomousNavigator(q2)

            except KeyboardInterrupt:
                print("exiting navigator with error!")
