reset_e = '''
v = v_reset_e
theta = theta + theta_coef * (max_theta - theta)
'''

thresh_e = 'v > (theta - offset + v_thresh_e)'

neuron_eqs = '''
I_synE = ge * (e_ex - v) : amp
I_synI = gi * (e_in - v) : amp
dge/dt = -ge / tc_ge     : siemens
dgi/dt = -gi / tc_gi     : siemens
'''

# dv/dt describes the rate of change of membrane potential
# 1. 'v_rest - v' pulls v towards v_rest
# 2. 'ge * (0 - v)' pulls v towards 0, proportionally to ge
# 3. 'ge * (-100 - v)' pulls v towards -100, proportionally to gi
neuron_eqs_e = neuron_eqs + '''
dv/dt = ((v_rest - v) + (I_synE + I_synI) * 1 * ohm) / tc_v : volt (unless refractory)
dtheta/dt = -theta / (tc_theta)                             : volt
theta_mod                                                   : 1
max_ge                                                      : siemens
x                                                           : 1
y                                                           : 1
'''

reset_i = 'v = v_reset_i'
thresh_i = 'v > v_thresh_i'

neuron_eqs_i = neuron_eqs + '''
dv/dt = ((v_rest - v) + (I_synE + I_synI) * 1 * ohm) / tc_v : volt
'''

eqs_stdp_ee = '''
w                             : 1
dpre/dt = -pre / tc_pre_ee    : 1 (event-driven)
dpost/dt = -post / tc_post_ee : 1 (event-driven)
'''

eqs_stdp_pre_ee = '''
ge_post += w * siemens
pre = 1
w = clip(w - nu_ee_pre * post - pre_w_decrease, 0, wmax_ee)
'''

eqs_stdp_post_ee = '''
post = 1
w = clip(w + nu_ee_post * pre, 0, wmax_ee)
'''
