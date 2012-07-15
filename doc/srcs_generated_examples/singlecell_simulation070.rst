
16. Visualising the internal states of a neuron
===============================================


Visualising the internal states of a neuron

We look at the internal states of an HH neuron, and plot the properties on
different graphs.

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
	from morphforgecontrib.stdimports import *
	
	
	
	# Create the environment:
	env = NeuronSimulationEnvironment()
	
	# Create the simulation:
	mySim = env.Simulation()
	
	
	# Create a cell:
	morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
	m1 = MorphologyTree.fromDictionary(morphDict1)
	myCell = mySim.create_cell(name="Cell1", morphology=m1)
	
	
	lkChannels = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Lk", env=env)
	naChannels = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Na", env=env)
	kChannels = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="K", env=env)
	
	
	# Apply the channels uniformly over the cell
	apply_mechanism_everywhere_uniform(myCell, lkChannels )
	apply_mechanism_everywhere_uniform(myCell, naChannels )
	apply_mechanism_everywhere_uniform(myCell, kChannels )
	apply_passive_everywhere_uniform(myCell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )
	
	# Get a cell_location on the cell:
	somaLoc = myCell.get_location("soma")
	
	# Create the stimulus and record the injected current:
	cc = mySim.create_currentclamp( name="Stim1", amp=unit("250:pA"), dur=unit("100:ms"), delay=unit("100:ms"), cell_location=somaLoc)
	mySim.record( cc, what=StandardTags.Current)
	# Define what to record:
	mySim.record( myCell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = somaLoc )
	
	
	mySim.record( lkChannels, cell_location = somaLoc, what=StandardTags.ConductanceDensity )
	mySim.record( naChannels, cell_location = somaLoc, what=StandardTags.ConductanceDensity )
	mySim.record( kChannels,  cell_location = somaLoc, what=StandardTags.ConductanceDensity )
	
	mySim.record( lkChannels, cell_location = somaLoc,what=StandardTags.CurrentDensity )
	mySim.record( naChannels, cell_location = somaLoc,what=StandardTags.CurrentDensity )
	mySim.record( kChannels,  cell_location = somaLoc, what=StandardTags.CurrentDensity )
	
	
	mySim.record( naChannels, cell_location = somaLoc, what=StandardTags.StateVariable, state="m" )
	mySim.record( naChannels, cell_location = somaLoc, what=StandardTags.StateVariable, state="h" )
	mySim.record( kChannels,  cell_location = somaLoc, what=StandardTags.StateVariable, state="n" )
	
	
	# Also:
	#mySim.record( naChannels, where = somaLoc, what=StandardTags.StateTimeConstant, state="m" )
	#mySim.record( naChannels, where = somaLoc, what=StandardTags.StateTimeConstant, state="h" )
	#mySim.record( kChannels,  where = somaLoc, what=StandardTags.StateTimeConstant, state="n" )
	
	#mySim.record( naChannels, where = somaLoc, what=StandardTags.StateSteadyState, state="m" )
	#mySim.record( naChannels, where = somaLoc, what=StandardTags.StateSteadyState, state="h" )
	#mySim.record( kChannels,  where = somaLoc, what=StandardTags.StateSteadyState, state="n" )
	
	
	# run the simulation
	results = mySim.run()
	
	
	# Display the results, there is a lot of info for one graph, so lets split it up:
	TagViewer([results], timeranges=[(50, 250)*pq.ms], show=False )
	
	
	TagViewer([results], timeranges=[(50, 250)*pq.ms], show=False,
	          plotspecs = [
	                       DefaultPlotSpec.Voltage,
	                       DefaultPlotSpec.Current,
	                       DefaultPlotSpec.CurrentDensity,
	                       ] )
	
	
	TagViewer([results], timeranges=[(100, 120)*pq.ms], show=True,
	          plotspecs = [
	                       DefaultPlotSpec.Voltage,
	                       DefaultPlotSpec.ConductanceDensity,
	                       DefaultPlotSpec.StateVariable,
	                       ] )
	




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation070_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation070_out1.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation070_out2.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation070_out2.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation070_out3.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation070_out3.png>`






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
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
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
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
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
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.physics
	['name', 'simulation']
	kwargs {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0xabe958c>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.MNeuronSimulation object at 0xabd3c6c>}
	kwargs2: {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0xabe958c>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.MNeuronSimulation object at 0xabd3c6c>}
	kwargs {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0xabe958c>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.MNeuronSimulation object at 0xabd3c6c>}
	kwargs2: {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0xabe958c>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.MNeuronSimulation object at 0xabd3c6c>}
	kwargs {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0xabe958c>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.MNeuronSimulation object at 0xabd3c6c>}
	kwargs2: {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0xabe958c>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.MNeuronSimulation object at 0xabd3c6c>}
	kwargs {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0xabe958c>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.MNeuronSimulation object at 0xabd3c6c>}
	kwargs2: {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0xabe958c>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.MNeuronSimulation object at 0xabd3c6c>}
	kwargs {'state': 'm', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0xabe958c>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.MNeuronSimulation object at 0xabd3c6c>}
	kwargs2: {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0xabe958c>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.MNeuronSimulation object at 0xabd3c6c>}
	kwargs {'state': 'h', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0xabe958c>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.MNeuronSimulation object at 0xabd3c6c>}
	kwargs2: {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0xabe958c>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.MNeuronSimulation object at 0xabd3c6c>}
	kwargs {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0xabe958c>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.MNeur2012-07-15 15:57:12,043 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:12,043 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
	onSimulation object at 0xabd3c6c>}
	kwargs2: {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0xabe958c>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.MNeuronSimulation object at 0xabd3c6c>}
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa54ccac>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa55b84c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa55b5cc>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa55b50c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa55ba4c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa54ccac>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa55b5cc>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa55b84c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa54ccac>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa55b50c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa55ba4c>
	Saving File _output/figures/singlecell_simulation070/eps/fig000_Autosave_figure_1.eps
	Saving File _output/figures/singlecell_simulation070/pdf/fig000_Autosave_figure_1.pdf
	Saving File _output/figures/singlecell_simulation070/png/fig000_Autosave_figure_1.png
	Saving File _output/figures/singlecell_simulation070/svg/fig000_Autosave_figure_1.svg
	Saving File _output/figures/singlecell_simulation070/eps/fig001_Autosave_figure_2.eps
	Saving File _output/figures/singlecell_simulation070/pdf/fig001_Autosave_figure_2.pdf
	Saving File _output/figures/singlecell_simulation070/png/fig001_Autosave_figure_2.png
	Saving File _output/figures/singlecell_simulation070/svg/fig001_Autosave_figure_2.svg
	Saving File _output/figures/singlecell_simulation070/eps/fig002_Autosave_figure_3.eps
	Saving File _output/figures/singlecell_simulation070/pdf/fig002_Autosave_figure_3.pdf
	Saving File _output/figures/singlecell_simulation070/png/fig002_Autosave_figure_3.png
	Saving File _output/figures/singlecell_simulation070/svg/fig002_Autosave_figure_3.svg
	




