"""
intermojo protocol
    00: channel
    01: channel
    02: channel
    03: channel
    04: channel
    05: command [pwm/freq]
    06: data 0
    07: data 1
    08: data 2
    09: data 3
    10: data 4
    11: data 5
    12: data 6
    13: data 7
    14: data 8
    15: data 9
    16: data 10
    17: data 11
    18: data 12 
    19: data 13
    20: data 14
    21: data 15
    22: data 16
    23: data 17

input functions:
    hz (channel, freq in Hz as float between 1 and )
    pitch (channel, octave, pitch, cents)
    pwm (channel, duty cycle as float between 0.0 and 100.0)
    pulse (channel, duration in seconds)
    digital (channel, 0 or 1)

    set (channel, freq, pwm)

    get ()

internal:
    init all channels
        default freq = ?
        default pwm = 0

0.000007629 s

18 data bits = 262144
minimum time slice = 1 sec/ 262144 = 0.000003815 sec or 3.815 x 10^-6

50,000,000 FPGA clock cycles * 0.000003815 = 190.75 clock cycles

"""

import x24bitParallelPort
import time

FREQ_MIN = 1.0 # Hz
FREQ_MAX = 262144.0 # Hz
FREQ_DIGITAL_DEFAULT = 10000 # Hz

class Channel():
    def __init__(self, channel):
        self.channel = channel
        self.freq = 10089.0
        self.pwm = 0.0
        self.setFreq(self.freq)
        self.setPwm(self.pwm)
    def formatCommand(self,command):  # command = [pwm|freq]
        channel_bin_str = '{0:05b}'.format(self.channel)
        if command=="freq":
            command_bin_str = "0"
            slices = int(FREQ_MAX/self.freq)
            adjustedFreq_f = float(FREQ_MAX/slices)
            sliceCount_bin_str = '{0:018b}'.format(slices)
            return [list(channel_bin_str + command_bin_str + sliceCount_bin_str), adjustedFreq_f]
        if command=="pwm":
            command_bin_str = "1"
            pwm_bin_str = '{0:018b}'.format(int(self.pwm*10.24))
            return list(channel_bin_str + command_bin_str + pwm_bin_str)  
    def setFreq(self, freq): # Hz
        if FREQ_MIN <= float(freq) <= FREQ_MAX:
            command_l, adjustedFreq = self.formatCommand("freq")
            #print "Channel %d frequency %f adjusted to %f" % (self.channel, freq, adjustedFreq)
            x24bitParallelPort.send(command_l)
        else:
            print "Freqency out of range (0Hz-262,144Hz)", freq
    def setPwm(self, pwm_f): # float%
        if 0.0 <= pwm_f <= 100.0:
            command_l = self.formatCommand("pwm")
            x24bitParallelPort.send(command_l)
        else:
            print "PWM out of range (0.0-100.0)", pwm_f
    def squareWave(self, freq, pwm):
        self.setFreq(freq)
        self.setPwm(pwm)

    def digital(self, bool):
        self.setFreq(FREQ_DIGITAL_DEFAULT)
        self.setPwm(0.0 if bool==0 else 100.0)

    def pulse(self, pulselength):
        self.digital(1)
        time.sleep(pulselength)
        self.digital(0)

    def get(self):
        return {
            "channel":self.channel,
            "freq":self.freq,
            "pwm":self.pwm
        }

class Channels():
    def __init__(self):
        self.channels_l = [ Channel(x) for x in range(24) ]

channels = Channels()
