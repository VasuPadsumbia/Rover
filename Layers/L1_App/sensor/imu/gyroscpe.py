import os, argparse
from sbp.client.drivers.network_drivers import TCPDriver
from sbp.client import Handler, Framer
from json.decoder import JSONDecodeError
import json
from sbp.imu import SBP_MSG_IMU_RAW


class connect_pksi_gyroscope():

    def __init__(self) -> None:

        """_summary_

        This code opens piksi multi at IP address mentioned in Config.json file in workspace
        and generats coordinates of the rover and saves it into imu/gyro_data.json.

        """
        self.gyr_x_ = 0.0
        self.gyr_y_ = 0.0
        self.gyr_z_ = 0.0
        
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

                    msg, metadata = next(source.filter([SBP_MSG_IMU_RAW]),(None,None))
                    if msg is not None:
                        print(f'Data Recieving from piksi at IP {msg.sender}')
                        self.gyr_x_= msg.gyr_x * 1e-3
                        self.gyr_y_= msg.gyr_y * 1e-3
                        self.gyr_z_= msg.gyr_z * 1e-3
                        
                    self.log()
                    # Print out the Acceleration in X, Y, Z directions of the rover
                    print("Gyroscope X : %.4f, "
                          "Gyroscope Y : %.4f,"
                          "Gyroscope Z : %.4f"
                            % (self.gyr_x_, self.gyr_y_, self.gyr_z_))

                except KeyboardInterrupt:
                    raise NotImplementedError("Sensor data not obtained")

    def log(self):
        data_JSON =  {
            "gyr_x": self.gyr_x_,
            "gyr_y": self.gyr_y_,
            "gyr_z": self.gyr_z_
        }
        with open("imu/gyro_data.json", "w") as write_file:
            json.dump(data_JSON, write_file)
    

    