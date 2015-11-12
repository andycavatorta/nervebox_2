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
        try:
            nosc = self.mapping[deviceName][str(channel)][str(cmd)][str(note)]
            nosc = nosc.replace("@pitch", str(note)).replace("@velocity", str(velocity))
            self.callback(nosc)
        except Exception, e:
            print "exception in mapMIDIToNerveOSC.Mappings.input:", deviceName, cmd, channel, note, velocity, e

inputs = {
    "Alesis_Q25":None,
    "M-Audio_Oxygen_88":None
}

outputs = {
    "TR505":{
        "paths":{
            "/sound/low_conga/accent/":None,
            "/sound/low_conga/bang/":None,
            "/sound/low_conga/off/":None,
            "/sound/low_conga/pitch/@":None,

            "/sound/hi_conga/accent/":None,
            "/sound/hi_conga/bang/":None,
            "/sound/hi_conga/off/":None,
            "/sound/hi_conga/pitch/@":None,

            "/sound/timbale/accent/":None,
            "/sound/timbale/bang/":None,
            "/sound/timbale/off/":None,
            "/sound/timbale/pitch/@":None,

            "/sound/low_cowbell/accent/":None,
            "/sound/low_cowbell/bang/":None,
            "/sound/low_cowbell/off/":None,
            "/sound/low_cowbell/pitch/@":None,

            "/sound/hi_cowbell/accent/":None,
            "/sound/hi_cowbell/bang/":None,
            "/sound/hi_cowbell/off/":None,
            "/sound/hi_cowbell/pitch/@":None,

            "/sound/hand_clap/accent/":None,
            "/sound/hand_clap/bang/":None,
            "/sound/hand_clap/off/":None,
            "/sound/hand_clap/pitch/@":None,

            "/sound/crash_cymbal/accent/":None,
            "/sound/crash_cymbal/bang/":None,
            "/sound/crash_cymbal/off/":None,
            "/sound/crash_cymbal/pitch/@":None,

            "/sound/ride_cymbal/accent/":None,
            "/sound/ride_cymbal/bang/":None,
            "/sound/ride_cymbal/off/":None,
            "/sound/ride_cymbal/pitch/@":None,

            "/sound/bass_drum/accent/":None,
            "/sound/bass_drum/bang/":None,
            "/sound/bass_drum/off/":None,
            "/sound/bass_drum/pitch/@":None,

            "/sound/snare_drum/accent/":None,
            "/sound/snare_drum/bang/":None,
            "/sound/snare_drum/off/":None,
            "/sound/snare_drum/pitch/@":None,

            "/sound/low_tom/accent/":None,
            "/sound/low_tom/bang/":None,
            "/sound/low_tom/off/":None,
            "/sound/low_tom/pitch/@":None,

            "/sound/mid_tom/accent/":None,
            "/sound/mid_tom/bang/":None,
            "/sound/mid_tom/off/":None,
            "/sound/mid_tom/pitch/@":None,

            "/sound/hi_tom/accent/":None,
            "/sound/hi_tom/bang/":None,
            "/sound/hi_tom/off/":None,
            "/sound/hi_tom/pitch/@":None,

            "/sound/rim_shot/accent/":None,
            "/sound/rim_shot/bang/":None,
            "/sound/rim_shot/off/":None,
            "/sound/rim_shot/pitch/@":None,

            "/sound/closed_hi-hat/accent/":None,
            "/sound/closed_hi-hat/bang/":None,
            "/sound/closed_hi-hat/off/":None,
            "/sound/closed_hi-hat/pitch/@":None,

            "/sound/open_hi-hat/accent/":None,
            "/sound/open_hi-hat/bang/":None,
            "/sound/open_hi-hat/off/":None,
            "/sound/open_hi-hat/pitch/@":None,

            "/system/power/on/":None,
            "/system/power/off/":None,

            "/system/clock/1/":None,
            "/system/clock/2/":None,
            "/system/clock/3/":None,
            "/system/clock/4/":None,

            "/system/miditest/start/":None,
            "/system/miditest/stop/":None,
            "/system/midipanic/":None,

        },
    },
    "Tempest":{
        "paths":{}
    },
    "HR16":{
        "paths":{
            "/sound/tom_1/accent/":None,
            "/sound/tom_1/bang/":None,
            "/sound/tom_1/off/":None,
            "/sound/tom_1/pitch/@":None,

            "/sound/tom_2/accent/":None,
            "/sound/tom_2/bang/":None,
            "/sound/tom_2/off/":None,
            "/sound/tom_2/pitch/@":None,

            "/sound/tom_3/accent/":None,
            "/sound/tom_3/bang/":None,
            "/sound/tom_3/off/":None,
            "/sound/tom_3/pitch/@":None,

            "/sound/tom_4/accent/":None,
            "/sound/tom_4/bang/":None,
            "/sound/tom_4/off/":None,
            "/sound/tom_4/pitch/@":None,

            "/sound/ride/accent/":None,
            "/sound/ride/bang/":None,
            "/sound/ride/off/":None,
            "/sound/ride/pitch/@":None,

            "/sound/crash/accent/":None,
            "/sound/crash/bang/":None,
            "/sound/crash/off/":None,
            "/sound/crash/pitch/@":None,

            "/sound/perc_1/accent/":None,
            "/sound/perc_1/bang/":None,
            "/sound/perc_1/off/":None,
            "/sound/perc_1/pitch/@":None,

            "/sound/perc_2/accent/":None,
            "/sound/perc_2/bang/":None,
            "/sound/perc_2/off/":None,
            "/sound/perc_2/pitch/@":None,

            "/sound/kick/accent/":None,
            "/sound/kick/bang/":None,
            "/sound/kick/off/":None,
            "/sound/kick/pitch/@":None,

            "/sound/snare/accent/":None,
            "/sound/snare/bang/":None,
            "/sound/snare/off/":None,
            "/sound/snare/pitch/@":None,

            "/sound/closed_hat/accent/":None,
            "/sound/closed_hat/bang/":None,
            "/sound/closed_hat/off/":None,
            "/sound/closed_hat/pitch/@":None,

            "/sound/mid_hat/accent/":None,
            "/sound/mid_hat/bang/":None,
            "/sound/mid_hat/off/":None,
            "/sound/mid_hat/pitch/@":None,

            "/sound/open_hat/accent/":None,
            "/sound/open_hat/bang/":None,
            "/sound/open_hat/off/":None,
            "/sound/open_hat/pitch/@":None,

            "/sound/claps/accent/":None,
            "/sound/claps/bang/":None,
            "/sound/claps/off/":None,
            "/sound/claps/pitch/@":None,

            "/sound/perc_3/accent/":None,
            "/sound/perc_3/bang/":None,
            "/sound/perc_3/off/":None,
            "/sound/perc_3/pitch/@":None,

            "/sound/perc_4/accent/":None,
            "/sound/perc_4/bang/":None,
            "/sound/perc_4/off/":None,
            "/sound/perc_4/pitch/@":None,

            "/system/power/on/":None,
            "/system/power/off/":None,

            "/system/clock/1/":None,
            "/system/clock/2/":None,
            "/system/clock/3/":None,
            "/system/clock/4/":None,

            "/system/miditest/start/":None,
            "/system/miditest/stop/":None,
            "/system/midipanic/":None,
        }
    },
}

