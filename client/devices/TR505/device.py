
print "device imported"



# creating OSC endpoint methds

def sound_low_conga_accent(value):
    pass
def sound_low_conga_bang(value):
    pass
def sound_low_conga_off(value):
    pass
def sound_low_conga_pitch(value):
    pass
def sound_hi_conga_accent(value):
    pass
def sound_hi_conga_bang(value):
    pass
def sound_hi_conga_off(value):
    pass
def sound_hi_conga_pitch(value):
    pass
def sound_timbale_accent(value):
    pass
def sound_timbale_bang(value):
    pass
def sound_timbale_off(value):
    pass
def sound_timbale_pitch(value):
    pass
def sound_low_cowbell_accent(value):
    pass
def sound_low_cowbell_bang(value):
    pass
def sound_low_cowbell_off(value):
    pass
def sound_low_cowbell_pitch(value):
    pass
def sound_hi_cowbell_accent(value):
    pass
def sound_hi_cowbell_bang(value):
    pass
def sound_hi_cowbell_off(value):
    pass
def sound_hi_cowbell_pitch(value):
    pass
def sound_hand_clap_accent(value):
    pass
def sound_hand_clap_bang(value):
    pass
def sound_hand_clap_off(value):
    pass
def sound_hand_clap_pitch(value):
    pass
def sound_crash_cymbal_accent(value):
    pass
def sound_crash_cymbal_bang(value):
    pass
def sound_crash_cymbal_off(value):
    pass
def sound_crash_cymbal_pitch(value):
    pass
def sound_ride_cymbal_accent(value):
    pass
def sound_ride_cymbal_bang(value):
    pass
def sound_ride_cymbal_off(value):
    pass
def sound_ride_cymbal_pitch(value):
    pass
def sound_bass_drum_accent(value):
    pass
def sound_bass_drum_bang(value):
    pass
def sound_bass_drum_off(value):
    pass
def sound_bass_drum_pitch(value):
    pass
def sound_snare_drum_accent(value):
    pass
def sound_snare_drum_bang(value):
    pass
def sound_snare_drum_off(value):
    pass
def sound_snare_drum_pitch(value):
    pass
def sound_low_tom_accent(value):
    pass
def sound_low_tom_bang(value):
    pass
def sound_low_tom_off(value):
    pass
def sound_low_tom_pitch(value):
    pass
def sound_mid_tom_accent(value):
    pass
def sound_mid_tom_bang(value):
    pass
def sound_mid_tom_off(value):
    pass
def sound_mid_tom_pitch(value):
    pass
def sound_hi_tom_accent(value):
    pass
def sound_hi_tom_bang(value):
    pass
def sound_hi_tom_off(value):
    pass
def sound_hi_tom_pitch(value):
    pass
def sound_rim_shot_accent(value):
    pass
def sound_rim_shot_bang(value):
    pass
def sound_rim_shot_off(value):
    pass
def sound_rim_shot_pitch(value):
    pass
def sound_closed_hi_hat_accent(value):
    pass
def sound_closed_hi_hat_bang(value):
    pass
def sound_closed_hi_hat_off(value):
    pass
def sound_closed_hi_hat_pitch(value):
    pass
def sound_open_hi_hat_accent(value):
    pass
def sound_open_hi_hat_bang(value):
    pass
def sound_open_hi_hat_off(value):
    pass
def sound_open_hi_hat_pitch(value):
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
    pass
def system_miditest_stop(value):
    pass
def system_midipanic(value):
    pass


