import json, time, os
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt
from helper import *
from json.decoder import JSONDecodeError

from Layers.L2_Data.pub_data_handler import Pub_Handler

def test():
    publish = Pub_Handler()
    
    msg_dict = {
                    "topic": '/bot/command',
                    "botCommand": "forward",
                    "manualMode": True,
                    "autoMode": False,
                    "targetLocation": (53.540966, 8.585301)
                }
    
    publish.data_handler(msg_dict)

