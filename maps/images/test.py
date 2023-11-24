from sbp.client.drivers.network_drivers import TCPDriver
from sbp.client import Handler, Framer
from sbp.navigation import SBP_MSG_BASELINE_NED, SBP_MSG_POS_LLH, \
    SBP_MSG_VEL_NED, SBP_MSG_GPS_TIME

import argparse


class RtkMessage:
    '''
    Saves and outputs parsed RTK data from Piks
    '''

    def __init__(self):
        self.flag = 0.0
        self.n = 0.0
        self.e = 0.0
        self.d = 0.0
        self.lat = 0.0
        self.lon = 0.0
        self.h = 0.0
        self.v_n = 0.0
        self.v_e = 0.0
        self.v_d = 0.0
        self.wn = 0
        self.tow = 0

    def whole_string(self):
        '''
        Returns all the data as a string
        '''

        return('%.0f\t%.0f\t%2.8f\t%2.8f\t%4.6f\t%6.0f\t%6.0f\t%6.0f\t'
               '%6.0f\t%6.0f\t%6.0f\t%.0f\t' %
               (self.wn, self.tow, self.lat, self.lon, self.h, self.n, self.e,
                self.d, self.v_n, self.v_e, self.v_d, self.flag))


def read_rtk(port='/dev/ttyUSB0', baud=115200):
    '''
    Reads the RTK output from SwiftNav Piksi, parses the messege and prints.
    Piksi's must be configured to give RTK message through the serial port.
    NOTE: Current official sbp drivers only support python-2

    Args:
        port: serial port [[default='/dev/ttyUSB0']
        baud: baud rate [default=115200]

    Returns:
        None
    '''

    print('Reading from {} at {}'.format(port, baud))

    m = RtkMessage()
    # t_now = datetime.now().strftime('%Y%m%d%H%M%S')
    # out_file = 'GPS_' + t_now + '.txt'

    # open a connection to Piksi
    # with open(out_file, 'w') as f:
    with PySerialDriver(port, baud) as driver:
        with Handler(Framer(driver.read, None, verbose=True)) as source:
            try:
                msg_list = [SBP_MSG_BASELINE_NED, SBP_MSG_POS_LLH,
                            SBP_MSG_VEL_NED, SBP_MSG_GPS_TIME]
                for msg, metadata in source.filter(msg_list):

                    # LLH position in deg-deg-m
                    if msg.msg_type == 522:
                        m.lat = msg.lat
                        m.lon = msg.lon
                        m.h = msg.height

                    # RTK position in mm (from base to rover)
                    elif msg.msg_type == 524:
                        m.n = msg.n
                        m.e = msg.e
                        m.d = msg.d
                        m.flag = msg.flags

                    # RTK velocity in mm/s
                    elif msg.msg_type == 526:
                        m.v_n = msg.n
                        m.v_e = msg.e
                        m.v_d = msg.d

                    # GPS time
                    elif msg.msg_type == 258:
                        m.wn = msg.wn
                        m.tow = msg.tow  # in millis

                    else:
                        pass

                    print(m.whole_string())
                    # f.write(line)
                    # f.write('\n')

            except KeyboardInterrupt:
                pass

    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            'Opens and reads the output of SwiftNav Piksi. \
            Developed based on Swift Navigation SBP example.'))
    parser.add_argument(
        '-p', '--port',
        default=['/dev/ttyUSB0'],
        nargs=1,
        help='specify the serial port to use [default = \'/dev/ttyUSB0\']')
    parser.add_argument(
        '-b', '--baud',
        default=[115200],
        nargs=1,
        help='specify the baud rate [default = 115200]')
    args = parser.parse_args()

    read_rtk(args.port[0], args.baud[0])