def handleNOSC(nosc_d):
    print nosc_d

    pathToMethod_d = {
        "/sound/low_conga/accent/":sound_low_conga_accent,
        "/sound/low_conga/bang/":sound_low_conga_bang,
        "/sound/low_conga/off/":sound_low_conga_off,
        "/sound/low_conga/pitch/@":sound_low_conga_pitch,
        "/sound/hi_conga/accent/":sound_hi_conga_accent,
        "/sound/hi_conga/bang/":sound_hi_conga_bang,
        "/sound/hi_conga/off/":sound_hi_conga_off,
        "/sound/hi_conga/pitch/@":sound_hi_conga_pitch,
        "/sound/timbale/accent/":sound_timbale_accent,
        "/sound/timbale/bang/":sound_timbale_bang,
        "/sound/timbale/off/":sound_timbale_off,
        "/sound/timbale/pitch/@":sound_timbale_pitch,
        "/sound/low_cowbell/accent/":sound_low_cowbell_accent,
        "/sound/low_cowbell/bang/":sound_low_cowbell_bang,
        "/sound/low_cowbell/off/":sound_low_cowbell_off,
        "/sound/low_cowbell/pitch/@":sound_low_cowbell_pitch,
        "/sound/hi_cowbell/accent/":sound_hi_cowbell_accent,
        "/sound/hi_cowbell/bang/":sound_hi_cowbell_bang,
        "/sound/hi_cowbell/off/":sound_hi_cowbell_off,
        "/sound/hi_cowbell/pitch/@":sound_hi_cowbell_pitch,
        "/sound/hand_clap/accent/":sound_hand_clap_accent,
        "/sound/hand_clap/bang/":sound_hand_clap_bang,
        "/sound/hand_clap/off/":sound_hand_clap_off,
        "/sound/hand_clap/pitch/@":sound_hand_clap_pitch,
        "/sound/crash_cymbal/accent/":sound_crash_cymbal_accent,
        "/sound/crash_cymbal/bang/":sound_crash_cymbal_bang,
        "/sound/crash_cymbal/off/":sound_crash_cymbal_off,
        "/sound/crash_cymbal/pitch/@":sound_crash_cymbal_pitch,
        "/sound/ride_cymbal/accent/":sound_ride_cymbal_accent,
        "/sound/ride_cymbal/bang/":sound_ride_cymbal_bang,
        "/sound/ride_cymbal/off/":sound_ride_cymbal_off,
        "/sound/ride_cymbal/pitch/@":sound_ride_cymbal_pitch,
        "/sound/bass_drum/accent/":sound_bass_drum_accent,
        "/sound/bass_drum/bang/":sound_bass_drum_bang,
        "/sound/bass_drum/off/":sound_bass_drum_off,
        "/sound/bass_drum/pitch/@":sound_bass_drum_pitch,
        "/sound/snare_drum/accent/":sound_snare_drum_accent,
        "/sound/snare_drum/bang/":sound_snare_drum_bang,
        "/sound/snare_drum/off/":sound_snare_drum_off,
        "/sound/snare_drum/pitch/@":sound_snare_drum_pitch,
        "/sound/low_tom/accent/":sound_low_tom_accent,
        "/sound/low_tom/bang/":sound_low_tom_bang,
        "/sound/low_tom/off/":sound_low_tom_off,
        "/sound/low_tom/pitch/@":sound_low_tom_pitch,
        "/sound/mid_tom/accent/":sound_mid_tom_accent,
        "/sound/mid_tom/bang/":sound_mid_tom_bang,
        "/sound/mid_tom/off/":sound_mid_tom_off,
        "/sound/mid_tom/pitch/@":sound_mid_tom_pitch,
        "/sound/hi_tom/accent/":sound_hi_tom_accent,
        "/sound/hi_tom/bang/":sound_hi_tom_bang,
        "/sound/hi_tom/off/":sound_hi_tom_off,
        "/sound/hi_tom/pitch/@":sound_hi_tom_pitch,
        "/sound/rim_shot/accent/":sound_rim_shot_accent,
        "/sound/rim_shot/bang/":sound_rim_shot_bang,
        "/sound/rim_shot/off/":sound_rim_shot_off,
        "/sound/rim_shot/pitch/@":sound_rim_shot_pitch,
        "/sound/closed_hi-hat/accent/":sound_closed_hi_hat_accent,
        "/sound/closed_hi-hat/bang/":sound_closed_hi_hat_bang,
        "/sound/closed_hi-hat/off/":sound_closed_hi_hat_off,
        "/sound/closed_hi-hat/pitch/@":sound_closed_hi_hat_pitch,
        "/sound/open_hi-hat/accent/":sound_open_hi_hat_accent,
        "/sound/open_hi-hat/bang/":sound_open_hi_hat_bang,
        "/sound/open_hi-hat/off/":sound_open_hi_hat_off,
        "/sound/open_hi-hat/pitch/@":sound_open_hi_hat_pitch,
        "/system/power/on/":system_power_on,
        "/system/power/off/":system_power_off,
        "/system/clock/1/":system_clock_1,
        "/system/clock/2/":system_clock_2,
        "/system/clock/3/":system_clock_3,
        "/system/clock/4/":system_clock_4,
        "/system/miditest/start/":system_miditest_start,
        "/system/miditest/stop/":system_miditest_stop,
        "/system/midipanic/":system_midipanic,
    }

def init():
    pass

