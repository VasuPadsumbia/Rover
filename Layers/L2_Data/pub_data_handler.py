# ------------------------------------------------
# --- Author: Farogh Iftekhar
# ------------------------------------------------
''' Description: This file accept data from L3 layer and send data to L1 MQTT'''

import json

from Layers.L1_App.mqtt.mqtt_publish import MQTT_Publish

class Singleton_meta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton_meta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Pub_Handler(metaclass = Singleton_meta):
    def __init__(self) -> None:
        self.mqtt_pub = MQTT_Publish()

    def data_handler(self, msg_dict):
        '''responsible to send the data'''
        # convert dict to JSON
        value = self.dictTOjson(msg_dict)
        topic = value[0]
        msg = value[1]

        # pulish to mqtt broker
        self.mqtt_pub.connect_publisher(topic, msg)
        
    def dictTOjson(self, msg_dict):
        '''Coverts Dict to Json and return JSON'''
        try:
            if msg_dict.get('topic')!=None:
                topic = msg_dict["topic"]
                msg_dict.pop('topic')
                msg_json = json.dumps(msg_dict, indent=4)
                value = [topic, msg_json]
                return value

        except Exception:
            print("Missing topic in dictionary")