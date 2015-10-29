import json
import os
import struct
import time
import threading
import sys

import zmq

# constants
PI_NATIVE = os.uname()[4].startswith("arm") # TRUE if running on RPi
BASE_PATH = "/home/pi/nervebox_2" if PI_NATIVE else "/home/stella/Dropbox/projects/current/nervebox_2/" 
CLIENT_PATH = "%sclient/" % (BASE_PATH )
COMMON_PATH = "%scommon/" % (BASE_PATH )

# local paths
sys.path.append(BASE_PATH)
sys.path.append(COMMON_PATH)
sys.path.append(CLIENT_PATH)

# import local modules
import discovery
import duplexSockets

# load config
with open(COMMON_PATH + 'settings.json', 'r') as f:
    CONFIG = json.load(f)

# DONE WITH BASIC SET UP


def duplexSockets_handleMessages(msg):
    print "duplexPort_handleMessages", msg

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

"""
def Recv():
    port = 50000
    context = zmq.Context.instance()
    socket = context.socket(zmq.DEALER)
    socket.setsockopt(zmq.IDENTITY, b'MRQ1')
    socket.connect("tcp://localhost:%d" % (port))

    while True:
        print "++++++"
        request = socket.recv()
        print repr(request)

recv = threading.Thread(target=Recv)
recv.start()

def cb(msg):
    print "IP received from discovered server", msg

def main():
    global HOSTNAME
    global IP

    cmd = "ip addr list eth0 |grep \"inet \" |cut -d' ' -f6|cut -d/ -f1"
    resp = commands.getstatusoutput(cmd)
    print resp
    IP = resp[1]
    HOSTNAME = socket.gethostname()

    receiveIpFromServer = threading.Thread(target=ReceiveIpFromServer)
    receiveIpFromServer.start()

    broadcastIpToServer = threading.Thread(target=BroadcastIpToServer)
    broadcastIpToServer.start()

main()

"""