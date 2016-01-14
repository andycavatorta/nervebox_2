import mido
import time
import json
import traceback

oNames = mido.get_output_names()

midi_out = mido.open_output(oNames[1])


# creating OSC endpoint methds

def sound_0_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=40, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_1_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=41, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_2_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=42, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_3_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=43, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_4_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=44, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_5_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=45, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_6_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=46, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_7_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=47, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_8_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=48, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_9_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=49, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_10_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=50, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_11_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=51, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_12_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=52, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_13_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=53, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_14_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=54, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_15_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=55, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_16_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=56, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_17_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=57, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_18_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=58, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_19_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=59, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_20_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=60, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_21_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=61, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_22_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=62, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_23_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=63, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_24_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=64, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_25_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=65, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_26_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=66, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_27_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=67, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_28_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=68, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_29_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=69, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_30_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=70, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_31_bang(params):
    midi_out.send(mido.Message('note_on', channel = 9, note=71, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass

def sound_off(params):
    pass

def system_power_on(params):
    pass
def system_power_off(params):
    pass
def system_clock_1(params):
    pass
def system_clock_2(params):
    pass
def system_clock_3(params):
    pass
def system_clock_4(params):
    pass
def system_miditest_start(params):
    #for channel in range(16):
        for pitch in range(0,127):
            msg_midi = mido.Message('note_on')
            msg_midi.channel = 9
            msg_midi.note = pitch
            print msg_midi
            midi_out.send(msg_midi)
            time.sleep(4)

def system_miditest_stop(params):
    midi_out.panic()
    pass
def system_midipanic(params):
    pass

def ping(params):
    pass

def handleNOSC(nosc_d):
    try:
        pathToMethod_d[nosc_d["innerpath"]](nosc_d["params"])
    except Exception as e:
        traceback.print_exc()
        print "device: path not found", e

def init():
    pass


pathToMethod_d = {
    "/R8MKII/sound/0/bang":sound_0_bang,
    "/R8MKII/sound/1/bang":sound_1_bang,
    "/R8MKII/sound/2/bang":sound_2_bang,
    "/R8MKII/sound/3/bang":sound_3_bang,
    "/R8MKII/sound/4/bang":sound_4_bang,
    "/R8MKII/sound/5/bang":sound_5_bang,
    "/R8MKII/sound/6/bang":sound_6_bang,
    "/R8MKII/sound/7/bang":sound_7_bang,
    "/R8MKII/sound/8/bang":sound_8_bang,
    "/R8MKII/sound/9/bang":sound_9_bang,
    "/R8MKII/sound/10/bang":sound_10_bang,
    "/R8MKII/sound/11/bang":sound_11_bang,
    "/R8MKII/sound/12/bang":sound_12_bang,
    "/R8MKII/sound/13/bang":sound_13_bang,
    "/R8MKII/sound/14/bang":sound_14_bang,
    "/R8MKII/sound/15/bang":sound_15_bang,
    "/R8MKII/sound/16/bang":sound_16_bang,
    "/R8MKII/sound/17/bang":sound_17_bang,
    "/R8MKII/sound/18/bang":sound_18_bang,
    "/R8MKII/sound/19/bang":sound_19_bang,
    "/R8MKII/sound/20/bang":sound_20_bang,
    "/R8MKII/sound/21/bang":sound_21_bang,
    "/R8MKII/sound/22/bang":sound_22_bang,
    "/R8MKII/sound/23/bang":sound_23_bang,
    "/R8MKII/sound/24/bang":sound_24_bang,
    "/R8MKII/sound/25/bang":sound_25_bang,
    "/R8MKII/sound/26/bang":sound_26_bang,
    "/R8MKII/sound/27/bang":sound_27_bang,
    "/R8MKII/sound/28/bang":sound_28_bang,
    "/R8MKII/sound/29/bang":sound_29_bang,
    "/R8MKII/sound/30/bang":sound_30_bang,
    "/R8MKII/sound/31/bang":sound_31_bang,

    "/R8MKII/sound/0/off":sound_off,
    "/R8MKII/sound/1/off":sound_off,
    "/R8MKII/sound/2/off":sound_off,
    "/R8MKII/sound/3/off":sound_off,
    "/R8MKII/sound/4/off":sound_off,
    "/R8MKII/sound/5/off":sound_off,
    "/R8MKII/sound/6/off":sound_off,
    "/R8MKII/sound/7/off":sound_off,
    "/R8MKII/sound/8/off":sound_off,
    "/R8MKII/sound/9/off":sound_off,
    "/R8MKII/sound/10/off":sound_off,
    "/R8MKII/sound/11/off":sound_off,
    "/R8MKII/sound/12/off":sound_off,
    "/R8MKII/sound/13/off":sound_off,
    "/R8MKII/sound/14/off":sound_off,
    "/R8MKII/sound/15/off":sound_off,
    "/R8MKII/sound/16/off":sound_off,
    "/R8MKII/sound/17/off":sound_off,
    "/R8MKII/sound/18/off":sound_off,
    "/R8MKII/sound/19/off":sound_off,
    "/R8MKII/sound/20/off":sound_off,
    "/R8MKII/sound/21/off":sound_off,
    "/R8MKII/sound/22/off":sound_off,
    "/R8MKII/sound/23/off":sound_off,
    "/R8MKII/sound/24/off":sound_off,
    "/R8MKII/sound/25/off":sound_off,
    "/R8MKII/sound/26/off":sound_off,
    "/R8MKII/sound/27/off":sound_off,
    "/R8MKII/sound/28/off":sound_off,
    "/R8MKII/sound/29/off":sound_off,
    "/R8MKII/sound/30/off":sound_off,
    "/R8MKII/sound/31/off":sound_off,

    "/system/power/on/":system_power_on,
    "/system/power/off":system_power_off,
    "/system/clock/1/":system_clock_1,
    "/system/clock/2/":system_clock_2,
    "/system/clock/3/":system_clock_3,
    "/system/clock/4/":system_clock_4,
    "/system/miditest":system_miditest_start,
    "/system/midipanic":system_midipanic,
    "/system/ping":ping,
    "/system/ping/":ping,
    "/ping":ping,
    "/ping/":ping,
}


pathToMethod_d = {
    "/R8MKII/sound/0/bang":sound_0_bang,
    "/R8MKII/sound/1/bang":sound_1_bang,
    "/R8MKII/sound/2/bang":sound_2_bang,
    "/R8MKII/sound/3/bang":sound_3_bang,
    "/R8MKII/sound/4/bang":sound_4_bang,
    "/R8MKII/sound/5/bang":sound_5_bang,
    "/R8MKII/sound/6/bang":sound_6_bang,
    "/R8MKII/sound/7/bang":sound_7_bang,
    "/R8MKII/sound/8/bang":sound_8_bang,
    "/R8MKII/sound/9/bang":sound_9_bang,
    "/R8MKII/sound/10/bang":sound_10_bang,
    "/R8MKII/sound/11/bang":sound_11_bang,
    "/R8MKII/sound/12/bang":sound_12_bang,
    "/R8MKII/sound/13/bang":sound_13_bang,
    "/R8MKII/sound/14/bang":sound_14_bang,
    "/R8MKII/sound/15/bang":sound_15_bang,
    "/R8MKII/sound/16/bang":sound_16_bang,
    "/R8MKII/sound/17/bang":sound_17_bang,
    "/R8MKII/sound/18/bang":sound_18_bang,
    "/R8MKII/sound/19/bang":sound_19_bang,
    "/R8MKII/sound/20/bang":sound_20_bang,
    "/R8MKII/sound/21/bang":sound_21_bang,
    "/R8MKII/sound/22/bang":sound_22_bang,
    "/R8MKII/sound/23/bang":sound_23_bang,
    "/R8MKII/sound/24/bang":sound_24_bang,
    "/R8MKII/sound/25/bang":sound_25_bang,
    "/R8MKII/sound/26/bang":sound_26_bang,
    "/R8MKII/sound/27/bang":sound_27_bang,
    "/R8MKII/sound/28/bang":sound_28_bang,
    "/R8MKII/sound/29/bang":sound_29_bang,
    "/R8MKII/sound/30/bang":sound_30_bang,
    "/R8MKII/sound/31/bang":sound_31_bang,

    "/R8MKII/sound/0/off":sound_off,
    "/R8MKII/sound/1/off":sound_off,
    "/R8MKII/sound/2/off":sound_off,
    "/R8MKII/sound/3/off":sound_off,
    "/R8MKII/sound/4/off":sound_off,
    "/R8MKII/sound/5/off":sound_off,
    "/R8MKII/sound/6/off":sound_off,
    "/R8MKII/sound/7/off":sound_off,
    "/R8MKII/sound/8/off":sound_off,
    "/R8MKII/sound/9/off":sound_off,
    "/R8MKII/sound/10/off":sound_off,
    "/R8MKII/sound/11/off":sound_off,
    "/R8MKII/sound/12/off":sound_off,
    "/R8MKII/sound/13/off":sound_off,
    "/R8MKII/sound/14/off":sound_off,
    "/R8MKII/sound/15/off":sound_off,
    "/R8MKII/sound/16/off":sound_off,
    "/R8MKII/sound/17/off":sound_off,
    "/R8MKII/sound/18/off":sound_off,
    "/R8MKII/sound/19/off":sound_off,
    "/R8MKII/sound/20/off":sound_off,
    "/R8MKII/sound/21/off":sound_off,
    "/R8MKII/sound/22/off":sound_off,
    "/R8MKII/sound/23/off":sound_off,
    "/R8MKII/sound/24/off":sound_off,
    "/R8MKII/sound/25/off":sound_off,
    "/R8MKII/sound/26/off":sound_off,
    "/R8MKII/sound/27/off":sound_off,
    "/R8MKII/sound/28/off":sound_off,
    "/R8MKII/sound/29/off":sound_off,
    "/R8MKII/sound/30/off":sound_off,
    "/R8MKII/sound/31/off":sound_off,

    "/R8MKII/system/power/on/":system_power_on,
    "/R8MKII/system/power/off":system_power_off,
    "/R8MKII/system/clock/1/":system_clock_1,
    "/R8MKII/system/clock/2/":system_clock_2,
    "/R8MKII/system/clock/3/":system_clock_3,
    "/R8MKII/system/clock/4/":system_clock_4,
    "/R8MKII/system/miditest":system_miditest_start,
    "/R8MKII/system/midipanic":system_midipanic,
    "/R8MKII/system/ping":ping,
    "/R8MKII/system/ping/":ping,
    "/R8MKII/ping":ping,
    "/R8MKII/ping/":ping,
}