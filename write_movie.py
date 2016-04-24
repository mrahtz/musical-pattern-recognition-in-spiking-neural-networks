#!/usr/bin/env python

from __future__ import print_function, division
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pickle
import argparse

def get_input_filename():
    parser = argparse.ArgumentParser()
    parser.add_argument("pickle_filename", metavar="variables.pickle")
    args = parser.parse_args()
    return args.pickle_filename

pickle_filename = get_input_filename()
print("Loading pickle...", end='')
with open(pickle_filename, 'rb') as f:
    objects = pickle.load(f)
    (potential, weights, weight_targets, spike_times, spike_indices) = objects
print("done!")

n_neurons = potential.shape[0]
max_spike_index = np.amax(spike_indices)
n_afferents = weights.shape[0] / n_neurons
max_afferent_shown = max(n_afferents, max_spike_index)
min_pot = np.amin(potential)
max_pot = np.amax(potential)

def get_potential(frame_n):
    p = potential[:, frame_n]
    p -= min_pot
    p /= (max_pot - min_pot)
    return p

def get_weight_diffs(frame_n):
    diff = weights[:, frame_n] - weights[:, 0]
    return diff

def spikes_range(start_s, end_s):
    relevant_spikes = (spike_times >= start_s) & (spike_times <= end_s)
    times = spike_times[relevant_spikes]
    indices = spike_indices[relevant_spikes]
    return (times, indices)

def initial_plot():
    fig = plt.figure()
    weight_lines = []
    potential_ims = []

    gs = gridspec.GridSpec(n_neurons+3, 5)

    # draw input spike raster at top
    plt.subplot(gs[0:3, 0:-1])
    cur_time = 0
    times, indices = spikes_range(cur_time, cur_time+0.5)
    input_spike_raster = \
        plt.plot(indices, times, 'k.', markersize=1)[0]
    plt.xlim([0, max_afferent_shown])
    plt.xticks([])
    plt.yticks([])

    pot = get_potential(0)
    diff = get_weight_diffs(0)
    for neuron_n in range(n_neurons):
        # draw weights down the left
        plt.subplot(gs[neuron_n+3, 0:-1])
        relevant_weight_idx = (weight_targets == neuron_n)
        relevant_weights = diff[relevant_weight_idx]
        line = plt.plot(relevant_weights, 'k')[0]
        weight_lines.append(line)
        plt.xlim([0, max_afferent_shown])
        plt.xticks([])
        plt.yticks([])
        plt.ylim([min_diff*1.05, max_diff * 1.05])

        # draw membrane potential on the right
        plt.subplot(gs[neuron_n+3, -1])
        im = plt.imshow(X=np.matrix(pot[neuron_n]), interpolation='none')
        potential_ims.append(im)
        im.set_clim([0,1])
        ax = im.get_axes()
        ax.set_xticks([])
        ax.set_yticks([])

    plt.tight_layout(pad=0)

    return (fig, input_spike_raster, weight_lines, potential_ims)

def update_plots(frame_n):
    global input_spike_raster, weight_lines, potential_ims
    print("Frame %d" % frame_n)

    # update input spike raster
    cur_time = frame_n * 1/60.0
    times, indices = spikes_range(cur_time, cur_time+5)
    times -= cur_time
    input_spike_raster.set_data(indices, times)

    # update weights/membrane potential
    pot = get_potential(frame_n)
    diff = get_weight_diffs(frame_n)
    for neuron_n in range(n_neurons):
        relevant_weights = (weight_targets == neuron_n)
        weight_lines[neuron_n].set_ydata(diff[relevant_weights])
        potential_ims[neuron_n].set_data(np.matrix(pot[neuron_n]))

    return [input_spike_raster, weight_lines, potential_ims]

full_diff = get_weight_diffs(weights.shape[1]-1)
max_diff = np.max(full_diff)
min_diff = np.min(full_diff)

print("Setting up plot...", end='')
fig, input_spike_raster, weight_lines, potential_ims = initial_plot()
print("done!")

print("Generating movie...")
n_frames = potential.shape[1]
interval_ms = 1000/60
ani = animation.FuncAnimation(fig, func=update_plots,
        frames=n_frames, interval=interval_ms)
writer = animation.writers['ffmpeg'](bitrate=-1, fps=60)
movie_filename = pickle_filename.replace('.pickle', '.video.mp4')
ani.save(movie_filename)
print("done!")
