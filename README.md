# Musical Pattern Recognition in Spiking Neural Networks

This repository contains the source code for my final-year project in my BEng
degree, 'Musical Pattern Recognition in Spiking Neural Networks'. The title of
the project should hopefully be self-descriptive as to the purpose of the
project.

As seems to be the case with pretty much all final-year projects, only a small
portion of what was originally intended was actually achieved. This code
implements the first layer of the model proposed in the report: a layer of
spiking neurons which can differentiate between individual notes in a series of
simple monophonic test audio sequences.

The architecture of the network comes from Peter Diehl's model in [Unsupervised
learning of digit recognition using spike-timing-dependent
plasticity](http://dx.doi.org/10.3389/fncom.2015.00099).

## Requirements

Needs:

* Python
* Brian 2 (http://briansimulator.org)
  * (This code was implemented using Brian 2.0b4. Some changes may be necessary
    for later versions.)
* NumPy
* matplotlib
* ffmpeg for animation generation

## Files

* `test_inputs` contains a number of test sequences in `.wav` files, generated
  by `gen_test_inputs.py` using the Mingus music library and the Fluid R3
  SoundFont (https://musescore.org/en/handbook/soundfont). The `.pickle` files
  are spike-coded representations of these sequences in `.pickle` files,
  generated by `gen_audio_spikes.py`.
  * (`comptine*.wav` is a test sequence based on the first few chords of Yann
    Tiersen's 'Comptine d'un autre été', generated by a script not supplied.)
* `stdp_sounds.py` is the main simulation script. See `params/*_cmdline.txt` for
  examples of good parameters to run it with for each test sequence. The
  simulation script will record the parameters used in `params`, save results in
  `results`, and save figures generated in `figures`.
* `modules` contains Python modules used for the simulation.
* `input-layer1e-weights.pickle` is a cache of the random initial synaptic
  weights used in the simulation, for repeatability.
* `prepare_movie_with_sound.sh` uses `write_movie.py` and the results of a
  single simulation (as stored in `results/monitors_<test sequence
  name>.pickle`) to generate an animation showing the input spikes, neuron
  membrane potentials and weight changes over time, then combine it with the
  corresponding audio track using `ffmpeg`. Examples of these animations are
  included in `results`.

## Running Simulation

To generate spikes for an audio file:
```
$ ./gen_audio_spikes.py test_inputs/two_notes_0.5_s.wav
...
Writing spike files...
done!
```

To then run a simulation:
```
$ python -i stdp_sounds.py --input_spikes_file test_inputs/two_notes_0.5_s.pickle
...
done!
<observe pretty figures>
```

The time the simulation takes to complete can be reduced somewhat by turning off
the visualisation neurons and not saving anything: `--no_vis --no_save`.

If the simulation uses too much memory, you can decrease the resolution of
state variable recordings by increasing `--monitors_dt`.

Alternatively, run a simulation using a saved set of parameters:

```
$ python -i stdp_sounds.py --parameters_file params/two_notes_0.5_s.txt
```

Note that all other arguments are ignored when using `--parameters_file`.

## Tests

The code includes a few basic tests:

* LIF test, run with `python -i stdp_sounds.py --test_neurons`. This sets up a
  simple network of regularly-firing input neurons and a bunch of output
  neurons, then plots graphs of input/output spikes and membrane potential of
  the output neurons. Graphs can then be inspected to check that LIF
  dynamics/threshold adaptation is working correctly.
* Winner-take-all inhibitory connections test, run with `python -i
  stdp_sounds.py --test_competition`. This runs the same thing as the LIF tests
  but with inhibitory connections enabled.
* STDP curve test, run with `python -i stdp_sounds.py --test_stdp_curve`. This
  plots the STDP curve. A heavily-potentiation skewed STDP curve is used here
  because for the rate-coded input setup used it's actually much simpler to just
  do Hebbian-like learning.
