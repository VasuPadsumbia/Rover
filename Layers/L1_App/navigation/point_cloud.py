import numpy as np
import Layers.L1_App.sensor.Laser.sickpy.sick as sickpy
import cv2

class PointCloud():
    def __init__(self, port):
        self.sick = sickpy.SICK(port)
        self.cartesian = None
        self.norm_coord = None
        self.grid = None
        self.cartesian = self.sick.cartesian
        while True:
            print(".")
            if self.sick.get_frame():
                print(self.sick.cartesian)
                cv2.imshow("img", self.sick.image)
                cv2.waitKey(5)
    def generate_grid(self):
        x_coordinates = [float(point[0]) for point in self.cartesian]
        y_coordinates = [float(point[1]) for point in self.cartesian]