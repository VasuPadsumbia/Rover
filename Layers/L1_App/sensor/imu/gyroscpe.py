import os, argparse
from sbp.client.drivers.network_drivers import TCPDriver
from sbp.client import Handler, Framer
from json.decoder import JSONDecodeError
import json, math
from sbp.mag import SBP_MSG_MAG_RAW


class connect_pksi_gyroscope():

    def __init__(self) -> None:

        """_summary_

        This code opens piksi multi at IP address mentioned in Config.json file in workspace
        and generats coordinates of the rover and saves it into imu/gyro_data.json.

        """
        self.mag_x_ = 0.0
        self.mag_y_ = 0.0
        self.mag_z_ = 0.0
        
        self.config_path = f'{os.path.abspath(os.path.join(os.path.dirname(__file__),"../../../.."))}/Configure.json'
        

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

                    msg, metadata = next(source.filter([SBP_MSG_MAG_RAW]),(None,None))
                    if msg is not None:
                        print(f'Data Recieving from piksi at IP {msg.sender}')
                        self.mag_x_= msg.mag_x_ * 1e-3
                        self.mag_y_= msg.mag_y_ * 1e-3
                        self.mag_z_= msg.mag_z_ * 1e-3
                        
                    self.log()
                    # Print out the Acceleration in X, Y, Z directions of the rover
                    print("Magnetometer X : %.4f, "
                          "Magnetometer Y : %.4f,"
                          "Magnetometer Z : %.4f"
                            % (self.mag_x_, self.mag_y_, self.mag_z_))

                except KeyboardInterrupt:
                    raise NotImplementedError("Sensor data not obtained")

    def log(self):
        data_JSON =  {
            "mag_x": self.mag_x_,
            "mag_y": self.mag_y_,
            "mag_z": self.mag_z_
        }
        with open(f'{os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),"../../.."))}/L2_Data/gyro_data.json', "w") as write_file:
            json.dump(data_JSON, write_file)
    

    def calculate_orientation(device_latitude, device_longitude, map_orientation):
        # Calculate the azimuth angle between the device and a reference point on the map
        map_reference_latitude =  # Latitude of a reference point on the map
        map_reference_longitude =  # Longitude of a reference point on the map

        # Calculate the difference in longitude
        delta_longitude = device_longitude - map_reference_longitude

        # Calculate the azimuth angle (bearing) between the two points
        azimuth_angle = math.atan2(
            math.sin(math.radians(delta_longitude)),
            math.cos(math.radians(map_reference_latitude)) * math.tan(math.radians(device_latitude)) -
            math.sin(math.radians(map_reference_latitude)) * math.cos(math.radians(delta_longitude))
        )

        # Convert the azimuth angle to degrees
        azimuth_angle_degrees = math.degrees(azimuth_angle)

        # Calculate the orientation of the device relative to the map orientation
        device_orientation = azimuth_angle_degrees - map_orientation

        # Adjust the orientation to be in the range [0, 360)
        device_orientation = (device_orientation + 360) % 360

        return device_orientation