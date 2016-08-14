#!/usr/bin/env python

"""
Set up and run a simulation for a spiking neural network with:
* An input layer of excitatory neurons
* An output layer of pairs of excitatory and inhibitory neurons set up for
  competitive winner-take-all dynamics
* Plasticity simulated using spike-timing-dependent plasticity (STDP)
"""

from __future__ import print_function, division
import os.path
import pickle
import brian2 as b2
import numpy as np
import matplotlib.pyplot as plt

import modules.analysis as analysis_mod
import modules.synapses as synapse_mod
import modules.neurons as neuron_mod
import modules.params as param_mod
import modules.tests as test_mod

def load_input(run_params):
    """
    Load spikes to be used for input neurons.
    """

    pickle_filename = run_params['input_spikes_filename']
    with open(pickle_filename, 'rb') as pickle_file:
        (input_spike_times, input_spike_indices) = pickle.load(pickle_file)
    input_spike_times = input_spike_times * b2.second

    spikes = {}
    spikes['indices'] = input_spike_indices
    spikes['times'] = input_spike_times

    return spikes

def init_neurons(input_spikes, layer_n_neurons, neuron_params):
    """
    Initialise neurons.
    """
    neurons = {}

    # We use 1025 neurons in gen_audio_spikes.py, but in the end there are only
    # spikes on about the first half of these. We hard-code this here rather
    # than, say, just instantiating as many neurons as the highest spike index
    # from gen_audio_spikes, so that we can re-use the same initial random
    # weight matrix even if the spike indices change slightly.
    n_inputs = 575
    neurons['input'] = neuron_mod.prespecified_spike_neurons(
        n_neurons=n_inputs,
        spike_indices=input_spikes['indices'],
        spike_times=input_spikes['times']
    )

    # excitatory neurons
    neurons['layer1e'] = neuron_mod.excitatory_neurons(
        n_neurons=layer_n_neurons,
        params=neuron_params
    )
    # load saved threshold adjustments
    if neuron_params['theta_file'] is not None:
        print("Loading saved theta values")
        pickle_obj = pickle.load(neuron_params['theta_file'])
        neurons['layer1e'].theta  = pickle_obj * b2.mV

    # inhibitory neurons
    neurons['layer1i'] = neuron_mod.inhibitory_neurons(
        n_neurons=layer_n_neurons,
        params=neuron_params
    )

    return neurons

def save_weights(weights, filename):
    """
    Save plastic synaptic weights to a pickle file.
    """
    with open(filename, 'wb') as pickle_file:
        pickle.dump(weights, pickle_file)

def save_theta(neurons, filename):
    """
    Save neuron threshold adaptation to a pickle file.
    """
    theta = neurons['layer1e'].theta / b2.mV
    with open(filename, 'wb') as pickle_file:
        pickle.dump(theta, pickle_file)

def init_connections(neurons, connection_params):
    """
    Initialise synaptic connections between different layers of neurons.
    """

    connections = {}

    # input to layer 1 connections

    source = neurons['input']
    target = neurons['layer1e']
    connections['input-layer1e'] = synapse_mod.stdp_ex_synapses(
        source=source,
        target=target,
        connectivity=True, # all-to-all connectivity
        params=connection_params
    )

    # load saved weights
    init_weights_filename = 'input-layer1e-init-weights.pickle'
    if connection_params['weight_file'] is not None:
        print("Loading specified saved weights")
        pickle_obj = pickle.load(connection_params['weight_file'])
        connections['input-layer1e'].w = np.array(pickle_obj)
    elif os.path.exists(init_weights_filename):
        print("Loading saved random weights")
        with open(init_weights_filename, 'rb') as pickle_file:
            pickle_obj = pickle.load(pickle_file)
            connections['input-layer1e'].w = pickle_obj
    else:
        print("Generating new initial random weights")
        connections['input-layer1e'].w = 'rand() * 0.4'
        save_weights(
            np.array(connections['input-layer1e'].w),
            init_weights_filename
        )

    # excitatory to inhibitory
    connections['layer1e-layer1i'] = synapse_mod.nonplastic_synapses(
        source=neurons['layer1e'],
        target=neurons['layer1i'],
        connectivity='i == j',
        synapse_type='excitatory'
    )
    connections['layer1e-layer1i'].w = connection_params['ex-in-w']

    # inhibitory to excitatory
    connections['layer1i-layer1e'] = synapse_mod.nonplastic_synapses(
        source=neurons['layer1i'],
        target=neurons['layer1e'],
        connectivity='i != j',
        synapse_type='inhibitory'
    )
    connections['layer1i-layer1e'].w = connection_params['in-ex-w']

    return connections

