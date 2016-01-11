import json
import socket
import sys

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

# load config
with open(COMMON_PATH + 'settings.json', 'r') as f:
    SETTINGS = json.load(f)

subscribernames = ["nervebox"]

def recvCallback(topic, msg):
    print repr(topic), ":", repr(msg)

def netStateCallback(hostname, connected):
  print "netStateCallback", hostname, connected
  callerSend.setServerFound(connected)

def handleSubscriberFound(msg):
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
    handleSubscriberFound
)
