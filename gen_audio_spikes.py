#!/usr/bin/env python

from __future__ import print_function, division
import brian2 as b2
import brian2.hears as b2h
import matplotlib.pyplot as plt
import numpy as np
import os.path
import os
import pickle
import pylab
import argparse
from scipy import ndimage

def preprocess_sound(sound):
        plt.figure()
        plt.subplot(2, 1, 1)
        (pxx, freqs, bins, im) = pylab.specgram(
            x=sound[:, 0].flatten(), NFFT=2048, Fs=sound.samplerate
        )
        n_freqs = len(freqs)
        spectral_power = 10 * np.log10(pxx)

        min_power = np.amin(spectral_power)
        max_power = np.amax(spectral_power)
        power_range = max_power - min_power
        spectral_power_normalised = (spectral_power - min_power)/power_range
        plt.imshow(spectral_power_normalised, aspect='auto', origin='lower')
        plt.colorbar()

        spectral_input = np.copy(spectral_power_normalised)
        per = np.percentile(spectral_input, 90)
        spectral_input[spectral_input < per] = 0

        plt.subplot(2, 1, 2)
        plt.imshow(spectral_input, aspect='auto', origin='lower')

        dt = (bins[1] - bins[0]) * b2.second
        sound_input = b2.TimedArray(1.2*spectral_input.T, dt=dt)

        return sound_input

def generate_spikes(wav_filename):
    sound = b2h.loadsound(wav_filename)
    run_time = sound.duration
    sound_input = preprocess_sound(sound)
    n_freqs = sound_input.values.shape[1]


    eqs = '''
    dv/dt = (I-v)/(10*ms) : 1
    I = intensity*sound_input(t, i): 1
    '''

    n_spikes_ok = False
    intensity = 1

    while not n_spikes_ok:
        anf = b2.NeuronGroup(
            N=n_freqs,
            model=eqs,
            reset='v=0',
            threshold='v>1',
            method='euler' # automatically suggested by Brian
        )
        m = b2.SpikeMonitor(anf)

        print("Building and running simulation...")
        net = b2.Network()
        net.add(anf)
        net.add(m)
        net.run(run_time, report='stdout')
        print("Done!")

        # only count spikes in the range where we know signal content lies:
        # neuron numbers 150 to 400
        n_spikes = sum((m.i > 150) & (m.i < 400))
        print("For input %s, intensity %.3f, got %d spikes" %
                (wav_filename, intensity, n_spikes))

        # aim for between 5,000 and 6,000 spikes
        tweak_factor = 1.01
        if n_spikes < 5000:
            intensity *= tweak_factor
        elif n_spikes > 6000:
            intensity /= tweak_factor
        else:
            n_spikes_ok = True

        if n_spikes_ok:
            print("Got the right number of spikes; moving on")
        else:
            print("Not yet the right number of spikes; adjusting intensity" \
                + " and re-running")

    return m.i, m.t, run_time

def sim(input_wav_filenames, output_spike_filename):
    spike_indices_all = np.array([])
    spike_times_all = np.array([])
    cur_time = 0

    for input_n, input_filename in enumerate(input_wav_filenames):
        input_name = os.path.basename(input_filename).replace(".wav", "")

        spike_indices, spike_times, run_time = generate_spikes(input_filename)

        spike_indices_all = np.append(spike_indices_all, spike_indices)
        spike_times_all = np.append(
            spike_times_all,
            cur_time+spike_times/b2.second
        )
        cur_time += run_time / b2.second

    plt.figure()
    plt.plot(spike_times_all, spike_indices_all, 'k.', markersize=2)

    print("Writing spike files...")
    pickle_file = output_spike_filename
    with open(pickle_file, 'wb') as f:
        pickle.dump((spike_times_all, spike_indices_all), f)
    print("done!")

train_filenames = [
    'tibicen_train/bh.wav',
    'tibicen_train/fl.wav',
    'tibicen_train/jp.wav'
]

test_filenames = [
    'tibicen_test/1.wav', 'tibicen_test/2.wav', 'tibicen_test/3.wav',
    'tibicen_test/4.wav', 'tibicen_test/5.wav', 'tibicen_test/6.wav',
    'tibicen_test/7.wav', 'tibicen_test/8.wav', 'tibicen_test/9.wav',
    'tibicen_test/10.wav', 'tibicen_test/11.wav', 'tibicen_test/12.wav',
    'tibicen_test/13.wav', 'tibicen_test/14.wav', 'tibicen_test/15.wav',
    'tibicen_test/16.wav', 'tibicen_test/17.wav', 'tibicen_test/18.wav',
    'tibicen_test/19.wav', 'tibicen_test/20.wav', 'tibicen_test/lq1.wav',
    'tibicen_test/lq2.wav', 'tibicen_test/lq3.wav', 'tibicen_test/lq4.wav',
    'tibicen_test/lq5.wav', 'tibicen_train/bh.wav', 'tibicen_train/fl.wav',
    'tibicen_train/jp.wav'
]

parser = argparse.ArgumentParser()
parser.add_argument('--train', action='store_true')
parser.add_argument('--test', action='store_true')
args = parser.parse_args()

if args.train:
    sim(
        input_wav_filenames=train_filenames,
        output_spike_filename='tibicen_train/tibicen_train.pickle'
    )
if args.test:
    sim(
        input_wav_filenames=test_filenames,
        output_spike_filename='tibicen_test/tibicen_test_train.pickle'
    )
