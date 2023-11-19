from abc import abstractmethod
import argparse
from sbp.client.drivers.network_drivers import TCPDriver
from sbp.client import Handler, Framer
from sbp.imu import SBP_MSG_VEL_NED_DEP_A

class Velocity():
    def __init__(self) -> None:
        parser = argparse.ArgumentParser(
            description="Get Velocity of vehicle along with direction.")
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
                    for msg, metadata in source.filter(SBP_MSG_VEL_NED_DEP_A):
                        v_n= msg.n * 1e-3
                        v_e= msg.e * 1e-3
                        v_d= msg.d * 1e-3
                        # Print out the Acceleration in X, Y, Z directions of the rover
                        print("Velocity North coordinate : %.4f, "
                              "Velocity East coordinate : %.4f,"
                              "Velocity Down coordinate : %.4f"
                                % (v_n, v_e, v_d))
                    return [v_n, v_e, v_d]
                except:
                    raise NotImplementedError("Sensor data not obtained")

    

    