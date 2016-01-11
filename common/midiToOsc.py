
import json

statusMap = {
    128:"note_off",
    144:"note_on",
    160:"polyphonic_aftertouch",
    176:"control_change",
    192:"program_change",
    208:"channel_aftertouch",
    224:"pitch_wheel",
    240:"system_exclusive",
    241:"system_common",
    242:"song_position_pointer",
    243:"song_select",
    244:"system_common",
    245:"system_common",
    246:"tune_request",
    247:"end_of_sysex",
    248:"timing_clock",
    249:"undefined",
    250:"start",
    251:"continue",
    252:"stop",
    253:"undefined",
    254:"active_sensing",
    255:"sys_reset",
}

ccMap = {
    0:"Continuous_controller",
    1:"Modulation_wheel",
    2:"Breath_control",
    3:"Continuous_controller",
    4:"Foot_controller",
    5:"Portamento_time",
    6:"Data_Entry",
    7:"Main_Volume",
    8:"Continuous_controller",
    9:"Continuous_controller",
    10:"Continuous_controller",
    11:"Continuous_controller",
    12:"Continuous_controller",
    13:"Continuous_controller",
    14:"Continuous_controller",
    15:"Continuous_controller",
    16:"Continuous_controller",
    17:"Continuous_controller",
    18:"Continuous_controller",
    19:"Continuous_controller",
    20:"Continuous_controller",
    21:"Continuous_controller",
    22:"Continuous_controller",
    23:"Continuous_controller",
    24:"Continuous_controller",
    25:"Continuous_controller",
    26:"Continuous_controller",
    27:"Continuous_controller",
    28:"Continuous_controller",
    29:"Continuous_controller",
    30:"Continuous_controller",
    31:"Continuous_controller",
    32:"Continuous_controller",
    33:"Modulation_wheel",
    34:"Breath_control",
    35:"Continuous_controller",
    36:"Foot_controller",
    37:"Portamento_time",
    38:"Data_entry",
    39:"Main_volume",
    40:"Continuous_controller",
    41:"Continuous_controller",
    42:"Continuous_controller",
    43:"Continuous_controller",
    44:"Continuous_controller",
    45:"Continuous_controller",
    46:"Continuous_controller",
    47:"Continuous_controller",
    48:"Continuous_controller",
    49:"Continuous_controller",
    50:"Continuous_controller",
    51:"Continuous_controller",
    52:"Continuous_controller",
    53:"Continuous_controller",
    54:"Continuous_controller",
    55:"Continuous_controller",
    56:"Continuous_controller",
    57:"Continuous_controller",
    58:"Continuous_controller",
    59:"Continuous_controller",
    60:"Continuous_controller",
    61:"Continuous_controller",
    62:"Continuous_controller",
    63:"Continuous_controller",
    64:"Damper_pedal_on/off",
    65:"Portamento_on/off",
    66:"Sustenuto_on/off",
    67:"Soft_pedal_on/off",
    68:"Undefined_on/off",
    69:"Undefined_on/off",
    70:"Undefined_on/off",
    71:"Undefined_on/off",
    72:"Undefined_on/off",
    73:"Undefined_on/off",
    74:"Undefined_on/off",
    75:"Undefined_on/off",
    76:"Undefined_on/off",
    77:"Undefined_on/off",
    78:"Undefined_on/off",
    79:"Undefined_on/off",
    80:"Undefined_on/off",
    81:"Undefined_on/off",
    82:"Undefined_on/off",
    83:"Undefined_on/off",
    84:"Undefined_on/off",
    85:"Undefined_on/off",
    86:"Undefined_on/off",
    87:"Undefined_on/off",
    88:"Undefined_on/off",
    89:"Undefined_on/off",
    90:"Undefined_on/off",
    91:"Undefined_on/off",
    92:"Undefined_on/off",
    93:"Undefined_on/off",
    94:"Undefined_on/off",
    95:"Undefined_on/off",
    96:"Data_entry_+1",
    97:"Data_entry_-1",
    98:"Undefined",
    99:"Undefined",
    100:"Undefined",
    101:"Undefined",
    102:"Undefined",
    103:"Undefined",
    104:"Undefined",
    105:"Undefined",
    106:"Undefined",
    107:"Undefined",
    108:"Undefined",
    109:"Undefined",
    110:"Undefined",
    111:"Undefined",
    112:"Undefined",
    113:"Undefined",
    114:"Undefined",
    115:"Undefined",
    116:"Undefined",
    117:"Undefined",
    118:"Undefined",
    119:"Undefined",
    120:"Undefined",
    121:"Undefined",
    122:"Local_control_on/off",
    123:"All_notes_off",
    124:"Omni_mode_off",
    125:"Omni_mode_on",
    126:"Poly_mode_on/off",
    127:"Poly_mode_on",
}

def makePitch(midiNoteNumber, cents_int=0):
    return {
        'pitch':["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"][midiNoteNumber%12],
        'octave':math.floor(midiNoteNumber/12)-1,
        'cents':cents_int,
        'freq':440.0 * (2.0**((midiNoteNumber-69+cents_int)/12.0)),
        'midi':midiNoteNumber
    }

def convert(devicename, event):

    #### PARSE MIDI ####
    if event[0] < 0xF0:
        channel = (event[0] & 0xF) + 1
        status_int = event[0] & 0xF0
    else:
        status_int = event[0]
        channel = None
    status = statusMap[int(status_int)]
    data1 = data2 = None
    num_bytes = len(event)
    if num_bytes >= 2:
        data1 = event[1]
    if num_bytes >= 3:
        data2 = event[2]
    if status in ["note_off","note_on","polyphonic_aftertouch","channel_aftertouch"]:
        data1 = makePitch(data1)
    if status == "control_change":
        data1 = [data1, ccMap[data1]]

    #### CREATE OSC ####
    params = {
        "channel":channel, 
        "data1":data1,
        "data2":data2
    }
    if status in ["note_off","note_on"]:
        params = {
            "channel":channel,
            "pitch":data1,
            "amplitude":data2
        }
    if status =="polyphonic_aftertouch":
        params = {
            "channel":channel,
            "pitch":data1,
            "pressure":data2
        }
    if status =="program_change":
        params = {
            "channel":channel,
            "program":data1
        }
    if status =="channel_aftertouch":
        params = {
            "channel":channel,
            "pressure":data1
        }
    if status in ["system_common","tune_request","end_of_sysex","timing_clock","start","continue","stop","undefined","active_sensing","sys_reset"]:
        params = {
            "channel":channel
        }
    if status =="pitch_wheel":
        params = {
            "channel":channel,
            "value":int(data1) + int(data2)<<7
        }
    if status =="song_select":
        params = {
            "channel":channel,
            "value":data1
        }
    if status =="song_position_pointer":
        params = {
            "channel":channel,
            "value":int(data1) + int(data2)<<7
        }
    if status =="system_exclusive":
        params = {
            "channel":channel,
            "vendorID":data1,
            "value":data2
        }
    if status =="system_common":
        params = {
            "channel":channel
        }
    if status =="control_change":
        params = {
            "channel":channel,
            "type":data1,
            "value":data2
        }

    params_j = json.dumps(params)
    return "%s/%s %s" % (devicename,status, params_j)
