from __future__ import print_function, division
import numpy as np
import matplotlib.pyplot as plt
import brian2 as b2
import modules.neurons as ns
import modules.synapses as ss

"""
(very) Basic test suite for simulation code.
"""

def test_neurons(neuron_params, connection_params, with_competition):
    """
    Test LIF/threshold adaptation/winner-take-all competition code.
    * Sets up a layer of input neurons and a layer of output neurons
    * Goes through each input neuron in the layer one after the other,
      making each spike a few times.
    * Plots spike rasters of input spikes and output spikes.
    * Plots membrane potential of output neurons with firing threshold drawn as
      a red line.
    """
    # set up input spikes
    n_inputs = 10
    n_spikes_per_neuron = 10
    input_range = np.arange(n_inputs)
    total_spikes = n_inputs * n_spikes_per_neuron
    input_spike_indices = np.repeat(input_range, n_spikes_per_neuron)

    cur_time_ms = 0
    rest_time_ms = 100
    input_spike_times = np.array([])
    for _ in range(n_inputs):
        for _ in range(n_spikes_per_neuron):
            input_spike_times = np.append(input_spike_times, cur_time_ms)
            cur_time_ms += 5
        cur_time_ms += rest_time_ms
    input_spike_times = input_spike_times * b2.ms

    # set up input neurons
    neurons = {}
    neurons['input'] = ns.prespecified_spike_neurons(
        n_neurons=n_inputs,
        spike_indices=input_spike_indices,
        spike_times=input_spike_times
    )

    # set up output neurons
    n_output_neurons = 3
    neurons['output'] = ns.excitatory_neurons(
        n_neurons=n_output_neurons,
        params=neuron_params
    )

    if with_competition:
        # set up inhibitory neurons
        neurons['inhib'] = ns.inhibitory_neurons(
            n_neurons=n_output_neurons,
            params=neuron_params
        )

    # connect input neurons to output neurons
    connections = {}
    connections['input-output'] = ss.nonplastic_synapses(
        neurons['input'],
        neurons['output'],
        connectivity=True, # all-to-all connectivity
        synapse_type='excitatory'
    )
    connections['input-output'].w = '100 * rand()'

    if with_competition:
        # make connections between inhibitory neurons and output neurons

        # output to inhibitory
        connections['output-inhib'] = ss.nonplastic_synapses(
            source=neurons['output'],
            target=neurons['inhib'],
            connectivity='i == j',
            synapse_type='excitatory'
        )
        connections['output-inhib'].w = connection_params['ex-in-w']

        # inhibitory to output
        connections['inhib-output'] = ss.nonplastic_synapses(
            source=neurons['inhib'],
            target=neurons['output'],
            connectivity='i != j',
            synapse_type='inhibitory'
        )
        connections['inhib-output'].w = connection_params['in-ex-w']

    # set up spike and state variable monitors
    monitors = {}
    monitors['input_spikes'] = b2.SpikeMonitor(neurons['input'])
    monitors['output_spikes'] = b2.SpikeMonitor(neurons['output'])
    monitors['output_neurons'] = b2.StateMonitor(
        neurons['output'],
        ['v', 'theta'],
        record=True # record from all neurons
    )

    if with_competition:
        monitors['inhib_spikes'] = b2.SpikeMonitor(neurons['inhib'])

    # run simulation
    net = b2.Network()
    for group in neurons:
        net.add(neurons[group])
    for group in connections:
        net.add(connections[group])
    for group in monitors:
        net.add(monitors[group])
    last_input_spike_time = np.amax(input_spike_times)
    run_time = last_input_spike_time + 50 * b2.ms
    net.run(run_time, report='text')

    # plot results

    plt.ion()
    plt.figure()

    # spikes

    if with_competition:
        n_spike_plots = 3
    else:
        n_spike_plots = 2

    plt.subplot(n_spike_plots, 1, 1)
    plt.title("Input spikes")
    plt.plot(
        monitors['input_spikes'].t/b2.ms,
        monitors['input_spikes'].i,
        'k.',
        markersize=2
    )
    plt.xlabel("Time (ms)")
    plt.ylabel("Neuron no.")
    plt.ylim([-1, n_inputs])

    plt.subplot(n_spike_plots, 1, 2)
    plt.title("Output spikes")
    plt.plot(
        monitors['output_spikes'].t/b2.ms,
        monitors['output_spikes'].i,
        'k.',
        markersize=2
    )
    plt.xlabel("Time (ms)")
    plt.ylabel("Neuron no.")
    plt.ylim([-1, n_output_neurons])

    if with_competition:
        plt.subplot(n_spike_plots, 1, 3)
        plt.title("Inhibitory spikes")
        plt.plot(
            monitors['inhib_spikes'].t/b2.ms,
            monitors['inhib_spikes'].i,
            'k.',
            markersize=2
        )
        plt.xlabel("Time (ms)")
        plt.ylabel("Neuron no.")
        plt.ylim([-1, n_output_neurons])

    plt.tight_layout()

    # membrane potential
    plt.figure()
    plt.suptitle("Output neurons membrane potential (mV)")
    for neuron_n in range(n_output_neurons):
        plt.subplot(n_output_neurons, 1, neuron_n+1)
        plt.plot(
            monitors['output_neurons'].t/b2.ms,
            monitors['output_neurons'].v[neuron_n, :]/b2.mV,
            'k'
        )
        effective_threshold = \
            monitors['output_neurons'].theta[neuron_n, :] / b2.mV \
            + neuron_params['v_thresh_e'] / b2.mV \
            - neuron_params['offset'] / b2.mV
        plt.plot(
            monitors['output_neurons'].t/b2.ms,
            effective_threshold,
            'r'
        )

        plt.ylabel("N. %d" % neuron_n)
        plt.xlim([0, run_time / b2.ms])
    plt.xlabel("Time (ms)")

    return (neurons, connections, monitors, net)

