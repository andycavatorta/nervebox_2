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
import commands
# import inotify.adapters
import threading
import time
from operator import itemgetter

class DeviceTracker(threading.Thread):
    def __init__(self, deviceCallback, midiCallback):
        threading.Thread.__init__(self)
        self.deviceCallback = deviceCallback
        self.midiCallback = midiCallback
        self.homeDir = '/dev/snd'
        self.devices_d = {}
        # self.i = inotify.adapters.Inotify()
        # self.i.add_watch(self.homeDir)
        self.listMidiDevices()

    def compareTimestamps(self,a,b):
        return self.timestampToFloat(b) - self.timestampToFloat(a)

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
                    timesxNames.append((abs(t_f - timestamp_f), tokens[8]))
            timesxNames = sorted(timesxNames, key=itemgetter(0))
            if timesxNames[0][0] < 1:
                return timesxNames[0][1][4:-3]
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
            deviceName = self.matchDeviceNameByTimestamp(timestamp_f)
            if deviceName != None:
                self.addDevice(filename, deviceName)

    def addDevice(self, deviceId, deviceName):
        path =  "%s/%s" % (self.homeDir, deviceId)
        device = Device(path, deviceId, deviceName, self.midiCallback)
        device.start()
        self.devices_d[deviceId] = device
        self.deviceCallback("add",deviceId, deviceName)
        #self.devices_d[deviceId] = Device(path, deviceId, deviceName, self.midiCallback)
        #self.devices_d[deviceId].start()

    def removeDevice(self, deviceId):
        self.deviceCallback("remove",deviceId, self.devices_d[deviceId].deviceName)
        #print "removeDevice", deviceId
        self.devices_d[deviceId].join()
        del self.devices_d[deviceId]

    def run(self):
         pass
        # try:
        #     for event in self.i.event_gen():
        #         if event is not None:
        #             (header, type_names, watch_path, filename) = event
        #             if filename[0:4] != "midi":
        #                 continue
        #             if type_names[0] == 'IN_CREATE':
        #                 resp = commands.getstatusoutput("ls --full-time /dev/snd/%s" % (filename))
        #                 timestamp1 = resp[1].split(" ")[7]
        #                 time.sleep(1)
        #                 byid = commands.getstatusoutput("ls --full-time /dev/snd/by-id/")
        #                 byid_lines =  byid[1].split("\n")
        #                 timesxNames = []
        #                 for line in byid_lines:
        #                     tokens = line.split(" ")
        #                     if len(tokens) >= 7:
        #                         timestamp2 = tokens[6]
        #                         timesxNames.append((self.compareTimestamps(timestamp2,timestamp1), tokens[8]))
        #                 timesxNames = sorted(timesxNames, key=itemgetter(0))
        #                 if timesxNames[0][0] < 1:
        #                     self.addDevice(filename,timesxNames[0][1][4:-3])
        #             if type_names[0] == 'IN_DELETE':
        #                 self.removeDevice(filename)
        # finally:
        #     self.i.remove_watch('/dev/snd')

class Device(threading.Thread):
    def __init__(self, path, deviceId, deviceName, callback):
        threading.Thread.__init__(self)
        self.path = path
        self.deviceId = deviceId
        self.deviceName = deviceName
        self.callback = callback
        self.device = open(self.path)
    def parseMIDI(self, midi_str):
        stat_int = ord(midi_str[0])
        note_int = ord(midi_str[1])
        velocity_int = ord(midi_str[2])
        statBin_str = self.dec2bin(int(stat_int), 8)
        command_int = int(statBin_str[0:4], 2)
        channel_int = int(statBin_str[4:8], 2)
        return [command_int, channel_int, note_int, velocity_int]
    def dec2bin(self, n, fill):
        bStr = ''
        while n > 0:
            bStr = str(n % 2) + bStr
            n = n >> 1
        return bStr.zfill(fill)
    def run(self):
        lastTime = time.time()
        bytesFromDev_l = []
        while True:
            #try:
                midi_chr = self.device.read(1)
                thisTime = time.time()
                if thisTime - lastTime <= 0.01:
                    bytesFromDev_l.append(midi_chr)
                    if len(bytesFromDev_l)>=3:
                        midi_str = "".join(bytesFromDev_l)
                        midi_l = self.parseMIDI(midi_str)
                        #command_int = midi_l[0]
                        #channel_int = midi_l[1]
                        #note_int = midi_l[2]
                        #velocity_int = midi_l[3]
                        self.callback(
                            self.deviceName, 
                            midi_l[0], 
                            midi_l[1], 
                            midi_l[2], 
                            midi_l[3]
                        )
                        bytesFromDev_l = []
                else:
                    bytesFromDev_l = [midi_chr]
                lastTime = thisTime
            #except Exception as e:
            #    print "exception in Device %s", self.deviceId
            #    break

def init(dcb, mcb):
    deviceTracker = DeviceTracker(dcb, mcb)
    deviceTracker.start()

"""
def deviceCallback(msg):
    print "deviceCallback", msg 

def midiCallback(deviceName, cmd, channel, note, velocity):
    print "midiCallback", deviceName, cmd, channel, note, velocity

init(deviceCallback, midiCallback)
"""
