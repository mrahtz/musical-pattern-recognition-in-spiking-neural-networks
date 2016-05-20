
#include "objects.h"
#include "synapses_classes.h"
#include "brianlib/clocks.h"
#include "brianlib/dynamic_array.h"
#include "brianlib/stdint_compat.h"
#include "network.h"
#include<vector>
#include<iostream>
#include<fstream>

namespace brian {

//////////////// networks /////////////////
Network magicnetwork;

//////////////// arrays ///////////////////
double * _array_defaultclock_dt;
const int _num__array_defaultclock_dt = 1;
double * _array_defaultclock_t;
const int _num__array_defaultclock_t = 1;
uint64_t * _array_defaultclock_timestep;
const int _num__array_defaultclock_timestep = 1;
int32_t * _array_neurongroup__spikespace;
const int _num__array_neurongroup__spikespace = 258;
int32_t * _array_neurongroup_i;
const int _num__array_neurongroup_i = 257;
double * _array_neurongroup_v;
const int _num__array_neurongroup_v = 257;
int32_t * _array_spikemonitor__source_idx;
const int _num__array_spikemonitor__source_idx = 257;
int32_t * _array_spikemonitor_count;
const int _num__array_spikemonitor_count = 257;
int32_t * _array_spikemonitor_N;
const int _num__array_spikemonitor_N = 1;
int32_t * _array_statemonitor__indices;
const int _num__array_statemonitor__indices = 257;
double * _array_statemonitor_I;
const int _num__array_statemonitor_I = (0, 257);
int32_t * _array_statemonitor_N;
const int _num__array_statemonitor_N = 1;
double * _array_statemonitor_v;
const int _num__array_statemonitor_v = (0, 257);

//////////////// dynamic arrays 1d /////////
std::vector<int32_t> _dynamic_array_spikemonitor_i;
std::vector<double> _dynamic_array_spikemonitor_t;
std::vector<double> _dynamic_array_statemonitor_t;

//////////////// dynamic arrays 2d /////////
DynamicArray2D<double> _dynamic_array_statemonitor_I;
DynamicArray2D<double> _dynamic_array_statemonitor_v;

/////////////// static arrays /////////////
int32_t * _static_array__array_statemonitor__indices;
const int _num__static_array__array_statemonitor__indices = 257;
double * _timedarray_values;
const int _num__timedarray_values = 468254;

//////////////// synapses /////////////////

//////////////// clocks ///////////////////
Clock defaultclock;  // attributes will be set in run.cpp

// Profiling information for each code object
double neurongroup_resetter_codeobject_profiling_info = 0.0;
double neurongroup_stateupdater_codeobject_profiling_info = 0.0;
double neurongroup_thresholder_codeobject_profiling_info = 0.0;
double spikemonitor_codeobject_profiling_info = 0.0;
double statemonitor_codeobject_profiling_info = 0.0;

}

void _init_arrays()
{
	using namespace brian;

    // Arrays initialized to 0
	_array_statemonitor__indices = new int32_t[257];
	
	for(int i=0; i<257; i++) _array_statemonitor__indices[i] = 0;
	_array_spikemonitor__source_idx = new int32_t[257];
	
	for(int i=0; i<257; i++) _array_spikemonitor__source_idx[i] = 0;
	_array_neurongroup__spikespace = new int32_t[258];
	
	for(int i=0; i<258; i++) _array_neurongroup__spikespace[i] = 0;
	_array_spikemonitor_count = new int32_t[257];
	
	for(int i=0; i<257; i++) _array_spikemonitor_count[i] = 0;
	_array_defaultclock_dt = new double[1];
	
	for(int i=0; i<1; i++) _array_defaultclock_dt[i] = 0;
	_array_neurongroup_i = new int32_t[257];
	
	for(int i=0; i<257; i++) _array_neurongroup_i[i] = 0;
	_array_spikemonitor_N = new int32_t[1];
	
	for(int i=0; i<1; i++) _array_spikemonitor_N[i] = 0;
	_array_statemonitor_N = new int32_t[1];
	
	for(int i=0; i<1; i++) _array_statemonitor_N[i] = 0;
	_array_defaultclock_t = new double[1];
	
	for(int i=0; i<1; i++) _array_defaultclock_t[i] = 0;
	_array_defaultclock_timestep = new uint64_t[1];
	
	for(int i=0; i<1; i++) _array_defaultclock_timestep[i] = 0;
	_array_neurongroup_v = new double[257];
	
	for(int i=0; i<257; i++) _array_neurongroup_v[i] = 0;

	// Arrays initialized to an "arange"
	_array_spikemonitor__source_idx = new int32_t[257];
	
	for(int i=0; i<257; i++) _array_spikemonitor__source_idx[i] = 0 + i;
	_array_neurongroup_i = new int32_t[257];
	
	for(int i=0; i<257; i++) _array_neurongroup_i[i] = 0 + i;

	// static arrays
	_static_array__array_statemonitor__indices = new int32_t[257];
	_timedarray_values = new double[468254];
}

