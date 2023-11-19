from abc import abstractmethod
import argparse
from sbp.client.drivers.network_drivers import TCPDriver
from sbp.client import Handler, Framer
from sbp.imu import SBP_MSG_IMU_RAW

class Gyroscope():
    def __init__(self) -> None:
        parser = argparse.ArgumentParser(
            description="Swift IMU SBP Example.")
        parser.add_argument(
            "-a",
            "--host",
            default='localhost',
            help="specify the host address.")
        parser.add_argument(
            "-p",
            "--port",
            default=55555,
            help="specify the port to use.")
        args = parser.parse_args()
    
    @abstractmethod
    def task_rotation(self, args):
            # Open a connection to Piksi using TCP
        with TCPDriver(args.host, args.port) as driver:
            with Handler(Framer(driver.read, None, verbose=True)) as source:
                try:
                    for msg, metadata in source.filter(SBP_MSG_IMU_RAW):
                        gyr_x_= msg.gyr_x * 1e-3
                        gyr_y_= msg.gyr_y * 1e-3
                        gyr_z_= msg.gyr_z * 1e-3
                        # Print out the Acceleration in X, Y, Z directions of the rover
                        print("Gyroscope X : %.4f, "
                              "Gyroscope Y : %.4f,"
                              "Gyroscope Z : %.4f"
                                % (gyr_x_, gyr_y_, gyr_z_))
                    return [gyr_x_, gyr_y_, gyr_z_]
                except:
                    raise NotImplementedError("Sensor data not obtained")

    

    