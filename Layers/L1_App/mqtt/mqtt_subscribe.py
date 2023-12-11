# ------------------------------------------------
# --- Author: Farogh Iftekhar
# ------------------------------------------------
''' Description: This file has mqtt subscribe class and function to receive the data from the broaker'''
from paho.mqtt import client as mqtt_client
import time
import json
import random
from json.decoder import JSONDecodeError
from helper import *

class Singleton_meta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton_meta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class MQTT_Subscribe(metaclass = Singleton_meta):
    def __init__(self):
        self.config_path = config_path()
        self.Connected = True
        try:
            with open(self.config_path, "r") as config_file:
                data = json.load(config_file)
                self.broker = data['mqtt']['broker']
                self.port = data['mqtt']['port']
                self.qos = data['mqtt']['qos']
                config_file.close()
                
        except JSONDecodeError as e:
            print("Failed to read JSON, return code %d\n", e)

    def subscribe_mqtt(self, queue):
        ''' Creates MQTT connection'''
        def on_connect(client, userdata, flag, rc):
            if rc == 0:
                print('Connected to MQTT Broaker: {}'.format(self.broker))

            else:
                print("Failed to connect, return code %d\n", rc)

        def on_message(client, userdata, message):
            #print ("Message received: "  + message.payload.decode('utf-8'))
            queue.put(message.payload.decode('utf-8'))

        client_name = "BOT-" + str(random.randint(20001, 30000))
        client = mqtt_client.Client(client_name)
        client.on_connect = on_connect
        client.on_message = on_message 
        client.connect(self.broker, int(self.port))

        #start the loop
        client.loop_start()       

        #Wait for connection
        while self.Connected != True:    
            time.sleep(0.1)
            
        client.subscribe("/bot/control")
            
        try:
            while True:
                time.sleep(1)
            
        except KeyboardInterrupt:
            print ("exiting")
            client.disconnect()
            client.loop_stop()
