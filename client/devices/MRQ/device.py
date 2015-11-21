import duplexPort
import time
import os
import sys
import traceback

PI_NATIVE = os.uname()[4].startswith("arm") # TRUE if running on RPi
#HOSTNAME = socket.gethostname()
BASE_PATH = "/home/pi/nervebox_2/" if PI_NATIVE else "/home/stella/Dropbox/projects/current/nervebox_2/" 
COMMON_PATH = "%scommon/" % (BASE_PATH )

sys.path.append(COMMON_PATH)

import duplexPort

duplexPort.init(None)

volume = 0 # range 0-127
clock0 = 0 # range 1-127
clock1 = 0 # range 1-127
clock2 = 0 # range 1-127
externalClock = 0 # range 0-1
power = 0 # range 0-1

snare = 65535
bongo = 65535 
block = 65535
bass = 65535
brush = 65535

PAUSE_TIME = 0.5

FPGA_ON = 0
FPGA_OFF = 65535

BASS_BANG_MODULE_ID = 23
BLOCK_BANG_MODULE_ID = 22
BONGO_BANG_MODULE_ID = 21
BRUSH_BANG_MODULE_ID = 24
BRUSH_DAMPER_MODULE_ID = 25
SNARE_BANG_MODULE_ID = 20

BASS_DRONE_MODULE_ID = 14
BLOCK_DRONE_MODULE_ID = 13
BONGO_DRONE_MODULE_ID = 12
BRUSH_DRONE_MODULE_ID = 15
SNARE_DRONE_MODULE_ID = 11

CLOCK_MODULE_ID = 10
CLOCK_SOURCE_ID = 31
POWER_TOGGLE_MODULE_ID = 30
VOLUME_MODULE_ID = 40
BALANCE_MODULE_ID = 40

def sound_bass_bang(params):
    duplexPort.send(BASS_BANG_MODULE_ID,FPGA_ON)
    time.sleep(PAUSE_TIME)
    duplexPort.send(BASS_BANG_MODULE_ID,FPGA_OFF)
def sound_bass_pitch(params):
    global clock0, clock1, clock2
    clock = int(clock0 + clock1 + clock2/2)
    duplexPort.send(BASS_DRONE_MODULE_ID,clock) 
def sound_bass_off(params):
    duplexPort.send(BASS_DRONE_MODULE_ID,FPGA_OFF) 
    duplexPort.send(BASS_BANG_MODULE_ID,FPGA_OFF)
def sound_block_bang(params):
    duplexPort.send(BLOCK_BANG_MODULE_ID,FPGA_ON)
    time.sleep(PAUSE_TIME)
    duplexPort.send(BLOCK_BANG_MODULE_ID,FPGA_OFF)
def sound_block_pitch(params):
    global clock0, clock1, clock2
    clock = int(clock0 + clock1 + clock2/2)
    duplexPort.send(BLOCK_DRONE_MODULE_ID,clock) 
def sound_block_off(params):
    duplexPort.send(BLOCK_BANG_MODULE_ID,FPGA_OFF)
    duplexPort.send(BLOCK_DRONE_MODULE_ID,FPGA_OFF) 
def sound_bongo_bang(params):
    duplexPort.send(BONGO_BANG_MODULE_ID,FPGA_ON)
    time.sleep(PAUSE_TIME)
    duplexPort.send(BONGO_BANG_MODULE_ID,FPGA_OFF)
def sound_bongo_pitch(params):
    global clock0, clock1, clock2
    clock = int(clock0 + clock1 + clock2/2)
    duplexPort.send(BONGO_DRONE_MODULE_ID,clock) 
def sound_bongo_off(params):
    duplexPort.send(BONGO_DRONE_MODULE_ID,FPGA_OFF)
    duplexPort.send(BONGO_BANG_MODULE_ID,FPGA_OFF) 
def sound_brush_bang(params):
    duplexPort.send(BRUSH_DAMPER_MODULE_ID,FPGA_OFF)
    duplexPort.send(BRUSH_BANG_MODULE_ID,FPGA_ON)
    time.sleep(PAUSE_TIME)
    duplexPort.send(BRUSH_BANG_MODULE_ID,FPGA_OFF)
def sound_brush_pitch(params):
    global clock0, clock1, clock2
    clock = int(clock0 + clock1 + clock2/2)
    duplexPort.send(BRUSH_DRONE_MODULE_ID,clock) 
def sound_brush_off(params):
    duplexPort.send(BRUSH_DAMPER_MODULE_ID,FPGA_ON)
    duplexPort.send(BRUSH_DRONE_MODULE_ID,FPGA_OFF) 
