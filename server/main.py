"""
This module is the Server.
It 
1) listens for network discovery connections from clients and vimina
2) 
3) 
4) 
"""

#############################################
##### MODULES, EVENIRONMENT AND GLOBALS #####
#############################################

import json
#import mapMIDIToNerveOSC
import os
import socket
import struct
import time
import sys
import zmq


PI_NATIVE = os.uname()[4].startswith("arm") # TRUE if running on RPi
BASE_PATH = "/home/pi/nervebox_2" if PI_NATIVE else "/home/stella/Dropbox/projects/current/nervebox_2/" 
COMMON_PATH = "%scommon/" % (BASE_PATH )
DEVICES_PATH = "%sclient/devices/" % (BASE_PATH )
HOSTNAME = socket.gethostname()
SERVER_PATH = "%sserver/" % (BASE_PATH )
STORE_PATH = "%sstore/" % SERVER_PATH

# local paths
sys.path.append(BASE_PATH)
sys.path.append(COMMON_PATH)
sys.path.append(SERVER_PATH)

# import local modules
import discovery
#import duplexSockets
import pubsub
import parseOsc
import midiToOsc
import midiDeviceManager

# load config
with open(COMMON_PATH + 'settings.json', 'r') as f:
    SETTINGS = json.load(f)

with open(COMMON_PATH + 'mappings.json', 'r') as f:
    MAPPINGS = json.load(f)

MAPPING = MAPPINGS["MAPPINGS"]["default"] # todo: the mapping name will have to be dynamically updated

######################
##### NETWORKING #####
######################

# Listen for and connect to vimina input and black box outputs

subscribernames = filter(lambda x: os.path.isdir(os.path.join(DEVICES_PATH, x)), os.listdir(DEVICES_PATH))
subscribernames.append("nervebox2")

def recvCallback(topic, msg):
  print "recvCallback", repr(topic), repr(msg)

def netStateCallback(hostname, connected):
  print "netStateCallback", hostname, connected

def handleSubscriberFound(msg):
  pubsub_api["subscribe"](msg["hostname"],msg["ip"],SETTINGS["pubsub_pubPort"], ("__heartbeat__","osc"))

pubsub_api = pubsub.init(
  subscribernames,
  HOSTNAME, 
  SETTINGS["pubsub_pubPort"], 
  recvCallback,
  netStateCallback
)

# multicast discovery
discovery.init_responder(
  SETTINGS["discovery_multicastGroup"], 
  SETTINGS["discovery_multicastPort"],
  SETTINGS["discovery_responsePort"],
  handleSubscriberFound
)

###########################################
##### MIDI DEVICES ATTACHED TO SERVER #####
###########################################

def deviceCallback(eventType, deviceID, deviceName):
    print "deviceCallback", eventType, deviceID, deviceName

statusMap = {
    8:"note_off",
    9:"note_on",
    10:"polyphonic_aftertouch",
    11:"control_change",
    12:"program_change",
    13:"channel_aftertouch",
    14:"pitch_wheel",
    15:"system_exclusive"
}

def midiCallback(devicename, cmd, channel, note, velocity):
    #print "midiCallback", devicename, cmd, channel, note, velocity
    cmd = statusMap[int(cmd)]
    osc_msg = midiToOsc.convert(devicename, cmd, channel, note, velocity) # convert MIDI so OSC
    #print "midiCallback", osc_msg
    mapOscInToOscOut(osc_msg)

midiDeviceManager.init(deviceCallback, midiCallback)

#################################
##### MAP OSC IN TO OSC OUT #####
#################################

def mapOscInToOscOut(osc):
  print osc
  [device, command, params, params_str] = parseOsc.parse(osc)
  if command in ["note_on", "note_off"]:
    try:
      [oscOutDevice, oscOutPath] = MAPPING["INPUTDEVICES"][device]["CHANNEL"][params['channel']]["PITCH_12TET"][params["pitch"]["12tet"]]["COMMAND"][command]
      oscOut = "%s %s"%(oscOutPath,params_str)
      #print oscOut
      #pubsub_api["publish"]("osc", '/HR16/sound/tom_3/bang {"timbre":null,"dynamics":{"amplitude":0.5196850393700787},"channel":"1","pitch":{"midi":57,"cents":0,"12tet":"A3","octave":3,"pitch":"A","freq":220.0}}')
      pubsub_api["publish"](oscOutDevice, oscOut)
    except Exception as e:
      print "mapping not found", osc
