"""
This module contains all of the networking code for the server

The server's clients are all black boxes, viminina, and GUI.

The server maintains publishers for all clients
The server subscribes to publishers from all clients

For network discovery, the server listens for multicast requests from clients and responds with the server IP

A client is considered to be connected if it has received a heartbeat from it within n seconds
The server sends heartbeats to all cleints so they can know their connection status

The server gathers conf data from the settings file and the local IP and hostname

network exposes this API:


init(recvCallback, networkEventCallback)
getHostname()
getIp()
getSubscribers()
send(host, msg)
"""

import json
import os
import time
import socket
import sys
import zmq

# constants
BASE_PATH = "/home/stella/Dropbox/projects/current/nervebox_2/" 
SERVER_PATH = "%sserver/" % (BASE_PATH )
COMMON_PATH = "%scommon/" % (BASE_PATH )
DEVICES_PATH = "%sclient/devices/" % (BASE_PATH )
HOSTNAME = socket.gethostname()

# local paths
sys.path.append(BASE_PATH)
sys.path.append(COMMON_PATH)
sys.path.append(SERVER_PATH)

# import local modules
import discovery
import pubsub

with open(COMMON_PATH + 'settings.json', 'r') as f:
  SETTINGS = json.load(f)

subscribernames = filter(lambda x: os.path.isdir(os.path.join(DEVICES_PATH, x)), os.listdir(DEVICES_PATH))

subscribernames.append("nervebox2")

def recvCallback(topic, msg):
  print "recvCallback", repr(topic), repr(msg)

def netStateCallback(hostname, connected):
  print "netStateCallback", hostname, connected

def handleSubscriberFound(msg):
  pubsub_api["subscribe"](msg["hostname"],msg["ip"],SETTINGS["pubsub_pubPort"], ("__heartbeat__"))

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