def sound_snare_bang(params):
    duplexPort.send(SNARE_BANG_MODULE_ID,FPGA_ON)
    time.sleep(PAUSE_TIME)
    duplexPort.send(SNARE_BANG_MODULE_ID,FPGA_OFF)
def sound_snare_pitch(params):
    global clock0, clock1, clock2
    clock = int(clock0 + clock1 + clock2/2)
    duplexPort.send(SNARE_DRONE_MODULE_ID,clock) 
def sound_snare_off(params):
    duplexPort.send(SNARE_DRONE_MODULE_ID,FPGA_OFF) 
def system_clock_1_set(params):
    global clock0, clock1, clock2
    v = int(params["dynamics"]["amplitude"]*127) / 4
    clock0 = v << 11
    fpgaValue = int((clock0 + clock1 + clock2)/2)
    fpgaValue = fpgaValue if fpgaValue > 0 else fpgaValue +1 # what is this shit?
    print "fpgaValue",fpgaValue
    duplexPort.send(CLOCK_MODULE_ID,fpgaValue)
def system_clock_2_set(params):
    global clock0, clock1, clock2
    v = int(params["dynamics"]["amplitude"]*127) / 4
    clock1 = v << 6
    fpgaValue = int((clock0 + clock1 + clock2)/2)
    fpgaValue = fpgaValue if fpgaValue > 0 else fpgaValue +1 # what is this shit?
    print "fpgaValue",fpgaValue
    duplexPort.send(CLOCK_MODULE_ID,fpgaValue)
def system_clock_3_set(params):
    global clock0, clock1, clock2
    clock2 = int(params["dynamics"]["amplitude"]*127) / 2
    fpgaValue = int((clock0 + clock1 + clock2)/2)
    fpgaValue = fpgaValue if fpgaValue > 0 else fpgaValue +1 # what is this shit?
    print "fpgaValue",fpgaValue
    duplexPort.send(CLOCK_MODULE_ID,fpgaValue)
def system_clock_source_toggle(params):
    global externalClock
    externalClock = FPGA_ON if externalClock==FPGA_OFF else FPGA_OFF
    duplexPort.send(CLOCK_SOURCE_ID,externalClock)
def system_power_toggle(params):
    global power
    power = FPGA_ON if power==FPGA_OFF else FPGA_OFF
    duplexPort.send(POWER_TOGGLE_MODULE_ID,power)
def system_volume_set(params):
    global volume
    fpgaValue = int(params["dynamics"]["amplitude"]*100) << 9
    duplexPort.send(VOLUME_MODULE_ID,fpgaValue/2)
def system_balance_set(params):
    global volume
    fpgaValue = int(params["dynamics"]["amplitude"]*100) << 9
    duplexPort.send(BALANCE_MODULE_ID,fpgaValue/2)
def system_miditest_start(params):
    pass
def system_midipanic(params):
    pass
def ping(params):
    pass
def init():
    pass

def handleNOSC(nosc_d):
    #print nosc_d
    #print 'nosc_d["innerpath"]', nosc_d["innerpath"]
    try:
        pathToMethod_d[nosc_d["innerpath"]](nosc_d["params"])
    except Exception as e:
        traceback.print_exc()
        print "device: path not found", e
    #pathToMethod_d[nosc_d["innerpath"]](nosc_d["value"])


pathToMethod_d = {
    "/sound/bass/bang":sound_bass_bang,
    "/sound/bass/off":sound_bass_off,
    "/sound/bass/pitch":sound_bass_pitch,
    "/sound/block/bang":sound_block_bang,
    "/sound/block/off":sound_block_off,
    "/sound/block/pitch":sound_block_pitch,
    "/sound/bongo/bang":sound_bongo_bang,
    "/sound/bongo/off":sound_bongo_off,
    "/sound/bongo/pitch":sound_bongo_pitch,
    "/sound/brush/bang":sound_brush_bang,
    "/sound/brush/off":sound_brush_off,
    "/sound/brush/pitch":sound_brush_pitch,
    "/sound/snare/bang":sound_snare_bang,
    "/sound/snare/off":sound_snare_off,
    "/sound/snare/pitch":sound_snare_pitch,
    "/system/clock/1/set":system_clock_1_set,
    "/system/clock/2/set":system_clock_2_set,
    "/system/clock/3/set":system_clock_3_set,
    "/system/clock/source/toggle":system_clock_source_toggle,
    "/system/power/toggle":system_power_toggle,
    "/system/volume/set":system_volume_set,
    "/system/balance/set":system_balance_set,
    "/system/miditest":system_miditest_start,
    "/system/midipanic":system_midipanic,
    "/system/ping":ping,
    "/ping":ping,
}