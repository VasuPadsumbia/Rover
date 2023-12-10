from abc import abstractmethod
import argparse
from sbp.client.drivers.network_drivers import TCPDriver
from sbp.client import Handler, Framer
from sbp.navigation import * 
from json.decoder import JSONDecodeError
import os
class connect_pksi_velocity():

    def __init__(self) -> None:

        """_summary_

        This code opens piksi multi at IP address mentioned in Config.json file in workspace
        and generats coordinates of the rover and saves it into imu/gyro_data.json.

        """
        self.sog_ = 0.0
        
        self.config_path = f'{os.path.abspath(os.path.join(os.path.dirname(__file__),"../.."))}/Configure.json'
        

        try:
            with open(self.config_path, "r") as config_file:
                data = json.load(config_file)
                self.IP_add = data['dgps']['IP_add']
                self.port = data['dgps']['port']
                config_file.close()
        
        except JSONDecodeError as e:
            print("Failed to read JSON, return code %d\n", e)

    
    def get_data(self):
        # Open a connection to Piksi using TCP
        with TCPDriver(self.IP_add, self.port) as driver:
            with Handler(Framer(driver.read, None, verbose=True)) as source:
                print(f'Connection Eshtablished for piksi at IP {self.IP_add}')

                ''' Getting data'''
                try:

                    msg, metadata = next(source.filter([SBP_MSG_VEL_COG]),(None,None))
                    if msg is not None:
                        self.sog_= msg.sog * 1e-3
                        # Print out the Acceleration in X, Y, Z directions of the rover
                        print("Speed over ground (based on horizontal velocity) : %.4f, "
                                % (self.sog_))
                except KeyboardInterrupt:
                    raise NotImplementedError("Sensor data not obtained")
    
        def log(self):
            data_JSON =  {
                "sog": self.sog_,
            }
            with open("imu/speed_over_gnd_data.json", "w") as write_file:
                json.dump(data_JSON, write_file)
    
    
    

    