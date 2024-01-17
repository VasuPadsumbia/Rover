# ------------------------------------------------
# --- Author: Vasu Padsumbia
# ------------------------------------------------
''' Description: This file return paths and other helper actions'''

import os
import logging
import re
from setuptools import errors
from setuptools import logging as setuptools_logging

setuptools_logging.configure()
log = logging.getLogger()

#------------------------------------------------------------
# File/Folder path Configuration
#------------------------------------------------------------

def log_path():
    ''' It returns the log file path'''
    try:
        CWD = os.getcwd() #get current directory
        temp = os.path.join(CWD, "Logs")
        logs_path = os.path.join(temp, "application.log")
        return logs_path
        
    except OSError as errors :
        print(errors)

def config_path():
    '''It return the config file path'''
    try:
        CWD = os.getcwd() #get current directory
        config_path = os.path.join(CWD, "Configure.json")
        return config_path
        
    except OSError as errors :
        print(errors)

def map_coordinate_path():
    '''It return the smallMap_path file path'''
    try:
        CWD = os.getcwd() #get current directory

        folder1 = os.path.join(CWD, "Layers")
        folder2 = os.path.join(folder1, "L2_Data")
        map_coordinate_path = os.path.join(folder2, "coordinates.json")
        return map_coordinate_path
        
    except OSError as errors :
        print(errors)
        return None

def gps_path():
    '''It return the polarMap_path file path'''
    try:
        CWD = os.getcwd() #get current directory
        temp = os.path.join(CWD, "\Layers\L2_Data")
        gps_path = os.path.join(temp, "gps_data.json")
        return gps_path
        
    except OSError as errors :
        print(errors)
        return None