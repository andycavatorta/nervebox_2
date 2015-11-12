"""



"""
import json
import os
import struct
import time
import threading
import sys
import socket
#import zmq

# constants
PI_NATIVE = os.uname()[4].startswith("arm") # TRUE if running on RPi
HOSTNAME = socket.gethostname()
BASE_PATH = "/home/pi/nervebox_2/" if PI_NATIVE else "/home/stella/Dropbox/projects/current/nervebox_2/" 
CLIENT_PATH = "%sclient/" % (BASE_PATH )
DEVICES_PATH = "%sclient/devices/" % (BASE_PATH )
COMMON_PATH = "%scommon/" % (BASE_PATH )
SPECIFIC_CLIENT_PATH = "%sclient/devices/%s/" % (BASE_PATH, HOSTNAME)

# local paths
sys.path.append(BASE_PATH)
sys.path.append(COMMON_PATH)
sys.path.append(CLIENT_PATH)
sys.path.append(SPECIFIC_CLIENT_PATH)

# import local modules
import discovery
import duplexSockets
import nerveOSC

# load config
with open(COMMON_PATH + 'settings.json', 'r') as f:
    CONFIG = json.load(f)

# SET UP NETWORKING
def duplexSockets_handleMessages(msg):
    print "duplexPort_handleMessages", msg
    nosc_d = nerveOSC.parse(msg)
    print "nosc_d=", nosc_d

def duplexSockets_handleOutgoingConfirmation(msg):
    print "duplexPort_handleOutgoingConfirmation", msg

def discovery_handleServerFound(msg_d):
    print "discovery_handleServerFound", msg_d
    duplexSockets_send = duplexSockets.init(
        msg_d["ip"], 
        msg_d["server_port"], 
        CONFIG["duplexSockets_devicePort"],
        duplexSockets_handleMessages, 
        duplexSockets_handleOutgoingConfirmation
    )

discovery.init_caller(
    CONFIG["discovery_multicastGroup"], 
    CONFIG["discovery_multicastPort"],
    CONFIG["discovery_responsePort"],
    discovery_handleServerFound
)


