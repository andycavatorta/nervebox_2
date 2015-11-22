import mido
import time
import json
import traceback

oNames = mido.get_output_names()

midi_out = mido.open_output(oNames[1])


# creating OSC endpoint methds

def sound_0_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=66, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_1_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=67, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_2_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=68, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_3_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=69, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_4_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=70, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_5_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=71, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_6_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=72, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_7_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=73, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_8_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=74, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_9_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=75, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_10_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=76, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_11_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=77, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_12_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=78, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_13_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=79, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_14_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=80, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_15_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=81, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_16_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=82, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_17_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=83, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_18_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=84, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_19_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=85, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_20_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=86, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_21_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=87, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_22_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=88, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_23_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=89, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_24_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=90, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_25_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=91, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_26_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=92, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_27_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=93, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_28_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=94, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_29_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=95, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_30_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=96, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_31_bang(params):
    midi_out.send(mido.Message('note_on', channel = 0, note=97, velocity=int(params["dynamics"]["amplitude"]*127)))
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
    "/sound/0/bang":sound_0_bang,
    "/sound/1/bang":sound_1_bang,
    "/sound/2/bang":sound_2_bang,
    "/sound/3/bang":sound_3_bang,
    "/sound/4/bang":sound_4_bang,
    "/sound/5/bang":sound_5_bang,
    "/sound/6/bang":sound_6_bang,
    "/sound/7/bang":sound_7_bang,
    "/sound/8/bang":sound_8_bang,
    "/sound/9/bang":sound_9_bang,
    "/sound/10/bang":sound_10_bang,
    "/sound/11/bang":sound_11_bang,
    "/sound/12/bang":sound_12_bang,
    "/sound/13/bang":sound_13_bang,
    "/sound/14/bang":sound_14_bang,
    "/sound/15/bang":sound_15_bang,
    "/sound/16/bang":sound_16_bang,
    "/sound/17/bang":sound_17_bang,
    "/sound/18/bang":sound_18_bang,
    "/sound/19/bang":sound_19_bang,
    "/sound/20/bang":sound_20_bang,
    "/sound/21/bang":sound_21_bang,
    "/sound/22/bang":sound_22_bang,
    "/sound/23/bang":sound_23_bang,
    "/sound/24/bang":sound_24_bang,
    "/sound/25/bang":sound_25_bang,
    "/sound/26/bang":sound_26_bang,
    "/sound/27/bang":sound_27_bang,
    "/sound/28/bang":sound_28_bang,
    "/sound/29/bang":sound_29_bang,
    "/sound/30/bang":sound_30_bang,
    "/sound/31/bang":sound_31_bang,

    "/sound/0/off":sound_off,
    "/sound/1/off":sound_off,
    "/sound/2/off":sound_off,
    "/sound/3/off":sound_off,
    "/sound/4/off":sound_off,
    "/sound/5/off":sound_off,
    "/sound/6/off":sound_off,
    "/sound/7/off":sound_off,
    "/sound/8/off":sound_off,
    "/sound/9/off":sound_off,
    "/sound/10/off":sound_off,
    "/sound/11/off":sound_off,
    "/sound/12/off":sound_off,
    "/sound/13/off":sound_off,
    "/sound/14/off":sound_off,
    "/sound/15/off":sound_off,
    "/sound/16/off":sound_off,
    "/sound/17/off":sound_off,
    "/sound/18/off":sound_off,
    "/sound/19/off":sound_off,
    "/sound/20/off":sound_off,
    "/sound/21/off":sound_off,
    "/sound/22/off":sound_off,
    "/sound/23/off":sound_off,
    "/sound/24/off":sound_off,
    "/sound/25/off":sound_off,
    "/sound/26/off":sound_off,
    "/sound/27/off":sound_off,
    "/sound/28/off":sound_off,
    "/sound/29/off":sound_off,
    "/sound/30/off":sound_off,
    "/sound/31/off":sound_off,

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
    "/sound/0/bang":sound_0_bang,
    "/sound/1/bang":sound_1_bang,
    "/sound/2/bang":sound_2_bang,
    "/sound/3/bang":sound_3_bang,
    "/sound/4/bang":sound_4_bang,
    "/sound/5/bang":sound_5_bang,
    "/sound/6/bang":sound_6_bang,
    "/sound/7/bang":sound_7_bang,
    "/sound/8/bang":sound_8_bang,
    "/sound/9/bang":sound_9_bang,
    "/sound/10/bang":sound_10_bang,
    "/sound/11/bang":sound_11_bang,
    "/sound/12/bang":sound_12_bang,
    "/sound/13/bang":sound_13_bang,
    "/sound/14/bang":sound_14_bang,
    "/sound/15/bang":sound_15_bang,
    "/sound/16/bang":sound_16_bang,
    "/sound/17/bang":sound_17_bang,
    "/sound/18/bang":sound_18_bang,
    "/sound/19/bang":sound_19_bang,
    "/sound/20/bang":sound_20_bang,
    "/sound/21/bang":sound_21_bang,
    "/sound/22/bang":sound_22_bang,
    "/sound/23/bang":sound_23_bang,
    "/sound/24/bang":sound_24_bang,
    "/sound/25/bang":sound_25_bang,
    "/sound/26/bang":sound_26_bang,
    "/sound/27/bang":sound_27_bang,
    "/sound/28/bang":sound_28_bang,
    "/sound/29/bang":sound_29_bang,
    "/sound/30/bang":sound_30_bang,
    "/sound/31/bang":sound_31_bang,

    "/sound/0/off":sound_off,
    "/sound/1/off":sound_off,
    "/sound/2/off":sound_off,
    "/sound/3/off":sound_off,
    "/sound/4/off":sound_off,
    "/sound/5/off":sound_off,
    "/sound/6/off":sound_off,
    "/sound/7/off":sound_off,
    "/sound/8/off":sound_off,
    "/sound/9/off":sound_off,
    "/sound/10/off":sound_off,
    "/sound/11/off":sound_off,
    "/sound/12/off":sound_off,
    "/sound/13/off":sound_off,
    "/sound/14/off":sound_off,
    "/sound/15/off":sound_off,
    "/sound/16/off":sound_off,
    "/sound/17/off":sound_off,
    "/sound/18/off":sound_off,
    "/sound/19/off":sound_off,
    "/sound/20/off":sound_off,
    "/sound/21/off":sound_off,
    "/sound/22/off":sound_off,
    "/sound/23/off":sound_off,
    "/sound/24/off":sound_off,
    "/sound/25/off":sound_off,
    "/sound/26/off":sound_off,
    "/sound/27/off":sound_off,
    "/sound/28/off":sound_off,
    "/sound/29/off":sound_off,
    "/sound/30/off":sound_off,
    "/sound/31/off":sound_off,

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