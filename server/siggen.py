import time
#import threading
import sys
import socket
import os


BASE_PATH = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
COMMON_PATH = "%s/common/" % (BASE_PATH )
SERVER_PATH = "%s/server/" % (BASE_PATH )


sys.path.append(COMMON_PATH)
sys.path.append(SERVER_PATH)

import x24bitParallelPort

CHANNEL_COUNT = 12
DEFAUT_FREQ = 30000.0

FPGA_FREQ = 50000000 #Hz
                      
channels = [{"freq":DEFAUT_FREQ,"dutyCycle":0} for x in range(CHANNEL_COUNT) ]

def send(verb, channel=None, data0=0, data1=0):
    #print ">>>>", verb, channel, data0, data1
    if verb == "status":
        return _status(channel)
    if verb == "pulse":
        return _pulse(channel, data0)
    if verb == "digital":
        return _ditigal(channel, data0)
    if verb == "freq":
        return _freq(channel, data0)
    if verb == "freqDutyCycle":
        return _freqDutyCycle(channel, data0, data1)
    if verb == "dutyCycle":
        return _dutyCycle(channel, data0)

def _status(channel="all"):
    return [channel, channels if channel == "all" else channels[channel]]

def _ditigal(channel, bool):
    channels[channel]["dutyCycle"] = 100 if bool else 0
    _sendToFPGA(
        channel,
        channels[channel]["freq"], 
        channels[channel]["dutyCycle"]
    )
    return _status(channel)    
def _freqDutyCycle(channel, data0, data1):
    channels[channel]["freq"] = data0
    channels[channel]["dutyCycle"] = data1
    _sendToFPGA(
        channel,
        channels[channel]["freq"],
        channels[channel]["dutyCycle"]
    )
    return _status(channel)
def _freq(channel, freq):
    return _freqDutyCycle(
        channel,
        freq,
        channels[channel]["dutyCycle"]
    )
def _pulse(channel, duration):
    _ditigal(channel, True)
    time.sleep(duration)
    _ditigal(channel, True)
    #threading.Timer(_ditigal, duration, [False])
    return _status(channel)
def _dutyCycle(channel, dutyCycle):
    return _freqDutyCycle(
        channel,
        channels[channel]["freq"],
        dutyCycle
    )
def _convertFreqToFpga(freq):
    return int (FPGA_FREQ/freq)

def _convertPercentTo7Bit(percent):
    return int(percent*1.27)

def _dec2bin(n, fill):
  bStr = ''
  while n > 0:
    bStr = str(int(n) % 2) + bStr
    n = n >> 1
  return bStr.zfill(fill)

def _sendToFPGA(channel, dutyCycle, freq):
    fpgaCycles = _convertFreqToFpga(channels[channel]["freq"])
    dutyCycle127 = _convertPercentTo7Bit(channels[channel]["dutyCycle"])
    channel_ba = _dec2bin(channel, 5)
    dutyCycle_ba = _dec2bin(dutyCycle127, 7)
    fpgaCycles_ba = _dec2bin(fpgaCycles, 34)
    # Assuming MSB
    frame_ba = "%s%s%s" % (channel_ba, dutyCycle_ba, fpgaCycles_ba)

    word1 = "%s%s" % (frame_ba[0:23], "0")
    word2 = "%s%s" % (frame_ba[23:46], "1")
    #print channel, dutyCycle, freq
    print channel_ba, dutyCycle_ba, fpgaCycles_ba
    print word1, word2
    x24bitParallelPort.send(word1)
    x24bitParallelPort.send(word2)