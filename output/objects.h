
#ifndef _BRIAN_OBJECTS_H
#define _BRIAN_OBJECTS_H

#include "synapses_classes.h"
#include "brianlib/clocks.h"
#include "brianlib/dynamic_array.h"
#include "brianlib/stdint_compat.h"
#include "network.h"
#include<vector>


namespace brian {

//////////////// clocks ///////////////////
extern Clock defaultclock;

//////////////// networks /////////////////
extern Network magicnetwork;
extern Network magicnetwork;

//////////////// dynamic arrays ///////////
extern std::vector<int32_t> _dynamic_array_spikemonitor_i;
extern std::vector<double> _dynamic_array_spikemonitor_t;
extern std::vector<double> _dynamic_array_statemonitor_t;

//////////////// arrays ///////////////////
extern double *_array_defaultclock_dt;
extern const int _num__array_defaultclock_dt;
extern double *_array_defaultclock_t;
extern const int _num__array_defaultclock_t;
extern uint64_t *_array_defaultclock_timestep;
extern const int _num__array_defaultclock_timestep;
extern int32_t *_array_neurongroup__spikespace;
extern const int _num__array_neurongroup__spikespace;
extern int32_t *_array_neurongroup_i;
extern const int _num__array_neurongroup_i;
extern double *_array_neurongroup_v;
extern const int _num__array_neurongroup_v;
extern int32_t *_array_spikemonitor__source_idx;
extern const int _num__array_spikemonitor__source_idx;
extern int32_t *_array_spikemonitor_count;
extern const int _num__array_spikemonitor_count;
extern int32_t *_array_spikemonitor_N;
extern const int _num__array_spikemonitor_N;
extern int32_t *_array_statemonitor__indices;
extern const int _num__array_statemonitor__indices;
extern double *_array_statemonitor_I;
extern const int _num__array_statemonitor_I;
extern int32_t *_array_statemonitor_N;
extern const int _num__array_statemonitor_N;
extern double *_array_statemonitor_v;
extern const int _num__array_statemonitor_v;

//////////////// dynamic arrays 2d /////////
extern DynamicArray2D<double> _dynamic_array_statemonitor_I;
extern DynamicArray2D<double> _dynamic_array_statemonitor_v;

/////////////// static arrays /////////////
extern int32_t *_static_array__array_statemonitor__indices;
extern const int _num__static_array__array_statemonitor__indices;
extern double *_timedarray_values;
extern const int _num__timedarray_values;

//////////////// synapses /////////////////

// Profiling information for each code object
extern double neurongroup_resetter_codeobject_profiling_info;
extern double neurongroup_stateupdater_codeobject_profiling_info;
extern double neurongroup_thresholder_codeobject_profiling_info;
extern double spikemonitor_codeobject_profiling_info;
extern double statemonitor_codeobject_profiling_info;

}

void _init_arrays();
void _load_arrays();
void _write_arrays();
void _dealloc_arrays();

#endif


