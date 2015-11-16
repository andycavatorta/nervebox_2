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
HOST_SPECIFIC_PATH = "%sclient/devices/%s/" % (BASE_PATH, HOSTNAME)


# local paths
sys.path.append(BASE_PATH)
sys.path.append(COMMON_PATH)
sys.path.append(CLIENT_PATH)
sys.path.append(HOST_SPECIFIC_PATH)

# import local modules
import discovery
import duplexSockets
import nerveOSC
import device

# load config
with open(COMMON_PATH + 'settings.json', 'r') as f:
    CONFIG = json.load(f)

device.init()

# SET UP NETWORKING
def duplexSockets_handleMessages(msg):
    print "duplexPort_handleMessages", msg
    print "------------", nerveOSC.parse(msg)
    device.handleNOSC(nerveOSC.parse(msg))

def duplexSockets_handleOutgoingConfirmation(msg):
    print "duplexPort_handleOutgoingConfirmation", msg

def duplexSockets_handleException(msg):
    print "duplexSockets_handleException", msg

def discovery_handleServerFound(msg_d):
    print "discovery_handleServerFound", msg_d
    duplexSockets_send = duplexSockets.init(
        msg_d["ip"], 
        msg_d["server_port"], 
        CONFIG["duplexSockets_devicePort"],
        "/system/ping/",
        duplexSockets_handleMessages, 
        duplexSockets_handleOutgoingConfirmation,
        duplexSockets_handleException
    )

discovery.init_caller(
    CONFIG["discovery_multicastGroup"], 
    CONFIG["discovery_multicastPort"],
    CONFIG["discovery_responsePort"],
    discovery_handleServerFound
)


