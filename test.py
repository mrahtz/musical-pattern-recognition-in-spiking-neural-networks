from brian import *
from brian.hears import *

#sound = whitenoise(100*ms).ramp()
#sound.level = 50*dB
sound = loadsound('test_inputs/scale_0.5_s.wav')

### example of a bank of bandpass filter ################
nchannels = 100
center_frequencies = linspace(200*Hz, 2000*Hz, nchannels)  #center frequencies
#bw = linspace(5*Hz, 60*Hz, nchannels)  #bandwidth of the filters
bw = 100 * Hz
# The maximum loss in the passband in dB. Can be a scalar or an array of length
# nchannels
gpass = 0.1*dB
# The minimum attenuation in the stopband in dB. Can be a scalar or an array
# of length nchannels
gstop = 10.*dB
#arrays of shape (2 x nchannels) defining the passband frequencies (Hz)
passband = vstack((center_frequencies-bw/2, center_frequencies+bw/2))
#arrays of shape (2 x nchannels) defining the stopband frequencies (Hz)
stopband = vstack((center_frequencies-1.1*bw, center_frequencies+1.1*bw))

filterbank = IIRFilterbank(sound, nchannels, passband, stopband, gpass, gstop,
                           'bandstop', 'cheby1')
filterbank_mon = filterbank.process()

figure()
ion()
imshow(filterbank_mon.T, aspect='auto')
show()
