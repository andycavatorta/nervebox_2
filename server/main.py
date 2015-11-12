"""



"""
import json
import mapMIDIToNerveOSC
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
STORE_PATH = "%sstore/" % SERVER_PATH

# local paths
sys.path.append(BASE_PATH)
sys.path.append(COMMON_PATH)
sys.path.append(SERVER_PATH)

# import local modules
import discovery
import duplexSockets
import nerveOSC
import midiDeviceManager

# load config
with open(COMMON_PATH + 'settings.json', 'r') as f:
    CONFIG = json.load(f)

# SET UP NETWORKING

class Hosts():
    def __init__(self):
        self.hosts = {}
        self.nextPort = 50000
        #self.hostnameXDevname_d
    def addHost(self, msg_d):
        msg_d["server_port"] = self.nextPort
        self.nextPort += 1
        print "addHost", msg_d
        self.hosts[msg_d["hostname"]] = host = Host(msg_d["hostname"])
        send = duplexSockets.init(
            msg_d["ip"], 
            CONFIG["duplexSockets_devicePort"],
            msg_d["server_port"], 
            "/system/ping/",
            host.handleIncoming, 
            host.handleOutgoingResponse,
            host.handleException

        )
        host.setSend(send)
        return msg_d
    def removeHost(self, hostname):
        return 
    def routeMessageToHost(self,hostname,msg):
        print self.hosts
        if self.hosts.has_key(hostname):
            self.hosts[hostname].send(msg)
        else:
            print "main.Hosts.routeMessageToHost: host not connected:", hostname, msg

hosts = Hosts()

class Host():
    def __init__(self, hostname):
        self.hostname = hostname
    def send(self, msg):
        print "outgoing port not set up", msg
    def handleIncoming(self, msg):
        print "handleIncoming",self.hostname, msg
    def handleOutgoingResponse(self, msg):
        print "handleOutgoingResponse",self.hostname, msg
    def handleException(self, msg):
        print "handleException",self.hostname, msg

    def setSend(self, func):
        self.send = func

discovery.init_responder(
	CONFIG["discovery_multicastGroup"], 
	CONFIG["discovery_multicastPort"],
	CONFIG["discovery_responsePort"],
	hosts.addHost # discovery_handleDeviceFound 
)

# SET UP Mapping to NerveOSC
def nerveOSCRouter(nosc):
    nosc_d = nerveOSC.parse(nosc)
    print nosc, nosc_d
    hosts.routeMessageToHost(nosc_d["host"],nosc_d["path"])

mapMIDIToNerveOSC.init("test1", nerveOSCRouter, STORE_PATH)

# SET UP MIDI
def deviceCallback(eventType, deviceID, deviceName):
    print "deviceCallback", eventType, deviceID, deviceName

def midiCallback(deviceName, cmd, channel, note, velocity):
    print "midiCallback", deviceName, cmd, channel, note, velocity

midiDeviceManager.init(deviceCallback, mapMIDIToNerveOSC.midiIn)
