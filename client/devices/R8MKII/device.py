import mido
import time
import json
import traceback

oNames = mido.get_output_names()

midi_out = mido.open_output(oNames[1])


# creating OSC endpoint methds

def sound_low_conga_accent(params):
    pass
def sound_low_conga_bang(params):
    midi_out.send(mido.Message('note_on', note=63, velocity=int(params["dynamics"]["amplitude"]*127)))
def sound_low_conga_off(params):
    pass
def sound_low_conga_pitch(params):
    pass
def sound_hi_conga_accent(params):
    pass
def sound_hi_conga_bang(params):
    midi_out.send(mido.Message('note_on', note=62, velocity=int(params["dynamics"]["amplitude"]*127)))
def sound_hi_conga_off(params):
    pass
def sound_hi_conga_pitch(params):
    pass
def sound_timbale_accent(params):
    pass
def sound_timbale_bang(params):
    midi_out.send(mido.Message('note_on', note=65, velocity=int(params["dynamics"]["amplitude"]*127)))
def sound_timbale_off(params):
    pass
def sound_timbale_pitch(params):
    pass
def sound_low_cowbell_accent(params):
    pass
def sound_low_cowbell_bang(params):
    midi_out.send(mido.Message('note_on', note=68, velocity=int(params["dynamics"]["amplitude"]*127)))
def sound_low_cowbell_off(params):
    pass
def sound_low_cowbell_pitch(params):
    pass
def sound_hi_cowbell_accent(params):
    pass
def sound_hi_cowbell_bang(params):
    midi_out.send(mido.Message('note_on', note=67, velocity=int(params["dynamics"]["amplitude"]*127)))
def sound_hi_cowbell_off(params):
    pass
def sound_hi_cowbell_pitch(params):
    pass
def sound_hand_clap_accent(params):
    pass
def sound_hand_clap_bang(params):
    midi_out.send(mido.Message('note_on', note=39, velocity=int(params["dynamics"]["amplitude"]*127)))
def sound_hand_clap_off(params):
    pass
def sound_hand_clap_pitch(params):
    pass
def sound_crash_cymbal_accent(params):
    pass
def sound_crash_cymbal_bang(params):
    midi_out.send(mido.Message('note_on', note=49, velocity=int(params["dynamics"]["amplitude"]*127)))
def sound_crash_cymbal_off(params):
    pass
def sound_crash_cymbal_pitch(params):
    pass
def sound_ride_cymbal_accent(params):
    pass
def sound_ride_cymbal_bang(params):
    midi_out.send(mido.Message('note_on', note=51, velocity=int(params["dynamics"]["amplitude"]*127)))
def sound_ride_cymbal_off(params):
    pass
def sound_ride_cymbal_pitch(params):
    pass
def sound_bass_drum_accent(params):
    pass
def sound_bass_drum_bang(params):
    midi_out.send(mido.Message('note_on', note=35, velocity=int(params["dynamics"]["amplitude"]*127)))
def sound_bass_drum_off(params):
    pass
def sound_bass_drum_pitch(params):
    pass
def sound_snare_drum_accent(params):
    pass
def sound_snare_drum_bang(params):
    midi_out.send(mido.Message('note_on', note=38, velocity=int(params["dynamics"]["amplitude"]*127)))
def sound_snare_drum_off(params):
    pass
def sound_snare_drum_pitch(params):
    pass
def sound_low_tom_accent(params):
    pass
def sound_low_tom_bang(params):
    midi_out.send(mido.Message('note_on', note=41, velocity=int(params["dynamics"]["amplitude"]*127)))
def sound_low_tom_off(params):
    pass
def sound_low_tom_pitch(params):
    pass
def sound_mid_tom_accent(params):
    pass
def sound_mid_tom_bang(params):
    midi_out.send(mido.Message('note_on', note=45, velocity=int(params["dynamics"]["amplitude"]*127)))
def sound_mid_tom_off(params):
    pass
def sound_mid_tom_pitch(params):
    pass
def sound_hi_tom_accent(params):
    pass
def sound_hi_tom_bang(params):
    midi_out.send(mido.Message('note_on', note=48, velocity=int(params["dynamics"]["amplitude"]*127)))
def sound_hi_tom_off(params):
    pass
def sound_hi_tom_pitch(params):
    pass
def sound_rim_shot_accent(params):
    pass
def sound_rim_shot_bang(params):
    midi_out.send(mido.Message('note_on', note=37, velocity=int(params["dynamics"]["amplitude"]*127)))
def sound_rim_shot_off(params):
    pass
def sound_rim_shot_pitch(params):
    pass
def sound_closed_hi_hat_accent(params):
    pass
def sound_closed_hi_hat_bang(params):
    # open hi-hat is note 46.  how to control open/close?
    midi_out.send(mido.Message('note_on', note=42, velocity=int(params["dynamics"]["amplitude"]*127)))
def sound_closed_hi_hat_off(params):
    pass
def sound_closed_hi_hat_pitch(params):
    pass
def sound_open_hi_hat_accent(params):
    pass
def sound_open_hi_hat_bang(params):
    midi_out.send(mido.Message('note_on', note=46, velocity=int(params["dynamics"]["amplitude"]*127)))
def sound_open_hi_hat_off(params):
    pass
def sound_open_hi_hat_pitch(params):
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
            time.sleep(1)

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