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
            m = self.mapping[deviceName][str(channel)][str(cmd)][str(note)]
            print m
            x_params = m[2]
            d = self.makeDynamics(velocity) if "velocity" in x_params else self.makeDynamics(0)
            p = self.makePitch(note) if "pitch" in x_params else {}
            t = self.makeTimbre() if "timbre" in x_params else {}
            payload_d = {'dynamics':d,'pitch':p,'timbre':t}
            paylod_j = json.dumps(payload_d, separators=(',', ':'))
            nosc = nerveOSC.assemble(m[0], m[1], paylod_j)
            self.callback(nosc)
        except Exception, e:
            pass
            #traceback.print_exc()
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
            "/sound/snare/pitch/":None,
            "/sound/bongo/bang/":None,
            "/sound/bongo/off/":None,
            "/sound/bongo/pitch/":None,
            "/sound/block/bang/":None,
            "/sound/block/off/":None,
            "/sound/block/pitch/":None,
            "/sound/bass/bang/":None,
            "/sound/bass/off/":None,
            "/sound/bass/pitch/":None,
            "/sound/brush/bang/":None,
            "/sound/brush/off/":None,
            "/sound/brush/pitch/":None,
            "/system/clock/1/set/":None,
            "/system/clock/2/set/":None,
            "/system/clock/3/set/":None,
            "/system/clock/source/toggle/":None,
            "/system/power/toggle/":None,
            "/system/volume/set/":None,
            "/system/balance/set/":None,
            "/system/miditest":None,
            "/system/midipanic":None,
            "/system/ping":None,
            "/ping":None,
        }
    },
    "RHYTHM_ACE":{
        "paths":{
            "/sound/bass/bang/":None,
            "/sound/bass/pitch/":None,
            "/sound/bass/off/":None,
            "/sound/snare/bang/":None,
            "/sound/snare/pitch/":None,
            "/sound/snare/off/":None,
            "/sound/low_conga/bang/":None,
            "/sound/low_conga/pitch/":None,
            "/sound/low_conga/off/":None,
            "/sound/log_bongo/bang/":None,
            "/sound/log_bongo/pitch/":None,
            "/sound/log_bongo/off/":None,
            "/sound/cowbell/bang/":None,
            "/sound/cowbell/pitch/":None,
            "/sound/cowbell/off/":None,
            "/sound/claves/bang/":None,
            "/sound/claves/pitch/":None,
            "/sound/claves/off/":None,
            "/sound/cymbal/bang/":None,
            "/sound/cymbal/pitch/":None,
            "/sound/cymbal/off/":None,
            "/sound/maracas/bang/":None,
            "/sound/maracas/pitch/":None,
            "/sound/maracas/off/":None,
            "/sound/brush/bang/":None,
            "/sound/brush/pitch/":None,
            "/sound/brush/off/":None,
            "/system/power/toggle/":None,
            "/system/start/":None,
            "/system/stop/":None,
            "/system/volume/set/":None,
            "/system/balance/set/":None,
            "/system/miditest":None,
        }
    },
    "R8MKII":{
        "paths":{
            "/sound/0/bang/":None,
            "/sound/1/bang/":None,
            "/sound/2/bang/":None,
            "/sound/3/bang/":None,
            "/sound/4/bang/":None,
            "/sound/5/bang/":None,
            "/sound/6/bang/":None,
            "/sound/7/bang/":None,
            "/sound/8/bang/":None,
            "/sound/9/bang/":None,
            "/sound/10/bang/":None,
            "/sound/11/bang/":None,
            "/sound/12/bang/":None,
            "/sound/13/bang/":None,
            "/sound/14/bang/":None,
            "/sound/15/bang/":None,
            "/sound/16/bang/":None,
            "/sound/17/bang/":None,
            "/sound/18/bang/":None,
            "/sound/19/bang/":None,
            "/sound/20/bang/":None,
            "/sound/21/bang/":None,
            "/sound/22/bang/":None,
            "/sound/23/bang/":None,
            "/sound/24/bang/":None,
            "/sound/25/bang/":None,
            "/sound/26/bang/":None,
            "/sound/27/bang/":None,
            "/sound/28/bang/":None,
            "/sound/29/bang/":None,
            "/sound/30/bang/":None,
            "/sound/31/bang/":None,
            "/system/miditest":None,
        }
    }
}

