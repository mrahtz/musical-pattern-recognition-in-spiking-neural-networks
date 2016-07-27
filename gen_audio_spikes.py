#!/usr/bin/env python

from __future__ import print_function, division
import brian2 as b2
import brian2.hears as b2h
import matplotlib.pyplot as plt
import numpy as np
import os.path
import pickle
import pylab
import argparse
from scipy import ndimage

parser = argparse.ArgumentParser()
parser.add_argument('wav_file')
parser.add_argument('--interactive', action='store_true')
args = parser.parse_args()

input_filename = args.wav_file
input_name = os.path.basename(input_filename).replace(".wav", "")

b2.set_device(
    'cpp_standalone',
    directory=('/tmp/brian_standalone_%s' % input_name)
)

sound = b2h.loadsound(input_filename)

if args.interactive:
    plt.ion()

plt.figure()
(pxx, freqs, bins, im) = \
        pylab.specgram(x=sound[:, 0].flatten(), NFFT=1024, Fs=sound.samplerate)
n_freqs = len(freqs)
plt.savefig('figures/%s_spectrogram.png' % input_name)
spectral_power = 10 * np.log10(pxx)

min_power = np.amin(spectral_power)
max_power = np.amax(spectral_power)
power_range = max_power - min_power
spectral_power_normalised = (spectral_power - min_power)/power_range

# emphasise components extending horizontally, in time
kernel_len = 4
kernel = np.ones((1, kernel_len))
spectral_input = ndimage.convolve(spectral_power_normalised, kernel)
spectral_input[spectral_input < 0.7*kernel_len] = 0

plt.figure()
plt.imshow(spectral_input, aspect='auto', origin='lower')
plt.savefig('figures/%s_spectral_input.png' % input_name)

dt = (bins[1] - bins[0]) * b2.second
sound_input = b2.TimedArray(spectral_input.T, dt=dt)

eqs = '''
dv/dt = (I-v)/(10*ms) : 1
I = sound_input(t, i): 1
'''
anf = b2.NeuronGroup(N=n_freqs, model=eqs, reset='v=0', threshold='v>1')
m = b2.SpikeMonitor(anf)

print("Building and running simulation...")
b2.run(sound.duration, report='stdout')
print("Done!")

print("Writing spike files...")
indices = np.array(m.i)
times = np.array(m.t)
pickle_file = 'test_inputs/' + input_name + '.pickle'
with open(pickle_file, 'wb') as f:
    pickle.dump((times, indices), f)
print("done!")

plt.figure()
plt.plot(m.t/b2.second, m.i, 'k.', markersize=1)
plt.ylim([0, n_freqs])
plt.savefig('figures/spectrogram_%s_spikes.png' % input_name)
