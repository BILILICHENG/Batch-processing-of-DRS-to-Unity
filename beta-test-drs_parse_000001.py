pos_track = { #position -> note track
    '65536' : '1',
    '61440' : '2',
    '57344' : '3',
    '53248' : '4',
    '49152' : '5',
    '45056' : '6',
    '40960' : '7',
    '36864' : '8',
    '32768' : '9',
    '28672' : '10',
    '24576' : '11',
    '20480' : '12',
    '16384' : '13',
    '12288' : '14',
    '8192' : '15',
    '4096' : '16',
    '0' : '17'
}

note_color = { #Note type 1 or 2 -> corresponding color
    '1' : 'Yellow',
    '2' : 'Blue'
}

def step_to_data(thestep): #get the parsed step, slice it to tuple of notes
    if thestep.find('kind').text == '4': #Jump note
        return [('Jump', thestep.find('start_tick').text[:-1])] #Type, time frame
    elif thestep.find('kind').text == '3': #Down note
        return [('Down', thestep.find('start_tick').text[:-1])] #Type, time frame
    elif thestep.find('kind').text == '1' or thestep.find('kind').text == '2': #Blue or Yellow note
        note_type = thestep.find('kind').text
        if thestep.find('long_point') is None: #Standard note
            return [(f'Note{note_color[note_type]}', thestep.find('start_tick').text[:-1], pos_track[thestep.find('right_pos').text], pos_track[thestep.find('left_pos').text])] #Type, time frame, trackR, trackL
        elif thestep.find('long_point').find('point') is None:
                return [(f'Note{note_color[note_type]}', thestep.find('start_tick').text[:-1], pos_track[thestep.find('right_pos').text], pos_track[thestep.find('left_pos').text])]
        elif thestep.find('long_point').find('point') is not None: #Long note
            points = thestep.find('long_point').findall('point')
            result = []
            if points[0].find('left_pos').text == thestep.find('left_pos').text: #Analyze the 0th point | Static long note
                result += [(f'LongNote{note_color[note_type]}', thestep.find('start_tick').text[:-1], points[0].find('tick').text[:-1], pos_track[thestep.find('right_pos').text], pos_track[thestep.find('left_pos').text])]#Type, start frame, end frame, trackR, trackL
                if points[0].find('left_end_pos') is not None: #L/R slick after Static long note
                    if int(points[0].find('left_end_pos').text) > int(points[0].find('left_pos').text): #R slick
                        result += [(f'RNote{note_color[note_type]}', points[0].find('tick').text[:-1], pos_track[points[0].find('left_pos').text], pos_track[points[0].find('right_end_pos').text])] #Type, time frame, start track, end track
                    elif int(points[0].find('left_end_pos').text) < int(points[0].find('left_pos').text): #L slick
                        result += [(f'LNote{note_color[note_type]}', points[0].find('tick').text[:-1], pos_track[points[0].find('right_pos').text], pos_track[points[0].find('left_end_pos').text])] #Type, time frame, start track, end track
            elif points[0].find('left_pos').text != thestep.find('left_pos').text: #Moving Long note
                result += [(f'PYLongNote{note_color[note_type]}', thestep.find('start_tick').text[:-1], points[0].find('tick').text[:-1], pos_track[thestep.find('right_pos').text], pos_track[thestep.find('left_pos').text], pos_track[points[0].find('right_pos').text], pos_track[points[0].find('left_pos').text])]#Type, start frame, end frame, start trackR, start trackL, end trackR, end trackL
            for x in range(1, len(points)): #Analyze the 1st~ point
                if points[x].find('left_pos').text == points[x-1].find('left_pos').text and points[x-1].find('left_end_pos') is None: #Mid static long note
                    result += [(f'ZLongNote{note_color[note_type]}', points[x-1].find('tick').text[:-1], points[x].find('tick').text[:-1], pos_track[points[x].find('right_pos').text], pos_track[points[x].find('left_pos').text])]#Type, start frame, end frame, trackR, trackL
                elif points[x].find('left_pos').text != points[x-1].find('left_pos').text and points[x-1].find('left_end_pos') is None: #Mid moving Long note
                    result += [(f'ZPYLongNote{note_color[note_type]}', points[x-1].find('tick').text[:-1], points[x].find('tick').text[:-1], pos_track[points[x-1].find('right_pos').text], pos_track[points[x-1].find('left_pos').text], pos_track[points[x].find('right_pos').text], pos_track[points[x].find('left_pos').text])]#Type, start frame, end frame, start trackR, start trackL, end trackR, end trackL
                elif points[x-1].find('left_end_pos') is not None: #Handle exception caused by L/R slick
                    if points[x].find('left_pos').text == points[x-1].find('left_end_pos').text: #Exception for mid static long note
                        result += [(f'ZLongNote{note_color[note_type]}', points[x-1].find('tick').text[:-1], points[x].find('tick').text[:-1], pos_track[points[x].find('right_pos').text], pos_track[points[x].find('left_pos').text])]
                    elif points[x].find('left_pos').text != points[x-1].find('left_end_pos').text: #Exception for mid moving long note
                        result += [(f'ZPYLongNote{note_color[note_type]}', points[x-1].find('tick').text[:-1], points[x].find('tick').text[:-1], pos_track[points[x-1].find('right_end_pos').text], pos_track[points[x-1].find('left_end_pos').text], pos_track[points[x].find('right_pos').text], pos_track[points[x].find('left_pos').text])]
                if points[x].find('left_end_pos') is not None: #L/R slick after mid long note
                    if int(points[x].find('left_end_pos').text) > int(points[x].find('left_pos').text): #R slick
                        result += [(f'RNote{note_color[note_type]}', points[x].find('tick').text[:-1], pos_track[points[x].find('left_pos').text], pos_track[points[x].find('right_end_pos').text])] #Type, time frame, start track, end track
                    elif int(points[x].find('left_end_pos').text) < int(points[x].find('left_pos').text): #L slick
                        result += [(f'LNote{note_color[note_type]}', points[x].find('tick').text[:-1], pos_track[points[x].find('right_pos').text], pos_track[points[x].find('left_end_pos').text])] #Type, time frame, start track, end track
            return result

