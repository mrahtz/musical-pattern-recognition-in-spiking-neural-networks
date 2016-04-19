#!/usr/bin/env python

import os
from mingus.midi import fluidsynth
from mingus.containers import Note

note_sequences = {}
note_sequences['two_notes'] = ['C-5', 'G-5']
note_sequences['three_notes'] = ['C-5', 'E-5', 'G-5']
note_sequences['scale'] = ['C-5', 'D-5', 'E-5', 'F-5', 'G-5', 'A-5', 'B-5']

separations_seconds = [0.5, 1, 2]

fluidsynth.init(sf2='FluidR3 GM2-2.SF2')

def play_sequence(sequence, separation_seconds):
    for note_str in sequence:
        note = Note(note_str)
        fluidsynth.play_Note(note)
        fluidsynth.midi.sleep(seconds=separation_seconds)
        fluidsynth.stop_Note(note)

# generate tracks for each sequence separately

temp_n = 1
for sequence in note_sequences:
    for separation_seconds in separations_seconds:
        temp_filename = '/tmp/temp%d.wav' % temp_n
        fluidsynth.midi.start_recording(temp_filename)
        for _ in range(20):
            play_sequence(note_sequences[sequence], separation_seconds)

        final_filename = \
            'test_inputs/%s_%.1f_s.wav' % (sequence, separation_seconds)
        # drop right channel, downmix to 10 kHz
        os.system("sox %s %s remix 1 rate 10000" % \
            (temp_filename, final_filename))
        temp_n += 1

# generate a training track (scale) followed  by a testing track (arpeggio)

temp_filename = '/tmp/temp%d.wav' % temp_n
fluidsynth.midi.start_recording(temp_filename)
separation_seconds = 0.5
for _ in range(4):
    play_sequence(note_sequences['scale'], separation_seconds)
for _ in range(5):
    play_sequence(note_sequences['three_notes'], separation_seconds)
final_filename = \
    'test_inputs/%s_%.1f_s.wav' % ('scale-three_notes', separation_seconds)
os.system("sox %s %s remix 1 rate 10000" % \
    (temp_filename, final_filename))