void _load_arrays()
{
	using namespace brian;

	ifstream f_static_array__array_statemonitor__indices;
	f_static_array__array_statemonitor__indices.open("static_arrays/_static_array__array_statemonitor__indices", ios::in | ios::binary);
	if(f_static_array__array_statemonitor__indices.is_open())
	{
		f_static_array__array_statemonitor__indices.read(reinterpret_cast<char*>(_static_array__array_statemonitor__indices), 257*sizeof(int32_t));
	} else
	{
		std::cout << "Error opening static array _static_array__array_statemonitor__indices." << endl;
	}
	ifstream f_timedarray_values;
	f_timedarray_values.open("static_arrays/_timedarray_values", ios::in | ios::binary);
	if(f_timedarray_values.is_open())
	{
		f_timedarray_values.read(reinterpret_cast<char*>(_timedarray_values), 468254*sizeof(double));
	} else
	{
		std::cout << "Error opening static array _timedarray_values." << endl;
	}
}

void _write_arrays()
{
	using namespace brian;

	ofstream outfile__array_defaultclock_dt;
	outfile__array_defaultclock_dt.open("results/_array_defaultclock_dt_-9215759865592636245", ios::binary | ios::out);
	if(outfile__array_defaultclock_dt.is_open())
	{
		outfile__array_defaultclock_dt.write(reinterpret_cast<char*>(_array_defaultclock_dt), 1*sizeof(_array_defaultclock_dt[0]));
		outfile__array_defaultclock_dt.close();
	} else
	{
		std::cout << "Error writing output file for _array_defaultclock_dt." << endl;
	}
	ofstream outfile__array_defaultclock_t;
	outfile__array_defaultclock_t.open("results/_array_defaultclock_t_7263079326120112646", ios::binary | ios::out);
	if(outfile__array_defaultclock_t.is_open())
	{
		outfile__array_defaultclock_t.write(reinterpret_cast<char*>(_array_defaultclock_t), 1*sizeof(_array_defaultclock_t[0]));
		outfile__array_defaultclock_t.close();
	} else
	{
		std::cout << "Error writing output file for _array_defaultclock_t." << endl;
	}
	ofstream outfile__array_defaultclock_timestep;
	outfile__array_defaultclock_timestep.open("results/_array_defaultclock_timestep_-8300011050550298960", ios::binary | ios::out);
	if(outfile__array_defaultclock_timestep.is_open())
	{
		outfile__array_defaultclock_timestep.write(reinterpret_cast<char*>(_array_defaultclock_timestep), 1*sizeof(_array_defaultclock_timestep[0]));
		outfile__array_defaultclock_timestep.close();
	} else
	{
		std::cout << "Error writing output file for _array_defaultclock_timestep." << endl;
	}
	ofstream outfile__array_neurongroup__spikespace;
	outfile__array_neurongroup__spikespace.open("results/_array_neurongroup__spikespace_6291509255835556833", ios::binary | ios::out);
	if(outfile__array_neurongroup__spikespace.is_open())
	{
		outfile__array_neurongroup__spikespace.write(reinterpret_cast<char*>(_array_neurongroup__spikespace), 258*sizeof(_array_neurongroup__spikespace[0]));
		outfile__array_neurongroup__spikespace.close();
	} else
	{
		std::cout << "Error writing output file for _array_neurongroup__spikespace." << endl;
	}
	ofstream outfile__array_neurongroup_i;
	outfile__array_neurongroup_i.open("results/_array_neurongroup_i_-2688036259655650195", ios::binary | ios::out);
	if(outfile__array_neurongroup_i.is_open())
	{
		outfile__array_neurongroup_i.write(reinterpret_cast<char*>(_array_neurongroup_i), 257*sizeof(_array_neurongroup_i[0]));
		outfile__array_neurongroup_i.close();
	} else
	{
		std::cout << "Error writing output file for _array_neurongroup_i." << endl;
	}
	ofstream outfile__array_neurongroup_v;
	outfile__array_neurongroup_v.open("results/_array_neurongroup_v_-2688036259655650190", ios::binary | ios::out);
	if(outfile__array_neurongroup_v.is_open())
	{
		outfile__array_neurongroup_v.write(reinterpret_cast<char*>(_array_neurongroup_v), 257*sizeof(_array_neurongroup_v[0]));
		outfile__array_neurongroup_v.close();
	} else
	{
		std::cout << "Error writing output file for _array_neurongroup_v." << endl;
	}
	ofstream outfile__array_spikemonitor__source_idx;
	outfile__array_spikemonitor__source_idx.open("results/_array_spikemonitor__source_idx_-4045852888739339153", ios::binary | ios::out);
	if(outfile__array_spikemonitor__source_idx.is_open())
	{
		outfile__array_spikemonitor__source_idx.write(reinterpret_cast<char*>(_array_spikemonitor__source_idx), 257*sizeof(_array_spikemonitor__source_idx[0]));
		outfile__array_spikemonitor__source_idx.close();
	} else
	{
		std::cout << "Error writing output file for _array_spikemonitor__source_idx." << endl;
	}
	ofstream outfile__array_spikemonitor_count;
	outfile__array_spikemonitor_count.open("results/_array_spikemonitor_count_-3651895352503201284", ios::binary | ios::out);
	if(outfile__array_spikemonitor_count.is_open())
	{
		outfile__array_spikemonitor_count.write(reinterpret_cast<char*>(_array_spikemonitor_count), 257*sizeof(_array_spikemonitor_count[0]));
		outfile__array_spikemonitor_count.close();
	} else
	{
		std::cout << "Error writing output file for _array_spikemonitor_count." << endl;
	}
	ofstream outfile__array_spikemonitor_N;
	outfile__array_spikemonitor_N.open("results/_array_spikemonitor_N_73938390545997659", ios::binary | ios::out);
	if(outfile__array_spikemonitor_N.is_open())
	{
		outfile__array_spikemonitor_N.write(reinterpret_cast<char*>(_array_spikemonitor_N), 1*sizeof(_array_spikemonitor_N[0]));
		outfile__array_spikemonitor_N.close();
	} else
	{
		std::cout << "Error writing output file for _array_spikemonitor_N." << endl;
	}
	ofstream outfile__array_statemonitor__indices;
	outfile__array_statemonitor__indices.open("results/_array_statemonitor__indices_6163485638831984707", ios::binary | ios::out);
	if(outfile__array_statemonitor__indices.is_open())
	{
		outfile__array_statemonitor__indices.write(reinterpret_cast<char*>(_array_statemonitor__indices), 257*sizeof(_array_statemonitor__indices[0]));
		outfile__array_statemonitor__indices.close();
	} else
	{
		std::cout << "Error writing output file for _array_statemonitor__indices." << endl;
	}
	ofstream outfile__array_statemonitor_N;
	outfile__array_statemonitor_N.open("results/_array_statemonitor_N_1126150466128921572", ios::binary | ios::out);
	if(outfile__array_statemonitor_N.is_open())
	{
		outfile__array_statemonitor_N.write(reinterpret_cast<char*>(_array_statemonitor_N), 1*sizeof(_array_statemonitor_N[0]));
		outfile__array_statemonitor_N.close();
	} else
	{
		std::cout << "Error writing output file for _array_statemonitor_N." << endl;
	}

	ofstream outfile__dynamic_array_spikemonitor_i;
	outfile__dynamic_array_spikemonitor_i.open("results/_dynamic_array_spikemonitor_i_3873805716461528078", ios::binary | ios::out);
	if(outfile__dynamic_array_spikemonitor_i.is_open())
	{
        if (! _dynamic_array_spikemonitor_i.empty() )
        {
			outfile__dynamic_array_spikemonitor_i.write(reinterpret_cast<char*>(&_dynamic_array_spikemonitor_i[0]), _dynamic_array_spikemonitor_i.size()*sizeof(_dynamic_array_spikemonitor_i[0]));
		    outfile__dynamic_array_spikemonitor_i.close();
		}
	} else
	{
		std::cout << "Error writing output file for _dynamic_array_spikemonitor_i." << endl;
	}
	ofstream outfile__dynamic_array_spikemonitor_t;
	outfile__dynamic_array_spikemonitor_t.open("results/_dynamic_array_spikemonitor_t_3873805716461528083", ios::binary | ios::out);
	if(outfile__dynamic_array_spikemonitor_t.is_open())
	{
        if (! _dynamic_array_spikemonitor_t.empty() )
        {
			outfile__dynamic_array_spikemonitor_t.write(reinterpret_cast<char*>(&_dynamic_array_spikemonitor_t[0]), _dynamic_array_spikemonitor_t.size()*sizeof(_dynamic_array_spikemonitor_t[0]));
		    outfile__dynamic_array_spikemonitor_t.close();
		}
	} else
	{
		std::cout << "Error writing output file for _dynamic_array_spikemonitor_t." << endl;
	}
	ofstream outfile__dynamic_array_statemonitor_t;
	outfile__dynamic_array_statemonitor_t.open("results/_dynamic_array_statemonitor_t_6620044162385838772", ios::binary | ios::out);
	if(outfile__dynamic_array_statemonitor_t.is_open())
	{
        if (! _dynamic_array_statemonitor_t.empty() )
        {
			outfile__dynamic_array_statemonitor_t.write(reinterpret_cast<char*>(&_dynamic_array_statemonitor_t[0]), _dynamic_array_statemonitor_t.size()*sizeof(_dynamic_array_statemonitor_t[0]));
		    outfile__dynamic_array_statemonitor_t.close();
		}
	} else
	{
		std::cout << "Error writing output file for _dynamic_array_statemonitor_t." << endl;
	}

	ofstream outfile__dynamic_array_statemonitor_I;
	outfile__dynamic_array_statemonitor_I.open("results/_dynamic_array_statemonitor_I_6620044162385838729", ios::binary | ios::out);
	if(outfile__dynamic_array_statemonitor_I.is_open())
	{
        for (int n=0; n<_dynamic_array_statemonitor_I.n; n++)
        {
            if (! _dynamic_array_statemonitor_I(n).empty())
            {
                outfile__dynamic_array_statemonitor_I.write(reinterpret_cast<char*>(&_dynamic_array_statemonitor_I(n, 0)), _dynamic_array_statemonitor_I.m*sizeof(_dynamic_array_statemonitor_I(0, 0)));
            }
        }
        outfile__dynamic_array_statemonitor_I.close();
	} else
	{
		std::cout << "Error writing output file for _dynamic_array_statemonitor_I." << endl;
	}
	ofstream outfile__dynamic_array_statemonitor_v;
	outfile__dynamic_array_statemonitor_v.open("results/_dynamic_array_statemonitor_v_6620044162385838774", ios::binary | ios::out);
	if(outfile__dynamic_array_statemonitor_v.is_open())
	{
        for (int n=0; n<_dynamic_array_statemonitor_v.n; n++)
        {
            if (! _dynamic_array_statemonitor_v(n).empty())
            {
                outfile__dynamic_array_statemonitor_v.write(reinterpret_cast<char*>(&_dynamic_array_statemonitor_v(n, 0)), _dynamic_array_statemonitor_v.m*sizeof(_dynamic_array_statemonitor_v(0, 0)));
            }
        }
        outfile__dynamic_array_statemonitor_v.close();
	} else
	{
		std::cout << "Error writing output file for _dynamic_array_statemonitor_v." << endl;
	}

	// Write profiling info to disk
	ofstream outfile_profiling_info;
	outfile_profiling_info.open("results/profiling_info.txt", ios::out);
	if(outfile_profiling_info.is_open())
	{
	outfile_profiling_info << "neurongroup_resetter_codeobject\t" << neurongroup_resetter_codeobject_profiling_info << std::endl;
	outfile_profiling_info << "neurongroup_stateupdater_codeobject\t" << neurongroup_stateupdater_codeobject_profiling_info << std::endl;
	outfile_profiling_info << "neurongroup_thresholder_codeobject\t" << neurongroup_thresholder_codeobject_profiling_info << std::endl;
	outfile_profiling_info << "spikemonitor_codeobject\t" << spikemonitor_codeobject_profiling_info << std::endl;
	outfile_profiling_info << "statemonitor_codeobject\t" << statemonitor_codeobject_profiling_info << std::endl;
	outfile_profiling_info.close();
	} else
	{
	    std::cout << "Error writing profiling info to file." << std::endl;
	}

	// Write last run info to disk
	ofstream outfile_last_run_info;
	outfile_last_run_info.open("results/last_run_info.txt", ios::out);
	if(outfile_last_run_info.is_open())
	{
		outfile_last_run_info << (Network::_last_run_time) << " " << (Network::_last_run_completed_fraction) << std::endl;
		outfile_last_run_info.close();
	} else
	{
	    std::cout << "Error writing last run info to file." << std::endl;
	}
}

void _dealloc_arrays()
{
	using namespace brian;


	// static arrays
	if(_static_array__array_statemonitor__indices!=0)
	{
		delete [] _static_array__array_statemonitor__indices;
		_static_array__array_statemonitor__indices = 0;
	}
	if(_timedarray_values!=0)
	{
		delete [] _timedarray_values;
		_timedarray_values = 0;
	}
}

