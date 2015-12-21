import rtmidi_python as rtmidi

def callback(message, time_stamp):
    print message, time_stamp

midi_in = rtmidi.MidiIn()
midi_in.callback = callback
midi_in.open_port(0)