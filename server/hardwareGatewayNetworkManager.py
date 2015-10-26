"""
This module manages the connection between clients and the server.
Clients discover the server through IP multicast.
Server manages client connections.
Exceptions sending to clients cause connection to be destroyed.  
    How will client discover server disconnetion?  Timeout?


"""
import json
import socket
import struct
import time
import threading
import sys
import zmq

"""
The Discover Class listens for IP Multicast requests on a specified port.
It forwards the requests for the Manager class
future:
    test multicast requests for expected format
    report exceptions to central logger
"""
class Discover(threading.Thread):
    def __init__(self, multicast_port, callback):
        threading.Thread.__init__(self)
        self.multicast_port = multicast_port
        self.callback = callback
        MCAST_GRP = '224.0.0.1' # no need to place this in settings.json
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((MCAST_GRP, multicast_port))
        self.mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, self.mreq)
    def run(self):
        #try:
            msg = self.sock.recv(1024)
            clienthost, clientip = msg.split("|")
            print "Event: Hardware Gateway Discovered:",clienthost, clientip
            self.callback(clienthost, clientip)
        #except Exception as e:
        #    print "Exception in hardwareGatewayNetworkManager.Discovery: %s" % (repr(e))

"""
The Manage class creates, destroys, and tracks the network connections from hardware gateways
"""
class Manage():
    def __init__(self,clientPort, recvdMsgCallback):
        self.clientPort = clientPort
        self.recvdMsgCallback = recvdMsgCallback
        self.gateways = {}
    def add(self,hostname, ip):
        self.gateways[hostname] = Gateway(hostname, ip, self.clientPort, self.recvdMsgCallback)
        self.gateways[hostname].start()
        self.gateways[hostname].send("asdf")
    def remove(self, hostname):
        self.gateways[hostname].close()
        self.gateways[hostname].join()
        delete(self.gateways[hostname])
    def getlist(self, verbose=False):
        return self.gateways.keys()

"""
The Gateway class contains the network connections for a Gateway
"""
class Gateway(threading.Thread):
    def __init__(self, hostname, ip, port, gatewayRecvCallback_f):
        threading.Thread.__init__(self)
        self.hostname = hostname
        self.ip = ip
        self.port = port
        self.gatewayRecvCallback_f = gatewayRecvCallback_f
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PAIR)
        print ">>>>>>", self.ip,self.port
        self.socket.connect("tcp://self.ip:%d" % (self.port))
        #self.socket.bind("tcp://%s:%d" % (self.ip,self.port))
    def close(self):
        pass
        # future: close self.context using zmq_ctx_term
    def send(self, msg_str):
        try:
            self.socket.send(msg_str)
        except Exception as e:
            print "Exception in hardwareGatewayNetworkManager.Gateway.send for %s: %s" % (self.hostname,repr(e))
    def run(self):
        if self.gatewayRecvCallback_f:
            while True:
                try:
                    msg = self.socket.recv()
                    self.gatewayRecvCallback_f(self.hostname,msg)
                except Exception as e:
                    # future: delete this instance using Manage.remove
                    print "Exception in hardwareGatewayNetworkManager.Gateway.run for %s: %s" % (self.hostname,repr(e))

def main(clientPort, multicast_port, recvdMsgCallback=False):
    manage = Manage(clientPort, recvdMsgCallback)
    discover = Discover(multicast_port, manage.add)
    discover.start()
