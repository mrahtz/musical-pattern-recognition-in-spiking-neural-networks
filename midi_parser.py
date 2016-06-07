#!/usr/bin/env python

from __future__ import division, print_function
from mingus.midi.midi_file_in import MIDI_to_Composition
import pickle

composition = MIDI_to_Composition('comptine.mid')
with open('comptine.pickle', 'w') as f:
    pickle.dump(composition, f)
