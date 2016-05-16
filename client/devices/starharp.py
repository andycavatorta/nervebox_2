"""
what top-level interfaces are needed by all devices?

anything other than [a]sync [in|out]put?

"""

import duplexPort
import time

# 
clock0 = 0 # range 1-127
clock1 = 0 # range 1-127
clock2 = 0 # range 1-127
externalClock = 0 # range 0-1
power = 0 # range 0-1
volume = 0 # range 0-127

snare = 65535
bongo = 65535 
block = 65535
bass = 65535
brush = 65535
brushOff = 65535


def system_clock_set(path, value):  #setClockOscillator
	global clock0, clock1, clock2
	fpgaModuleId = 10
	if modifier == 0: # coarse
		v = msg.value / 4
		clock0 = v << 11
	if modifier == 1: # middle 
		v = msg.value / 4
		clock1 = v << 6
	if modifier == 2: # fine
		clock2 = msg.value / 2
	fpgaValue = int((clock0 + clock1 + clock2)/2)
	#print fpgaValue
	fpgaValue = fpgaValue if fpgaValue > 0 else fpgaValue +1
	#return [fpgaModuleId,fpgaValue]
	duplexPort.send(fpgaModuleId,fpgaValue)
	return None
def system_balance_set(path, value):  #setBalance
	global volume
	fpgaModuleId = 41
	fpgaValue = msg.value << 9
	#return [fpgaModuleId,fpgaValue/2]
	duplexPort.send(fpgaModuleId,fpgaValue/2)
	return None
def system_intExt_set(path, value):  #toggleExternalClock
	if msg.type != "note_on":
		return None
	global externalClock
	externalClock = 0 if externalClock>0 else 65535
	fpgaModuleId = 31
	#return [fpgaModuleId,externalClock]
	duplexPort.send(fpgaModuleId,externalClock)
	return None
def system_power_set(path, value):  #togglePower
	if msg.type != "note_on":
		return None
	global power
	power = 0 if power>0 else 65535
	fpgaModuleId = 30
	#return [fpgaModuleId,power]
	duplexPort.send(fpgaModuleId,power)
	return None
def system_volume_set(path, value):  #setVolume
	global volume
	fpgaModuleId = 40
	fpgaValue = msg.value << 9
	#return [fpgaModuleId,fpgaValue/2]
	duplexPort.send(fpgaModuleId,fpgaValue/2)
	return None
def instrument_snare_trigger(path, value):  #triggerSnare
	fpgaModuleId = 20
	global snare
	snare = 0 if snare > 0 else 65535
	duplexPort.send(fpgaModuleId,snare)
	time.sleep(0.001)
	snare = 0 if snare > 0 else 65535
	duplexPort.send(fpgaModuleId,snare)
	return None
def instrument_snare_pitch(path, value):  #droneSnare
	fpgaModuleId = 11
	if msg.type == "note_on":
		global clock0, clock1, clock2
		clock = int(clock0 + clock1 + clock2/2)
		duplexPort.send(fpgaModuleId,clock)	
	if msg.type == "note_off":
		clock = 0
		duplexPort.send(fpgaModuleId,clock)	
	return None
def instrument_bongo_trigger(path, value):  #triggerBongo
	fpgaModuleId = 21
	global bongo
	bongo = 0 if bongo > 0 else 65535
	duplexPort.send(fpgaModuleId,bongo)
	time.sleep(0.001)
	bongo = 0 if bongo > 0 else 65535
	duplexPort.send(fpgaModuleId,bongo)	
	return None
def instrument_bongo_pitch(path, value):  #droneBongo
	fpgaModuleId = 12
	if msg.type != "note_on":
		global clock0, clock1, clock2
		clock = int(clock0 + clock1 + clock2/2)
		duplexPort.send(fpgaModuleId,clock)	
	if msg.type != "note_off":
		clock = 0
		duplexPort.send(fpgaModuleId,clock)	
	return None
def instrument_block_trigger(path, value):  #triggerBlock
	fpgaModuleId = 22
	global block
	block = 0 if block > 0 else 65535
	duplexPort.send(fpgaModuleId,block)
	time.sleep(0.001)
	block = 0 if block > 0 else 65535
	duplexPort.send(fpgaModuleId,block)
	return None
def instrument_block_pitch(path, value):  #droneBass
	fpgaModuleId = 13
	if msg.type != "note_on":
		global clock0, clock1, clock2
		clock = int(clock0 + clock1 + clock2/2)
		duplexPort.send(fpgaModuleId,clock)	
	if msg.type != "note_off":
		clock = 0
		duplexPort.send(fpgaModuleId,clock)	
	return None
def instrument_bass_trigger(path, value):  #triggerBass
	fpgaModuleId = 23
	global bass
	bass = 0 if bass > 0 else 65535
	duplexPort.send(fpgaModuleId,bass)
	time.sleep(0.001)
	bass = 0 if bass > 0 else 65535
	duplexPort.send(fpgaModuleId,bass)
	return None
def instrument_bass_pitch(path, value):  #droneBrush
	fpgaModuleId = 14
	if msg.type != "note_on":
		global clock0, clock1, clock2
		clock = int(clock0 + clock1 + clock2/2)
		duplexPort.send(fpgaModuleId,clock)	
	if msg.type != "note_off":
		clock = 0
		duplexPort.send(fpgaModuleId,clock)	
	return None
def instrument_brush_trigger(path, value):  #triggerBrush
	global brush
	if msg.type == "note_on":
		fpgaModuleId = 25
		duplexPort.send(fpgaModuleId,65535)

		fpgaModuleId = 24
		#brush = 0 if brush > 0 else 65535
		#brush = 65535
		duplexPort.send(fpgaModuleId,0)
		time.sleep(0.001)
		#brush = 0 if brush > 0 else 65535
		brush = 0
		duplexPort.send(fpgaModuleId,65535)
	else:
		fpgaModuleId = 25
		#brush = 0 if brush > 0 else 65535
		duplexPort.send(fpgaModuleId,0)
	return None
def instrument_brush_pitch(path, value):  #droneBlock
	fpgaModuleId = 15
	if msg.type != "note_on":
		global clock0, clock1, clock2
		clock = int(clock0 + clock1 + clock2/2)
		duplexPort.send(fpgaModuleId,clock)	
	if msg.type != "note_off":
		clock = 0
		duplexPort.send(fpgaModuleId,clock)	
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

