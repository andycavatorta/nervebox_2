"""
This module create receives MIDI message




mapping operations:
    open 
    save
    create
    delete
    update
    clone
    getInputs
    getOutputs
    getMapping
    input
"""
#import store
import os
import sys

# constants
PI_NATIVE = os.uname()[4].startswith("arm") # TRUE if running on RPi
BASE_PATH = "/home/pi/nervebox_2" if PI_NATIVE else "/home/stella/Dropbox/projects/current/nervebox_2/" 
SERVER_PATH = "%sserver/" % (BASE_PATH )
COMMON_PATH = "%scommon/" % (BASE_PATH )
STORE_PATH = "%sstore/" % SERVER_PATH

# local paths
sys.path.append(BASE_PATH)
sys.path.append(COMMON_PATH)
sys.path.append(SERVER_PATH)

import nerveOSC

mappings = None

def midiIn(deviceName, cmd, channel, note, velocity):
    global mappings
    #print deviceName, cmd, channel, note, velocity
    mappings.input(deviceName, cmd, channel, note, velocity)

class Mappings():
    def __init__(self, callback):
        self.mapping = None
        self.callback = callback
        # first run: make sure mappings shelf exists.

    def open(self, mapping_r):
        self.mapping = mapping_r
    def save(self, mappingName, mapping):
        pass
    def create(self):
        pass
    def delete(self):
        pass
    def update(self):
        pass
    def getInputs(self):
        pass
    def getOutputs(self):
        pass
    def getMapping(self):
        pass
    def setOutput(self, callback):
        self.callback = callback
    def input(self, deviceName, cmd, channel, note, velocity):
        #try:
            nosc = self.mapping[deviceName][str(channel)][str(cmd)][str(note)]
            nosc.replace("@pitch", str(note)).replace("@velocity", str(velocity))
            self.callback(nosc)
        #except Exception, e:
        #    print "exception in mapMIDIToNerveOSC.Mappings.input:", deviceName, cmd, channel, note, velocity, e

inputs = {
    "Alesis_Q25":None,
    "M-Audio_Oxygen_88":None
}

outputs = {
    "TR505":{
        "paths":{
            "/sound/low_conga/accent":None,
            "/sound/low_conga/bang":None,
            "/sound/low_conga/off":None,
            "/sound/low_conga/pitch/@":None,

            "/sound/hi_conga/accent":None,
            "/sound/hi_conga/bang":None,
            "/sound/hi_conga/off":None,
            "/sound/hi_conga/pitch/@":None,

            "/sound/timbale/accent":None,
            "/sound/timbale/bang":None,
            "/sound/timbale/off":None,
            "/sound/timbale/pitch/@":None,

            "/sound/low_cowbell/accent":None,
            "/sound/low_cowbell/bang":None,
            "/sound/low_cowbell/off":None,
            "/sound/low_cowbell/pitch/@":None,

            "/sound/hi_cowbell/accent":None,
            "/sound/hi_cowbell/bang":None,
            "/sound/hi_cowbell/off":None,
            "/sound/hi_cowbell/pitch/@":None,

            "/sound/hand_clap/accent":None,
            "/sound/hand_clap/bang":None,
            "/sound/hand_clap/off":None,
            "/sound/hand_clap/pitch/@":None,

            "/sound/crash_cymbal/accent":None,
            "/sound/crash_cymbal/bang":None,
            "/sound/crash_cymbal/off":None,
            "/sound/crash_cymbal/pitch/@":None,

            "/sound/ride_cymbal/accent":None,
            "/sound/ride_cymbal/bang":None,
            "/sound/ride_cymbal/off":None,
            "/sound/ride_cymbal/pitch/@":None,

            "/sound/bass_drum/accent":None,
            "/sound/bass_drum/bang":None,
            "/sound/bass_drum/off":None,
            "/sound/bass_drum/pitch/@":None,

            "/sound/snare_drum/accent":None,
            "/sound/snare_drum/bang":None,
            "/sound/snare_drum/off":None,
            "/sound/snare_drum/pitch/@":None,

            "/sound/low_tom/accent":None,
            "/sound/low_tom/bang":None,
            "/sound/low_tom/off":None,
            "/sound/low_tom/pitch/@":None,

            "/sound/mid_tom/accent":None,
            "/sound/mid_tom/bang":None,
            "/sound/mid_tom/off":None,
            "/sound/mid_tom/pitch/@":None,

            "/sound/hi_tom/accent":None,
            "/sound/hi_tom/bang":None,
            "/sound/hi_tom/off":None,
            "/sound/hi_tom/pitch/@":None,

            "/sound/rim_shot/accent":None,
            "/sound/rim_shot/bang":None,
            "/sound/rim_shot/off":None,
            "/sound/rim_shot/pitch/@":None,

            "/sound/closed_hi-hat/accent":None,
            "/sound/closed_hi-hat/bang":None,
            "/sound/closed_hi-hat/off":None,
            "/sound/closed_hi-hat/pitch/@":None,

            "/sound/open_hi-hat/accent":None,
            "/sound/open_hi-hat/bang":None,
            "/sound/open_hi-hat/off":None,
            "/sound/open_hi-hat/pitch/@":None,

            "/system/power/on":None,
            "/system/power/off":None,

            "/system/clock/1/":None,
            "/system/clock/2/":None,
            "/system/clock/3/":None,
            "/system/clock/4/":None,
        },
    },
    "Tempest":{
        "paths":{}
    },
    "HR16":{
        "paths":{}
    },
}

