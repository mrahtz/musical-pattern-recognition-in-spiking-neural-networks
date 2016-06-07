#!/usr/bin/env python

from __future__ import print_function, division
import pickle
from mingus.containers import Note
from mingus.midi import fluidsynth
import wave
import os
from IPython.core.debugger import Tracer

with open('comptine.pickle', 'r') as f:
    comptine = pickle.load(f)

bpm = comptine[1]
rest = comptine[0]

"""
for thing in rest[0]:
    print(thing)
"""

track1 = rest[1]
track2 = rest[2]

"""
max_i = 8*5
fluidsynth.init(sf2='FluidR3 GM2-2.SF2', file='comptine_training.wav')
i = max_i
all_notes = []
for track in [track1, track2]:
    for l1 in track:
        for l2 in l1:
            notes = l2[2]
            for note in notes:
                notes = str(note)
                notes = notes[1:-1]
                all_notes.append(notes)
all_notes = list(set(all_notes))
all_notes.sort()

n_seconds = 0
for i in range(20):
    for note in all_notes:
        fluidsynth.play_Note(Note(note));
        fluidsynth.midi.sleep(seconds=1)
        fluidsynth.stop_Note(Note(note));
        n_seconds += 1
print(n_seconds)
"""

for separation in [0.125, 0.25, 0.5, 1.0]:
    print(separation)
    fluidsynth.initialized = False
    temp_filename=('foo%s.wav' % separation)
    fluidsynth.init(sf2='FluidR3 GM2-2.SF2', file=temp_filename)
    for _ in range(3):
        for l1 in track2[0:4]:
            for l2 in l1:
                notes = l2[2]
                for note in notes:
                    fluidsynth.play_Note(Note(note))
                fluidsynth.midi.sleep(seconds=separation)
                for note in notes:
                    fluidsynth.stop_Note(Note(note))

for separation in [0.125, 0.25, 0.5, 1.0]:
    print(separation)
    temp_filename=('foo%s.wav' % separation)
    final_filename=('comptine_%f_s.wav' % separation)
    os.system("sox %s %s remix 1 rate 10000" % (temp_filename, final_filename))