import xml.etree.ElementTree as ET

import sys
drop = sys.argv[1] #Dropped file

import os
filename = os.path.basename(drop)

def rename_tags(element): #integrate different data format
    tag_mapping = { #Alt format -> format used in this code
        'pos_left': 'left_pos',
        'pos_right': 'right_pos',
        'pos_lend': 'left_end_pos',
        'pos_rend': 'right_end_pos',
        'stime_ms': 'start_tick',
        'etime_ms': 'end_tick',
        'point_time': 'tick'
    }
    
    for elem in element.iter():
        if elem.tag in tag_mapping:
            elem.tag = tag_mapping[elem.tag]

tree = ET.parse(drop)
root = tree.getroot()

rename_tags(root)

steps = root.find('sequence_data').findall('step')

step_seq = []
for step in steps: #generate a list of tuples of notes
    step_seq += step_to_data(step)

step_seq_translated = [] #convert the tuples to str with assigned format
for x in step_seq:
    step_seq_translated += [','.join(x)]

end_tick = '' #get end data
if root.find('info').find('end_tick') is not None:
    end_tick = root.find('info').find('end_tick').text[:-1]
else:
    end_tick = int(steps[-1].find('end_tick').text[:-1]) + 500

bpm = root.find('info').find('bpm_info').find('bpm').find('bpm').text #get bpm data

with open(f'{filename}.txt', mode = 'w+') as output_file: #txt output with assigned format
    output_file.writelines([f'BPM,{bpm[:-2]},End,{end_tick}' + '\n'] + [','.join(translated_step) + '\n' for translated_step in step_seq])
