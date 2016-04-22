#!/usr/bin/env python

from __future__ import print_function, division
import argparse
import pickle
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
import utils
import os.path

parser = argparse.ArgumentParser()
parser.add_argument('pickle_file')
args = parser.parse_args()

if 'scale' in args.pickle_file:
    n_notes = 7
elif '_three_' in args.pickle_file:
    n_notes = 3
elif '_two_' in args.pickle_file:
    n_notes = 2
else:
    raise Exception("Unknown number of notes for pickle '%s'" %
                    args.pickle_file)
note_length = 0.5

print("Loading results...")
with open(args.pickle_file, 'rb') as pickle_file:
    monitors = pickle.load(pickle_file)
print("Done!")

input_spike_indices = monitors['spikes']['input']['i']
input_spike_times = monitors['spikes']['input']['t']

output_spike_indices = monitors['spikes']['layer1e']['i']
output_spike_times = monitors['spikes']['layer1e']['t']

plt.ion()
plt.figure(figsize=(6,4.5))

# input spikes
plt.subplot(2, 2, 1)
plt.plot(input_spike_times, input_spike_indices, 'k.', markersize=2)
plt.xlim([0, 5])
plt.subplot(2, 2, 2)
plt.plot(input_spike_times, input_spike_indices, 'k.', markersize=2)
max_time = np.amax(input_spike_times)
plt.xlim([max_time-5, max_time])

if 'scale-three_notes' in args.pickle_file:
    from_time = 5
    to_time = 12
else:
    from_time = max_time/2
    to_time = max_time
# output spikes
favourite_notes = utils.analyse_note_responses(
    output_spike_indices,
    output_spike_times,
    note_length,
    n_notes,
    from_time=from_time,
    to_time=to_time
)
plt.subplot(2, 2, 3)
utils.ordered_spike_raster(output_spike_indices, output_spike_times,
                           favourite_notes)
plt.xlim([0, 5])
plt.subplot(2, 2, 4)
utils.ordered_spike_raster(output_spike_indices, output_spike_times,
                           favourite_notes)
if 'scale-three_notes' in args.pickle_file:
    plt.xlim([11, 16])
else:
    plt.xlim([max_time-5, max_time])

for i in [1, 2, 3, 4]:
    plt.subplot(2, 2, i)
    plt.gca().xaxis.set_minor_locator(MultipleLocator(0.5))
    plt.grid(which='minor')

for i in [1, 2]:
    plt.subplot(2, 2, i)
    plt.ylim([0, 512])

plt.subplot(2, 2, 1)
plt.ylabel("Input\nAfferent no.")
plt.subplot(2, 2, 3)
plt.ylabel("Output\nNeuron no.")
plt.xlabel("Time (s)")
plt.subplot(2, 2, 4)
plt.xlabel("Time (s)")

plt.tight_layout(pad=0.1)
seq_name = os.path.basename(args.pickle_file)\
    .replace('.pickle', '').replace('monitors_', '')
fig_name = 'input_output_spikes_%s' % seq_name
plt.savefig('figures/%s.png' % fig_name, dpi=500)
