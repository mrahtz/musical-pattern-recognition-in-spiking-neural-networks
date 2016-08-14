import os.path
import pickle
import os
import numpy as np
from struct import unpack
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import brian2 as b2
import math

def save_figures(name):
    print("Saving figures...")
    figs = plt.get_fignums()
    for fig in figs:
        plt.figure(fig)
        os.system('rm -f figures/%s_fig_%d.pdf' % (name, fig))
        plt.savefig('figures/%s_fig_%d.png' % (name, fig))
    print("done!")

def set_xlims(xlim):
    for fig_n in plt.get_fignums():
        plt.figure(fig_n)
        fig_set_xlims(xlim)

def fig_set_xlims(xlim):
    for ax in plt.gcf().get_axes():
        ax.set_xlim(xlim)

def plot_state_var(monitor, state_vals, firing_neurons, title):
    plt.figure()
    n_firing_neurons = len(firing_neurons)
    min_val = float('inf')
    max_val = -float('inf')
    for i, neuron_n in enumerate(firing_neurons):
        plt.subplot(n_firing_neurons, 1, i+1)
        neuron_val = state_vals[neuron_n, :]
        neuron_val_min = np.amin(neuron_val)
        if neuron_val_min < min_val:
            min_val = neuron_val_min
        neuron_val_max = np.amax(neuron_val)
        if neuron_val_max > max_val:
            max_val = neuron_val_max
        plt.plot(monitor.t, neuron_val)
        plt.ylabel("N. %d" % neuron_n)
    for i, _ in enumerate(firing_neurons):
        plt.subplot(n_firing_neurons, 1, i+1)
        plt.ylim([min_val, max_val])
        plt.yticks([min_val, max_val])
    for i in range(len(firing_neurons)-1):
        plt.subplot(n_firing_neurons, 1, i+1)
        plt.xticks([])
    plt.subplot(n_firing_neurons, 1, 1)
    plt.title(title)

def analyse_note_responses(spike_indices, spike_times,
                           note_length, n_notes, from_time, to_time):
    max_spikes = 0
    for neuron_n in set(spike_indices):
        relevant_spike_times = \
            spike_times[spike_indices == neuron_n]
        relevant_spike_times = \
            [t for t in relevant_spike_times if t > from_time and t < to_time]
        n_spikes = len(relevant_spike_times)
        if n_spikes > max_spikes:
            max_spikes = n_spikes

    favourite_notes = {}
    for neuron_n in set(spike_indices):
        relevant_spike_times = \
            spike_times[spike_indices == neuron_n]
        relevant_spike_times = \
            [t for t in relevant_spike_times if t > from_time and t < to_time]
        relevant_spike_times = np.array(relevant_spike_times)
        n_spikes = len(relevant_spike_times)
        if n_spikes == 0 or n_spikes < 0.2 * max_spikes:
            continue

        note_bin_firings = np.floor(relevant_spike_times / note_length).astype(int)
        note_responses = np.mod(note_bin_firings, n_notes)
        most_common_note = np.argmax(np.bincount(note_responses))
        n_misfirings = sum(note_responses != most_common_note)
        misfirings_pct = float(n_misfirings) / len(note_responses) * 100
        print("Neuron %d likes note %d, %.1f%% mistakes" \
            % (neuron_n, most_common_note, misfirings_pct))
        favourite_notes[neuron_n] = most_common_note

    return favourite_notes

def order_spikes_by_note(spike_indices, spike_times, favourite_notes):
    # favourite_notes is a dictionary mapping neuron number to which
    # note it fires in response to
    # e.g. favourite_notes[3] == 2 => neuron 3 fires in response to note 2
    # extract spike times of the neurons which actually fire consistently
    relevant_times = [time
        for (spike_n, time) in enumerate(spike_times)
        if spike_indices[spike_n] in favourite_notes
    ]
    # extract the neuron indices corresponding to those spike times
    relevant_indices = [i for i in spike_indices if i in favourite_notes]

    # generate a list of which neuron in favourite_notes
    # each spike corresponds to, sorted by note order
    # (we need to do it like this instead of just plotting times against
    #  favourite_notes[spike_index] in case more than one neuron responds to
    #  each note)
    # first of all we need to sort the list by note order
    fav_note_neurons = np.array(favourite_notes.keys())
    fav_note_notes = np.array(favourite_notes.values())
    neurons_ordered_by_note = fav_note_neurons[np.argsort(fav_note_notes)]
    # now we figure out which index of that list each spike corresponds to
    neurons_ordered_by_note_indices = \
        [np.argwhere(neurons_ordered_by_note == i)[0][0]
         for i in relevant_indices]

    return (relevant_times, neurons_ordered_by_note_indices,
            neurons_ordered_by_note)


def ordered_spike_raster(spike_indices, spike_times, favourite_notes):
    (relevant_times, neurons_ordered_by_note_indices,
     neurons_ordered_by_note) = \
        order_spikes_by_note(spike_indices, spike_times, favourite_times)

    plt.plot(relevant_times, neurons_ordered_by_note_indices,
             'k.', markersize=2)
    # of course, the y values will still correspond to indices of
    # neurons_ordered_by_note, whereas what we actually want to show is which
    # neuron is firing
    # so we need to map from note number to number
    n_notes = len(neurons_ordered_by_note)
    plt.yticks(
        range(n_notes),
        [str(neurons_ordered_by_note[i]) for i in range(n_notes)]
    )
    plt.ylim([-1, n_notes])
    plt.grid()

def plot_weight_diff(connections, weight_monitor, from_t=0, to_t=-1, newfig=True):
    if newfig:
        plt.figure()
    else:
        plt.clf()
    neurons = set(connections.j)
    n_neurons = len(neurons)

    plt.subplot(n_neurons, 1, 1)
    plt.title('Weight adjustments for each neuron')

    from_i = np.where(weight_monitor.t >= from_t * b2.second)[0][0]
    if to_t == -1:
        to_i = -1
    else:
        to_i = np.where(weight_monitor.t <= to_t * b2.second)[0][-1]

    weight_diffs = weight_monitor.w[:, to_i] - weight_monitor.w[:, from_i]
    max_diff = np.max(weight_diffs)
    min_diff = np.min(weight_diffs)

    for neuron_n in neurons:
        plt.subplot(n_neurons, 1, neuron_n+1)
        relevant_weights = connections.j == neuron_n
        diff = weight_diffs[relevant_weights]
        plt.plot(diff)
        plt.ylim([min_diff, max_diff])
        plt.yticks([])
        plt.xticks([])
        plt.ylabel("%d" % neuron_n)

def plot_weights(connections):
    plt.figure()
    for i in range(16):
        plt.subplot(16, 1, i+1)
        relevant_weights = connections['input-layer1e'].j == i
        weights = np.array(connections['input-layer1e'].w)[relevant_weights]
        plt.plot(weights)
        plt.ylim([0, 1])
