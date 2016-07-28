#############################################
##### MODULES, EVENIRONMENT AND GLOBALS #####
#############################################

import json
import os
import struct
import time
import threading
import sys
import socket
import errorlog as elog


# constants
#PI_NATIVE = os.uname()[4].startswith("arm") # TRUE if running on RPi
#BASE_PATH = "/home/pi/nervebox_2/" if PI_NATIVE else "/home/stella/Dropbox/projects/current/nervebox_2/" 
HOSTNAME = socket.gethostname()
BASE_PATH = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
CLIENT_PATH = "%s/client/" % (BASE_PATH )
DEVICES_PATH = "%s/client/devices/" % (BASE_PATH )
COMMON_PATH = "%s/common/" % (BASE_PATH )
HOST_SPECIFIC_PATH = "%s/client/devices/%s/" % (BASE_PATH, HOSTNAME)
SERVER_PATH = "%s/server/" % (BASE_PATH )
STORE_PATH = "%s/store/" % SERVER_PATH
clientnames = ("blueberrypie")
ROLE = "client" if HOSTNAME in clientnames else "server"
response = raw_input("Dashboard (yes/no)?")
if response == 'yes':
    ROLE = 'dashboard'
print ROLE

# local paths
sys.path.append(BASE_PATH)
sys.path.append(COMMON_PATH)
sys.path.append(CLIENT_PATH)
sys.path.append(SERVER_PATH)
sys.path.append(HOST_SPECIFIC_PATH)

try:
    # import local modules
    import dps
    import nerveOSC
    if ROLE == "client":
        import device
        device.init()
    else:
        import parseOsc
        import midiToOsc
        import midiDeviceManager
        import midiserver

    # load config
    with open(COMMON_PATH + 'settings.json', 'r') as f:
        SETTINGS = json.load(f)

    with open(COMMON_PATH + 'mappings.json', 'r') as f:
        MAPPINGS = json.load(f)

    MAPPING = MAPPINGS["MAPPINGS"]["default"] # todo: the mapping name will have to be dynamically updated

    ######################
    ##### NETWORKING #####
    ######################

    if ROLE == "client":
        subscribernames = ["nervebox"]
    else:
        subscribernames = filter(lambda x: os.path.isdir(os.path.join(DEVICES_PATH, x)), os.listdir(DEVICES_PATH))
        subscribernames.append("nervebox2")
        subscribernames.append(HOSTNAME)

    dps.init_networking(
        subscribernames,
        HOSTNAME,
        ROLE,
        SETTINGS["pubsub_pubPort"],
        SETTINGS["pubsub_pubPort2"],
        SETTINGS["discovery_multicastGroup"],
        SETTINGS["discovery_multicastPort"],
        SETTINGS["discovery_multicastPort2"],
        SETTINGS["discovery_responsePort"],
        SETTINGS["discovery_responsePort2"]
    )
except:
    elog.elog.logerror()
