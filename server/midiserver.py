###########################################
##### MIDI DEVICES ATTACHED TO SERVER #####
###########################################
import midiDeviceManager

def deviceCallback(eventType, deviceID, deviceName):
    print "deviceCallback", eventType, deviceID, deviceName

statusMap = {
    8:"note_off",
    9:"note_on",
    10:"polyphonic_aftertouch",
    11:"control_change",
    12:"program_change",
    13:"channel_aftertouch",
    14:"pitch_wheel",
    15:"system_exclusive"
}

def midiCallback(devicename, cmd, channel, note, velocity):
    #print "midiCallback", devicename, cmd, channel, note, velocity
    cmd = statusMap[int(cmd)]
    osc_msg = midiToOsc.convert(devicename, cmd, channel, note, velocity) # convert MIDI so OSC
    #print "midiCallback", osc_msg
    mapOscInToOscOut(osc_msg)

midiDeviceManager.init(deviceCallback, midiCallback)

#################################
##### MAP OSC IN TO OSC OUT #####
#################################


def mapOscInToOscOut(osc):
  print osc
  [device, command, params, params_str] = parseOsc.parse(osc)
  if command in ["note_on", "note_off"]:
    try:
      [oscOutDevice, oscOutPath] = MAPPING["INPUTDEVICES"][device]["CHANNEL"][params['channel']]["PITCH_12TET"][params["pitch"]["12tet"]]["COMMAND"][command]
      oscOut = "%s %s"%(oscOutPath,params_str)
      #print oscOut
      #pubsub_api["publish"]("osc", '/HR16/sound/tom_3/bang {"timbre":null,"dynamics":{"amplitude":0.5196850393700787},"channel":"1","pitch":{"midi":57,"cents":0,"12tet":"A3","octave":3,"pitch":"A","freq":220.0}}')
      dps.pubsub_api["publish"](oscOutDevice, oscOut)
    except Exception as e:
      print "mapping not found", osc