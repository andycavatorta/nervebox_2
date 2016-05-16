"""
what top-level interfaces are needed by all devices?

anything other than [a]sync [in|out]put?

"""


import time
import mido


def system_clock_set(path, value):  #setClockOscillator
	return None
def system_balance_set(path, value):  #setBalance
	return None
def system_intExt_set(path, value):  #toggleExternalClock
	return None
def system_power_set(path, value):  #togglePower
	return None
def system_volume_set(path, value):  #setVolume
	return None
def instrument_snare_trigger(path, value):  #triggerSnare
	return None
def instrument_snare_pitch(path, value):  #droneSnare
	return None
def instrument_bongo_trigger(path, value):  #triggerBongo
	return None
def instrument_bongo_pitch(path, value):  #droneBongo
	return None
def instrument_block_trigger(path, value):  #triggerBlock
	return None
def instrument_bass_trigger(path, value):  #triggerBassss)
	return None
def instrument_bass_pitch(path, value):  #droneBrush
	return None
def instrument_brush_trigger(path, value):  #triggerBrush
	return None
def instrument_brush_pitch(path, value):  #droneBlock	
	return None

def syncRouter(path, value):
	pathToMethod_d = {
		"system/clock/set":system_clock_set,
		"system/balance/set":system_balance_set,
		"system/intExt/set":system_intExt_set,
		"system/power/set":system_power_set,
		"system/volume/set":system_volume_set,
		"instrument/snare/trigger":instrument_snare_trigger,
		"instrument/snare/pitch":instrument_snare_pitch,
		"instrument/bongo/trigger":instrument_bongo_trigger,
		"instrument/bongo/pitch":instrument_bongo_pitch,
		"instrument/block/trigger":instrument_block_trigger,
		"instrument/block/pitch":instrument_block_pitch,
		"instrument/block/pitch":instrument_block_pitch,
		"instrument/bass/trigger":instrument_bass_trigger,
		"instrument/bass/pitch":instrument_bass_pitch,
		"instrument/brush/trigger":instrument_brush_trigger,
		"instrument/brush/pitch":instrument_brush_pitch,
	}
	# to do: add try/except block here
	return pathToMethod_d[path](value)
	
def sendAsyncEvent(path, value):
	return [path, value]

def init():
	return [syncRouter, sendAsyncEvent]

