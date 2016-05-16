
import sys
import socket
import os

BASE_PATH = os.path.split(os.path.dirname(os.path.realpath(__file__)))[0]
COMMON_PATH = "%s/common/" % (BASE_PATH )
SERVER_PATH = "%s/server/" % (BASE_PATH )

sys.path.append(COMMON_PATH)
sys.path.append(SERVER_PATH)

import siggen

CHANNEL_COUNT = 12

def printHelp(msg=""):
    print msg
    print "suggested formats  blah  "

def displayChannelOptions():
    print "Enter channel number (0-%d)  " % (CHANNEL_COUNT-1),

def testChannelOption(channel_str):
    try:
        channel_int = int(channel_str)
        assert channel_int >= 0 and channel_int <=11
        return [ True, channel_int]
    except Exception as e:
        print e
        return [ False, None ]

functions_l = [
    ["status","status of signals"],
    ["pulse","send pulse"],
    ["digital","digital on/off"],
    ["freq","set frequency"],
    ["dutyCycle","set duty cycle (pwm)"],
    ["freqDutyCycle","set frequency and duty cycle (pwm)"]
]

def displayFunctionOptions():
    print "select function (by number)  "
    for i in range(len(functions_l)):
        print "%d) %s" % (i, functions_l[i][1])

def testFunctionOption(functionOrdinal_str):
    try:
        function_int = int(functionOrdinal_str.rstrip())
        assert 0 <= function_int < len(functions_l)
        return [ True, functions_l[function_int][0]]
    except Exception as e:
        print e
        return [ False, None ]

def displayPulseOptions():
    print "Enter pulse duration in seconds ( ex: 0.001, 0.2, 5.2 )  ",

def testPulseOption(pulseDuration_str):
    try:
        pulseDuration_f = float(pulseDuration_str.rstrip())
        assert pulseDuration_f >= 0.001
        return [ True, pulseDuration_f]
    except Exception as e:
        print e
        return [ False, None ]

def displayDitigalOptions():
    print "Enter ditigal output value (0 or 1)  ",

def testDitigalOption(bool_str):
    try:
        bool_int = int(bool_str.rstrip())
        assert bool_int in [0,1]
        return [ True, bool_int]
    except Exception as e:
        print e
        return [ False, None ]

def displayFreqOptions():
    print "Enter frequency in Hz, range from 0.1 to 100,000.00  ",

def testFreqOption(freq_str):
    try:
        freq_f = float(freq_str.rstrip())
        assert 0.1 <= freq_f <= 100000.0
        return [ True, freq_f]
    except Exception as e:
        print e
        return [ False, None ]

def displayDutyCycleOptions():
    print "Enter pwm duty cycle in %, range from 0 to 100  ",

def testDutyCycleOption(dutyCycle_str):
    try:
        dutyCycle_f = int(dutyCycle_str.rstrip())
        assert 0 <= dutyCycle_f <= 100
        return [ True, dutyCycle_f]
    except Exception as e:
        print e
        return [ False, None ]

def displayStatus(status_l):
    msg = "Channel %d is set at freq = %f and duty cycle = %d" % (status_l[0], status_l[1]["freq"], status_l[1]["dutyCycle"])
    print ""
    print msg
    print "-" * len(msg)
    print ""

while True:
#try:
    good = False
    while not good:
        displayChannelOptions()
        good, channel_int = testChannelOption(sys.stdin.readline())
    good = False
    while not good:
        displayFunctionOptions()
        good, function_str = testFunctionOption(sys.stdin.readline())
    if function_str == "status":
        status = siggen.send(function_str,channel_int)
        displayStatus(status)
        #print status
    if function_str == "pulse":
        good = False
        while not good:
            displayPulseOptions()
            good, pulseDuration_f = testPulseOption(sys.stdin.readline())
        status = siggen.send(function_str, channel_int, pulseDuration_f)
        displayStatus(status)
    if function_str == "digital":
        good = False
        while not good:
            displayDitigalOptions()
            good, bool_int = testDitigalOption(sys.stdin.readline())
        status = siggen.send(function_str, channel_int, bool_int)
        displayStatus(status)
    if function_str == "freq":
        good = False
        while not good:
            displayFreqOptions()
            good, freq_f = testFreqOption(sys.stdin.readline())
        status = siggen.send(function_str, channel_int, freq_f)
        displayStatus(status)
    if function_str == "dutyCycle":
        good = False
        while not good:
            displayDutyCycleOptions()
            good, dutyCycle_f = testDutyCycleOption(sys.stdin.readline())
        status = siggen.send(function_str, channel_int, dutyCycle_f)
        displayStatus(status)
    if function_str == "freqDutyCycle":
        good = False
        while not good:
            displayFreqOptions()
            good, freq_f = testFreqOption(sys.stdin.readline())
        good = False
        while not good:
            displayDutyCycleOptions()
            good, dutyCycle_f = testDutyCycleOption(sys.stdin.readline())
        status = siggen.send(function_str, channel_int, freq_f, dutyCycle_f)
        displayStatus(status)

#    except Exception as e:
#        print e
