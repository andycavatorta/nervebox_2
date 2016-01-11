#import commands
#import json
#import socket
#import struct
import threading
import time
import zmq


class IncomingSocket(threading.Thread):
    def __init__(self, local_port, callback,exception_callback):
        threading.Thread.__init__(self)
        self.local_port = local_port
        self.callback = callback
        self.exception_callback = exception_callback
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.bind("tcp://*:%s" % local_port)
        self.socket.setsockopt(zmq.SUBSCRIBE, "all")
    def run(self):
        while True:
            #try:
                message = self.socket.recv()
                print "duplexSocket.IncomingSocket --> ", message
                resp = self.callback(message)
                #if resp == None:
                #    resp = ""
                #self.socket.send(resp)
            #except Exception as e:
            #    print "exception in duplexSockets.IncomingSocket.send", e
            #    self.exception_callback(e)

class OutgoingSocket(threading.Thread):
    def __init__(self, remote_ip, remote_port, ping_msg, callback,exception_callback):
        threading.Thread.__init__(self)
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.callback = callback
        self.exception_callback = exception_callback
        self.ping_msg = ping_msg
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.connect("tcp://%s:%s" % (self.remote_ip, self.remote_port))

    def send(self, msg):
        #try:
            print "duplexSocket.OutgoingSocket.send --> ", msg
            #self.socket.send_string(msg)
            self.socket.send("%d %d" % ("all", msg))
            #msg = self.socket.recv()
            #if self.callback:
            #    self.callback(msg)
        #except Exception as e:
        #    print "exception in duplexSockets.OutgoingSocket.send", e
        #    self.exception_callback(e)

    def run(self):
        while True:            
            time.sleep(5)
            self.send(self.ping_msg)
            #message = self.socket.recv()
            #resp = self.callback(message)
            #if resp == None:
            #    resp = ""
            #self.socket.send(resp)

def init(remote_ip, remote_port, local_port, ping_msg, incoming_callback, outgoing_callback, exception_callback):
    #print "duplexSockets.init",remote_ip, remote_port, local_port
    incomingSocket = IncomingSocket(local_port, incoming_callback, exception_callback)
    incomingSocket.start()
    outgoingSocket = OutgoingSocket(remote_ip, remote_port, ping_msg, outgoing_callback, exception_callback)
    outgoingSocket.start()
    print incomingSocket, outgoingSocket
    return outgoingSocket.send
