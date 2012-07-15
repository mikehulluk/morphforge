
17. Applying different channel densities over a cell
====================================================


Applying different channel densities over a cell.
We start with a cell with a long axon, and then apply Hodgkin-Huxley channels over the surface.
We look at the effect of changing the density of leak and sodium channels in just the axon
of the neuron (not the soma)

This example also shows the use of tags; 300 traces are recorded in this experiment; but we don't ever need to get
involved in managing them directly. We can just specify that all traces recorded on simulation X should be tagged with "SIMY", and
then tell the TagViewer to plot everything with a tag 'SIMY'

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
	from morphforgecontrib.data_library.stdmodels import StandardModels
	
	
	def sim( glk_multiplier, gna_multiplier, tag):
	    # Create the environment:
	    env = NeuronSimulationEnvironment()
	
	    # Create the simulation:
	    mySim = env.Simulation()
	
	    # Create a cell:
	    morph = MorphologyBuilder.get_soma_axon_morph(axon_length=3000.0, axon_radius=0.3, soma_radius=9.0, axon_sections=20)
	    myCell = mySim.create_cell(name="Cell1", morphology=morph)
	
	
	    lkChannels = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Lk", env=env)
	    naChannels = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Na", env=env)
	    kChannels  = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="K", env=env)
	
	    # Apply the channels uniformly over the cell
	    apply_mechanism_everywhere_uniform(myCell, lkChannels )
	    apply_mechanism_everywhere_uniform(myCell, naChannels )
	    apply_mechanism_everywhere_uniform(myCell, kChannels )
	
	    # Over-ride the parameters in the axon:
	    apply_mechanism_region_uniform(cell=myCell, mechanism=lkChannels, region=morph.get_region("axon"), parameter_multipliers={'gScale':glk_multiplier})
	    apply_mechanism_region_uniform(cell=myCell, mechanism=naChannels, region=morph.get_region("axon"), parameter_multipliers={'gScale':gna_multiplier})
	
	    apply_passive_everywhere_uniform(myCell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )
	
	
	    for cell_location in CellLocator.get_locations_at_distances_away_from_dummy(cell=myCell, distances=range(9, 3000, 100) ):
	        mySim.record( myCell, what=StandardTags.Voltage, cell_location=cell_location, user_tags=[tag])
	
	    # Create the stimulus and record the injected current:
	    cc = mySim.create_currentclamp( name="Stim1", amp=unit("250:pA"), dur=unit("5:ms"), delay=unit("100:ms"), cell_location=myCell.get_location("soma"))
	    mySim.record( cc, what=StandardTags.Current)
	
	    # run the simulation
	    return mySim.run()
	
	
	# Display the results:
	results_a = [
	    sim( glk_multiplier=0.1, gna_multiplier=1.0, tag="SIM1"),
	    sim( glk_multiplier=0.5, gna_multiplier=1.0, tag="SIM2"),
	    sim( glk_multiplier=1.0, gna_multiplier=1.0, tag="SIM3"),
	    sim( glk_multiplier=5.0, gna_multiplier=1.0, tag="SIM4"),
	    sim( glk_multiplier=10.0, gna_multiplier=1.0, tag="SIM5"),
	]
	
	TagViewer(results_a, timeranges=[(97.5, 140)*pq.ms], show=False,
	          plotspecs = [
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM1}", ylabel='gLeak: 0.1\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM2}", ylabel='gLeak: 0.5\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM3}", ylabel='gLeak: 1.0\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM4}", ylabel='gLeak: 5.0\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM5}", ylabel='gLeak: 10.0\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
	                        ] )
	
	results_b = [
	    sim( gna_multiplier=0.1,  glk_multiplier=1.0, tag="SIM6"),
	    sim( gna_multiplier=0.5,  glk_multiplier=1.0, tag="SIM7"),
	    sim( gna_multiplier=0.75,  glk_multiplier=1.0, tag="SIM8"),
	    sim( gna_multiplier=1.0,  glk_multiplier=1.0, tag="SIM9"),
	]
	
	TagViewer(results_b, timeranges=[(97.5, 140)*pq.ms],show=True,
	          plotspecs = [
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM6}", ylabel='gNa: 0.10\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM7}", ylabel='gNa: 0.50\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM8}", ylabel='gNa: 0.75\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM9}", ylabel='gNa: 1.00\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
	                        ] )
	
	




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation080_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation080_out1.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation080_out2.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation080_out2.png>`






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
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class '2012-07-15 15:57:16,493 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:16,493 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
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
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
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
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.physics
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/70/707c29ed0b279c26824d99de385160dd.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0001'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 1, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0002'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 2, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0003'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 2, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0004'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 3, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0005'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 4, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0006'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 4, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0007'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 5, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0008'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0009'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0010'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 7, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0011'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 8, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0012'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 8, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0013'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 9, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0014'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 10, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0015'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 10, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0016'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 11, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0017'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 12, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0018'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 12, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0019'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 13, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0020'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 14, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0021'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 14, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0022'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 15, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0023'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 16, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0024'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 12012-07-15 15:57:17,298 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:17,298 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0025'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 17, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0026'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 18, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0027'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 18, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0028'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 19, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0029'}
	Time for Building Mod-Files:  0.00070595741272
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_9b5f608a37f872edf03d16c72ccd71c5.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_74c59031c780519a8019364f7c98b1b3.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_0aa0a8d639fdf428b84cdd20ccde5bd3.so
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
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa27ec0c> t= 495.0 ms
	Time for Simulation:  1.12704896927
	Time for Extracting Data: (30 records) 0.0834000110626
	Simulation Time Elapsed:  1.53092384338
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
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
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
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
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
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
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
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.physics
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/d0/d0c46ba47905fc834176e24842d6573d.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0031'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 1, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0032'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 2, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0033'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 2, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0034'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 3, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0035'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 4, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0036'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 4, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0037'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 5, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0038'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0039'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0040'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 7, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0041'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 8, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0042'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 8, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0043'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 9, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0044'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 10, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0045'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 10, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0046'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 11, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0047'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 12, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0048'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 12, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0049'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 13, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0050'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 14, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0051'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 14, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0052'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 15, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0053'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 16, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0054'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 12012-07-15 15:57:19,588 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:19,589 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0055'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 17, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0056'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 18, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0057'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 18, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0058'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 19, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0059'}
	Time for Building Mod-Files:  0.000821113586426
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_60c3176ccd39a2716e59acb4aae32c6c.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_e38908b5bc02fc80d5b0e1d97d5b1aa7.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_714554be3b0a5b42eb0b14c97a5be284.so
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
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac6ac0c> t= 495.0 ms
	Time for Simulation:  0.907974004745
	Time for Extracting Data: (30 records) 0.0827829837799
	Simulation Time Elapsed:  1.29950594902
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
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
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
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.physics
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/ab/ab1dda01705443c2e12f94086579b371.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0061'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 1, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0062'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 2, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0063'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 2, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0064'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 3, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0065'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 4, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0066'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 4, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0067'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 5, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0068'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0069'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0070'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 7, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0071'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 8, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0072'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 8, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0073'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 9, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0074'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 10, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0075'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 10, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0076'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 11, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0077'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 12, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0078'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 12, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0079'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 13, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0080'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 14, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0081'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 14, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0082'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 15, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0083'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 16, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0084'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 12012-07-15 15:57:21,650 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:21,650 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0085'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 17, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0086'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 18, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0087'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 18, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0088'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 19, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0089'}
	Time for Building Mod-Files:  0.000795841217041
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_50fb1e9eb45ab8ccf2c2d61ae32fac39.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_a2e55ea8a1465ff936503e6d0f3a9d0e.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_12d1194d4bb488866054871d73cc817b.so
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
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xaa8bc0c> t= 495.0 ms
	Time for Simulation:  1.02453303337
	Time for Extracting Data: (30 records) 0.0834400653839
	Simulation Time Elapsed:  1.42239499092
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
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
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
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
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
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/f8/f8b5d6240d9a6e5fdac654115d56004c.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0091'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 1, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0092'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 2, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0093'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 2, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0094'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 3, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0095'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 4, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0096'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 4, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0097'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 5, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0098'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0099'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0100'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 7, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0101'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 8, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0102'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 8, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0103'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 9, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0104'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 10, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0105'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 10, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0106'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 11, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0107'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 12, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0108'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 12, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0109'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 13, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0110'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 14, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0111'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 14, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0112'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 15, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0113'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 16, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0114'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 12012-07-15 15:57:23,800 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:23,800 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0115'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 17, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0116'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 18, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0117'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 18, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0118'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 19, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0119'}
	Time for Building Mod-Files:  0.000798940658569
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_e2e990f5aa1742450266b98ba6885b64.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_c76c931cde75f4416460c45b2b7bcfc5.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_5a083cfce4e72edc3d6a4e32ec25038e.so
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
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa236c0c> t= 495.0 ms
	Time for Simulation:  1.01828312874
	Time for Extracting Data: (30 records) 0.0823349952698
	Simulation Time Elapsed:  1.41232419014
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
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
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
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
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
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/e0/e076fdafb2545efd5975fa6d44647e91.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0121'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 1, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0122'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 2, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0123'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 2, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0124'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 3, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0125'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 4, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0126'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 4, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0127'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 5, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0128'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0129'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0130'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 7, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0131'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 8, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0132'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 8, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0133'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 9, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0134'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 10, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0135'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 10, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0136'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 11, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0137'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 12, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0138'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 12, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0139'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 13, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0140'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 14, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0141'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 14, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0142'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 15, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0143'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 16, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0144'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 12012-07-15 15:57:25,960 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:25,960 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0145'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 17, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0146'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 18, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0147'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 18, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0148'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 19, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0149'}
	Time for Building Mod-Files:  0.000838994979858
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_05e1ace8ef45977a676d63590128e99c.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_0170d153d6ca1ececc3a1c9260c86586.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_eb6e5311202ce099218f66120c8a2be0.so
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
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9c14c0c> t= 495.0 ms
	Time for Simulation:  0.878076076508
	Time for Extracting Data: (30 records) 0.0829241275787
	Simulation Time Elapsed:  1.27732896805
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
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
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
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
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
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.physics
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/5b/5b2324c575c20e6fefceb305e56d1b0d.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0151'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 1, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0152'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 2, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0153'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 2, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0154'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 3, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0155'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 4, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0156'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 4, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0157'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 5, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0158'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0159'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0160'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 7, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0161'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 8, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0162'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 8, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0163'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 9, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0164'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 10, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0165'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 10, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0166'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 11, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0167'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 12, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0168'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 12, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0169'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 13, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0170'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 14, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0171'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 14, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0172'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 15, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0173'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 16, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0174'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 12012-07-15 15:57:28,413 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:28,413 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0175'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 17, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0176'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 18, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0177'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 18, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0178'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 19, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0179'}
	Time for Building Mod-Files:  0.00080394744873
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_1d0a7aab6a2979cc91b79a0046d619b6.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_e8ff9ed10d98f17b5b92ecae798304a9.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_ae8dc2e5f41a7aaf4d284687ad6f4546.so
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
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa923c0c> t= 495.0 ms
	Time for Simulation:  0.674100875854
	Time for Extracting Data: (30 records) 0.0832660198212
	Simulation Time Elapsed:  1.06122207642
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
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
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
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
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
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/90/9007f86c87bb1439cff32943e2727e69.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0181'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 1, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0182'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 2, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0183'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 2, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0184'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 3, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0185'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 4, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0186'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 4, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0187'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 5, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0188'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0189'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0190'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 7, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0191'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 8, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0192'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 8, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0193'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 9, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0194'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 10, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0195'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 10, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0196'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 11, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0197'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 12, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0198'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 12, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0199'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 13, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0200'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 14, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0201'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 14, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0202'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 15, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0203'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 16, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0204'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 12012-07-15 15:57:30,209 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:30,209 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0205'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 17, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0206'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 18, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0207'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 18, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0208'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 19, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0209'}
	Time for Building Mod-Files:  0.00085186958313
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_ad483f2dfaa4e0d8e2b14d0692ee3129.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_856de19994ece1aa19cdd264bc77e176.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_a1a4ac5c6a7af10df928da5f85ad473e.so
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
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb149c0c> t= 495.0 ms
	Time for Simulation:  1.03541517258
	Time for Extracting Data: (30 records) 0.0833389759064
	Simulation Time Elapsed:  1.43234705925
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
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
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
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
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
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
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
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/c5/c58688ce8aa7798e78691e6e05586009.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0211'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 1, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0212'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 2, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0213'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 2, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0214'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 3, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0215'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 4, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0216'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 4, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0217'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 5, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0218'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0219'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0220'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 7, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0221'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 8, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0222'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 8, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0223'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 9, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0224'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 10, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0225'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 10, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0226'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 11, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0227'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 12, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0228'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 12, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0229'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 13, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0230'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 14, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0231'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 14, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0232'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 15, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0233'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 16, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0234'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 12012-07-15 15:57:32,478 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:32,478 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0235'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 17, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0236'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 18, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0237'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 18, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0238'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 19, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0239'}
	Time for Building Mod-Files:  0.000783920288086
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_60c3176ccd39a2716e59acb4aae32c6c.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_e38908b5bc02fc80d5b0e1d97d5b1aa7.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_714554be3b0a5b42eb0b14c97a5be284.so
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
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa769c0c> t= 495.0 ms
	Time for Simulation:  1.2959561348
	Time for Extracting Data: (30 records) 0.0848181247711
	Simulation Time Elapsed:  1.72490501404
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
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
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
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
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
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
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
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/9c/9c7de7305967afb35d9b602a8e679df4.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0241'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 1, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0242'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 2, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0243'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 2, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0244'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 3, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0245'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 4, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0246'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 4, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0247'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 5, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0248'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0249'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0250'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 7, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0251'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 8, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0252'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 8, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0253'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 9, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0254'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 10, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0255'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 10, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0256'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 11, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0257'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 12, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0258'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 12, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0259'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 13, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0260'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 14, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0261'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 14, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0262'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 15, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0263'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 16, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0264'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 12012-07-15 15:57:35,106 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:35,106 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	6, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0265'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 17, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0266'}
	{'sectionpos': 0.27333333333333332, 'sectionindex': 18, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0267'}
	{'sectionpos': 0.93999999999999995, 'sectionindex': 18, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0268'}
	{'sectionpos': 0.60666666666666669, 'sectionindex': 19, 'cellname': 'cell_Cell1', 'recVecName': 'AnonObj0269'}
	Time for Building Mod-Files:  0.000779151916504
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_50fb1e9eb45ab8ccf2c2d61ae32fac39.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_a2e55ea8a1465ff936503e6d0f3a9d0e.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_12d1194d4bb488866054871d73cc817b.so
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
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9b3dc0c> t= 495.0 ms
	Time for Simulation:  1.12112092972
	Time for Extracting Data: (30 records) 0.0860569477081
	Simulation Time Elapsed:  1.54594278336
	Suceeded
	neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.neuro
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.physics
	['name', 'simulation']
	['name', 'simulation']
	['name', 'simulation']
	['name', 'simulation']
	['name', 'simulation']
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa243c6c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa25c6cc>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa1eaf4c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa26cc8c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa175ecc>
	['name', 'simulation']
	['name', 'simulation']
	['name', 'simulation']
	['name', 'simulation']
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xae43bec>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xae43fcc>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa26d76c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xad9652c>
	Saving File _output/figures/singlecell_simulation080/eps/fig000_Autosave_figure_1.eps
	Saving File _output/figures/singlecell_simulation080/pdf/fig000_Autosave_figure_1.pdf
	Saving File _output/figures/singlecell_simulation080/png/fig000_Autosave_figure_1.png
	Saving File _output/figures/singlecell_simulation080/svg/fig000_Autosave_figure_1.svg
	Saving File _output/figures/singlecell_simulation080/eps/fig001_Autosave_figure_2.eps
	Saving File _output/figures/singlecell_simulation080/pdf/fig001_Autosave_figure_2.pdf
	Saving File _output/figures/singlecell_simulation080/png/fig001_Autosave_figure_2.png
	Saving File _output/figures/singlecell_simulation080/svg/fig001_Autosave_figure_2.svg
	




