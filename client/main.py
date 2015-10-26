import commands
import json
import socket
import time
import threading
import zmq

HOSTNAME = ""
IP = ""
SERVER_IP = ""

def broadcastIpToServer(msg):
    try:
        MCAST_GRP = '224.0.0.1'
        MCAST_PORT = 10000
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        print "common/main_client.py broadcastIpToServer()", msg
        sock.sendto(msg, (MCAST_GRP, MCAST_PORT))
    except Exception as e:
        print repr(e)

def Recv():

    port = "50000"
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.bind("tcp://*:%s" % port)

    while True:
        print "++++++"
        msg = socket.recv()
        print msg
        socket.send("Server message to client3")
        time.sleep(1)

recv = threading.Thread(target=Recv)
recv.start()

def ControlLoop():
    while 1:
        if SERVER_IP == "": # or time.time() - lastContactTime > serverTimeout: # if server is missing
            msg = "%s|%s" % (HOSTNAME, IP)
            broadcastIpToServer(msg)
        time.sleep(1)

def main():
    global HOSTNAME
    global IP

    cmd = "ip addr list eth0 |grep \"inet \" |cut -d' ' -f6|cut -d/ -f1"
    resp = commands.getstatusoutput(cmd)
    print resp
    IP = resp[1]
    HOSTNAME = socket.gethostname()

    controlloop = threading.Thread(target=ControlLoop)
    controlloop.start()

main()