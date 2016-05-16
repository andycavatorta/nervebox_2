"""
This module manages MIDI input devices

API:
    init(deviceCallback, msgCallback, filterType=None)
    getDeviceList()

events:
    device connected (name, time)
    device removed (name)
    midi message received (device name, msg)

"""
import mido
import threading
import time


IGNORED_DEVICES = ["Midi Through Port-0"]

class DeviceTracker(threading.Thread):
    def __init__(self, deviceCallback, msgCallback, filterType=None):
        threading.Thread.__init__(self)
        self.deviceCallback = deviceCallback
        self.msgCallback = msgCallback
        self.filterType = filterType
        self.devices_d = {}

    def listMidiDevices(self): 
        return
    def getDeviceDiff(self, perceived):
        known = self.devices_d.keys()
        deleted = set(known) - set(perceived)
        new =  set(known) ^ set(perceived)
        return [new, deleted]
    def addDevice(self, newDeviceName):
        self.deviceCallback(["add",newDeviceName])
        #self.devices_d[newDeviceName] = mido.open_input(newDeviceName, callback=self.msgCallback)
    def deleteDevice(self, deletedDeviceName):
        self.deviceCallback(["remove",deletedDeviceName])
        #self.devices_d[deletedDeviceName].close()
        #del self.devices_d[deletedDeviceName]
    def start(self):
        while True:
            names = mido.get_input_names()
            print names
            for id in IGNORED_DEVICES:
                names.remove(id) 
            (newDevices_l, deletedDevices_l) = self.getDeviceDiff(names)
            print newDevices_l, deletedDevices_l, self.devices_d.keys()
            for newDeviceName in newDevices_l:
                self.addDevice(newDeviceName)
            for deletedDeviceName in deletedDevices_l:
                self.deleteDevice(deletedDeviceName)
            time.sleep(1)

def cb1(msg):
    print msg 

def cb2(msg):
    print msg 

def init(cb1, cb2):
    deviceTracker = DeviceTracker(cb1, cb2)
    deviceTracker.start()


if __name__ == '__main__':
    init(cb1, cb2)


#######################################
"""
import commands
import inotify.adapters
import threading
import time
from operator import itemgetter

class DeviceTracker(threading.Thread):
    def __init__(self, callback):
        threading.Thread.__init__(self)
        self.callback = callback
        self.homeDir = '/dev/snd'
        self.devices_d = {}
        self.i = inotify.adapters.Inotify()
        self.i.add_watch(self.homeDir)
        self.listMidiDevices()

    def compareTimestamps(self,a,b):
        [a_h,a_m,a_s] = a.split(":")
        [b_h,b_m,b_s] = b.split(":")
        a_f = (int(a_h) * 24) + (int(a_m) * 60) + (float(a_s)) 
        b_f = (int(b_h) * 24) + (int(b_m) * 60) + (float(b_s)) 
        return b_f - a_f

    def timestampToFloat(self, ts_str):
        [a_h,a_m,a_s] = ts_str.split(":")
        return (int(a_h) * 24) + (int(a_m) * 60) + (float(a_s)) 

    def matchDeviceNameByTimestamp(self, t_f):
            byid = commands.getstatusoutput("ls --full-time /dev/snd/by-id/")
            byid_lines =  byid[1].split("\n")
            timesxNames = []
            for line in byid_lines:
                tokens = line.split(" ")
                if len(tokens) >= 7:
                    timestamp_str = tokens[6]
                    timestamp_f = self.timestampToFloat(timestamp_str)
                    print t_f - timestamp_f, t_f , timestamp_f
                    timesxNames.append((t_f - timestamp_f, tokens[8]))
            timesxNames = sorted(timesxNames, key=itemgetter(0))
            if timesxNames[0][0] < 1:
                print ">>",timesxNames[0][1]
            else:
                return False

    def listMidiDevices(self): 
        bydev = commands.getstatusoutput("ls --full-time %s" % self.homeDir)
        bydev_lines =  bydev[1].split("\n")
        for line in bydev_lines:
            tokens = line.split(" ")
            if len(tokens) < 3:
                continue
            filename = tokens[-1:][0]
            if filename[0:4] != "midi":
                continue
            timestamp_str = tokens[-3:-2][0]
            timestamp_f = self.timestampToFloat(timestamp_str)
            date_str = tokens[-4:-3][0]

            print filename, timestamp_f, date_str
            print self.matchDeviceNameByTimestamp(timestamp_f)

    def sort(self, deviceList):
        pass

    def start(self):
        try:
            for event in self.i.event_gen():
                if event is not None:
                    (header, type_names, watch_path, filename) = event
                    if filename[0:4] != "midi":
                        continue
                    if type_names[0] == 'IN_CREATE':
                        resp = commands.getstatusoutput("ls --full-time /dev/snd/%s" % (filename))
                        timestamp1 = resp[1].split(" ")[7]
                        time.sleep(1)
                        byid = commands.getstatusoutput("ls --full-time /dev/snd/by-id/")
                        byid_lines =  byid[1].split("\n")
                        timesxNames = []
                        for line in byid_lines:
                            tokens = line.split(" ")
                            if len(tokens) >= 7:
                                timestamp2 = tokens[6]
                                timesxNames.append((self.compareTimestamps(timestamp2,timestamp1), tokens[8]))
                        timesxNames = sorted(timesxNames, key=itemgetter(0))
                        if timesxNames[0][0] < 1:
                            print "connected %s as %s" % (filename,timesxNames[0][1])
                    if type_names[0] == 'IN_DELETE':
                        print "removed", filename
        finally:
            self.i.remove_watch('/dev/snd')





def dummycallback(msg):
    print msg 


def init(cb):
    deviceTracker = DeviceTracker(cb)
    deviceTracker.start()


init(dummycallback)

"""