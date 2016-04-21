#!/usr/bin/env python

from __future__ import print_function, division
import argparse
import pickle
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('pickle_file')
args = parser.parse_args()

print("Loading results...")
with open(args.pickle_file, 'rb') as pickle_file:
    monitors = pickle.load(pickle_file)
print("Done!")

def spike_range(spike_times, spike_indices, from_time, to_time):
    max_time = np.amax(spike_times)
    if to_time == 'end':
        to_time = max_time
    if from_time < 0:
        from_time = max_time + from_time

    relevant_indices = (spike_times >= from_time) & (spike_times <= to_time)
    relevant_spike_times = spike_times[relevant_indices]
    relevant_spike_indices = spike_indices[relevant_indices]
    return (relevant_spike_indices, relevant_spike_times)

input_spike_indices = monitors['spikes']['input']['i']
input_spike_times = monitors['spikes']['input']['t']
(i_start_i, i_start_t) = \
    spike_range(input_spike_times, input_spike_indices, 0, 5)
(i_end_i, i_end_t) = \
    spike_range(input_spike_times, input_spike_indices, -5, 'end')

output_spike_indices = monitors['spikes']['layer1e']['i']
output_spike_times = monitors['spikes']['layer1e']['t']
(o_start_i, o_start_t) = \
    spike_range(output_spike_times, output_spike_indices, 0, 5)
(o_end_i, o_end_t) = \
    spike_range(output_spike_times, output_spike_indices, -5, 'end')

plt.ion()
plt.figure(figsize=(6,4.5))
plt.subplot(2, 2, 1)
plt.plot(i_start_t, i_start_i, 'k.', markersize=2)
plt.subplot(2, 2, 2)
plt.plot(i_end_t, i_end_i, 'k.', markersize=2)
plt.subplot(2, 2, 3)
plt.plot(o_start_t, o_start_i, 'k.', markersize=2)
plt.subplot(2, 2, 4)
plt.plot(o_end_t, o_end_i, 'k.', markersize=2)

for i in [1, 2, 3, 4]:
    plt.subplot(2, 2, i)
    plt.gca().xaxis.set_minor_locator(MultipleLocator(0.5))
    plt.grid(which='minor')

for i in [1, 2]:
    plt.subplot(2, 2, i)
    plt.ylim([0, 512])
for i in [3, 4]:
    plt.subplot(2, 2, i)
    plt.ylim([0, 15])

plt.subplot(2, 2, 1)
plt.ylabel("Input\nAfferent no.")
plt.subplot(2, 2, 3)
plt.ylabel("Output\nNeuron no.")
plt.xlabel("Time (s)")
plt.subplot(2, 2, 4)
plt.xlabel("Time (s)")

plt.tight_layout(pad=0.1)
