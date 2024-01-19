import os, argparse
from tkinter import N
from sbp.client.drivers.network_drivers import TCPDriver
from sbp.client import Handler, Framer
from json.decoder import JSONDecodeError
import json, math
from sbp.mag import SBP_MSG_MAG_RAW
from sbp.imu import SBP_MSG_IMU_RAW
import math


class connect_pksi_INS():

    def __init__(self) -> None:

        """_summary_

        This code opens piksi multi at IP address mentioned in Config.json file in workspace
        and generats coordinates of the rover and saves it into imu/gyro_data.json.

        """
        self.mag_x_ = 0.0
        self.mag_y_ = 0.0
        self.mag_z_ = 0.0
        self.acc_x_ = 0.0
        self.acc_y_ = 0.0
        self.acc_z_ = 0.0
        self.heading_deg = 0.0
        self.config_path = f'{os.path.abspath(os.path.join(os.path.dirname(__file__),"../../../.."))}/Configure.json'
        

        try:
            with open(self.config_path, "r") as config_file:
                data = json.load(config_file)
                self.IP_add = data['dgps']['IP_add']
                self.port = data['dgps']['port']
                config_file.close()
        
        except JSONDecodeError as e:
            print("Failed to read JSON, return code %d\n", e)

    def get_mag_data(self):
        # Open a connection to Piksi using TCP
        with TCPDriver(self.IP_add, self.port) as driver:
            with Handler(Framer(driver.read, None, verbose=True)) as source:
                print(f'Connection Eshtablished for piksi at IP {self.IP_add}')

                ''' Getting data'''
                try:

                    msg, metadata = next(source.filter([SBP_MSG_MAG_RAW]),(None,None))
                    if msg is not None:
                        print(f'Data Recieving from piksi at IP {msg.sender}')
                        self.mag_x_= msg.mag_x_ * 1e-3
                        self.mag_y_= msg.mag_y_ * 1e-3
                        self.mag_z_= msg.mag_z_ * 1e-3
                        
                    self.log()
                    # Print out the Acceleration in X, Y, Z directions of the rover
                    # print("Magnetometer X : %.4f, "
                    #       "Magnetometer Y : %.4f,"
                    #       "Magnetometer Z : %.4f"
                    #         % (self.mag_x_, self.mag_y_, self.mag_z_))
                    return self.mag_x_, self.mag_y_, self.mag_z_
                except KeyboardInterrupt:
                    raise NotImplementedError("Sensor data not obtained")

    def get_acc_data(self):
        # Open a connection to Piksi using TCP
        with TCPDriver(self.IP_add, self.port) as driver:
            with Handler(Framer(driver.read, None, verbose=True)) as source:
                # print(f'Connection Eshtablished for piksi at IP {self.IP_add}')

                ''' Getting data'''
                try:

                    msg, metadata = next(source.filter([SBP_MSG_IMU_RAW]),(None,None))
                    if msg is not None:
                        print(f'Data Recieving from piksi at IP {msg.sender}')
                        self.acc_x_= msg.acc_x * 1e-3
                        self.acc_y_= msg.acc_y * 1e-3
                        self.acc_z_= msg.acc_z * 1e-3
                        
                    self.log()
                    # Print out the Acceleration in X, Y, Z directions of the rover
                    # print("Acceleration X : %.4f,"
                    #       "Acceleration Y : %.4f,"
                    #       "Acceleration Z : %.4f"
                    #         % (self.acc_x_, self.acc_y_, self.acc_z_))
                    return self.acc_x_, self.acc_y_, self.acc_z_
                except KeyboardInterrupt:
                    raise NotImplementedError("Sensor data not obtained")
    def log(self):
        data_JSON =  {
            "mag_x": self.mag_x_,
            "mag_y": self.mag_y_,
            "mag_z": self.mag_z_,
            "acc_x": self.acc_x_,
            "acc_y": self.acc_y_,
            "acc_z": self.acc_z_
        }
        with open(f'{os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),"../../.."))}/L2_Data/gyro_data.json', "w") as write_file:
            json.dump(data_JSON, write_file)
    
    def get_heading(self):
        # Get accelerometer and magnetometer data
        self.get_acc_data()
        self.get_mag_data()

        # Calculate the pitch and roll angles
        pitch = math.atan2(self.acc_y_, math.sqrt(self.acc_x_**2 + self.acc_z_**2))
        roll = math.atan2(-self.acc_x_, self.acc_z_)

        # Compensate the magnetometer readings for the pitch and roll
        mag_x_comp = self.mag_x_ * math.cos(pitch) + self.mag_z_ * math.sin(pitch)
        mag_y_comp = self.mag_x_ * math.sin(roll) * math.sin(pitch) + self.mag_y_ * math.cos(roll) - self.mag_z_ * math.sin(roll) * math.cos(pitch)

        # Calculate the heading
        heading_rad = math.atan2(mag_y_comp, mag_x_comp)
        self.heading_deg = math.degrees(heading_rad)

        # Correct for when signs are reversed
        if self.heading_deg < 0:
            self.heading_deg += 360

        # Correct for local magnetic declination
        declination_angle = 4.16  # replace with local declination angle
        self.heading_deg += declination_angle
        if self.heading_deg > 360:
            self.heading_deg -= 360

        return self.heading_deg