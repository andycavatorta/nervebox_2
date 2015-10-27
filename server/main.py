"""


"""
import json
import os
import struct
import time
import threading
import sys

# constants
PI_NATIVE = os.uname()[4].startswith("arm") # TRUE if running on RPi
BASE_PATH = "/home/pi/nervebox_2" if PI_NATIVE else "/home/stella/Dropbox/projects/current/nervebox_2/server/" 

# load config
with open(BASE_PATH + 'settings.json', 'r') as f:
    CONFIG = json.load(f)

def tempca(hostname,msg):
	print "tempcc:", hostname,msg

def tempcb(hostname,msg):
	print "tempcb:", hostname,msg

# import local modules
import hardwareGatewayNetworkManager
hardwareGatewayNetworkManager.main(50000, 10000, tempca, tempcb)
