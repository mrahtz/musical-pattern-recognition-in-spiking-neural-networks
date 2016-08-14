from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import brian2 as b2

def plot_input_output_spikes(monitors):
    plt.figure()

    xticks = np.arange(0, 85, 3)

    plt.subplot(2, 1, 1)
    plt.title("Input spikes")
    plt.plot(
        monitors['spikes']['input'].t/b2.second,
        monitors['spikes']['input'].i,
        'k.',
        markersize=2
    )
    plt.ylabel("Neuron no.")
    plt.xticks(xticks)
    plt.grid()

    plt.subplot(2, 1, 2)
    plt.title("Output spikes")
    plt.plot(
        monitors['spikes']['layer1e'].t/b2.second,
        monitors['spikes']['layer1e'].i,
        'k.',
        markersize=2
    )
    plt.ylim([-1, max(monitors['spikes']['layer1e'].i)+1])
    plt.xticks(xticks)
    plt.grid()
    plt.ylabel("Neuron no.")

    plt.xlabel("Time (seconds)")
    plt.tight_layout()

    plt.savefig('input_output_spikes.png', dpi=300, bbox_inches='tight')

def classify_tibicen_responses(spike_monitor):
    neuron_n_to_species_map = {
        15: 'BH',
        11: 'FL',
        13: 'JP'
    }

    track_length = 3 * b2.second
    n_tracks = 28

    track_n = 1
    t = 0 * b2.second
    while t < n_tracks * track_length:
        time_select = (spike_monitor.t > t) & (spike_monitor.t < t+3*b2.second)
        firing_indices = np.array(spike_monitor.i)[time_select]
        firing_species = [neuron_n_to_species_map[i] for i in firing_indices]
        counts = Counter(firing_species)
        print("Spikes for track %d:" % track_n)
        for species_type in counts.keys():
            print("  %s neuron: %d" % (species_type, counts[species_type]))
        t += track_length
        track_n += 1
