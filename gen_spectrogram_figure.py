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
args = parser.parse_args()

input_filename = args.wav_file
input_name = os.path.basename(input_filename).replace(".wav", "")

sound = b2h.loadsound(input_filename)

plt.ion()
plt.figure()
(pxx, freqs, bins, im) = \
        pylab.specgram(x=sound[:, 0].flatten(), NFFT=1024, Fs=sound.samplerate)
n_freqs = len(freqs)
plt.savefig('figures/%s_spectrogram.png' % input_name)
spectral_power = 10 * np.log10(pxx)

plt.figure(figsize=(15.5,5))
plt.imshow(spectral_power, aspect='auto', origin='lower')
plt.xlim([0, 50])
plt.ylim([0, 250])
plt.gca().xaxis.set_major_formatter(plt.NullFormatter())
plt.gca().yaxis.set_major_formatter(plt.NullFormatter())
plt.tick_params(axis='both', which='both', bottom='off', left='off', right='off', top='off')
plt.savefig('spectrogram.png', bbox_inches='tight', dpi=200)
