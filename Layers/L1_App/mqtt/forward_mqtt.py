from roboclaw_3 import Roboclaw
import paho.mqtt.client as mqtt
import time

# Initialize RoboClaw
#roboclaw = Roboclaw("/dev/ttyUSB0",115200)
# Replace with your serial port and baud rate
roboclaw = Roboclaw("/dev/ttyACM0",115200)

# Open the serial port
roboclaw.Open()

# Motor channel numbers
address = 0x80

# MQTT broker details
broker_address = "172.20.48.222"  # Replace with the actual broker address
broker_port = 1883  # Replace with the actual broker port
topic = "move"  # Replace with the desired topic
client = mqtt.Client()

# Callback when a message is received from the MQTT broker
def on_message(client, userdata, msg):
    Received = msg.payload.decode(encoding = 'UTF-8')
    print(Received)

    if Received == "forward":
    #def forward(input())
            # Drive both motors forward
        roboclaw.ForwardM1(address,64)
        roboclaw.ForwardM2(address,64)
        time.sleep(3)

    elif Received == "rotate":
        roboclaw.ForwardM1(address,32)
        roboclaw.ForwardM2(address,0)
            
    elif Received== "backward":
    #def backward():
            # Drive both motors in reverse
        roboclaw.BackwardM1(address,32)
        roboclaw.BackwardM2(address,32)
        time.sleep(5)

    elif Received == "stop":
    #def stop():
        roboclaw.ForwardM1(address,0)
        roboclaw.ForwardM2(address,0)
        roboclaw.BackwardM1(address,0)
        roboclaw.BackwardM2(address,0)
        time.sleep(5)

    elif Received == "right":
    #def turnrightmixed():
        roboclaw.TurnRightMixed(address,32)
        time.sleep(5)

    elif Received == "left":
    #def turnleftmixed():
        roboclaw.TurnLeftMixed(address,32)
        time.sleep(5)

#forward()
#backward()
#forwardmixed()
#backwardmixed()
#turnrightmixed()
#turnleftmixed()
#stop()

# Start the MQTT loop to receive messages
# Set the callback function for when a message is received
client.on_message = on_message

# Connect to the broker
client.connect(broker_address, broker_port, 60)
# Subscribe to the MQTT topic
client.subscribe(topic)
client.loop_forever()
roboclaw.close()
