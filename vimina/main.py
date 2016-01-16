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

HOSTNAME = socket.gethostname()
#OS = os.name
#BASE_PATH = "/home/stella/Dropbox/projects/current/nervebox_2/" if OS=="posix" else "C:/Users/andy/Dropbox/projects/current/nervebox_2/"
#filepath = os.path.dirname(os.path.realpath(__file__))
BASE_PATH = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
COMMON_PATH = "%s/common/" % (BASE_PATH )
DEVICES_PATH = "%s/client/devices/" % (BASE_PATH )
#SERVER_PATH = "%sserver/" % (BASE_PATH )

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
    pubsub_api["subscribe"](msg["hostname"],msg["ip"],SETTINGS["pubsub_pubPort"], ("__heartbeat__","osc"))

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


statusMap = {
    128:"note_off",
    144:"note_on",
    160:"polyphonic_aftertouch",
    176:"control_change",
    192:"program_change",
    208:"channel_aftertouch",
    224:"pitch_wheel",
    240:"system_exclusive",
    241:"system_common",
    242:"song_position_pointer",
    243:"song_select",
    244:"system_common",
    245:"system_common",
    246:"tune_request",
    247:"end_of_sysex",
    248:"timing_clock",
    249:"undefined",
    250:"start",
    251:"continue",
    252:"stop",
    253:"undefined",
    254:"active_sensing",
    255:"sys_reset",
}

def midiEventCallback(devicename, msgAndTime_t, data=None):
    print "vimina/main midiEventCallback", devicename, msgAndTime_t, data
    event, deltatime = msgAndTime_t


    if event[0] < 0xF0:
        channel = (event[0] & 0xF) + 1
        status_int = event[0] & 0xF0
    else:
        status_int = event[0]
        channel = None
    status = statusMap[int(status_int)]
    data1 = data2 = None
    num_bytes = len(event)
    if num_bytes >= 2:
        data1 = event[1]
    if num_bytes >= 3:
        data2 = event[2]

    osc_msg = midiToOsc.convert(devicename, status, channel, data1, data2) # convert MIDI so OSC
    print osc_msg
    pubsub_api["publish"]("osc", osc_msg)

# following MIDI functions should be moved into common module
def createVirtualPort(devicename):
    midiin = rtmidi.MidiIn()
    vp = midiin.open_virtual_port(devicename)
    midiin.set_callback((lambda event, data: midiEventCallback(devicename, event, data)))
    return vp

virtualPorts = map(createVirtualPort, deviceNames)

print virtualPorts
