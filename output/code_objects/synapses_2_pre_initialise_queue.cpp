#include "objects.h"
#include "code_objects/synapses_2_pre_initialise_queue.h"
void _run_synapses_2_pre_initialise_queue() {
	using namespace brian;
 	
 double*   _ptr_array_defaultclock_dt = _array_defaultclock_dt;


    double* real_delays = synapses_2_pre.delay.empty() ? 0 : &(synapses_2_pre.delay[0]);
    int32_t* sources = synapses_2_pre.sources.empty() ? 0 : &(synapses_2_pre.sources[0]);
    const unsigned int n_delays = synapses_2_pre.delay.size();
    const unsigned int n_synapses = synapses_2_pre.sources.size();
    synapses_2_pre.prepare(16,
                        16,
                        real_delays, n_delays, sources,
                        n_synapses,
                        _ptr_array_defaultclock_dt[0]);
}
