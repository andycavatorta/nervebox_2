import mido
import time
import traceback

oNames = mido.get_output_names()

midi_out = mido.open_output(oNames[1])


# creating OSC endpoint methds

def sound_tom_1_bang(params):
    midi_out.send(mido.Message('note_on', note=48, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_tom_1_off(params):
    pass
def sound_tom_1_pitch(params):
    pass
def sound_tom_2_bang(params):
    midi_out.send(mido.Message('note_on', note=45, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_tom_2_off(params):
    pass
def sound_tom_2_pitch(params):
    pass
def sound_tom_3_bang(params):
    midi_out.send(mido.Message('note_on', note=41, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_tom_3_off(params):
    pass
def sound_tom_3_pitch(params):
    pass
def sound_tom_4_bang(params):
    midi_out.send(mido.Message('note_on', note=63, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_tom_4_off(params):
    pass
def sound_tom_4_pitch(params):
    pass
def sound_ride_bang(params):
    midi_out.send(mido.Message('note_on', note=51, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_ride_off(params):
    pass
def sound_ride_pitch(params):
    pass
def sound_crash_bang(params):
    midi_out.send(mido.Message('note_on', note=49, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_crash_off(params):
    pass
def sound_crash_pitch(params):
    pass
def sound_perc_1_bang(params):
    midi_out.send(mido.Message('note_on', note=65, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_perc_1_off(params):
    pass
def sound_perc_1_pitch(params):
    pass
def sound_perc_2_bang(params):
    midi_out.send(mido.Message('note_on', note=62, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_perc_2_off(params):
    pass
def sound_perc_2_pitch(params):
    pass
def sound_kick_bang(params):
    midi_out.send(mido.Message('note_on', note=35, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_kick_off(params):
    pass
def sound_kick_pitch(params):
    pass
def sound_snare_bang(params):
    midi_out.send(mido.Message('note_on', note=38, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_snare_off(params):
    pass
def sound_snare_pitch(params):
    pass
def sound_closed_hat_bang(params):
    midi_out.send(mido.Message('note_on', note=42, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_closed_hat_off(params):
    pass
def sound_closed_hat_pitch(params):
    pass
def sound_mid_hat_bang(params):
    midi_out.send(mido.Message('note_on', note=44, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_mid_hat_off(params):
    pass
def sound_mid_hat_pitch(params):
    pass
def sound_open_hat_bang(params):
    midi_out.send(mido.Message('note_on', note=46, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_open_hat_off(params):
    pass
def sound_open_hat_pitch(params):
    pass
def sound_claps_bang(params):
    midi_out.send(mido.Message('note_on', note=39, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_claps_off(params):
    pass
def sound_claps_pitch(params):
    pass
def sound_perc_3_bang(params):
    midi_out.send(mido.Message('note_on', note=67, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_perc_3_off(params):
    pass
def sound_perc_3_pitch(params):
    pass
def sound_perc_4_bang(params):
    midi_out.send(mido.Message('note_on', note=68, velocity=int(params["dynamics"]["amplitude"]*127)))
    pass
def sound_perc_4_off(params):
    pass
def sound_perc_4_pitch(params):
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
    for channel in range(16):
        for pitch in range(127):
            msg_midi = mido.Message('note_on')
            msg_midi.channel = 0
            msg_midi.note = pitch
            print msg_midi
            midi_out.send(msg_midi)
            time.sleep(0.1)

def system_miditest_stop(params):
    midi_out.panic()
    pass
def system_midipanic(params):
    pass

def ping(params):
    pass

def handleNOSC(nosc_d):
    print "handleNOSC",nosc_d
    #print 'nosc_d["innerpath"]', nosc_d["innerpath"]
    try:
        pathToMethod_d[nosc_d["innerpath"]](nosc_d["params"])
    except Exception as e:
        traceback.print_exc()
        print "device: path not found", e
    #pathToMethod_d[nosc_d["innerpath"]](nosc_d["value"])

def init():
    pass


pathToMethod_d = {
    "/HR16/sound/tom_1/bang":sound_tom_1_bang,
    "/HR16/sound/tom_1/off":sound_tom_1_off,
    "/HR16/sound/tom_1/pitch":sound_tom_1_pitch,
    "/HR16/sound/tom_2/bang":sound_tom_2_bang,
    "/HR16/sound/tom_2/off":sound_tom_2_off,
    "/HR16/sound/tom_2/pitch":sound_tom_2_pitch,
    "/HR16/sound/tom_3/bang":sound_tom_3_bang,
    "/HR16/sound/tom_3/off":sound_tom_3_off,
    "/HR16/sound/tom_3/pitch":sound_tom_3_pitch,
    "/HR16/sound/tom_4/bang":sound_tom_4_bang,
    "/HR16/sound/tom_4/off":sound_tom_4_off,
    "/HR16/sound/tom_4/pitch":sound_tom_4_pitch,
    "/HR16/sound/ride/bang":sound_ride_bang,
    "/HR16/sound/ride/off":sound_ride_off,
    "/HR16/sound/ride/pitch":sound_ride_pitch,
    "/HR16/sound/crash/bang":sound_crash_bang,
    "/HR16/sound/crash/off":sound_crash_off,
    "/HR16/sound/crash/pitch":sound_crash_pitch,
    "/HR16/sound/perc_1/bang":sound_perc_1_bang,
    "/HR16/sound/perc_1/off":sound_perc_1_off,
    "/HR16/sound/perc_1/pitch":sound_perc_1_pitch,
    "/HR16/sound/perc_2/bang":sound_perc_2_bang,
    "/HR16/sound/perc_2/off":sound_perc_2_off,
    "/HR16/sound/perc_2/pitch":sound_perc_2_pitch,
    "/HR16/sound/kick/bang":sound_kick_bang,
    "/HR16/sound/kick/off":sound_kick_off,
    "/HR16/sound/kick/pitch":sound_kick_pitch,
    "/HR16/sound/snare/bang":sound_snare_bang,
    "/HR16/sound/snare/off":sound_snare_off,
    "/HR16/sound/snare/pitch":sound_snare_pitch,
    "/HR16/sound/closed_hat/bang":sound_closed_hat_bang,
    "/HR16/sound/closed_hat/off":sound_closed_hat_off,
    "/HR16/sound/closed_hat/pitch":sound_closed_hat_pitch,
    "/HR16/sound/mid_hat/bang":sound_mid_hat_bang,
    "/HR16/sound/mid_hat/off":sound_mid_hat_off,
    "/HR16/sound/mid_hat/pitch":sound_mid_hat_pitch,
    "/HR16/sound/open_hat/bang":sound_open_hat_bang,
    "/HR16/sound/open_hat/off":sound_open_hat_off,
    "/HR16/sound/open_hat/pitch":sound_open_hat_pitch,
    "/HR16/sound/claps/bang":sound_claps_bang,
    "/HR16/sound/claps/off":sound_claps_off,
    "/HR16/sound/claps/pitch":sound_claps_pitch,
    "/HR16/sound/perc_3/bang":sound_perc_3_bang,
    "/HR16/sound/perc_3/off":sound_perc_3_off,
    "/HR16/sound/perc_3/pitch":sound_perc_3_pitch,
    "/HR16/sound/perc_4/bang":sound_perc_4_bang,
    "/HR16/sound/perc_4/off":sound_perc_4_off,
    "/HR16/sound/perc_4/pitch":sound_perc_4_pitch,
    "/HR16/system/power/on":system_power_on,
    "/HR16/system/power/off":system_power_off,
    "/HR16/system/clock/1":system_clock_1,
    "/HR16/system/clock/2":system_clock_2,
    "/HR16/system/clock/3":system_clock_3,
    "/HR16/system/clock/4":system_clock_4,
    "/HR16/system/miditest":system_miditest_start,
    "/HR16/system/midipanic":system_midipanic,
    "/HR16/system/ping":ping,
    "/HR16/system/ping/":ping,
    "/HR16/ping":ping,
    "/HR16/ping/":ping,
}