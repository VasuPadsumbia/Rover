import os, json, time
from json.decoder import JSONDecodeError
from roboclaw_python.roboclaw_3 import Roboclaw

class rover():
    
    def __init__(self) -> None:
        
        """_summary_

       

        """
        # Motor channel numbers
        self.address = 0x80

        self.config_path = f'{os.path.abspath
                              (os.path.join
                               (os.path.dirname(__file__),"../../../.."))}/Configure.json'

        try:
            with open(self.config_path, "r") as config_file:
                data = json.load(config_file)
                self.bus = data['roboclaw']['bus']
                self.baud = data['roboclaw']['baud']
                config_file.close()
        
        except JSONDecodeError as e:
            print("Failed to read JSON, return code %d\n", e)

        ''' Creates roboclaw connection'''
        try:
            self.roboclaw = Roboclaw(self.bus,self.baud)
            # Open the serial port
            self.roboclaw.Open()
        except Exception as e:
            print(f"Error: {e}")
        
    def command(self, json_object):

        if not (json_object.get("manualMode") is None):
            action = json_object["manualMode"]
            self.ManualMode(action)
        
        if not (json_object.get("autoMode") is None):
            self.AutonomousMode()

    def ManualMode(self, command):
        
        if command == "forward":
            # Drive both motors forward
            self.drive_forward()

        elif command == "rotate":
            self.rotate()
            
        elif command== "backward":
            # Drive both motors in reverse
            self.drive_backward()

        elif command == "stop":
            #def stop():
            self.stop()

        elif command == "right":
            #def turnrightmixed():
            self.turn_right()

        elif command == "left":
            #def turnleftmixed():
            self.turn_left()
    
    def AutonomousMode(self):
        pass

    def drive_forward(self):
        print("Driving forward")
        # Implement the logic to drive forward
        # Example: Move both motors forward for 3 seconds
        self.roboclaw.ForwardM1(self.address, 64)
        self.roboclaw.ForwardM2(self.address, 64)
        time.sleep(3)
        self.stop()

    def rotate(self):
        print("Rotating")
        # Implement the logic to rotate
        # Example: Turn right by moving M1 forward and M2 backward
        self.roboclaw.ForwardM1(self.address, 32)
        self.roboclaw.BackwardM2(self.address, 32)
        time.sleep(3)
        self.stop()

    def drive_backward(self):
        print("Driving backward")
        # Implement the logic to drive backward
        # Example: Move both motors backward for 5 seconds
        self.roboclaw.BackwardM1(self.address, 32)
        self.roboclaw.BackwardM2(self.address, 32)
        time.sleep(5)
        self.stop()

    def stop(self):
        print("Stopping")
        # Implement the logic to stop the motors
        self.roboclaw.ForwardM1(self.address, 0)
        self.roboclaw.ForwardM2(self.address, 0)
        self.roboclaw.BackwardM1(self.address, 0)
        self.roboclaw.BackwardM2(self.address, 0)

    def turn_right(self):
        print("Turning right")
        # Implement the logic to turn right
        # Example: Turn right by using TurnRightMixed
        self.roboclaw.TurnRightMixed(self.address, 32)
        time.sleep(5)
        self.stop()

    def turn_left(self):
        print("Turning left")
        # Implement the logic to turn left
        # Example: Turn left by using TurnLeftMixed
        self.roboclaw.TurnLeftMixed(self.address, 32)
        time.sleep(5)
        self.stop()
