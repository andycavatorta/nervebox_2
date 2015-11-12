import mido
import time

oNames = mido.get_output_names()

midi_out = mido.open_output(oNames[1])


# creating OSC endpoint methds

def sound_tom_1_bang(value):
    pass
def sound_tom_1_off(value):
    pass
def sound_tom_1_pitch(value):
    pass
def sound_tom_2_bang(value):
    pass
def sound_tom_2_off(value):
    pass
def sound_tom_2_pitch(value):
    pass
def sound_tom_3_bang(value):
    pass
def sound_tom_3_off(value):
    pass
def sound_tom_3_pitch(value):
    pass
def sound_tom_4_bang(value):
    pass
def sound_tom_4_off(value):
    pass
def sound_tom_4_pitch(value):
    pass
def sound_ride_bang(value):
    pass
def sound_ride_off(value):
    pass
def sound_ride_pitch(value):
    pass
def sound_crash_bang(value):
    pass
def sound_crash_off(value):
    pass
def sound_crash_pitch(value):
    pass
def sound_perc_1_bang(value):
    pass
def sound_perc_1_off(value):
    pass
def sound_perc_1_pitch(value):
    pass
def sound_perc_2_bang(value):
    pass
def sound_perc_2_off(value):
    pass
def sound_perc_2_pitch(value):
    pass
def sound_kick_bang(value):
    pass
def sound_kick_off(value):
    pass
def sound_kick_pitch(value):
    pass
def sound_snare_bang(value):
    pass
def sound_snare_off(value):
    pass
def sound_snare_pitch(value):
    pass
def sound_closed_hat_bang(value):
    pass
def sound_closed_hat_off(value):
    pass
def sound_closed_hat_pitch(value):
    pass
def sound_mid_hat_bang(value):
    pass
def sound_mid_hat_off(value):
    pass
def sound_mid_hat_pitch(value):
    pass
def sound_open_hat_bang(value):
    pass
def sound_open_hat_off(value):
    pass
def sound_open_hat_pitch(value):
    pass
def sound_claps_bang(value):
    pass
def sound_claps_off(value):
    pass
def sound_claps_pitch(value):
    pass
def sound_perc_3_bang(value):
    pass
def sound_perc_3_off(value):
    pass
def sound_perc_3_pitch(value):
    pass
def sound_perc_4_bang(value):
    pass
def sound_perc_4_off(value):
    pass
def sound_perc_4_pitch(value):
    pass



def system_power_on(value):
    pass
def system_power_off(value):
    pass
def system_clock_1(value):
    pass
def system_clock_2(value):
    pass
def system_clock_3(value):
    pass
def system_clock_4(value):
    pass
def system_miditest_start(value):
    print "system_miditest_start", value
    for channel in range(16):
        for pitch in range(30, 70):
            msg_midi = mido.Message('note_on')
            msg_midi.channel = 0
            msg_midi.note = pitch
            print msg_midi
            midi_out.send(msg_midi)
            time.sleep(1)

def system_miditest_stop(value):
    midi_out.panic()
    pass
def system_midipanic(value):
    pass


def handleNOSC(nosc_d):
    print nosc_d

    pathToMethod_d = {

        "/sound/tom_1/bang":sound_tom_1_bang,
        "/sound/tom_1/off":sound_tom_1_off,
        "/sound/tom_1/pitch":sound_tom_1_pitch,
        "/sound/tom_2/bang":sound_tom_2_bang,
        "/sound/tom_2/off":sound_tom_2_off,
        "/sound/tom_2/pitch":sound_tom_2_pitch,
        "/sound/tom_3/bang":sound_tom_3_bang,
        "/sound/tom_3/off":sound_tom_3_off,
        "/sound/tom_3/pitch":sound_tom_3_pitch,
        "/sound/tom_4/bang":sound_tom_4_bang,
        "/sound/tom_4/off":sound_tom_4_off,
        "/sound/tom_4/pitch":sound_tom_4_pitch,
        "/sound/ride/bang":sound_ride_bang,
        "/sound/ride/off":sound_ride_off,
        "/sound/ride/pitch":sound_ride_pitch,
        "/sound/crash/bang":sound_crash_bang,
        "/sound/crash/off":sound_crash_off,
        "/sound/crash/pitch":sound_crash_pitch,
        "/sound/perc_1/bang":sound_perc_1_bang,
        "/sound/perc_1/off":sound_perc_1_off,
        "/sound/perc_1/pitch":sound_perc_1_pitch,
        "/sound/perc_2/bang":sound_perc_2_bang,
        "/sound/perc_2/off":sound_perc_2_off,
        "/sound/perc_2/pitch":sound_perc_2_pitch,
        "/sound/kick/bang":sound_kick_bang,
        "/sound/kick/off":sound_kick_off,
        "/sound/kick/pitch":sound_kick_pitch,
        "/sound/snare/bang":sound_snare_bang,
        "/sound/snare/off":sound_snare_off,
        "/sound/snare/pitch":sound_snare_pitch,
        "/sound/closed_hat/bang":sound_closed_hat_bang,
        "/sound/closed_hat/off":sound_closed_hat_off,
        "/sound/closed_hat/pitch":sound_closed_hat_pitch,
        "/sound/mid_hat/bang":sound_mid_hat_bang,
        "/sound/mid_hat/off":sound_mid_hat_off,
        "/sound/mid_hat/pitch":sound_mid_hat_pitch,
        "/sound/open_hat/bang":sound_open_hat_bang,
        "/sound/open_hat/off":sound_open_hat_off,
        "/sound/open_hat/pitch":sound_open_hat_pitch,
        "/sound/claps/bang":sound_claps_bang,
        "/sound/claps/off":sound_claps_off,
        "/sound/claps/pitch":sound_claps_pitch,
        "/sound/perc_3/bang":sound_perc_3_bang,
        "/sound/perc_3/off":sound_perc_3_off,
        "/sound/perc_3/pitch":sound_perc_3_pitch,
        "/sound/perc_4/bang":sound_perc_4_bang,
        "/sound/perc_4/off":sound_perc_4_off,
        "/sound/perc_4/pitch":sound_perc_4_pitch,
        "/system/power/on":system_power_on,
        "/system/power/off":system_power_off,
        "/system/clock/1":system_clock_1,
        "/system/clock/2":system_clock_2,
        "/system/clock/3":system_clock_3,
        "/system/clock/4":system_clock_4,
        "/system/miditest":system_miditest_start,
        "/system/midipanic":system_midipanic,
    }
    print 'nosc_d["innerpath"]', nosc_d["innerpath"]
    pathToMethod_d[nosc_d["innerpath"]](nosc_d["value"])

def init():
    pass

