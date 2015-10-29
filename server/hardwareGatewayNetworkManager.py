"""
This module manages the connection between clients and the server.
Clients discover the server through IP multicast.
Server manages client connections.
Exceptions sending to clients cause connection to be destroyed.  
    How will client discover server disconnetion?  Timeout?


"""
import commands
import socket
import struct
import time
import threading
import zmq

"""
The Discover Class listens for IP Multicast requests on a specified port.
It forwards the requests for the Manager class
future:
    test multicast requests for expected format
    report exceptions to central logger
"""

class Discovery(threading.Thread):
    def __init__(self, multicast_port, response_port, localIP, callback):
        threading.Thread.__init__(self)
        self.multicast_port = multicast_port
        self.response_port = response_port
        self.localIP = localIP
        self.callback = callback
        MCAST_GRP = '224.0.0.1' # no need to place this in settings.json
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((MCAST_GRP, multicast_port))
        self.mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, self.mreq)
    def response(self, remoteIP):
        context = zmq.Context()
        socket = context.socket(zmq.PAIR)
        socket.connect("tcp://%s:%s" % (remoteIP,self.response_port))
        socket.send(self.localIP)
    def run(self):
        try:
            msg = self.sock.recv(1024)
            clienthost, clientip = msg.split("|")
            print "Event: Hardware Gateway Discovered:",clienthost, clientip
            self.response(clientip)
            #self.callback(clienthost, clientip)
        except Exception as e:
            print "Exception in hardwareGatewayNetworkManager.Discovery: %s" % (repr(e))

class Router(threading.Thread):
    def __init__(self, clientPort, recvdMsgCallback):
        threading.Thread.__init__(self)
        self.clientPort = clientPort
        self.recvdMsgCallback = recvdMsgCallback
        self.context = zmq.Context.instance()
        self.client = self.context.socket(zmq.ROUTER)
        self.client.bind("tcp://*:%d" % (clientPort))
    def sendToGateway(self, hostname, msg):
        self.client.send_multipart([hostname, msg])
    def run(self):
        while True:
            hostAndMsg = self.client.recv()
            print hostAndMsg

def main(clientPort, multicast_port, discoveryCallback, recvdMsgCallback=False):

    cmd = "ip addr list eth0 |grep \"inet \" |cut -d' ' -f6|cut -d/ -f1"
    resp = commands.getstatusoutput(cmd)
    print resp
    IP = resp[1]
    HOSTNAME = socket.gethostname()

    router = Router(clientPort, recvdMsgCallback)

    discovery = Discovery(multicast_port, 10001, IP, discoveryCallback)
    discovery.start()

    time.sleep(1)
    for i in range(30):
        router.sendToGateway(b'MRQ1', b'asdf')
        time.sleep(.1)
