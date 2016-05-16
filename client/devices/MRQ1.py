import duplexPort
import threading
import time
# init duplex port
def TestCallback():
	while True:
		time.sleep(1)
#duplexPort.init(testcallback)
testcallback = threading.Thread(target=TestCallback)
testcallback.start()

duplexPort.init(testcallback)


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
brushOff = 65535

def setClockOscillator(msg,modifier):
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

def triggerSnare(msg,modifier):
	fpgaModuleId = 20
	global snare
	snare = 0 if snare > 0 else 65535
	duplexPort.send(fpgaModuleId,snare)
	time.sleep(0.001)
	snare = 0 if snare > 0 else 65535
	duplexPort.send(fpgaModuleId,snare)

def triggerBongo(msg,modifier):
	fpgaModuleId = 21
	global bongo
	bongo = 0 if bongo > 0 else 65535
	duplexPort.send(fpgaModuleId,bongo)
	time.sleep(0.001)
	bongo = 0 if bongo > 0 else 65535
	duplexPort.send(fpgaModuleId,bongo)	

def triggerBlock(msg,modifier):
	fpgaModuleId = 22
	global block
	block = 0 if block > 0 else 65535
	duplexPort.send(fpgaModuleId,block)
	time.sleep(0.001)
	block = 0 if block > 0 else 65535
	duplexPort.send(fpgaModuleId,block)

def triggerBass(msg,modifier):
	fpgaModuleId = 23
	global bass
	bass = 0 if bass > 0 else 65535
	duplexPort.send(fpgaModuleId,bass)
	time.sleep(0.001)
	bass = 0 if bass > 0 else 65535
	duplexPort.send(fpgaModuleId,bass)

def triggerBrush(msg,modifier):
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

def setVolume(msg,modifier):
	global volume
	fpgaModuleId = 40
	fpgaValue = msg.value << 9
	#return [fpgaModuleId,fpgaValue/2]
	duplexPort.send(fpgaModuleId,fpgaValue/2)

def droneSnare(msg, modifier):
	fpgaModuleId = 11
	if msg.type == "note_on":
		global clock0, clock1, clock2
		clock = int(clock0 + clock1 + clock2/2)
		duplexPort.send(fpgaModuleId,clock)	
	if msg.type == "note_off":
		clock = 0
		duplexPort.send(fpgaModuleId,clock)	

def droneBongo(msg, modifier):
	fpgaModuleId = 12
	if msg.type != "note_on":
		global clock0, clock1, clock2
		clock = int(clock0 + clock1 + clock2/2)
		duplexPort.send(fpgaModuleId,clock)	
	if msg.type != "note_off":
		clock = 0
		duplexPort.send(fpgaModuleId,clock)	

def droneBass(msg, modifier):
	fpgaModuleId = 14
	if msg.type != "note_on":
		global clock0, clock1, clock2
		clock = int(clock0 + clock1 + clock2/2)
		duplexPort.send(fpgaModuleId,clock)	
	if msg.type != "note_off":
		clock = 0
		duplexPort.send(fpgaModuleId,clock)	

def droneBrush(msg, modifier):
	fpgaModuleId = 15
	if msg.type != "note_on":
		global clock0, clock1, clock2
		clock = int(clock0 + clock1 + clock2/2)
		duplexPort.send(fpgaModuleId,clock)	
	if msg.type != "note_off":
		clock = 0
		duplexPort.send(fpgaModuleId,clock)	

def droneBlock(msg, modifier):
	fpgaModuleId = 13
	if msg.type != "note_on":
		global clock0, clock1, clock2
		clock = int(clock0 + clock1 + clock2/2)
		duplexPort.send(fpgaModuleId,clock)	
	if msg.type != "note_off":
		clock = 0
		duplexPort.send(fpgaModuleId,clock)	

def setBalance(msg,modifier):
	global volume
	fpgaModuleId = 41
	fpgaValue = msg.value << 9
	#return [fpgaModuleId,fpgaValue/2]
	duplexPort.send(fpgaModuleId,fpgaValue/2)

def toggleExternalClock(msg,modifier):
	if msg.type != "note_on":
		return None
	global externalClock
	externalClock = 0 if externalClock>0 else 65535
	fpgaModuleId = 31
	#return [fpgaModuleId,externalClock]
	duplexPort.send(fpgaModuleId,externalClock)

def togglePower(msg,modifier):
	if msg.type != "note_on":
		return None
	global power
	power = 0 if power>0 else 65535
	fpgaModuleId = 30
	#return [fpgaModuleId,power]
	duplexPort.send(fpgaModuleId,power)
