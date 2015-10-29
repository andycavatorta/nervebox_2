#import commands
#import json
#import socket
#import struct
import threading
#import time
import zmq


class IncomingSocket(threading.Thread):
    def __init__(self, local_port, callback):
        threading.Thread.__init__(self)
        self.local_port = local_port
        self.callback = callback
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:%s" % local_port)
    def run(self):
        while True:
            msg = self.socket.recv()
            print "message=", message
            resp = self.callback(message)
            if resp == None:
                resp = ""
            self.socket.send(resp)

class OutgoingSocket():
    def __init__(self, remote_ip, remote_port, callback):
        #threading.Thread.__init__(self)
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.callback = callback
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        #self.connected = False
        #try:
        self.socket.connect("tcp://%s:%s" % (self.remote_ip, self.remote_port))
        #except Exception as e:
        #    print "Exception in OutgoingSocket: %s" % (repr(e))

    def send(self, msg):
        while True:
            self.socket.send(msg)
            msg = self.socket.recv(msg)
            print "message=", msg
            if self.callback:
                self.callback(msg)

def init(remote_ip, remote_port, local_port, incoming_callback, outgoing_callback=None):
    print "duplexSockets.init",remote_ip, remote_port, local_port
    incomingSocket = IncomingSocket(local_port, incoming_callback)
    incomingSocket.start()
    outgoingSocket = OutgoingSocket(remote_ip, remote_port, outgoing_callback)
    return outgoingSocket.send
