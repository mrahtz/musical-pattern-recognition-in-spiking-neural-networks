Step 1: place `bh.wav`, `fl.wav` and `jp.wav` in `tibicen_train` directory, and
`1.wav` through `lq5.wav` in `tibicen_test` directory.

Step 2: convert .wav files into spikes:

```
python gen_audio_spikes.py --train
python gen_audio_spikes.py --test
```

Step 3: use known sound data to train the network:

```
python stdp_sounds.py --input_spikes_file tibicen_train/tibicen_train.pickle --save_weights
```

Step 4: use the saved network state (synaptic weights + measure of intrinsic
plasticity, 'theta') to classify the test track:

```
python -i stdp_sounds.py --theta_coef 0 --nu_ee_post 0 --nu_ee_pre 0 --pre_w_decrease 0 --load_weights input-layer1e-weights-tibicen_train.pickle --load_theta theta-tibicen_train.pickle --input_spikes_file tibicen_test/tibicen_test_train.pickle --classify
```
