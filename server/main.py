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
BASE_PATH = "/home/pi/nervebox_2" if PI_NATIVE else "/home/stella/Dropbox/projects/current/nervebox_2/" 
SERVER_PATH = "%sserver/" % (BASE_PATH )
COMMON_PATH = "%scommon/" % (BASE_PATH )

# local paths
sys.path.append(BASE_PATH)
sys.path.append(COMMON_PATH)
sys.path.append(SERVER_PATH)

# import local modules
import discovery
import duplexSockets
import nerveOSC

# load config
with open(COMMON_PATH + 'settings.json', 'r') as f:
    CONFIG = json.load(f)

# to do: replace with python iterator
nport = 50000
def nextPort():
	global nport
	nport += 1
	return nport
    
# SET UP NETWORKING
def discovery_handleDeviceFound(msg_d):
    msg_d["server_port"] = nextPort()
    print "discovery_handleDeviceFound:", msg_d
    duplexSockets_send = duplexSockets.init(
        msg_d["ip"], 
        CONFIG["duplexSockets_devicePort"],
        msg_d["server_port"], 
        duplexSockets_handleMessages, 
        duplexSockets_handleOutgoingConfirmation
    )
    return msg_d

discovery.init_responder(
	CONFIG["discovery_multicastGroup"], 
	CONFIG["discovery_multicastPort"],
	CONFIG["discovery_responsePort"],
	discovery_handleDeviceFound 
)

def duplexSockets_handleMessages(msg):
    print "duplexPort_handleMessages", msg

def duplexSockets_handleOutgoingConfirmation(msg):
    print "duplexPort_handleOutgoingConfirmation", msg

