from roboclaw_3 import Roboclaw
import time

# Replace with your serial port and baud rate
roboclaw = Roboclaw("COM6",115200)
#roboclaw = Roboclaw("/dev/ttyACM0",115200)

# Open the serial port
roboclaw.Open()

# Motor channel numbers
address = 0x80
m2count = 0
m1count = 0
fixed_value_90 = 4700
fixed_value_distance = 9700
sample_time = 0.1   
one_round_cm = 69
speed = 32 #constant speed
plus = 20                     


def right(Angle):
        m2count = int((Angle*fixed_value_90)/90)
        #m2count = int((90*fixed_value_90)/90)
        print(m2count)
        roboclaw.ResetEncoders(0x80)
        roboclaw.ForwardM2(address,speed)
        roboclaw.BackwardM1(address,speed)
        
        while True :
            motor_2 = roboclaw.ReadEncM2(0x80)
            middle_value = int(motor_2[1]) #middle_value is the only encoder value other wise we got value (164,4700,0)
            print(middle_value) 
            range1 =  m2count - plus
            range2 =  m2count + plus  
            if range1< middle_value < range2:
                roboclaw.ForwardM1(address,0)
                roboclaw.ForwardM2(address,0)
                break
        time.sleep(sample_time)

def left(Angle):
        m1count= int((Angle*fixed_value_90)/90)
        #m1count= int((90*fixed_value_90)/90)
        print(m1count)
        roboclaw.ResetEncoders(0x80)
        roboclaw.ForwardM1(address,speed)
        roboclaw.BackwardM2(address,speed)
        while True :
                motor_1 = roboclaw.ReadEncM1(0x80)
                middle_value = int(motor_1[1])   
                range1 =  m1count - plus
                range2 =  m1count + plus   
                if range1< middle_value < range2:
                    roboclaw.ForwardM1(address,0)
                    roboclaw.ForwardM2(address,0)
                    break
        time.sleep(sample_time)

def forward(distance):
        #Drive both motors forward
        m1count= int((distance*fixed_value_distance)/one_round_cm) 
        #fixed_value_distance represent encoder value after one rotation
        #one_round_cm represent how much cm cover in one rotation
        print(m1count)
        roboclaw.ResetEncoders(0x80)
        roboclaw.ForwardM1(address,speed)
        roboclaw.ForwardM2(address,speed)
        while True :
                motor_1 = roboclaw.ReadEncM1(0x80)
                middle_value = int(motor_1[1])   
                range1 =  m1count - plus
                range2 =  m1count + plus   
                if range1< middle_value < range2:
                    roboclaw.ForwardM1(address,0)
                    roboclaw.ForwardM2(address,0)
                    break
        time.sleep(sample_time)

def forward1():
        #Drive both motors forward
        roboclaw.ForwardM1(address,speed)
        roboclaw.ForwardM2(address,speed)

def backward(distance):
        #Drive both motors backward
        m1count= int((-distance*fixed_value_distance)/one_round_cm)
        print(m1count)
        roboclaw.ResetEncoders(0x80)
        roboclaw.BackwardM1(address,speed)
        roboclaw.BackwardM2(address,speed)
        while True :
                motor_1 = roboclaw.ReadEncM1(0x80)
                middle_value = int(motor_1[1])   
                range1 =  m1count - plus
                range2 =  m1count + plus   
                if range1< middle_value < range2:
                    roboclaw.ForwardM1(address,0)
                    roboclaw.ForwardM2(address,0)
                    break
        time.sleep(sample_time)

def stop():
        #Stop both motors
        roboclaw.ForwardM1(address,0)
        roboclaw.ForwardM2(address,0)

# def rotate360():
#         #for rotating 360 digree
#         roboclaw.ResetEncoders(0x80)
#         roboclaw.ForwardM1(address,speed)
#         roboclaw.BackwardM2(address,speed)
#         m1count= (fixed_value_90 * 4)
        
#         while True :
#                 motor_1 = roboclaw.ReadEncM1(0x80)
#                 middle_value = int(motor_1[1])   
#                 range1 =  m1count - plus
#                 range2 =  m1count + plus   
#                 if range1< middle_value < range2:
#                     roboclaw.ForwardM1(address,0)
#                     roboclaw.ForwardM2(address,0)
#                     break
#         time.sleep(sample_time)
        
# while True:
#     #speed = int(input("Enter the speed: "))
#     #speed = 32 #constant speed
#     if 0 < speed <= 100:
#         plus = 20 if 0 < speed <= 32 else (40 if 33 <= speed <= 64 else (50 if 65 <= speed <= 100 else 0))
#         break
#     else:
#         print("Invalid speed. Please enter a speed between 1 and 100.")
        
        
# while True:
#         userio = input("What's your option (forward,backward,right,left,stop,360): ")

#         if userio in {"right","left"}:
#                 angle_input = int(input(" At what angle do you want turn: "))
#                 if userio == "right":
#                         right(angle_input)
#                 elif userio == "left":
#                         left(angle_input)
                        
#         elif userio in {"forward","backward"}:
#                 distance_input = int(input(" enter the distance: "))
#                 if userio == "forward":
#                         forward(distance_input)
#                 elif userio == "backward":
#                         backward(distance_input)
                        
#         match userio:

#                 case "stop":
#                         stop()

                # case "360":
                #         rotate360()



        