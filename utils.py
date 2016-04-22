import os.path
import pickle
import os
import numpy as np
from struct import unpack
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import brian2 as b2
import math

def get_labeled_data(picklename, bTrain = True):
    """Read input-vector (image) and target class (label, 0-9) and return
       it as list of tuples.
    """
    if os.path.isfile('%s.pickle' % picklename):
        data = pickle.load(open('%s.pickle' % picklename))
    else:
        # Open the images with gzip in read binary mode
        if bTrain:
            images = open('train-images.idx3-ubyte','rb')
            labels = open('train-labels.idx1-ubyte','rb')
        else:
            images = open('t10k-images.idx3-ubyte','rb')
            labels = open('t10k-labels.idx1-ubyte','rb')
        # Get metadata for images
        images.read(4)  # skip the magic_number
        number_of_images = unpack('>I', images.read(4))[0]
        rows = unpack('>I', images.read(4))[0]
        cols = unpack('>I', images.read(4))[0]
        # Get metadata for labels
        labels.read(4)  # skip the magic_number
        N = unpack('>I', labels.read(4))[0]

        N = number_of_images = 4

        if number_of_images != N:
            raise Exception('number of labels did not match the number of images')
        # Get the data
        x = np.zeros((N, rows, cols), dtype=np.uint8)  # Initialize numpy array
        y = np.zeros((N, 1), dtype=np.uint8)  # Initialize numpy array
        for i in xrange(N):
            if i % 1000 == 0:
                print("i: %i" % i)
            x[i] = [[unpack('>B', images.read(1))[0] for unused_col in xrange(cols)]  for unused_row in xrange(rows) ]
            y[i] = unpack('>B', labels.read(1))[0]

        data = {'x': x, 'y': y, 'rows': rows, 'cols': cols}
        pickle.dump(data, open("%s.pickle" % picklename, "wb"))
    return data

def get_2d_input_weights(n_input, n_e, connections):
    name = 'XeAe'
    weight_matrix = np.zeros((n_input, n_e))
    n_e_sqrt = int(np.sqrt(n_e))
    n_in_sqrt = int(np.sqrt(n_input))
    num_values_col = n_e_sqrt*n_in_sqrt
    num_values_row = num_values_col
    rearranged_weights = np.zeros((num_values_col, num_values_row))
    connMatrix = np.zeros((n_input, n_e))
    connMatrix[connections[name].i, connections[name].j] = connections[name].w
    weight_matrix = np.copy(connMatrix)

    for i in xrange(n_e_sqrt):
        for j in xrange(n_e_sqrt):
                rearranged_weights[i*n_in_sqrt : (i+1)*n_in_sqrt, j*n_in_sqrt : (j+1)*n_in_sqrt] = \
                    weight_matrix[:, i + j*n_e_sqrt].reshape((n_in_sqrt, n_in_sqrt))
    return rearranged_weights

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
                           note_length, n_notes, from_time):
    max_spikes = 0
    for neuron_n in set(spike_indices):
        relevant_spike_times = \
            spike_times[spike_indices == neuron_n]
        relevant_spike_times = \
            [t for t in relevant_spike_times if t > from_time]
        n_spikes = len(relevant_spike_times)
        if n_spikes > max_spikes:
            max_spikes = n_spikes

    favourite_notes = {}
    for neuron_n in set(spike_indices):
        relevant_spike_times = \
            spike_times[spike_indices == neuron_n]
        relevant_spike_times = \
            [t for t in relevant_spike_times if t > from_time]
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

def ordered_spike_raster(spike_indices, spike_times, favourite_notes):
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

    # generate a list of which note each spike corresponds to
    spike_notes = [favourite_notes[i] for i in relevant_indices]
    plt.plot(relevant_times, spike_notes, 'k.', markersize=2)
    # of course, the y values will be the notes, whereas we want to show
    # which neurons are actually firing
    # so we need to map from note number to number
    plt.yticks(
        favourite_notes.values(),
        [str(n) for n in favourite_notes.keys()]
    )
    max_note = max(favourite_notes.values())
    plt.ylim([-1, max_note+1])
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

def set_titles(title):
    for fig_n in plt.get_fignums():
        plt.figure(fig_n)
        plt.title(title)

def ani_weight_diff(connections, weight_monitor, speed, interval=0, from_t=0, to_t=-1):
    neurons = set(connections.j)
    n_neurons = len(neurons)

    weight_diffs = weight_monitor.w[:, -1] - weight_monitor.w[:, 0]
    max_diff = np.max(weight_diffs)
    min_diff = np.min(weight_diffs)

    fig, axes = plt.subplots(nrows=n_neurons)
    def plot(ax, i):
        neuron_n = i
        relevant_weights = connections.j == neuron_n
        diff = weight_diffs[relevant_weights]
        line = ax.plot(diff)[0]
        ax.set_yticks([])
        ax.set_xticks([])
        ax.set_ylim([min_diff, max_diff])
        ax.set_ylabel("N%d" % neuron_n)
        return line

    lines = [plot(ax, i) for i, ax in enumerate(axes)]

    from_i = np.where(weight_monitor.t >= from_t * b2.second)[0][0]
    if to_t == -1:
        to_i = weight_monitor.w.shape[1] - 1
    else:
        to_i = np.where(weight_monitor.t <= to_t * b2.second)[0][-1]
    print("From index %d to %d" % (from_i, to_i))

    def animate(i):
        i *= speed
        i += from_i
        time = weight_monitor.t[i] / b2.second
        print('Time %.1f seconds' % time)
        weight_diffs = weight_monitor.w[:, i] - weight_monitor.w[:, 0]
        for neuron_n, line in enumerate(lines):
            relevant_weights = connections.j == neuron_n
            line.set_ydata(weight_diffs[relevant_weights])
        return lines

    n_frames = int(math.floor((to_i - from_i + 1)/speed))
    ani = animation.FuncAnimation(fig, animate, frames=n_frames,
                                  interval=interval, blit=False, repeat=False)
    return ani
