"""
This module is the VIrtual MIdi Network Adapter.
It 
1) creates virtual midi devices in the host OS
2) discovers and connects to a Nervebox server
3) catpures midi events and converts them to OSC
4) sends osc messages to Nervebox server (if connected)
"""

#############################################
##### MODULES, EVENIRONMENT AND GLOBALS #####
#############################################

import json
import math
import os
import rtmidi  #https://github.com/SpotlightKid/python-rtmidi
import socket
import sys

OS = os.name
BASE_PATH = "/home/stella/Dropbox/projects/current/nervebox_2/" if OS=="posix" else "C:/Users/andy/Dropbox/projects/current/nervebox_2/"
COMMON_PATH = "%scommon/" % (BASE_PATH )
DEVICES_PATH = "%sclient/devices/" % (BASE_PATH )
#SERVER_PATH = "%sserver/" % (BASE_PATH )
HOSTNAME = socket.gethostname()

sys.path.append(BASE_PATH)
sys.path.append(COMMON_PATH)
#sys.path.append(SERVER_PATH)

# modules from COMMON_PATH
import discovery
import pubsub
import midiToOsc

with open(COMMON_PATH + 'settings.json', 'r') as f:
    SETTINGS = json.load(f)

######################
##### NETWORKING #####
######################

subscribernames = ["nervebox"]

def recvCallback(topic, msg):
    # there is not yet a reason for nervebox to publish to vimina
    print "recvCallback", repr(topic), repr(msg)

def netStateCallback(hostname, connected):
    print "netStateCallback", hostname, connected
    callerSend.setServerFound(connected)

def serverFoundCallback(msg):
    pubsub_api["subscribe"](msg["hostname"],msg["ip"],SETTINGS["pubsub_pubPort"], ("__heartbeat__"))

pubsub_api = pubsub.init(
    subscribernames,
    HOSTNAME, 
    SETTINGS["pubsub_pubPort"], 
    recvCallback,
    netStateCallback
)

callerSend = discovery.init_caller(
    SETTINGS["discovery_multicastGroup"], 
    SETTINGS["discovery_multicastPort"],
    SETTINGS["discovery_responsePort"],
    serverFoundCallback
)

###############################
##### VITUAL MIDI DEVICES #####
###############################

deviceNames = filter(lambda x: os.path.isdir(os.path.join(DEVICES_PATH, x)), os.listdir(DEVICES_PATH))

def midiEventCallback(devicename, msgAndTime_t, data=None):
    msg, deltatime = msgAndTime_t
    osc_msg = midiToOSC.convert(devicename, msg, data) # convert MIDI so OSC
    print osc_msg
    pubsub_api.publish("osc", osc_msg)
    # send to nervebox server  duplexSockets_send(osc)

# following MIDI functions should be moved into common module
def createVirtualPort(devicename):
    midiin = rtmidi.MidiIn()
    vp = midiin.open_virtual_port(devicename)
    midiin.set_callback((lambda event, data: midiEventCallback(devicename, event, data)))
    return vp

virtualPorts = map(createVirtualPort, deviceNames)

print virtualPorts
