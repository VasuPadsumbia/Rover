import os
import argparse
from sbp.client.drivers.network_drivers import TCPDriver
from sbp.client import Handler, Framer
from sbp.navigation import SBP_MSG_POS_ECEF
from json.decoder import JSONDecodeError
import json
from helper import *

class Singleton_meta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton_meta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class connect_pksi_dgps():

    def __init__(self) -> None:

        """_summary_

        Args:

        """

        self.config_path = f'{os.path.abspath(os.path.join(os.path.dirname(__file__),"../.."))}/Configure.json'
        #self.config_path = "Configure.json"

        try:
            with open(self.config_path, "r") as config_file:
                data = json.load(config_file)
                self.IP_add = data['dgps']['IP_add']
                self.port = data['dgps']['port']
                config_file.close()
        
        except JSONDecodeError as e:
            print("Failed to read JSON, return code %d\n", e)

    def connect_piksi(self):
        ''' Creates Piksi connection'''
        def on_connect(client, userdata, flag, rc):
            if rc == 0:
                print('Connected to MQTT Broaker: {}'.format(self.broker))

            else:
                print("Failed to connect, return code %d\n", rc)

        driver = TCPDriver(self.IP_add, self.port)
        source = Handler(Framer(driver.read, None, verbose=True))
        print(f'Connection Eshtablished for piksi at IP {self.IP_add}')
        return source

    def get_data(self):
        ''' Publish data to the broaker'''
        try:
            for msg, metadata in self.connect_piksi.filter(SBP_MSG_POS_ECEF):
                    # Print out the N, E, D coordinates of the baseline
                    print("he position solution message reports absolute Earth Centered Earth Fixed (ECEF)" 
                          "coordinates and the status (single point vs pseudo-absolute RTK) of"
                           "the position solution. If the rover receiver knows the surveyed position of"
                           "the base station and has an RTK solution, this reports a pseudo-absolute"
                           "position solution using the base station position and the rover's RTK"
                           "baseline vector.")
                    print(f'Data Recieving from piksi at IP {msg.sender}')
                    print(f'accuracy of data {msg.accuracy}')
                    print("Latitude: %.4f, Longitude: %.4f" % (msg.x , msg.y ))
                    #centre_point = lat,lon = (msg.x * 1e-3, msg.y * 1e-3)
                    #graph = ox.graph_from_point(centre_point, dist=1000, dist_type='bbox', 
                    #        network_type='walk')
                    #fig, ax = ox.plot_graph(graph, show=False, close=False, 
                    #                        bgcolor='w',node_color='b', node_size=2)
                    #plt.plot(lon, lat, marker="o", markersize=5, markeredgecolor="red", markerfacecolor="red", alpha=0.5)
                    #plt.show()         
        except:
            print("Error getting data!")