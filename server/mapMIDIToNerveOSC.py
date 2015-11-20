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
import json
import math
import os
import sys
import traceback

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

#   THIS SHOULD PROBABLY GO IN ITS OWN LIBRARY

def makePitch(midiNoteNumber, cents_int=0):
    return {
        pitch:["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"][midiNoteNumber%12],
        octave:math.floor(midiNoteNumber/12)-1,
        cents:cents_int,
        freq:440.0 * (2.0**((midiNoteNumber-69+bend_f)/12.0)),
        midi:midiNoteNumber
    }


# #######################################


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
    def makePitch(self, midiNoteNumber, cents_int=0):
        return {
            'pitch':["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"][midiNoteNumber%12],
            'octave':math.floor(midiNoteNumber/12)-1,
            'cents':cents_int,
            'freq':440.0 * (2.0**((midiNoteNumber-69+bend_f)/12.0)),
            'midi':midiNoteNumber
        }
    def makeDynamics(self,midiVelocity):
        return {'amplitude':float(midiVelocity)/128.0}
        
    def makeTimbre(self):
        # to do: finish this
        return {} 
    
    def input(self, deviceName, cmd, channel, note, velocity):
        try:
            print deviceName, cmd, channel, note, velocity
            # midi properties to send: velocity, pitch(+pitchwheel), modwheel as timbre
            m = self.mapping[deviceName][str(channel)][str(cmd)][str(note)]
            x_params = m[2]
            d = self.makeDynamics(velocity) if "velocity" in x_params and cmd==9 else self.makeDynamics(0)
            p = self.makePitch(note) if "pitch" in x_params else {}
            t = self.makeTimbre() if "timbre" in x_params else {}
            payload_d = {'dynamics':d,'pitch':p,'timbre':t}
            paylod_j = json.dumps(payload_d, separators=(',', ':'))
            nosc = nerveOSC.assemble(m[0], m[1], paylod_j)
            self.callback(nosc)
        except Exception, e:
            pass
            #traceback.print_exc()
            #print "exception in mapMIDIToNerveOSC.Mappings.input:", deviceName, cmd, channel, note, velocity, e

