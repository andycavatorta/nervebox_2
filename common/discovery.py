import commands
import fcntl
import json
import socket
import struct
import threading
import time
import zmq

"""
def getLocalIP():
    eth0 = commands.getstatusoutput("ip addr list eth0 |grep \"inet \" |cut -d' ' -f6|cut -d/ -f1")[1]
    wlan0 = commands.getstatusoutput("ip addr list wlan0 |grep \"inet \" |cut -d' ' -f6|cut -d/ -f1")[1]
    if eth0 == "":
        return wlan0
    else:
        return eth0
"""

def getLocalIP(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

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
        #print "Responder.response",remoteIP,self.response_port, msg_json
        if self.IpTiming.has_key(remoteIP):
            if self.IpTiming[remoteIP] + 6 > time.time():
                return
        else:
            self.IpTiming[remoteIP] = time.time()
        context = zmq.Context()
        socket = context.socket(zmq.PAIR)
        socket.connect("tcp://%s:%s" % (remoteIP,self.response_port))
        socket.send(msg_json)
        socket.close()
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
        getLocalIP('eth0'), 
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
        msg_json = self.listen_sock.recv()
        #print ">>>>>>>>>>", msg_json
        msg_d = json.loads(msg_json)
        self.callback(msg_d)
        # to do: test the connection
        self.callerSend.setServerFound(True)


#####################
##### INIT #####
#####################

def init_caller(mcast_grp, mcast_port, recv_port, callback):
    print "calling port" , mcast_port, "in multicast group", mcast_grp
    callerSend = CallerSend(
        socket.gethostname(), 
        getLocalIP('eth0'), 
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