def test_stdp_curve(connection_params):
    """
    Plot STDP curve.
    Based on code in Brian user manual,
    "Introduction to Brian 2 part 2: Synapses".
    """
    n_neurons = 100
    tmax = 50 * b2.ms

    neurons = {}

    # set up presynaptic neurons,
    # spiking sequentially from first to last in order
    neurons['presyn'] = b2.NeuronGroup(
            n_neurons,
            'tspike:second',
            threshold='t>tspike',
            refractory=100*b2.ms
    )
    neurons['presyn'].tspike = 'i / (n_neurons - 1.0) * tmax'

    # set up postsynaptic neurons,
    # spiking from last to first
    neurons['postsyn'] = b2.NeuronGroup(
            n_neurons,
            'tspike:second\nge:siemens',
            threshold='t>tspike',
            refractory=100*b2.ms
    )
    neurons['postsyn'].tspike = \
        '(n_neurons -  1.0 - i) / (n_neurons - 1) * tmax'

    # each presynpatic neuron connects to one postsynaptic neuron
    # between all pairs of pre- and post-synaptic neurons,
    # we cover a range of positive and negative spike time differences

    synapses = ss.stdp_ex_synapses(
        neurons['presyn'],
        neurons['postsyn'],
        connectivity='i==j',
        params=connection_params
    )
    initial_weights = connection_params['wmax_ee'] / 2
    synapses.w = initial_weights

    # run simulation
    net = b2.Network()
    net.add(neurons['presyn'])
    net.add(neurons['postsyn'])
    net.add(synapses)
    run_time = tmax + 1 * b2.ms
    net.run(run_time, report='text')

    # plot weight diff
    spike_time_diff = neurons['postsyn'].tspike - neurons['presyn'].tspike
    weight_diff = synapses.w - initial_weights
    plt.ion()
    plt.figure(figsize=(6,4.5))
    plt.plot(spike_time_diff/b2.ms, weight_diff, 'k', linewidth=2)
    plt.xlabel('Spike time difference (ms)')
    plt.ylabel('Weight change')
    plt.axhline(0, ls='-', c='k')
    plt.axvline(0, ls='-', c='k')
    plt.grid()
    plt.tight_layout()
    plt.savefig('figures/skewedstdp.pdf', bbox_inches='tight')

    monitors = None
    return (neurons, synapses, monitors, net)
