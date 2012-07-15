
29. Action potential propagation and synaptic transmission
==========================================================


Action potential propagation and synaptic transmission.
In this simulation, we create 3 neurons; Neuron 1 has an axon, and when the
soma is stimulated, we see the action potential propagate along it. Neuron 1
forms synapses onto cell2 and cell3 with different strengths and different
positions along the axon.

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
	
	
	
	
	
	
	
	
	import matplotlib as mpl
	mpl.rcParams['font.size'] = 14
	
	
	
	from morphforge.stdimports import *
	from morphforgecontrib.stdimports import *
	
	# Create a cell:
	def build_cell(name,sim):
	
	    my_morph = MorphologyBuilder.get_soma_axon_morph(axon_length=1500.0, axon_radius=0.3, soma_radius=10.0, )
	    my_cell = sim.create_cell(name=name, morphology=my_morph)
	
	    na_chls = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Na", env=sim.environment)
	    k_chls  = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="K",  env=sim.environment)
	    lk_chls = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Lk", env=sim.environment)
	
	    apply_mechanism_everywhere_uniform(my_cell, lk_chls )
	    apply_mechanism_everywhere_uniform(my_cell, k_chls )
	    apply_mechanism_everywhere_uniform(my_cell, na_chls )
	    apply_mechanism_region_uniform( my_cell,
	                                    na_chls,
	                                    region = my_cell.get_region("axon"),
	                                    parameter_multipliers={'gScale':1.0} )
	    return my_cell
	
	
	# Create a simulation:
	env = NeuronSimulationEnvironment()
	sim = env.Simulation()
	
	# Two cells:
	cell1 = build_cell(name="cell1",sim=sim)
	cell2 = build_cell(name="cell2",sim=sim)
	cell3 = build_cell(name="cell3",sim=sim)
	
	
	# Connect with a synapse:
	simple_ampa_syn = """
	EQNSET syn_simple {
	
	    g' = - g/g_tau
	    i = gmax * (v-erev) * g
	
	    gmax = 300pS * scale
	    erev = 0mV
	
	    g_tau = 10ms
	    <=> INPUT     v: mV       METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
	    <=> OUTPUT    i:(mA)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }
	    <=> PARAMETER scale:()
	    ==>> on_event() {
	        g = g + 1.0
	    }
	}
	"""
	
	
	syn1 = sim.create_synapse(
	        presynaptic_mech =  env.PreSynapticMechanism(
	                                    PreSynapticMech_VoltageThreshold,
	                                    cell_location = CellLocator.get_location_at_distance_away_from_dummy(cell1, 300),
	                                    voltage_threshold = U("0:mV"),  delay = U("0:ms"),     weight = U("1:nS"),
	                                    ),
	        postsynaptic_mech = env.PostSynapticMechanism(
	                                    NeuroUnitEqnsetPostSynaptic,
	                                    eqnset = neurounits.NeuroUnitParser.EqnSet(simple_ampa_syn),
	                                    default_parameters= {'scale':1.0*pq.dimensionless},
	                                    cell_location = cell2.get_location("soma")
	                                    )
	        )
	
	syn1 = sim.create_synapse(
	        presynaptic_mech =  env.PreSynapticMechanism(
	                                    PreSynapticMech_VoltageThreshold,
	                                    cell_location = CellLocator.get_location_at_distance_away_from_dummy(cell1, 700),
	                                    voltage_threshold = U("0:mV"),  delay = U("0:ms"), weight = U("1:nS"),
	                                    ),
	        postsynaptic_mech = env.PostSynapticMechanism(
	                                    NeuroUnitEqnsetPostSynaptic,
	                                    eqnset = neurounits.NeuroUnitParser.EqnSet(simple_ampa_syn),
	                                    default_parameters= {'scale':2.0*pq.dimensionless},
	                                    cell_location = cell3.get_location("soma")
	                                    )
	        )
	
	# Record Voltages from axons:
	for loc in CellLocator.get_locations_at_distances_away_from_dummy( cell1, range(0,1000,50) ):
	    sim.record(  what=StandardTags.Voltage, cell_location = loc, user_tags=['cell1'] )
	sim.record( what=StandardTags.Voltage, cell_location = cell2.get_location("soma"), user_tags=['cell2'] )
	sim.record( what=StandardTags.Voltage, cell_location = cell3.get_location("soma"), user_tags=['cell3'] )
	
	# Create the stimulus and record the injected current:
	cc = sim.create_currentclamp( name="CC1", amp=U("200:pA"), dur=U("1:ms"), delay=U("100:ms"), cell_location=cell1.get_location("soma"))
	sim.record(cc, what=StandardTags.Current)
	
	results = sim.run()
	TagViewer(results, timeranges=[(98, 120)*pq.ms], 
	          fig_kwargs = {'figsize':(12,10)},
	          show=True,
	          plotspecs = [
	              PlotSpec_DefaultNew('Current', yunit=pq.picoamp),
	              PlotSpec_DefaultNew('Voltage,cell1', yrange=(-80*mV,50*mV), yunit=pq.mV ),
	              PlotSpec_DefaultNew('Voltage AND ANY{cell2,cell3}', yrange=(-70*mV,-55*mV), yunit=pq.millivolt),
	              ],
	            )
	
	
	




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/poster2_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/poster2_out1.png>`






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
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
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
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.neuro
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.physics
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 3 A 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	Reading JSON: {"mf":{"role":"MEMBRANEVOLTAGE"}}
	Reading JSON: {"mf":{"role":"TRANSMEMBRANECURRENT"}}
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 3 A 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 3 A 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<neurounits.ast.astobjects.Parameter object at 0xb06b9ec>
	scale
	iii 1.0 dimensionless <class 'quantities.quantity.Quantity'>
	iiii 1.0 dimensionless <class 'quantities.quantity.Quantity'>
	gmax <class 'neurounits.ast.astobjects.AssignedVariable'>
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	g <class 'neurounits.ast.astobjects.StateVariable'>
	scale <class 'neurounits.ast.astobjects.Parameter'>
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xb15accc>])
	g <class 'neurounits.ast.astobjects.StateVariable'>
	g <class 'neurounits.ast.astobjects.StateVariable'>
	1
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 3 A 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	Reading JSON: {"mf":{"role":"MEMBRANEVOLTAGE"}}
	Reading JSON: {"mf":{"role":"TRANSMEMBRANECURRENT"}}
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (2012-07-15 15:57:57,296 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:57,296 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
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
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <cla2012-07-15 15:57:58,263 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:58,263 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
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
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.physics
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/fd/fd0a641f7b130c99bfe48d154d40d754.bundle
	{'sectionpos': 0.0, 'sectionindex': 0, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0003'}
	{'sectionpos': 0.20000000000000001, 'sectionindex': 1, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0004'}
	{'sectionpos': 0.53333333333333333, 'sectionindex': 1, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0005'}
	{'sectionpos': 0.8666666666666667, 'sectionindex': 1, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0006'}
	{'sectionpos': 0.20000000000000001, 'sectionindex': 2, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0007'}
	{'sectionpos': 0.53333333333333333, 'sectionindex': 2, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0008'}
	{'sectionpos': 0.8666666666666667, 'sectionindex': 2, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0009'}
	{'sectionpos': 0.20000000000000001, 'sectionindex': 3, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0010'}
	{'sectionpos': 0.53333333333333333, 'sectionindex': 3, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0011'}
	{'sectionpos': 0.8666666666666667, 'sectionindex': 3, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0012'}
	{'sectionpos': 0.20000000000000001, 'sectionindex': 4, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0013'}
	{'sectionpos': 0.53333333333333333, 'sectionindex': 4, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0014'}
	{'sectionpos': 0.8666666666666667, 'sectionindex': 4, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0015'}
	{'sectionpos': 0.20000000000000001, 'sectionindex': 5, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0016'}
	{'sectionpos': 0.53333333333333333, 'sectionindex': 5, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0017'}
	{'sectionpos': 0.8666666666666667, 'sectionindex': 5, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0018'}
	{'sectionpos': 0.20000000000000001, 'sectionindex': 6, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0019'}
	{'sectionpos': 0.53333333333333333, 'sectionindex': 6, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0020'}
	{'sectionpos': 0.8666666666666667, 'sectionindex': 6, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0021'}
	{'sectionpos': 0.20000000000000001, 'sectionindex': 7, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0022'}
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_cell2', 'recVecName': 'AnonObj0023'}
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_cell3', 'recVecName': 'AnonObj0024'}
	Time for Building Mod-Files:  0.000967025756836
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_60c3176ccd39a2716e59acb4aae32c6c.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_b9561f3b8794fa66ebc2cce450f95024.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_e38908b5bc02fc80d5b0e1d97d5b1aa7.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_714554be3b0a5b42eb0b14c97a5be284.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_422ddf5f55a4c4e8a54500196d657969.so
		1 
		1 
		1 
		50000 
		1 
		50000 
		1 
		50000 
		1 
		50000 
		1 
		50000 
		1 
		50000 
		1 
		50000 
		1 
		50000 
		1 
		50000 
		1 
		50000 
		1 
		50000 
		1 
		50000 
		1 
		50000 
		1 
		50000 
		1 
		50000 
		1 
		50000 
		1 
		50000 
		1 
		50000 
		1 
		50000 
		1 
		50000 
		1 
		50000 
		1 
		50000 
		1 
		50000 
		1 
	Running Simulation
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9de298c> t= 495.0 ms
	Time for Simulation:  1.17776823044
	Time for Extracting Data: (23 records) 0.0677881240845
	Simulation Time Elapsed:  1.70889091492
	Suceeded
	10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 3 A 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 3 A 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<neurounits.ast.astobjects.Parameter object at 0xb14bc0c>
	scale
	iii 1.0 dimensionless <class 'quantities.quantity.Quantity'>
	iiii 2.0 dimensionless <class 'quantities.quantity.Quantity'>
	gmax <class 'neurounits.ast.astobjects.AssignedVariable'>
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	g <class 'neurounits.ast.astobjects.StateVariable'>
	scale <class 'neurounits.ast.astobjects.Parameter'>
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xb14b58c>])
	g <class 'neurounits.ast.astobjects.StateVariable'>
	g <class 'neurounits.ast.astobjects.StateVariable'>
	1
	['name', 'simulation']
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xb06cc0c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xb14952c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xaab2f0c>
	Saving File _output/figures/poster2/eps/fig000_Autosave_figure_1.eps
	Saving File _output/figures/poster2/pdf/fig000_Autosave_figure_1.pdf
	Saving File _output/figures/poster2/png/fig000_Autosave_figure_1.png
	Saving File _output/figures/poster2/svg/fig000_Autosave_figure_1.svg
	