def init_monitors(neurons, connections, monitor_params):
    """
    Initialise Brian objects monitoring state variables in the network.
    """

    monitors = {
        'spikes': {},
        'neurons': {},
        'connections': {}
    }

    for layer in ['input', 'layer1e']:
        monitors['spikes'][layer] = b2.SpikeMonitor(neurons[layer])

    if 'monitors_dt' not in monitor_params:
        timestep = None
    else:
        timestep = monitor_params['monitors_dt']

    monitors['neurons']['layer1e'] = b2.StateMonitor(
        neurons['layer1e'],
        ['v', 'ge', 'max_ge', 'theta'],
        # record=True is currently broken for standalone simulations
        record=range(len(neurons['layer1e'])),
        dt=timestep
    )

    conn = connections['input-layer1e']
    n_connections = len(conn.target) * len(conn.source)
    monitors['connections']['input-layer1e'] = b2.StateMonitor(
        connections['input-layer1e'],
        ['w', 'post', 'pre'],
        record=range(n_connections),
        dt=timestep
    )

    return monitors

def run_simulation(run_params, neurons, connections, monitors, run_id):
    """
    Run the simulation using all the objects created so far.
    """

    net = b2.Network()
    for group in neurons:
        net.add(neurons[group])
    for connection in connections:
        net.add(connections[connection])
    for mon_type in monitors:
        for neuron_group in monitors[mon_type]:
            net.add(monitors[mon_type][neuron_group])

    net.run(run_params['run_time'], report='text')

    return net

def analyse_results(monitors, connections, analysis_params):
    """
    Analyse results of simulation and plot graphs.
    """

    if len(monitors['spikes']['layer1e']) == 0:
        print("No spikes detected; not analysing")
        return

    plt.ion()
    analysis_mod.plot_input_output_spikes(monitors)
    if analysis_params['classify']:
        analysis_mod.classify_tibicen_responses(monitors['spikes']['layer1e'])

def main_simulation(params):
    """
    Initialise simulation objects and run the simulation.
    """
    (neuron_params, connection_params, monitor_params, run_params,
     analysis_params) = params

    spike_filename = os.path.basename(run_params['input_spikes_filename'])
    run_id = spike_filename.replace('.pickle', '')
    if not run_params['from_paramfile']:
        param_mod.record_params(params, run_id)
    input_spikes = load_input(run_params)

    input_end_time = np.ceil(np.amax(input_spikes['times']))
    if 'run_time' not in run_params:
        run_params['run_time'] = input_end_time

    if not run_params['no_standalone']:
        if os.name == 'nt':
            build_dir = 'C:\\temp\\'
        else:
            build_dir = '/tmp/'
        build_dir += run_id
        b2.set_device('cpp_standalone', directory=build_dir)

    print("Initialising neurons...")
    neurons = init_neurons(
        input_spikes, run_params['layer_n_neurons'],
        neuron_params
    )
    print("done!")

    print("Initialising connections...")
    connections = init_connections(
        neurons,
        connection_params
    )
    print("done!")

    print("Initialising monitors...")
    monitors = init_monitors(neurons, connections, monitor_params)
    print("done!")

    print("Running simulation...")
    net = run_simulation(run_params, neurons, connections, monitors, run_id)
    print("done!")

    analyse_results(
        monitors,
        connections,
        analysis_params
    )

    if connection_params['save_weights']:
        print("Saving weights and theta...")

        weight_copy = np.copy(connections['input-layer1e'].w)
        # zero out weights which haven't changed and therefore appear to be
        # irrelevant for our stimuli (to make sure that random firing on these
        # synapses in future test stimuli isn't counted)
        w = monitors['connections']['input-layer1e'].w
        unchanged_weights = w[:, 0] == w[:, -1]
        weight_copy[unchanged_weights] = 0
        # zero out the weights of neurons that didn't respond to the stimuli
        # (these neurons shouldn't be involved in classification of future test
        # stimuli)
        # these numbers were manually hardcoded based on the results of the
        # training run
        firing_neurons = [11, 13, 15]
        nonfiring_neuron_weights = np.in1d(
            connections['input-layer1e'].j,
            firing_neurons,
            invert=True
        )
        weight_copy[nonfiring_neuron_weights] = 0
        save_weights(weight_copy, 'input-layer1e-weights-%s.pickle' % run_id)

        save_theta(neurons, 'theta-%s.pickle' % run_id)

    return (neurons, connections, monitors, net)

def main():
    """
    Get parameters parsed on command line, and use them to decide whether to run
    the test suite or actually run the simulate.
    """

    np.random.seed(1)

    params = param_mod.get_params()
    (neuron_params, connection_params, monitor_params, run_params,
     analysis_params) = params

    if run_params['test_stdp_curve']:
        neurons, connections, monitors, net = \
            test_mod.test_stdp_curve(connection_params)
    elif run_params['test_neurons']:
        neurons, connections, monitors, net = test_mod.test_neurons(
            neuron_params,
            connection_params,
            with_competition=False
        )
    elif run_params['test_competition']:
        neurons, connections, monitors, net = test_mod.test_neurons(
            neuron_params,
            connection_params,
            with_competition=True
        )
    else:
        neurons, connections, monitors, net = main_simulation(params)

    return (neuron_params, connection_params, monitor_params, run_params, \
        neurons, connections, monitors, net)

(n_p, c_p, m_p, r_p, ns, cs, ms, n) = main()
