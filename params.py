from __future__ import print_function, division
import sys
import pprint
import argparse
import brian2 as b2
from IPython.core.debugger import Tracer

def get_params():
    """
    Collect parameters for the simulation.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('--parameters')
    parser.add_argument('--theta_coef', type=float, default=1.7)
    parser.add_argument('--nu_ee_post', type=float, default=0.06)
    parser.add_argument('--max_theta', type=float, default=50)
    parser.add_argument('--run_time')
    parser.add_argument('--batch', action='store_true')
    parser.add_argument('--input_spikes', default='music_spikes.pickle')
    parser.add_argument('--monitors_dt', type=float, default=1)
    parser.add_argument('--monitor_all_time', action='store_true')
    parser.add_argument('--layer_n_neurons', type=int, default=128)
    parser.add_argument('--adaptation',
                        choices=['absolute',
                                 'weight-relative',
                                 'absolute-adapting-exp',
                                 'absolute-adapting-noexp',
                                 'ge-theta'],
                        default='absolute')
    parser.add_argument('--no_save', action='store_true')
    parser.add_argument('--note_separation', type=float)
    parser.add_argument('--n_notes', type=int)
    parser.add_argument('--no_standalone', action='store_true')
    parser.add_argument('--no_vis', action='store_true')
    parser.add_argument('--pre_w_decrease', type=float, default=0.0005)
    parser.add_argument('--test_neurons', action='store_true')
    parser.add_argument('--test_stdp_curve', action='store_true')
    parser.add_argument('--test_competition', action='store_true')
    args = parser.parse_args()

    if args.parameters is not None:
        (neuron_params, connection_params, monitor_params, run_params,
            analysis_params) = load_params(args.parameters)
        run_params['from_paramfile'] = True
    else:
        (neuron_params, connection_params, monitor_params, run_params,
            analysis_params) =  params_from_args(args)
        run_params['from_paramfile'] = False

    params = (neuron_params, connection_params, monitor_params, run_params,
         analysis_params)
    return params

def record_params(params, run_id):
    """
    Record parameters used for simulation for future reference and
    alignment to figures.
    """
    with open('params/' + run_id + '.txt', 'w') as param_file:
        pprint.pprint(params, stream=param_file)
    with open('params/' + run_id + '_cmdline.txt', 'w') as cmdline_file:
        cmdline = ' '.join(sys.argv)
        print(cmdline, file=cmdline_file)

def load_params(params_filename):
    """
    Load parameters saved by record_params function.
    """
    with open(params_filename, 'r') as param_file:
        contents = param_file.read()
        mvolt = b2.mvolt
        uvolt = b2.uvolt
        volt = b2.volt
        second = b2.second
        msecond = b2.msecond
        ksecond = b2.ksecond
        params = eval(contents)
    return params

def params_from_args(args):
    neuron_params = neuron_params_from_args(args)
    connection_params = connection_params_from_args(args)
    run_params = run_params_from_args(args)
    monitor_params = monitor_params_from_args(args)
    analysis_params = analysis_params_from_args(args)

    params = (neuron_params, connection_params, monitor_params, run_params,
              analysis_params)
    return params

def neuron_params_from_args(args):
    neuron_params = {}

    neuron_params['v_rest_e'] = -65 * b2.mV
    neuron_params['v_rest_i'] = -60 * b2.mV
    neuron_params['v_reset_e'] = -65 * b2.mV
    neuron_params['v_reset_i'] = -45 * b2.mV
    neuron_params['v_thresh_e'] = -52 * b2.mV
    neuron_params['v_thresh_i'] = -40 * b2.mV
    neuron_params['refrac_e'] = 5 * b2.ms
    neuron_params['refrac_i'] = 2 * b2.ms
    neuron_params['no_vis'] = args.no_vis
    neuron_params['tc_v_ex'] = 100 * b2.ms
    neuron_params['tc_v_in'] = 10 * b2.ms
    neuron_params['tc_ge'] = 1 * b2.ms
    neuron_params['tc_gi'] = 2 * b2.ms
    # reversal potentials for excitatory neurons
    # excitatory reversal potential
    neuron_params['e_ex_ex'] = 0 * b2.mV
    # inhibitory reversal potential
    neuron_params['e_in_ex'] = -100 * b2.mV
    # reversal potentials for inhibitory neurons
    neuron_params['e_ex_in'] = 0 * b2.mV
    neuron_params['e_in_in'] = -85 * b2.mV

    neuron_params['tc_theta'] = 1e6 * b2.ms
    neuron_params['min_theta'] = 0 * b2.mV
    neuron_params['offset'] = 20 * b2.mV
    neuron_params['theta_coef'] = args.theta_coef
    neuron_params['max_theta'] = args.max_theta * b2.mV
    neuron_params['adaptation'] = args.adaptation
    neuron_params['no_vis'] = args.no_vis

    return neuron_params

def connection_params_from_args(args):
    connection_params = {}

    connection_params['tc_pre_ee'] = 20 * b2.ms
    connection_params['tc_post_ee'] = 20 * b2.ms
    connection_params['nu_ee_pre'] = 0.0001
    connection_params['nu_ee_post'] = args.nu_ee_post
    connection_params['exp_ee_pre'] = 0.2
    connection_params['exp_ee_post'] = connection_params['exp_ee_pre']
    connection_params['wmax_ee'] = 1.0
    connection_params['pre_w_decrease'] = args.pre_w_decrease

    connection_params['tc_ge'] = 1 * b2.ms
    connection_params['tc_gi'] = 2 * b2.ms

    connection_params['min_theta'] = 0 * b2.mV
    connection_params['max_theta'] = args.max_theta * b2.mV
    connection_params['theta_coef'] = args.theta_coef
    connection_params['adaptation'] = args.adaptation

    connection_params['ex-in-w'] = 10.4
    connection_params['in-ex-w'] = 17.0

    return connection_params

def run_params_from_args(args):
    run_params = {}

    run_params['layer_n_neurons'] = args.layer_n_neurons
    run_params['input_spikes_filename'] = args.input_spikes
    run_params['no_standalone'] = args.no_standalone
    if args.run_time is not None:
        run_params['run_time'] = float(args.run_time) * b2.second
    run_params['no_save_results'] = args.no_save
    run_params['test_neurons'] = args.test_neurons
    run_params['test_stdp_curve'] = args.test_stdp_curve
    run_params['test_competition'] = args.test_competition

    return run_params

def monitor_params_from_args(args):
    monitor_params = {}

    if not args.monitor_all_time:
        monitor_params['monitors_dt'] = \
            args.monitors_dt * b2.ms

    return monitor_params

def analysis_params_from_args(args):
    analysis_params = {}

    analysis_params['batch'] = args.batch
    analysis_params['no_save_figs'] = args.no_save
    if args.note_separation is not None:
        analysis_params['note_separation'] = args.note_separation * b2.second
    else:
        analysis_params['note_separation'] = None
    if args.n_notes is not None:
        analysis_params['n_notes'] = args.n_notes
    else:
        analysis_params['n_notes'] = None

    return analysis_params
