# ------------------------------------------------
# --- Author: Farogh Iftekhar
# ------------------------------------------------
''' Description: This file return paths and other helper actions'''

import os
import logging
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
        config_path = os.path.join(CWD, "config.json")
        return config_path
        
    except OSError as errors :
        print(errors)

def smallMap_path():
    '''It return the smallMap_path file path'''
    try:
        CWD = os.getcwd() #get current directory
        temp = os.path.join(CWD, "maps")
        smallMap_path = os.path.join(temp, "map6_small.json")
        return smallMap_path
        
    except OSError as errors :
        print(errors)

def polarMap_path():
    '''It return the polarMap_path file path'''
    try:
        CWD = os.getcwd() #get current directory
        temp = os.path.join(CWD, "maps")
        polarMap_path = os.path.join(temp, "input5_small_polar_20deg.json")
        return polarMap_path
        
    except OSError as errors :
        print(errors)