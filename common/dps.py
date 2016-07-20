import commands
import json
import netifaces
import socket
import struct
import threading
import time
import zmq

from sys import platform as _platform

#####################
###### PUB SUB ######
#####################

HEARTBEAT = 1.0 # seconds

class PubSocket():
    def __init__(self, port):
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%s" % port)
    def send(self, topic, msg):
        self.socket.send_string("%s %s" % (topic, msg))   

class Subscription():
    def __init__(self, hostname):
        self.hostname = hostname
        self.ip = None
        self.localPort = None
        self.remotePort = None
        self.lastHeartbeat = 0.0
        self.connected = False
    def setHeartbeat(self):
        self.lastHeartbeat = time.time()
    def getLastHeartbeat(self, lastHeartbeat):
        return self.lastHeartbeat
    def testConnection(self):
        hb = self.lastHeartbeat + ( 2 * HEARTBEAT) > time.time() #if heartbeat is two beats stale
        if self.connected and not hb: # recently disconnected
            self.connected = False
            return False
        if not self.connected and hb: # recently connected
            self.connected = True            
            return True
        return None
    def setConnected(self, ip=None, remotePort=None):
        self.ip = ip
        self.remotePort = remotePort
        self.connected = True

class Subscriptions(threading.Thread):
    """ this class manages a zmq sub socket and code for tracking publishers' connect state using heartbeats """
    def __init__(self, hostnames, publish_port, recvCallback, netStateCallback):
        threading.Thread.__init__(self)
        # socket details
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.recvCallback = recvCallback
        # subscription tracking details
        self.subscriptions = {}
        map(self.addSubscription, hostnames)
        self.hbTimeout = 1.0
        self.publish_port = publish_port
        self.netStateCallback = netStateCallback
    def addSubscription(self, hostname):
        """ nominally registers a new subscription, does not connect a socket for them b/c it may not be connected at init """
        self.subscriptions[hostname] = Subscription(hostname)
    def connectSubscription(self, hostname, ip, port, topics_t):
        """ when a publisher's ip and hostname are discovered, we can connect a subscription to it """
        self.socket.connect("tcp://%s:%s" % (ip, port))
        for topic in topics_t:
            self.socket.setsockopt(zmq.SUBSCRIBE, topic)
        self.subscriptions[hostname].setConnected(ip, self.publish_port)
        self.netStateCallback(hostname, True)
    def disconnectSubscription(self, hostname):
        self.netStateCallback(hostname, False)
    def getSubscriptions(self):
        return self.subscriptions
    def recordHeartbeat(self, hostname):
        self.subscriptions[hostname].setHeartbeat()
    def run(self):
        while True:
            msg_str = self.socket.recv()
            topic, msg = msg_str.split(' ', 1)
            if topic == "__heartbeat__":
                self.recordHeartbeat(msg)
            else:
                self.recvCallback(topic, msg)

class CheckHeartbeats(threading.Thread):
    """ this class manages a zmq sub socket and code for tracking publishers' connect state using heartbeats """
    def __init__(self, subscriptions_instance):
        threading.Thread.__init__(self)
        self.subscriptions_instance = subscriptions_instance
    def run(self):
        while True:
            for hostname, subscriber in self.subscriptions_instance.getSubscriptions().iteritems():
                stat = subscriber.testConnection()
                if stat == True:
                    self.subscriptions_instance.netStateCallback(hostname, True)
                if stat == False:
                    self.subscriptions_instance.netStateCallback(hostname, False)
                time.sleep(HEARTBEAT)

def sendHeartbeats(pubsocket, heartbeatMsg):
    while True:
        pubsocket.send("__heartbeat__", heartbeatMsg)
        time.sleep(HEARTBEAT)

def init(subscribersnames,localName, publish_port, recvCallback,netStateCallback):
    #pubsocket = PubSocket(publish_port, localName)
    #pubsocket.start()
    pubsocket = PubSocket(publish_port)
    subscriptions = Subscriptions(subscribersnames, publish_port, recvCallback, netStateCallback)
    subscriptions.start()
    checkheartbeats = CheckHeartbeats(subscriptions)
    checkheartbeats.start()

    t1 = threading.Thread(target=sendHeartbeats, args=(pubsocket, localName))
    t1.start()

    return {
        "publish":pubsocket.send, # topic, msg
        "subscribe":subscriptions.connectSubscription, # hostname, ip, port, topics_t
        "getSubscriptions":subscriptions.getSubscriptions
    }

#####################
##### DISCOVERY #####
#####################

def getLocalIP():
    if _platform == "darwin":
        interfaceName = "en0"
    else:
        interfaceName = "eth0"
    netifaces.ifaddresses(interfaceName)    
    return netifaces.ifaddresses(interfaceName)[2][0]['addr']

#####################
##### RESPONDER #####
#####################

