import os
import argparse
from sbp.client.drivers.network_drivers import TCPDriver
from sbp.client import Handler, Framer
from sbp.navigation import *
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
        self.flag = 0.0
        self.n = 0.0
        self.e = 0.0
        self.d = 0.0
        self.lat = 0.0
        self.lon = 0.0
        self.height = 0.0
        self.h = 0.0
        self.v_n = 0.0
        self.v_e = 0.0
        self.v_d = 0.0
        self.wn = 0
        self.tow = 0
        
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


    def get_data(self):
        iteration = 0
        ''' Creates Piksi connection'''
        with TCPDriver(self.IP_add, self.port) as driver:
            with Handler(Framer(driver.read, None, verbose=True)) as source:
                print(f'Connection Eshtablished for piksi at IP {self.IP_add}')
        
                ''' Getting data'''
                try:
                    #msg_list = [SBP_MSG_BASELINE_NED, SBP_MSG_POS_LLH,
                    #                SBP_MSG_VEL_NED, SBP_MSG_GPS_TIME]
                    
                    for msg, metadata in source.filter(SBP_MSG_POS_LLH):
                            iteration = 1 + iteration
                            print("he position solution message reports absolute Earth Centered Earth Fixed (ECEF)" 
                                  "coordinates and the status (single point vs pseudo-absolute RTK) of"
                                   "the position solution. If the rover receiver knows the surveyed position of"
                                   "the base station and has an RTK solution, this reports a pseudo-absolute"
                                   "position solution using the base station position and the rover's RTK"
                                   "baseline vector.")
                            print(f'Data Recieving from piksi at IP {msg.sender}')
                            print(f'accuracy of data {msg.h_accuracy}')
                            print("Latitude: %.4f, Longitude: %.4f" % (msg.lat , msg.lon ))

                            # LLH position in deg-deg-m
                            if msg.msg_type == 522:
                                self.lat = msg.lat
                                self.lon = msg.lon
                                self.h = msg.height

                            # RTK position in mm (from base to rover)
                            elif msg.msg_type == 524:
                                self.n = msg.n
                                self.e = msg.e
                                self.d = msg.d
                                self.flag = msg.flags

                            # RTK velocity in mm/s
                            elif msg.msg_type == 526:
                                self.v_n = msg.n
                                self.v_e = msg.e
                                self.v_d = msg.d

                            # GPS time
                            elif msg.msg_type == 258:
                                self.wn = msg.wn
                                self.tow = msg.tow  # in millis

                            else:
                                pass
                            
                            self.log()
                            #print(self.whole_string())
                            # f.write(line)
                            # f.write('\n')

                except iteration==10:
                    print("Error getting data!")
    
    
    def whole_string(self):
        '''
        Returns all the data as a string
        '''

        return('%.0f\t%.0f\t%2.8f\t%2.8f\t%4.6f\t%6.0f\t%6.0f\t%6.0f\t'
               '%6.0f\t%6.0f\t%6.0f\t%.0f\t' %
               (self.wn, self.tow, self.lat, self.lon, self.h, self.n, self.e,
                self.d, self.v_n, self.v_e, self.v_d, self.flag))
    
    def log(self):
        data_JSON =  {
	        "tow": self.tow,
	        "lat": self.lat,
	        "lon": self.lon,
	        "height": self.height,
        }
        with open("map_coordinates.json", "w") as write_file:
            json.dump(data_JSON, write_file)