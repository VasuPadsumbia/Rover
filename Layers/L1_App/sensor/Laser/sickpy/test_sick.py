#!/usr/bin/python
import cv2
from sick import *

print("<<<< initing sick")
sick = SICK("COM10")
while True:
    print(".")
    if sick.get_frame():
        print(sick.cartesian)
        cv2.imshow("img", sick.image)
        cv2.waitKey(5)
        #print(f'logging coordinates(): {sick.log()}')