class Responder(threading.Thread):
    def __init__(self, listener_grp, listener_port, response_port, localIP, callback):
        threading.Thread.__init__(self)
        self.listener_port = listener_port
        self.response_port = response_port
        self.localIP = localIP
        self.callback = callback
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((listener_grp, listener_port))
        self.mreq = struct.pack("4sl", socket.inet_aton(listener_grp), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, self.mreq)
        self.IpTiming = {}
    def response(self, remoteIP, msg_json): # response sends the local IP to the remote device
        print "discovery Responder 1"
        if self.IpTiming.has_key(remoteIP):
            if self.IpTiming[remoteIP] + 6 > time.time():
                return
        else:
            self.IpTiming[remoteIP] = time.time()
        print "discovery Responder 2"
        context = zmq.Context()
        print "discovery Responder 3"
        socket = context.socket(zmq.PAIR)
        print "discovery Responder 4"
        socket.connect("tcp://%s:%s" % (remoteIP,self.response_port))
        print "discovery Responder 5"
        socket.send(msg_json)
        print "discovery Responder 6"
        socket.close()
        print "discovery Responder 7"
    def run(self):
        while True:
            #try:
                msg_json = self.sock.recv(1024)
                msg_d = json.loads(msg_json)
                print "Event: Device Discovered:",msg_json
                remoteIP = msg_d["ip"]
                resp_d = self.callback(msg_d)
                resp_json = json.dumps( {"ip":self.localIP,"hostname":socket.gethostname()})
                #print "resp_json=", resp_json
                self.response(remoteIP,resp_json)
            #except Exception as e:
            #    print "Exception in dynamicDiscovery.server.Discovery: %s" % (repr(e))

def init_responder(listener_grp, listener_port, response_port, callback):
    print "listening for multicast on port" , listener_port, "in multicast group", listener_grp
    responder = Responder(
        listener_grp,
        listener_port, 
        response_port, 
        getLocalIP(), 
        callback
    )
    responder.start()


##################
##### CALLER #####
##################

class CallerSend(threading.Thread):
    def __init__(self, localHostname, localIP, mcast_grp, mcast_port):
        #print "-----", localHostname, localIP, mcast_grp, mcast_port
        threading.Thread.__init__(self)
        self.mcast_grp = mcast_grp
        self.mcast_port = mcast_port
        self.mcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.mcast_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        self.msg_d = {"ip":localIP,"hostname":localHostname}
        self.msg_json = json.dumps(self.msg_d)
        self.mcast_msg = self.msg_json
        self.serverFound_b = False
    def setServerFound(self,b):
        self.serverFound_b = b
    def run(self):
        while True:
            if not self.serverFound_b:
                print "calling to",self.mcast_grp, self.mcast_port
                self.mcast_sock.sendto(self.mcast_msg, (self.mcast_grp, self.mcast_port))
            time.sleep(5)

class CallerRecv(threading.Thread):
    def __init__(self, recv_port, callback, callerSend):
        threading.Thread.__init__(self)
        self.callback = callback
        self.callerSend = callerSend
        self.listen_context = zmq.Context()
        self.listen_sock = self.listen_context.socket(zmq.PAIR)
        self.listen_sock.bind("tcp://*:%d" % recv_port)
        print "CallerRecv listening on port %d" % (recv_port)
    def run(self):
        #print "CallerRecv run"
        print "discovery CallerRecv 1"
        msg_json = self.listen_sock.recv()
        #print ">>>>>>>>>>", msg_json
        print "discovery CallerRecv 2"
        msg_d = json.loads(msg_json)
        print "discovery CallerRecv 3"
        self.callback(msg_d)
        # to do: test the connection
        print "discovery CallerRecv 4"
        self.callerSend.setServerFound(True)
        print "discovery CallerRecv 5"

def init_caller(mcast_grp, mcast_port, recv_port, callback):
    print "calling port" , mcast_port, "in multicast group", mcast_grp
    callerSend = CallerSend(
        socket.gethostname(), 
        getLocalIP(), 
        mcast_grp, 
        mcast_port
    )
    callerRecv = CallerRecv(
        recv_port, 
        callback, 
        callerSend
    )
    callerRecv.start()
    callerSend.start()
    return callerSend

#####################
#### GLOBAL INIT ####
#####################

def recvCallback(topic, msg):
    print "recvCallback", repr(topic), repr(msg)
    if ROLE == "client":
        device.handleNOSC(nerveOSC.parse(msg))

def netStateCallback(hostname, connected):
    print "netStateCallback", hostname, connected
    callerSend.setServerFound(connected)

def serverFoundCallback(msg):
    pubsub_api["subscribe"](msg["hostname"],msg["ip"],SETTINGS["pubsub_pubPort"], ("__heartbeat__", HOSTNAME))

def handleSubscriberFound(msg):
    pubsub_api["subscribe"](msg["hostname"],msg["ip"],SETTINGS["pubsub_pubPort"], ("__heartbeat__", "osc"))

def init_networking(subscribernames,hostname,settings,role):

    pubsub_api = init(
        subscribernames,
        hostname, 
        settings["pubsub_pubPort"], 
        recvCallback,
        netStateCallback
    )
    if role == "client":
        callerSend = init_caller(
            settings["discovery_multicastGroup"], 
            settings["discovery_multicastPort"],
            settings["discovery_responsePort"],
            serverFoundCallback
        )
    else:
        callerSend = init_responder(
            settings["discovery_multicastGroup"], 
            settings["discovery_multicastPort"],
            settings["discovery_responsePort"],
            handleSubscriberFound
        )