test1 = {
    "Alesis_Q25":{
        "0":{ # channel
            "9":{#note on
                "48":"TR505/sound/low_conga/bang",
                "49":"TR505/sound/hi_conga/bang",
                "50":"TR505/sound/timbale/bang",
                "51":"TR505/sound/low_cowbell/bang",
                "52":"TR505/sound/hi_cowbell/bang",
                "53":"TR505/sound/hand_clap/bang",
                "54":"TR505/sound/crash_cymbal/bang",
                "55":"TR505/sound/ride_cymbal/bang",
                "56":"TR505/sound/bass_drum/bang",
                "57":"TR505/sound/snare_drum/bang",
                "58":"TR505/sound/low_tom/bang",
                "59":"TR505/sound/mid_tom/bang",
                "60":"TR505/sound/hi_tom/bang",
                "61":"TR505/sound/rim_shot/bang",
                "62":"TR505/sound/closed_hi-hat/bang",
                "63":"TR505/sound/open_hi-hat/bang",
            },
            "8":{#note off
                "48":"TR505/sound/low_conga/off",
                "49":"TR505/sound/hi_conga/off",
                "50":"TR505/sound/timbale/off",
                "51":"TR505/sound/low_cowbell/off",
                "52":"TR505/sound/hi_cowbell/off",
                "53":"TR505/sound/hand_clap/off",
                "54":"TR505/sound/crash_cymbal/off",
                "55":"TR505/sound/ride_cymbal/off",
                "56":"TR505/sound/bass_drum/off",
                "57":"TR505/sound/snare_drum/off",
                "58":"TR505/sound/low_tom/off",
                "59":"TR505/sound/mid_tom/off",
                "60":"TR505/sound/hi_tom/off",
                "61":"TR505/sound/rim_shot/off",
                "62":"TR505/sound/closed_hi-hat/off",
                "63":"TR505/sound/open_hi-hat/off",
            }
        }
    },
    "M-Audio_Oxygen_88":{
        "1":{ # channel
            "9":{#note on
                "48":"/TR505/sound/snare_drum/pitch/@pitch",
                "49":"/TR505/sound/snare_drum/pitch/@pitch",
                "50":"/TR505/sound/snare_drum/pitch/@pitch",
                "51":"/TR505/sound/snare_drum/pitch/@pitch",
                "52":"/TR505/sound/snare_drum/pitch/@pitch",
                "53":"/TR505/sound/snare_drum/pitch/@pitch",
                "54":"/TR505/sound/snare_drum/pitch/@pitch",
                "55":"/TR505/sound/snare_drum/pitch/@pitch",
                "56":"/TR505/sound/snare_drum/pitch/@pitch",
                "57":"/TR505/sound/snare_drum/pitch/@pitch",
                "58":"/TR505/sound/snare_drum/pitch/@pitch",
                "59":"/TR505/sound/snare_drum/pitch/@pitch",
            },
            "8":{#note off
                "48":"/TR505/sound/snare_drum/off",
                "49":"/TR505/sound/snare_drum/off",
                "50":"/TR505/sound/snare_drum/off",
                "51":"/TR505/sound/snare_drum/off",
                "52":"/TR505/sound/snare_drum/off",
                "53":"/TR505/sound/snare_drum/off",
                "54":"/TR505/sound/snare_drum/off",
                "55":"/TR505/sound/snare_drum/off",
                "56":"/TR505/sound/snare_drum/off",
                "57":"/TR505/sound/snare_drum/off",
                "58":"/TR505/sound/snare_drum/off",
                "59":"/TR505/sound/snare_drum/off",
            },
        }
    },
}

def init(mappingName,nOSCcallback,dbPath):
    #store.init(dbPath)
    global mappings
    mappings = Mappings(nOSCcallback)
    mappings.open(test1)