test1 = {
    "0582_0009":{
        "0":{ # channel
            "9":{#note on
                "48":["TR505","/sound/bass_drum/bang",["velocity"]],
                "50":["TR505","/sound/snare_drum/bang",["velocity"]],
                "52":["TR505","/sound/rim_shot/bang",["velocity"]],
                "53":["TR505","/sound/low_tom/bang",["velocity"]],
                "55":["TR505","/sound/mid_tom/bang",["velocity"]],
                "57":["TR505","/sound/hi_tom/bang",["velocity"]],
                "59":["TR505","/sound/hand_clap/bang",["velocity"]],
                "60":["TR505","/sound/low_conga/bang",["velocity"]],
                "62":["TR505","/sound/hi_conga/bang",["velocity"]],
                "64":["TR505","/sound/timbale/bang",["velocity"]],
                "65":["TR505","/sound/low_cowbell/bang",["velocity"]],
                "67":["TR505","/sound/hi_cowbell/bang",["velocity"]],

                "49":["TR505","/system/miditest",["velocity"]],
                
                "58":["TR505","/sound/crash_cymbal/bang",["velocity"]],
                "66":["TR505","/sound/ride_cymbal/bang",["velocity"]],
                "61":["TR505","/sound/closed_hi-hat/bang",["velocity"]],
                "63":["TR505","/sound/open_hi-hat/bang",["velocity"]],

            },
            "8":{#note off

            }
        },
        "1":{ # channel
            "9":{#note on
                "34":["MRQ","/system/clock/source/toggle",["velocity"]],
                "37":["MRQ","/system/power/toggle",["velocity"]],
                "33":["MRQ","/sound/bass/bang",["velocity"]],
                "35":["MRQ","/sound/snare/bang",["velocity"]],
                "36":["MRQ","/sound/block/bang",["velocity"]],
                "38":["MRQ","/sound/bongo/bang",["velocity"]],
                "39":["MRQ","/system/miditest",["velocity"]],
                "40":["MRQ","/sound/brush/bang",["velocity"]],
                "41":["MRQ","/sound/bass/pitch",["velocity"]],
                "43":["MRQ","/sound/snare/pitch",["velocity"]],
                "45":["MRQ","/sound/block/pitch",["velocity"]],
                "47":["MRQ","/sound/bongo/pitch",["velocity"]],
                "48":["MRQ","/sound/brush/pitch",["velocity"]],
                
                "50":["HR16","/sound/kick/bang",["velocity"]],
                "52":["HR16","/sound/snare/bang",["velocity"]],
                "53":["HR16","/sound/tom_1/bang",["velocity"]],
                "55":["HR16","/sound/tom_2/bang",["velocity"]],
                "57":["HR16","/sound/tom_3/bang",["velocity"]],
                "59":["HR16","/sound/tom_4/bang",["velocity"]],
                "60":["HR16","/sound/perc_1/bang",["velocity"]],
                "62":["HR16","/sound/perc_2/bang",["velocity"]],
                "64":["HR16","/sound/perc_3/bang",["velocity"]],
                "65":["HR16","/sound/perc_4/bang",["velocity"]],
                "67":["HR16","/sound/claps/bang",["velocity"]],

                "51":["HR16","/system/miditest",["velocity"]],

                "54":["HR16","/sound/closed_hat/bang",["velocity"]],
                "56":["HR16","/sound/mid_hat/bang",["velocity"]],
                "58":["HR16","/sound/open_hat/bang",["velocity"]],
                "61":["HR16","/sound/ride/bang",["velocity"]],
                "63":["HR16","/sound/crash/bang",["velocity"]],

                "69":["RHYTHM_ACE","/sound/bass/bang",["velocity"]],
                "71":["RHYTHM_ACE","/sound/snare/bang",["velocity"]],
                "72":["RHYTHM_ACE","/sound/low_conga/bang",["velocity"]],
                "74":["RHYTHM_ACE","/sound/log_bongo/bang",["velocity"]],
                "76":["RHYTHM_ACE","/sound/maracas/bang",["velocity"]],
                "77":["RHYTHM_ACE","/sound/claves/bang",["velocity"]],
                "79":["RHYTHM_ACE","/sound/cowbell/bang",["velocity"]],
                "81":["RHYTHM_ACE","/sound/cymbal/bang",["velocity"]],
                "83":["RHYTHM_ACE","/sound/brush/bang",["velocity"]],

                "69":["RHYTHM_ACE","/sound/bass/pitch",["velocity"]],
                "71":["RHYTHM_ACE","/sound/snare/pitch",["velocity"]],
                "72":["RHYTHM_ACE","/sound/low_conga/pitch",["velocity"]],
                "74":["RHYTHM_ACE","/sound/log_bongo/pitch",["velocity"]],
                "76":["RHYTHM_ACE","/sound/maracas/pitch",["velocity"]],
                "77":["RHYTHM_ACE","/sound/claves/pitch",["velocity"]],
                "79":["RHYTHM_ACE","/sound/cowbell/pitch",["velocity"]],
                "81":["RHYTHM_ACE","/sound/cymbal/pitch",["velocity"]],
                "83":["RHYTHM_ACE","/sound/brush/pitch",["velocity"]],

                "70":["RHYTHM_ACE","/system/power/toggle",["velocity"]],
                "73":["RHYTHM_ACE","/system/start",["velocity"]],
                "75":["RHYTHM_ACE","/system/stop",["velocity"]],
                "78":["RHYTHM_ACE","/system/miditest",["velocity"]],


                "84":["R8MKII","/sound/0/bang",["velocity"]],
                "85":["R8MKII","/sound/1/bang",["velocity"]],
                "86":["R8MKII","/sound/2/bang",["velocity"]],
                "87":["R8MKII","/sound/3/bang",["velocity"]],
                "88":["R8MKII","/sound/4/bang",["velocity"]],
                "89":["R8MKII","/sound/5/bang",["velocity"]],
                "90":["R8MKII","/sound/6/bang",["velocity"]],
                "91":["R8MKII","/sound/7/bang",["velocity"]],
                "92":["R8MKII","/sound/8/bang",["velocity"]],
                "93":["R8MKII","/sound/9/bang",["velocity"]],
                "94":["R8MKII","/sound/10/bang",["velocity"]],
                "95":["R8MKII","/sound/11/bang",["velocity"]],
                "96":["R8MKII","/sound/12/bang",["velocity"]],
                "97":["R8MKII","/sound/13/bang",["velocity"]],
                "98":["R8MKII","/sound/14/bang",["velocity"]],
                "99":["R8MKII","/sound/15/bang",["velocity"]],
                "100":["R8MKII","/sound/16/bang",["velocity"]],
                "101":["R8MKII","/sound/17/bang",["velocity"]],
                "102":["R8MKII","/sound/18/bang",["velocity"]],
                "103":["R8MKII","/sound/19/bang",["velocity"]],
                "104":["R8MKII","/sound/20/bang",["velocity"]],
                "105":["R8MKII","/sound/21/bang",["velocity"]],
                "106":["R8MKII","/sound/22/bang",["velocity"]],
                "107":["R8MKII","/sound/23/bang",["velocity"]],
                "108":["R8MKII","/sound/24/bang",["velocity"]],
                "109":["R8MKII","/sound/25/bang",["velocity"]],
                "110":["R8MKII","/sound/26/bang",["velocity"]],
                "111":["R8MKII","/sound/27/bang",["velocity"]],
                "112":["R8MKII","/sound/28/bang",["velocity"]],
                "113":["R8MKII","/sound/29/bang",["velocity"]],
                "114":["R8MKII","/sound/30/bang",["velocity"]],
                "115":["R8MKII","/sound/31/bang",["velocity"]],

                "116":["R8MKII","/system/miditest",["velocity"]],


            },
            "8":{#note off
                "33":["MRQ","/sound/bass/off",["velocity"]],
                "35":["MRQ","/sound/snare/off",["velocity"]],
                "36":["MRQ","/sound/block/off",["velocity"]],
                "38":["MRQ","/sound/bongo/off",["velocity"]],
                "40":["MRQ","/sound/brush/off",["velocity"]],
                "41":["MRQ","/sound/bass/off",["velocity"]],
                "43":["MRQ","/sound/snare/off",["velocity"]],
                "45":["MRQ","/sound/block/off",["velocity"]],
                "47":["MRQ","/sound/bongo/off",["velocity"]],
                "48":["MRQ","/sound/brush/off",["velocity"]],

                "50":["HR16","/sound/kick/off",["velocity"]],
                "52":["HR16","/sound/snare/off",["velocity"]],
                "53":["HR16","/sound/tom_1/off",["velocity"]],
                "55":["HR16","/sound/tom_2/off",["velocity"]],
                "57":["HR16","/sound/tom_3/off",["velocity"]],
                "59":["HR16","/sound/tom_4/off",["velocity"]],
                "60":["HR16","/sound/perc_1/off",["velocity"]],
                "62":["HR16","/sound/perc_2/off",["velocity"]],
                "64":["HR16","/sound/perc_3/off",["velocity"]],
                "65":["HR16","/sound/perc_4/off",["velocity"]],
                "67":["HR16","/sound/claps/off",["velocity"]],

                "54":["HR16","/sound/closed_hat/off",["velocity"]],
                "56":["HR16","/sound/mid_hat/off",["velocity"]],
                "58":["HR16","/sound/open_hat/off",["velocity"]],
                "61":["HR16","/sound/ride/off",["velocity"]],
                "63":["HR16","/sound/crash/off",["velocity"]],

                "69":["RHYTHM_ACE","/sound/bass/off",["velocity"]],
                "71":["RHYTHM_ACE","/sound/snare/off",["velocity"]],
                "72":["RHYTHM_ACE","/sound/low_conga/off",["velocity"]],
                "74":["RHYTHM_ACE","/sound/log_bongo/off",["velocity"]],
                "76":["RHYTHM_ACE","/sound/maracas/off",["velocity"]],
                "77":["RHYTHM_ACE","/sound/claves/off",["velocity"]],
                "79":["RHYTHM_ACE","/sound/cowbell/off",["velocity"]],
                "81":["RHYTHM_ACE","/sound/cymbal/off",["velocity"]],
                "83":["RHYTHM_ACE","/sound/brush/off",["velocity"]],

                "69":["RHYTHM_ACE","/sound/bass/off",["velocity"]],
                "71":["RHYTHM_ACE","/sound/snare/off",["velocity"]],
                "72":["RHYTHM_ACE","/sound/low_conga/off",["velocity"]],
                "74":["RHYTHM_ACE","/sound/log_bongo/off",["velocity"]],
                "76":["RHYTHM_ACE","/sound/maracas/off",["velocity"]],
                "77":["RHYTHM_ACE","/sound/claves/off",["velocity"]],
                "79":["RHYTHM_ACE","/sound/cowbell/off",["velocity"]],
                "81":["RHYTHM_ACE","/sound/cymbal/off",["velocity"]],
                "83":["RHYTHM_ACE","/sound/brush/off",["velocity"]],

                "84":["R8MKII","/sound/0/off",["velocity"]],
                "85":["R8MKII","/sound/1/off",["velocity"]],
                "86":["R8MKII","/sound/2/off",["velocity"]],
                "87":["R8MKII","/sound/3/off",["velocity"]],
                "88":["R8MKII","/sound/4/off",["velocity"]],
                "89":["R8MKII","/sound/5/off",["velocity"]],
                "90":["R8MKII","/sound/6/off",["velocity"]],
                "91":["R8MKII","/sound/7/off",["velocity"]],
                "92":["R8MKII","/sound/8/off",["velocity"]],
                "93":["R8MKII","/sound/9/off",["velocity"]],
                "94":["R8MKII","/sound/10/off",["velocity"]],
                "95":["R8MKII","/sound/11/off",["velocity"]],
                "96":["R8MKII","/sound/12/off",["velocity"]],
                "97":["R8MKII","/sound/13/off",["velocity"]],
                "98":["R8MKII","/sound/14/off",["velocity"]],
                "99":["R8MKII","/sound/15/off",["velocity"]],
                "100":["R8MKII","/sound/16/off",["velocity"]],
                "101":["R8MKII","/sound/17/off",["velocity"]],
                "102":["R8MKII","/sound/18/off",["velocity"]],
                "103":["R8MKII","/sound/19/off",["velocity"]],
                "104":["R8MKII","/sound/20/off",["velocity"]],
                "105":["R8MKII","/sound/21/off",["velocity"]],
                "106":["R8MKII","/sound/22/off",["velocity"]],
                "107":["R8MKII","/sound/23/off",["velocity"]],
                "108":["R8MKII","/sound/24/off",["velocity"]],
                "109":["R8MKII","/sound/25/off",["velocity"]],
                "110":["R8MKII","/sound/26/off",["velocity"]],
                "111":["R8MKII","/sound/27/off",["velocity"]],
                "112":["R8MKII","/sound/28/off",["velocity"]],
                "113":["R8MKII","/sound/29/off",["velocity"]],
                "114":["R8MKII","/sound/30/off",["velocity"]],
                "115":["R8MKII","/sound/31/off",["velocity"]],
            },
        },
        "2":{ # channel
            "11":{# continuous controller
                "74":["MRQ","/system/clock/1/set",["velocity"]],
                "71":["MRQ","/system/clock/2/set",["velocity"]],
                "91":["MRQ","/system/clock/3/set",["velocity"]],
                "93":["MRQ","/system/volume/set",["velocity"]],
                "73":["MRQ","/system/balance/set",["velocity"]],
                "72":["RHYTHM_ACE","/system/volume/set",["velocity"]],
                "5" :["RHYTHM_ACE","/system/balance/set",["velocity"]],
                #"84":0,
                #"7":0,
            }
        }
    },
}



def init(mappingName,nOSCcallback,dbPath):
    global mappings
    mappings = Mappings(nOSCcallback)
    mappings.open(test1)

