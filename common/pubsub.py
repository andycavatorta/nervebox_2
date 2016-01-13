import threading
import time
import zmq

"""
class PubSocket(threading.Thread):
    def __init__(self, port, heartbeatMsg):
        threading.Thread.__init__(self)
        self.heartbeatMsg = heartbeatMsg
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%s" % port)
    def send(self, topic, msg):
        print "pubsub.py PubSocket.send", topic, msg
        self.socket.send("%s %s" % (topic, msg))   
    def run(self):
        while True:
            #print "send heartbeat"
            self.socket.send("%s %s" % ("__heartbeat__", self.heartbeatMsg))
            time.sleep(1)
"""
HEARTBEAT = 1.0 # seconds

class PubSocket():
    def __init__(self, port):
        self.port = port
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%s" % port)
    def send(self, topic, msg):
        print "pubsub.py PubSocket.send", self.port, topic, msg
        self.socket.send("%s %s" % (topic, msg))   

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
            print "msg recieved", msg_str
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
        #print "send heartbeat"
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

"""


"""