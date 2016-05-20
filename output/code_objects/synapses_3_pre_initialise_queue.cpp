#include "objects.h"
#include "code_objects/synapses_3_pre_initialise_queue.h"
void _run_synapses_3_pre_initialise_queue() {
	using namespace brian;
 	
 double*   _ptr_array_defaultclock_dt = _array_defaultclock_dt;


    double* real_delays = synapses_3_pre.delay.empty() ? 0 : &(synapses_3_pre.delay[0]);
    int32_t* sources = synapses_3_pre.sources.empty() ? 0 : &(synapses_3_pre.sources[0]);
    const unsigned int n_delays = synapses_3_pre.delay.size();
    const unsigned int n_synapses = synapses_3_pre.sources.size();
    synapses_3_pre.prepare(16,
                        16,
                        real_delays, n_delays, sources,
                        n_synapses,
                        _ptr_array_defaultclock_dt[0]);
}