inputs = {
    "Alesis_Q25":{
        "state":{
            "channel":{
                "note":{
                }
            }
        }
    },
    "M-Audio_Oxygen_88":{
        "state":{
            "channel":{
                "2":{
                    "note":{
                        "74":0,
                        "71":0,
                        "91":0,
                        "93":0,
                        "73":0,
                        "72":0,
                        "5":0,
                        "84":0,
                        "7":0,
                    }
                }
            }
        }
    }
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
        }
    },
    "HR16":{
        "paths":{
            "/sound/tom_1/bang/":None,
            "/sound/tom_1/off/":None,
            "/sound/tom_1/pitch/@":None,

            "/sound/tom_2/bang/":None,
            "/sound/tom_2/off/":None,
            "/sound/tom_2/pitch/@":None,

            "/sound/tom_3/bang/":None,
            "/sound/tom_3/off/":None,
            "/sound/tom_3/pitch/@":None,

            "/sound/tom_4/bang/":None,
            "/sound/tom_4/off/":None,
            "/sound/tom_4/pitch/@":None,

            "/sound/ride/bang/":None,
            "/sound/ride/off/":None,
            "/sound/ride/pitch/@":None,

            "/sound/crash/bang/":None,
            "/sound/crash/off/":None,
            "/sound/crash/pitch/@":None,

            "/sound/perc_1/bang/":None,
            "/sound/perc_1/off/":None,
            "/sound/perc_1/pitch/@":None,

            "/sound/perc_2/bang/":None,
            "/sound/perc_2/off/":None,
            "/sound/perc_2/pitch/@":None,

            "/sound/kick/bang/":None,
            "/sound/kick/off/":None,
            "/sound/kick/pitch/@":None,

            "/sound/snare/bang/":None,
            "/sound/snare/off/":None,
            "/sound/snare/pitch/@":None,

            "/sound/closed_hat/bang/":None,
            "/sound/closed_hat/off/":None,
            "/sound/closed_hat/pitch/@":None,

            "/sound/mid_hat/bang/":None,
            "/sound/mid_hat/off/":None,
            "/sound/mid_hat/pitch/@":None,

            "/sound/open_hat/bang/":None,
            "/sound/open_hat/off/":None,
            "/sound/open_hat/pitch/@":None,

            "/sound/claps/bang/":None,
            "/sound/claps/off/":None,
            "/sound/claps/pitch/@":None,

            "/sound/perc_3/bang/":None,
            "/sound/perc_3/off/":None,
            "/sound/perc_3/pitch/@":None,

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
    "MRQ":{
        "paths":{
            "/sound/snare/bang/":None,
            "/sound/snare/off/":None,
            "/sound/bongo/bang/":None,
            "/sound/bongo/off/":None,
            "/sound/block/bang/":None,
            "/sound/block/off/":None,
            "/sound/bass/bang/":None,
            "/sound/bass/off/":None,
            "/sound/brush/bang/":None,
            "/sound/brush/off/":None,
            "/system/clock/1/set/":None,
            "/system/clock/2/set/":None,
            "/system/clock/3/set/":None,
            "/system/clock/source/toggle/":None,
            "/system/power/toggle/":None,
            "/system/volume/set/":None,
            "/system/balance/set/":None,
        }
    }
}

test1 = {
    "Alesis_Q25":{
        "0":{ # channel
            "9":{#note on
                "48":["TR505","/sound/low_conga/bang",["velocity"]],
                "49":["TR505","/sound/hi_conga/bang",["velocity"]],
                "50":["TR505","/sound/timbale/bang",["velocity"]],
                "51":["TR505","/sound/low_cowbell/bang",["velocity"]],
                "52":["TR505","/sound/hi_cowbell/bang",["velocity"]],
                "53":["TR505","/sound/hand_clap/bang",["velocity"]],
                "54":["TR505","/sound/crash_cymbal/bang",["velocity"]],
                "55":["TR505","/sound/ride_cymbal/bang",["velocity"]],
                "56":["TR505","/sound/bass_drum/bang",["velocity"]],
                "57":["TR505","/sound/snare_drum/bang",["velocity"]],
                "58":["TR505","/sound/low_tom/bang",["velocity"]],
                "59":["TR505","/sound/mid_tom/bang",["velocity"]],
                "60":["TR505","/sound/hi_tom/bang",["velocity"]],
                "61":["TR505","/sound/rim_shot/bang",["velocity"]],
                "62":["TR505","/sound/closed_hi-hat/bang",["velocity"]],
                "63":["TR505","/sound/open_hi-hat/bang",["velocity"]],
            },
            "8":{#note off
                "48":["TR505","/sound/low_conga/off",["velocity"]],
                "49":["TR505","/sound/hi_conga/off",["velocity"]],
                "50":["TR505","/sound/timbale/off",["velocity"]],
                "51":["TR505","/sound/low_cowbell/off",["velocity"]],
                "52":["TR505","/sound/hi_cowbell/off",["velocity"]],
                "53":["TR505","/sound/hand_clap/off",["velocity"]],
                "54":["TR505","/sound/crash_cymbal/off",["velocity"]],
                "55":["TR505","/sound/ride_cymbal/off",["velocity"]],
                "56":["TR505","/sound/bass_drum/off",["velocity"]],
                "57":["TR505","/sound/snare_drum/off",["velocity"]],
                "58":["TR505","/sound/low_tom/off",["velocity"]],
                "59":["TR505","/sound/mid_tom/off",["velocity"]],
                "60":["TR505","/sound/hi_tom/off",["velocity"]],
                "61":["TR505","/sound/rim_shot/off",["velocity"]],
                "62":["TR505","/sound/closed_hi-hat/off",["velocity"]],
                "63":["TR505","/sound/open_hi-hat/off",["velocity"]],
            }
        }
    },
    "M-Audio_Oxygen_88":{
        "1":{ # channel
            "9":{#note on
                "48":["HR16","/sound/snare/bang",["velocity"]],
                "49":["HR16","/sound/closed_hat/bang",["velocity"]],
                "50":["HR16","/sound/mid_hat/bang",["velocity"]],
                "51":["HR16","/sound/open_hat/bang",["velocity"]],
                "52":["HR16","/sound/tom_1/bang",["velocity"]],
                "53":["HR16","/sound/tom_2/bang",["velocity"]],
                "54":["HR16","/sound/tom_3/bang",["velocity"]],
                "55":["HR16","/sound/tom_4/bang",["velocity"]],
                "56":["HR16","/sound/perc_1/bang",["velocity"]],
                "57":["HR16","/sound/perc_2/bang",["velocity"]],
                "58":["HR16","/sound/perc_3/bang",["velocity"]],
                "59":["HR16","/sound/perc_4/bang",["velocity"]],
                "60":["HR16","/sound/kick/bang",["velocity"]],
                "61":["HR16","/sound/claps/bang",["velocity"]],
                "62":["HR16","/sound/ride/bang",["velocity"]],
                "63":["HR16","/sound/crash/bang",["velocity"]],

                "64":["Tempest","/sound/low_conga/bang",["velocity"]],
                "65":["Tempest","/sound/hi_conga/bang",["velocity"]],
                "66":["Tempest","/sound/timbale/bang",["velocity"]],
                "67":["Tempest","/sound/low_cowbell/bang",["velocity"]],
                "68":["Tempest","/sound/hi_cowbell/bang",["velocity"]],
                "69":["Tempest","/sound/hand_clap/bang",["velocity"]],
                "70":["Tempest","/sound/crash_cymbal/bang",["velocity"]],
                "71":["Tempest","/sound/ride_cymbal/bang",["velocity"]],
                "72":["Tempest","/sound/bass_drum/bang",["velocity"]],
                "73":["Tempest","/sound/snare_drum/bang",["velocity"]],
                "74":["Tempest","/sound/low_tom/bang",["velocity"]],
                "75":["Tempest","/sound/mid_tom/bang",["velocity"]],
                "76":["Tempest","/sound/hi_tom/bang",["velocity"]],
                "77":["Tempest","/sound/rim_shot/bang",["velocity"]],
                "78":["Tempest","/sound/closed_hi-hat/bang",["velocity"]],
                "79":["Tempest","/sound/open_hi-hat/bang",["velocity"]],
                
                "80":["Tempest","/system/miditest/start",[]],
                "81":["Tempest","/system/miditest/stop",[]],
                "82":["Tempest","/system/midipanic",[]],
            },
            "8":{#note off
                "48":["HR16","/sound/snare/off",["velocity"]],
                "49":["HR16","/sound/closed_hat/off",["velocity"]],
                "50":["HR16","/sound/mid_hat/off",["velocity"]],
                "51":["HR16","/sound/open_hat/off",["velocity"]],
                "52":["HR16","/sound/tom_1/off",["velocity"]],
                "53":["HR16","/sound/tom_2/off",["velocity"]],
                "54":["HR16","/sound/tom_3/off",["velocity"]],
                "55":["HR16","/sound/tom_4/off",["velocity"]],
                "56":["HR16","/sound/perc_1/off",["velocity"]],
                "57":["HR16","/sound/perc_2/off",["velocity"]],
                "58":["HR16","/sound/perc_3/off",["velocity"]],
                "59":["HR16","/sound/perc_4/off",["velocity"]],
                "60":["HR16","/sound/kick/off",["velocity"]],
                "61":["HR16","/sound/claps/off",["velocity"]],
                "62":["HR16","/sound/ride/off",["velocity"]],
                "63":["HR16","/sound/crash/off",["velocity"]],

                "64":["Tempest","/sound/low_conga/off",["velocity"]],
                "65":["Tempest","/sound/hi_conga/off",["velocity"]],
                "66":["Tempest","/sound/timbale/off",["velocity"]],
                "67":["Tempest","/sound/low_cowbell/off",["velocity"]],
                "68":["Tempest","/sound/hi_cowbell/off",["velocity"]],
                "69":["Tempest","/sound/hand_clap/off",["velocity"]],
                "70":["Tempest","/sound/crash_cymbal/off",["velocity"]],
                "71":["Tempest","/sound/ride_cymbal/off",["velocity"]],
                "72":["Tempest","/sound/bass_drum/off",["velocity"]],
                "73":["Tempest","/sound/snare_drum/off",["velocity"]],
                "74":["Tempest","/sound/low_tom/off",["velocity"]],
                "75":["Tempest","/sound/mid_tom/off",["velocity"]],
                "76":["Tempest","/sound/hi_tom/off",["velocity"]],
                "77":["Tempest","/sound/rim_shot/off",["velocity"]],
                "78":["Tempest","/sound/closed_hi-hat/off",["velocity"]],
                "79":["Tempest","/sound/open_hi-hat/off",["velocity"]],
            },
        }
    },
}

def init(mappingName,nOSCcallback,dbPath):
    global mappings
    mappings = Mappings(nOSCcallback)
    mappings.open(test1)