test1 = {
    "Alesis_Q25":{
        "0":{ # channel
            "9":{#note on
                "48":"/TR505/sound/low_conga/bang/",
                "49":"/TR505/sound/hi_conga/bang/",
                "50":"/TR505/sound/timbale/bang/",
                "51":"/TR505/sound/low_cowbell/bang/",
                "52":"/TR505/sound/hi_cowbell/bang/",
                "53":"/TR505/sound/hand_clap/bang/",
                "54":"/TR505/sound/crash_cymbal/bang/",
                "55":"/TR505/sound/ride_cymbal/bang/",
                "56":"/TR505/sound/bass_drum/bang/",
                "57":"/TR505/sound/snare_drum/bang/",
                "58":"/TR505/sound/low_tom/bang/",
                "59":"/TR505/sound/mid_tom/bang/",
                "60":"/TR505/sound/hi_tom/bang/",
                "61":"/TR505/sound/rim_shot/bang/",
                "62":"/TR505/sound/closed_hi-hat/bang/",
                "63":"/TR505/sound/open_hi-hat/bang/",
                "64":"/TR505/system/miditest/start",
                "65":"/TR505/system/miditest/stop",
                "66":"/TR505/system/midipanic",
            },
            "8":{#note off
                "48":"/TR505/sound/low_conga/off/",
                "49":"/TR505/sound/hi_conga/off/",
                "50":"/TR505/sound/timbale/off/",
                "51":"/TR505/sound/low_cowbell/off/",
                "52":"/TR505/sound/hi_cowbell/off/",
                "53":"/TR505/sound/hand_clap/off/",
                "54":"/TR505/sound/crash_cymbal/off/",
                "55":"/TR505/sound/ride_cymbal/off/",
                "56":"/TR505/sound/bass_drum/off/",
                "57":"/TR505/sound/snare_drum/off/",
                "58":"/TR505/sound/low_tom/off/",
                "59":"/TR505/sound/mid_tom/off/",
                "60":"/TR505/sound/hi_tom/off/",
                "61":"/TR505/sound/rim_shot/off/",
                "62":"/TR505/sound/closed_hi-hat/off/",
                "63":"/TR505/sound/open_hi-hat/off/",
            }
        }
    },
    "M-Audio_Oxygen_88":{
        "1":{ # channel
            "9":{#note on
                "48":"/HR16/sound/snare/bang/",
                "49":"/HR16/sound/closed_hat/bang/",
                "50":"/HR16/sound/mid_hat/bang/",
                "51":"/HR16/sound/open_hat/bang/",
                "52":"/HR16/sound/tom_1/bang/",
                "53":"/HR16/sound/tom_2/bang/",
                "54":"/HR16/sound/tom_3/bang/",
                "55":"/HR16/sound/tom_4/bang/",
                "56":"/HR16/sound/perc_1/bang/",
                "57":"/HR16/sound/perc_2/bang/",
                "58":"/HR16/sound/perc_3/bang/",
                "59":"/HR16/sound/perc_4/bang/",
                "60":"/HR16/sound/kick/bang/",
                "61":"/HR16/sound/claps/bang/",
                "62":"/HR16/sound/ride/bang/",
                "63":"/HR16/sound/crash/bang/",

                "80":"/HR16/system/miditest/start",
                "81":"/HR16/system/miditest/stop",
                "82":"/HR16/system/midipanic",
            },
            "8":{#note off
                "48":"/HR16/sound/snare/off/",
                "49":"/HR16/sound/closed_hat/off/",
                "50":"/HR16/sound/mid_hat/off/",
                "51":"/HR16/sound/open_hat/off/",
                "52":"/HR16/sound/tom_1/off/",
                "53":"/HR16/sound/tom_2/off/",
                "54":"/HR16/sound/tom_3/off/",
                "55":"/HR16/sound/tom_4/off/",
                "56":"/HR16/sound/perc_1/off/",
                "57":"/HR16/sound/perc_2/off/",
                "58":"/HR16/sound/perc_3/off/",
                "59":"/HR16/sound/perc_4/off/",
                "60":"/HR16/sound/kick/off/",
                "61":"/HR16/sound/claps/off/",
                "62":"/HR16/sound/ride/off/",
                "63":"/HR16/sound/crash/off/",
            },
        }
    },
}

def init(mappingName,nOSCcallback,dbPath):
    global mappings
    mappings = Mappings(nOSCcallback)
    mappings.open(test1)

