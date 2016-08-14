import brian2 as b2
import modules.equations as eqs

def stdp_ex_synapses(source, target, connectivity, params):
    syn_params = {
        'tc_pre_ee': params['tc_pre_ee'],
        'tc_post_ee': params['tc_post_ee'],
        'nu_ee_pre': params['nu_ee_pre'],
        'pre_w_decrease': params['pre_w_decrease'],
        'wmax_ee': params['wmax_ee'],
        'nu_ee_post': params['nu_ee_post'],
        'theta_coef': params['theta_coef'],
        'min_theta': params['min_theta'],
        'max_theta': params['max_theta']
    }

    synapses = b2.Synapses(
        source=source,
        target=target,
        model=eqs.eqs_stdp_ee,
        on_pre=eqs.eqs_stdp_pre_ee,
        on_post=eqs.eqs_stdp_post_ee,
        namespace=syn_params
    )

    synapses.connect(connectivity)

    return synapses

def nonplastic_synapses(source, target, connectivity, synapse_type):
    if synapse_type == 'excitatory':
        pre = 'ge_post += w * siemens'
    elif synapse_type == 'inhibitory':
        pre = 'gi_post += w * siemens'
    else:
        raise Exception("Invalid synapse type: %s" % synapse_type)

    model = 'w : 1'

    synapses = b2.Synapses(
        source=source,
        target=target,
        model=model, on_pre=pre
    )

    synapses.connect(connectivity)

    return synapses

def visualisation_synapses(source, target, connectivity):
    pre = 'v_post += 1*mV'

    synapses = b2.Synapses(
        source=source,
        target=target,
        on_pre=pre
    )

    synapses.connect(connectivity)

    return synapses
