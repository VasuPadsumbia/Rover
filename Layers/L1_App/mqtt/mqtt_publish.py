# ------------------------------------------------
# --- Author: Farogh Iftekhar
# ------------------------------------------------
''' Description: This file has mqtt pulish class and function to send the data to the broaker'''

import time
import json
import random
from json.decoder import JSONDecodeError
from helper import *

from paho.mqtt import client as mqtt_client

class Singleton_meta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton_meta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class MQTT_Publish(metaclass = Singleton_meta):

    def __init__(self) -> None:
        self.config_path = config_path()

        try:
            with open(self.config_path, "r") as config_file:
                data = json.load(config_file)
                self.broker = data['mqtt']['broker']
                self.port = data['mqtt']['port']
                self.qos = data['mqtt']['qos']
                config_file.close()
                
        except JSONDecodeError as e:
            print("Failed to read JSON, return code %d\n", e)

    def connect_mqtt(self):
        ''' Creates MQTT connection'''
        def on_connect(client, userdata, flag, rc):
            if rc == 0:
                print('Connected to MQTT Broaker: {}'.format(self.broker))

            else:
                print("Failed to connect, return code %d\n", rc)

        client_name = "BOT-" + str(random.randint(10000, 20000))
        client = mqtt_client.Client(client_name)
        client.on_connect = on_connect
        client.connect(self.broker, int(self.port))
        return client

    def connect_publisher(self, topic, msg):
        ''' Publish data to the broaker'''
        try:
            client = self.connect_mqtt()
            client.loop_start()
            time.sleep(0.1)
            client.publish(topic, str(msg), qos=self.qos)  # publish message
            print (f'Message {msg} sent on topic {topic}')
            time.sleep(0.1)
            client.disconnect()    # disconnect gracefully
            client.loop_stop()     # stops network loop
        
        except:
            print("Error sending msg to the broker!")
        
