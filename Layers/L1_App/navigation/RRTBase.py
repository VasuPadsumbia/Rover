import random
import math
import numpy as np
import pygame


class RRTMap:
    def __init__(self, start, goal,  x_size, y_size, obstacle_list):
        self.start = start
        self.goal = goal
        self.x_size = x_size
        self.y_size = y_size
        self.obstacle_list = obstacle_list
        
        #window setup
        self.MapWindowName = "RRT Path Planning"
        pygame.display.set_caption(self.MapWindowName)
        self.map = pygame.display.set_mode((self.x_size, self.y_size))
        self.map.fill((255,255,255))
        self.nodeRad = 2
        self.nodeThickness = 0
        self.edgeThickness = 1
        self.grey = (220,220,220)
        self.black = (0,0,0)
        self.white = (255,255,255)
        self.red = (255,0,0)
        self.green = (0,255,0)
        self.blue = (0,0,255)
        self.nodeColor = self.black

        
     
    def drawMap(self):

        pass
    def drawPath(self):
        pass
    def drawObstacles(self):
        pass


class RRTGraph:
    
    def __init__(self, start, goal, x_size, y_size, obstacle_list):
        (x,y) = start
        
        self.start = start
        self.goal = goal
        self.x_size = x_size
        self.y_size = y_size
        self.obstacle_list = obstacle_list
        self.goalstate = False
        self.x = []
        self.y = []
        self.parent = []
        #initialize the tree with the start state
        self.x.append(x)
        self.y.append(y)
        self.parent.append(0)

        #obstacle list
        obstacle_list = []
        
        pass

    def makeRandomPoint(self):
        pass

    def makeobs(self):
        pass

    def add_node(self, n):
        pass

    def remove_node(self, n):
        pass
    
    def add_edge(self, a, b):
        pass

    def remove_edge(self, a, b):
        pass

    def number_of_nodes(self):
        pass

    def distance(self, a, b):
        pass

    def nearest_neighbor(self, n):
        pass

    def isfree(self, a, b):
        pass

    def crossObstacle(self, a, b):
        pass

    def connect(self, a, b):
        pass

    def step(self, a, b):
        pass

    def path_to_goal(self, goal):
        pass

    def getPathCoords(self, goal):
        pass

    def bias(self, goal):
        pass
    def expand(self, goal):
        pass
    def cost(self, a, b):
        pass
