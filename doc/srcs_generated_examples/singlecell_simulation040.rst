
12. Investigating the rheobase of a neuron with a parameter sweep
=================================================================


Investigating the rheobase of a neuron with a parameter sweep

WARNING: The automatic naming and linkage between grpah colors is currently under a refactor;
what is done in this script is not representing the best possible solution, or even something that
will reliably work in the future!

The aim of this script is just to show that it is possible to run multiple simulations from a single script!

Code
~~~~

.. code-block:: python

	#!/usr/bin/python
	# -*- coding: utf-8 -*-
	
	# ---------------------------------------------------------------------
	# Copyright (c) 2012 Michael Hull.
	# All rights reserved.
	#
	# Redistribution and use in source and binary forms, with or without
	# modification, are permitted provided that the following conditions
	# are met:
	#
	#  - Redistributions of source code must retain the above copyright 
	#    notice, this list of conditions and the following disclaimer. 
	#  - Redistributions in binary form must reproduce the above copyright 
	#    notice, this list of conditions and the following disclaimer in 
	#    the documentation and/or other materials provided with the 
	#    distribution.
	#
	# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
	# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
	# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR 
	# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT 
	# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
	# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT 
	# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
	# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY 
	# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
	# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
	#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
	# ----------------------------------------------------------------------
	
	
	
	
	
	
	from morphforge.stdimports import *
	from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmleak import MM_LeakChannel
	from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmalphabeta import MM_AlphaBetaChannel
	
	
	
	def get_Na_Channels(env):
	    naStateVars = {"m":
	                    {"alpha": [ 13.01,0,4,-1.01,-12.56 ], "beta": [5.73,0,1,9.01,9.69 ] },
	                   "h":
	                    {"alpha": [ 0.06,0,0,30.88,26 ], "beta": [3.06,0,1,-7.09,-10.21 ]}
	                   }
	
	    return  env.MembraneMechanism(
	                            MM_AlphaBetaChannel,
	                            name="NaChl", ion="na",
	                            equation="m*m*m*h",
	                            conductance=unit("210:nS") / unit("400:um2"),
	                            reversalpotential=unit("50.0:mV"),
	                            statevars=naStateVars,
	                            mechanism_id = 'Na_ID'
	                            )
	
	def get_Ks_Channels(env):
	    kfStateVars = {"ks": {"alpha": [ 0.2,0,1,-6.96,-7.74  ], "beta": [0.05,0,2,-18.07,6.1  ] } }
	
	    return  env.MembraneMechanism(
	                            MM_AlphaBetaChannel,
	                            name="KsChl", ion="ks",
	                            equation="ks*ks*ks*ks",
	                            conductance=unit("3:nS") / unit("400:um2"),
	                            reversalpotential=unit("-80.0:mV"),
	                            statevars=kfStateVars,
	                            mechanism_id = 'IN_Ks_ID'
	                            )
	
	def get_Kf_Channels(env):
	    kfStateVars = {"kf": {"alpha": [  3.1,0,1,-31.5,-9.3 ], "beta": [0.44,0,1,4.98,16.19  ] } }
	
	    return  env.MembraneMechanism(
	                            MM_AlphaBetaChannel,
	                            name="KfChl", ion="kf",
	                            equation="kf*kf*kf*kf",
	                            conductance=unit("0.5:nS") / unit("400:um2") ,
	                            reversalpotential=unit("-80.0:mV"),
	                            statevars=kfStateVars,
	                            mechanism_id = 'N_Kf_ID'
	                            )
	
	def get_Lk_Channels(env):
	    leakChannels = env.MembraneMechanism(
	                         MM_LeakChannel,
	                         name="LkChl",
	                         conductance=unit("3.6765:nS") / unit("400:um2"),
	                         reversalpotential=unit("-51:mV"),
	                         mechanism_id = 'Lk_ID'
	                        )
	    return leakChannels
	
	
	
	
	def simulate(current_inj_level):
	    # Create the environment:
	    env = NeuronSimulationEnvironment()
	
	    # Create the simulation:
	    mySim = env.Simulation(name="AA")
	
	
	    # Create a cell:
	    morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
	    morph = MorphologyTree.fromDictionary(morphDict1)
	    myCell = mySim.create_cell(name="Cell1", morphology=morph)
	
	    leakChannels = get_Lk_Channels(env)
	    sodiumChannels = get_Na_Channels(env)
	    potFastChannels = get_Kf_Channels(env)
	    potSlowChannels = get_Ks_Channels(env)
	
	    apply_mechanism_everywhere_uniform(myCell, leakChannels )
	    apply_mechanism_everywhere_uniform(myCell, sodiumChannels )
	    apply_mechanism_everywhere_uniform(myCell, potFastChannels )
	    apply_mechanism_everywhere_uniform(myCell, potSlowChannels )
	    apply_passive_everywhere_uniform(myCell, PassiveProperty.SpecificCapacitance, unit('2.0:uF/cm2') )
	
	
	    # Get a cell_location on the cell:
	    somaLoc = myCell.get_location("soma")
	
	    # Create the stimulus and record the injected current:
	    cc = mySim.create_currentclamp( amp=current_inj_level, dur=unit("100:ms"), delay=unit("100:ms"), cell_location=somaLoc)
	    mySim.record(cc, what=StandardTags.Current)
	
	    # Define what to record:
	    mySim.record( myCell, what=StandardTags.Voltage, cell_location = somaLoc )
	
	    # run the simulation
	    results = mySim.run()
	
	    return results
	
	
	# Display the results:
	results = [ simulate(current_inj_level='%d:pA'%i) for i in [50,100,150,200, 250, 300]   ]
	TagViewer(results, timeranges=[(95, 200)*pq.ms], show=True )
	
	




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation040_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation040_out1.png>`






Output
~~~~~~

.. code-block:: bash

    	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.math
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.geom
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class '2012-07-15 15:56:55,978 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:56:55,979 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.math
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.geom
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <cla2012-07-15 15:56:56,670 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:56:56,670 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	ss 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.neuro
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.physics
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/10/1022745089f3716f9acbc1e85edf9f5a.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0003'}
	Executing: /opt/nrn/i686/bin/modlunit /home/michael/old_home/mftmp/tmp_614307aa7da015001df5b10753239319.mod
	/mnt/sdb5/home/michael/mftmp/modbuild_29485
	Executing: /opt/nrn/i686/bin/nocmodl tmp_614307aa7da015001df5b10753239319.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/i686/lib"    -g -O2 -c -o tmp_614307aa7da015001df5b10753239319.lo tmp_614307aa7da015001df5b10753239319.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_614307aa7da015001df5b10753239319.la  -rpath /opt/nrn/i686/libs  tmp_614307aa7da015001df5b10753239319.lo  -L/opt/nrn/i686/lib -L/opt/nrn/i686/lib  /opt/nrn/i686/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/opt/nrn/include/nrn -I/opt/nrn/i686/lib -g -O2 -c tmp_614307aa7da015001df5b10753239319.c  -fPIC -DPIC -o .libs/tmp_614307aa7da015001df5b10753239319.o
	
	OP2: libtool: link: gcc -shared  .libs/tmp_614307aa7da015001df5b10753239319.o   -Wl,-rpath -Wl,/opt/nrn/i686/lib -Wl,-rpath -Wl,/opt/nrn/i686/lib -L/opt/nrn/i686/lib /opt/nrn/i686/lib/libnrniv.so /opt/nrn/i686/lib/libnrnoc.so /opt/nrn/i686/lib/liboc.so /opt/nrn/i686/lib/libmemacs.so /opt/nrn/i686/lib/libnrnmpi.so /opt/nrn/i686/lib/libscopmath.so /opt/nrn/i686/lib/libsparse13.so -lreadline -lncurses /opt/nrn/i686/lib/libivoc.so /opt/nrn/i686/lib/libneuron_gnu.so /opt/nrn/i686/lib/libmeschach.so /opt/nrn/i686/lib/libsundials.so -lm -ldl    -pthread -Wl,-soname -Wl,tmp_614307aa7da015001df5b10753239319.so.0 -o .libs/tmp_614307aa7da015001df5b10753239319.so.0.0.0
	libtool: link: (cd ".libs" && rm -f "tmp_614307aa7da015001df5b10753239319.so.0" && ln -s "tmp_614307aa7da015001df5b10753239319.so.0.0.0" "tmp_614307aa7da015001df5b10753239319.so.0")
	libtool: link: (cd ".libs" && rm -f "tmp_614307aa7da015001df5b10753239319.so" && ln -s "tmp_614307aa7da015001df5b10753239319.so.0.0.0" "tmp_614307aa7da015001df5b10753239319.so")
	libtool: link: ( cd ".libs" && rm -f "tmp_614307aa7da015001df5b10753239319.la" && ln -s "../tmp_614307aa7da015001df5b10753239319.la" "tmp_614307aa7da015001df5b10753239319.la" )
	
	Executing: /opt/nrn/i686/bin/modlunit /home/michael/old_home/mftmp/tmp_47a73077af2c6ec0c1ea8ec049ad42d0.mod
	/mnt/sdb5/home/michael/mftmp/modbuild_29485
	Executing: /opt/nrn/i686/bin/nocmodl tmp_47a73077af2c6ec0c1ea8ec049ad42d0.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/i686/lib"    -g -O2 -c -o tmp_47a73077af2c6ec0c1ea8ec049ad42d0.lo tmp_47a73077af2c6ec0c1ea8ec049ad42d0.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_47a73077af2c6ec0c1ea8ec049ad42d0.la  -rpath /opt/nrn/i686/libs  tmp_47a73077af2c6ec0c1ea8ec049ad42d0.lo  -L/opt/nrn/i686/lib -L/opt/nrn/i686/lib  /opt/nrn/i686/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/opt/nrn/include/nrn -I/opt/nrn/i686/lib -g -O2 -c tmp_47a73077af2c6ec0c1ea8ec049ad42d0.c  -fPIC -DPIC -o .libs/tmp_47a73077af2c6ec0c1ea8ec049ad42d0.o
	
	OP2: libtool: link: gcc -shared  .libs/tmp_47a73077af2c6ec0c1ea8ec049ad42d0.o   -Wl,-rpath -Wl,/opt/nrn/i686/lib -Wl,-rpath -Wl,/opt/nrn/i686/lib -L/opt/nrn/i686/lib /opt/nrn/i686/lib/libnrniv.so /opt/nrn/i686/lib/libnrnoc.so /opt/nrn/i686/lib/liboc.so /opt/nrn/i686/lib/libmemacs.so /opt/nrn/i686/lib/libnrnmpi.so /opt/nrn/i686/lib/libscopmath.so /opt/nrn/i686/lib/libsparse13.so -lreadline -lncurses /opt/nrn/i686/lib/libivoc.so /opt/nrn/i686/lib/libneuron_gnu.so /opt/nrn/i686/lib/libmeschach.so /opt/nrn/i686/lib/libsundials.so -lm -ldl    -pthread -Wl,-soname -Wl,tmp_47a73077af2c6ec0c1ea8ec049ad42d0.so.0 -o .libs/tmp_47a73077af2c6ec0c1ea8ec049ad42d0.so.0.0.0
	libtool: link: (cd ".libs" && rm -f "tmp_47a73077af2c6ec0c1ea8ec049ad42d0.so.0" && ln -s "tmp_47a73077af2c6ec0c1ea8ec049ad42d0.so.0.0.0" "tmp_47a73077af2c6ec0c1ea8ec049ad42d0.so.0")
	libtool: link: (cd ".libs" && rm -f "tmp_47a73077af2c6ec0c1ea8ec049ad42d0.so" && ln -s "tmp_47a73077af2c6ec0c1ea8ec049ad42d0.so.0.0.0" "tmp_47a73077af2c6ec0c1ea8ec049ad42d0.so")
	libtool: link: ( cd ".libs" && rm -f "tmp_47a73077af2c6ec0c1ea8ec049ad42d0.la" && ln -s "../tmp_47a73077af2c6ec0c1ea8ec049ad42d0.la" "tmp_47a73077af2c6ec0c1ea8ec049ad42d0.la" )
	
	Executing: /opt/nrn/i686/bin/modlunit /home/michael/old_home/mftmp/tmp_20a93e80a6c36b957e88f400fee94ab7.mod
	/mnt/sdb5/home/michael/mftmp/modbuild_29485
	Executing: /opt/nrn/i686/bin/nocmodl tmp_20a93e80a6c36b957e88f400fee94ab7.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/i686/lib"    -g -O2 -c -o tmp_20a93e80a6c36b957e88f400fee94ab7.lo tmp_20a93e80a6c36b957e88f400fee94ab7.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_20a93e80a6c36b957e88f400fee94ab7.la  -rpath /opt/nrn/i686/libs  tmp_20a93e80a6c36b957e88f400fee94ab7.lo  -L/opt/nrn/i686/lib -L/opt/nrn/i686/lib  /opt/nrn/i686/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/opt/nrn/include/nrn -I/opt/nrn/i686/lib -g -O2 -c tmp_20a93e80a6c36b957e88f400fee94ab7.c  -fPIC -DPIC -o .libs/tmp_20a93e80a6c36b957e88f400fee94ab7.o
	
	OP2: libtool: link: gcc -shared  .libs/tmp_20a93e80a6c36b957e88f400fee94ab7.o   -Wl,-rpath -Wl,/opt/nrn/i686/lib -Wl,-rpath -Wl,/opt/nrn/i686/lib -L/opt/nrn/i686/lib /opt/nrn/i686/lib/libnrniv.so /opt/nrn/i686/lib/libnrnoc.so /opt/nrn/i686/lib/liboc.so /opt/nrn/i686/lib/libmemacs.so /opt/nrn/i686/lib/libnrnmpi.so /opt/nrn/i686/lib/libscopmath.so /opt/nrn/i686/lib/libsparse13.so -lreadline -lncurses /opt/nrn/i686/lib/libivoc.so /opt/nrn/i686/lib/libneuron_gnu.so /opt/nrn/i686/lib/libmeschach.so /opt/nrn/i686/lib/libsundials.so -lm -ldl    -pthread -Wl,-soname -Wl,tmp_20a93e80a6c36b957e88f400fee94ab7.so.0 -o .libs/tmp_20a93e80a6c36b957e88f400fee94ab7.so.0.0.0
	libtool: link: (cd ".libs" && rm -f "tmp_20a93e80a6c36b957e88f400fee94ab7.so.0" && ln -s "tmp_20a93e80a6c36b957e88f400fee94ab7.so.0.0.0" "tmp_20a93e80a6c36b957e88f400fee94ab7.so.0")
	libtool: link: (cd ".libs" && rm -f "tmp_20a93e80a6c36b957e88f400fee94ab7.so" && ln -s "tmp_20a93e80a6c36b957e88f400fee94ab7.so.0.0.0" "tmp_20a93e80a6c36b957e88f400fee94ab7.so")
	libtool: link: ( cd ".libs" && rm -f "tmp_20a93e80a6c36b957e88fNEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	400fee94ab7.la" && ln -s "../tmp_20a93e80a6c36b957e88f400fee94ab7.la" "tmp_20a93e80a6c36b957e88f400fee94ab7.la" )
	
	Executing: /opt/nrn/i686/bin/modlunit /home/michael/old_home/mftmp/tmp_2386fb144ce2ed06ae9438bb96d9264a.mod
	/mnt/sdb5/home/michael/mftmp/modbuild_29485
	Executing: /opt/nrn/i686/bin/nocmodl tmp_2386fb144ce2ed06ae9438bb96d9264a.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/i686/lib"    -g -O2 -c -o tmp_2386fb144ce2ed06ae9438bb96d9264a.lo tmp_2386fb144ce2ed06ae9438bb96d9264a.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_2386fb144ce2ed06ae9438bb96d9264a.la  -rpath /opt/nrn/i686/libs  tmp_2386fb144ce2ed06ae9438bb96d9264a.lo  -L/opt/nrn/i686/lib -L/opt/nrn/i686/lib  /opt/nrn/i686/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/opt/nrn/include/nrn -I/opt/nrn/i686/lib -g -O2 -c tmp_2386fb144ce2ed06ae9438bb96d9264a.c  -fPIC -DPIC -o .libs/tmp_2386fb144ce2ed06ae9438bb96d9264a.o
	
	OP2: libtool: link: gcc -shared  .libs/tmp_2386fb144ce2ed06ae9438bb96d9264a.o   -Wl,-rpath -Wl,/opt/nrn/i686/lib -Wl,-rpath -Wl,/opt/nrn/i686/lib -L/opt/nrn/i686/lib /opt/nrn/i686/lib/libnrniv.so /opt/nrn/i686/lib/libnrnoc.so /opt/nrn/i686/lib/liboc.so /opt/nrn/i686/lib/libmemacs.so /opt/nrn/i686/lib/libnrnmpi.so /opt/nrn/i686/lib/libscopmath.so /opt/nrn/i686/lib/libsparse13.so -lreadline -lncurses /opt/nrn/i686/lib/libivoc.so /opt/nrn/i686/lib/libneuron_gnu.so /opt/nrn/i686/lib/libmeschach.so /opt/nrn/i686/lib/libsundials.so -lm -ldl    -pthread -Wl,-soname -Wl,tmp_2386fb144ce2ed06ae9438bb96d9264a.so.0 -o .libs/tmp_2386fb144ce2ed06ae9438bb96d9264a.so.0.0.0
	libtool: link: (cd ".libs" && rm -f "tmp_2386fb144ce2ed06ae9438bb96d9264a.so.0" && ln -s "tmp_2386fb144ce2ed06ae9438bb96d9264a.so.0.0.0" "tmp_2386fb144ce2ed06ae9438bb96d9264a.so.0")
	libtool: link: (cd ".libs" && rm -f "tmp_2386fb144ce2ed06ae9438bb96d9264a.so" && ln -s "tmp_2386fb144ce2ed06ae9438bb96d9264a.so.0.0.0" "tmp_2386fb144ce2ed06ae9438bb96d9264a.so")
	libtool: link: ( cd ".libs" && rm -f "tmp_2386fb144ce2ed06ae9438bb96d9264a.la" && ln -s "../tmp_2386fb144ce2ed06ae9438bb96d9264a.la" "tmp_2386fb144ce2ed06ae9438bb96d9264a.la" )
	
	Time for Building Mod-Files:  2.24586510658
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_4cc3885749eebcf1775a74eb11dd671d.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_a3553812a7f718c085a4a823bd216144.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_d4a5bc2a22fbec6439d6160858ee579f.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_19db2dbe48ecb0d3788957282bd83ad9.so
		1 
		1 
		1 
		50000 
		1 
		50000 
		1 
	Running Simulation
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3c2ac> t= 495.0 ms
	Time for Simulation:  0.0232088565826
	Time for Extracting Data: (2 records) 0.0269978046417
	Simulation Time Elapsed:  2.47572803497
	Suceeded
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.math
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.geom
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0)2012-07-15 15:56:59,785 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:56:59,785 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	 m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.neuro
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.physics
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/03/035f2d2995bbf88f7990032159ab5571.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0006'}
	Time for Building Mod-Files:  0.0185301303864
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_b07bbcf365ecea2aae6e648b610a1ff2.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_a1479dab1fe07b30ec5c2855b125eab7.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_10decdaa2e32802fec7781700d356b45.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_cbb831c4233006033934e95ad8c00b5e.so
		1 
		1 
		1 
		50000 
		1 
		50000 
		1 
	Running Simulation
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1490ec> t= 495.0 ms
	Time for Simulation:  0.024295091629
	Time for Extracting Data: (2 records) 0.0266988277435
	Simulation Time Elapsed:  0.254868984222
	Suceeded
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.math
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.geom
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <cla2012-07-15 15:57:00,661 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:00,661 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	ss 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.neuro
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.physics
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/de/de356f419ff736ee5978dd1862e70d03.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0009'}
	Time for Building Mod-Files:  0.00082802772522
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_eacbdcabc3bb4b562020900b87149ac4.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_2c04123bda44f28aa74fcc31c5271f49.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_7a3b5ec8d4fb46f977236bf9c08aa7a1.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_5c93fc6e3d09a04ecb6b138bd0e74fb8.so
		1 
		1 
		1 
		50000 
		1 
		50000 
		1 
	Running Simulation
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa5c70ec> t= 495.0 ms
	Time for Simulation:  0.0236411094666
	Time for Extracting Data: (2 records) 0.0266561508179
	Simulation Time Elapsed:  0.216575860977
	Suceeded
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.math
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.geom
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class '2012-07-15 15:57:01,513 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:01,514 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.neuro
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.physics
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/3d/3d444e8b1ae0a5cb4075a6823e77c174.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0012'}
	Time for Building Mod-Files:  0.000854969024658
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_d57e990052517b1e1526a5c75caed798.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_21dde146e3f31a5c601032da1341da93.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_837451c6db2b66ebcf2e741ab0ace7ec.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_abdd727e42d91e8646e026d8a97c9347.so
		1 
		1 
		1 
		50000 
		1 
		50000 
		1 
	Running Simulation
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb2290ec> t= 495.0 ms
	Time for Simulation:  0.0276951789856
	Time for Extracting Data: (2 records) 0.0265040397644
	Simulation Time Elapsed:  0.220376968384
	Suceeded
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.math
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.geom
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <cla2012-07-15 15:57:02,372 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:02,372 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	ss 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.neuro
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.physics
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/25/25438e7e76ceac867a7f0397259128ea.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0015'}
	Time for Building Mod-Files:  0.000834941864014
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_f84bd60faa7a35e41fca7277f26da86b.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_5125ada48cd4503c28ae4c72e09dde8d.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_e52c5d5ac4d8862da697bd2ce6638951.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_35aa1ff5dbd9fddc73194eb3d726bd04.so
		1 
		1 
		1 
		50000 
		1 
		50000 
		1 
	Running Simulation
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x97c50ec> t= 495.0 ms
	Time for Simulation:  0.0318119525909
	Time for Extracting Data: (2 records) 0.0268659591675
	Simulation Time Elapsed:  0.223824977875
	Suceeded
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.math
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.geom
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <cla2012-07-15 15:57:03,214 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:03,214 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	ss 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.neuro
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.physics
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/7b/7b1f3902349a3c1025279cc717088e14.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0018'}
	Time for Building Mod-Files:  0.0269439220428
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_ca23cee98765d97b15ab1db82308978f.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_a5e0e68cf36e7a6445a4d7e0e7bf31e4.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_59acc08507541e459acd3628a793800d.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_d40da2d1cf6807e702bb849854f744b8.so
		1 
		1 
		1 
		50000 
		1 
		50000 
		1 
	Running Simulation
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabcf0ec> t= 495.0 ms
	Time for Simulation:  0.0334160327911
	Time for Extracting Data: (2 records) 0.0264401435852
	Simulation Time Elapsed:  0.281780004501
	Suceeded
	neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.neuro
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.physics
	['simulation']
	['simulation']
	['simulation']
	['simulation']
	['simulation']
	['simulation']
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa1d308c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa1dd20c>
	Saving File _output/figures/singlecell_simulation040/eps/fig000_Autosave_figure_1.eps
	Saving File _output/figures/singlecell_simulation040/pdf/fig000_Autosave_figure_1.pdf
	Saving File _output/figures/singlecell_simulation040/png/fig000_Autosave_figure_1.png
	Saving File _output/figures/singlecell_simulation040/svg/fig000_Autosave_figure_1.svg
	




