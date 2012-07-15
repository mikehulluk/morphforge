
14. Visualising action potential propagation along an axon
==========================================================


Visualising action potential propagation along an axon
In this simulation, we create a cell with a long axon. We put HH-channels over its surface
and give it a short current injection into the soma. We look at the voltage at various points
along the axon, and see it propogate.

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
	
	
	# Create the environment:
	env = NeuronSimulationEnvironment()
	
	# Create the simulation:
	mySim = env.Simulation()
	
	# Create a cell:
	morph = MorphologyBuilder.get_soma_axon_morph(axon_length=3000.0, axon_radius=0.15, soma_radius=9.0, axon_sections=20)
	myCell = mySim.create_cell(name="Cell1", morphology=morph)
	
	
	leakChannels = env.MembraneMechanism(
	                         MM_LeakChannel,
	                         name="LkChl",
	                         conductance=unit("0.3:mS/cm2"),
	                         reversalpotential=unit("-54.3:mV"),
	                         mechanism_id = 'HULL12_DIN_LK_ID'
	                        )
	
	sodiumStateVars = { "m": {
	                      "alpha":[-4.00,-0.10,-1.00,40.00,-10.00],
	                      "beta": [ 4.00, 0.00, 0.00,65.00, 18.00]},
	                    "h": {
	                        "alpha":[0.07,0.00,0.00,65.00,20.00] ,
	                        "beta": [1.00,0.00,1.00,35.00,-10.00]}
	                  }
	
	sodiumChannels = env.MembraneMechanism(
	                        MM_AlphaBetaChannel,
	                        name="NaChl", ion="na",
	                        equation="m*m*m*h",
	                        conductance=unit("120:mS/cm2"),
	                        reversalpotential=unit("50:mV"),
	                        statevars=sodiumStateVars,
	                        mechanism_id="HH_NA_CURRENT"
	                        )
	kStateVars = { "n": {
	                      "alpha":[-0.55,-0.01,-1.0,55.0,-10.0],
	                      "beta": [0.125,0,0,65,80]},
	                   }
	
	kChannels = env.MembraneMechanism(
	                        MM_AlphaBetaChannel,
	                        name="KChl", ion="k",
	                        equation="n*n*n*n",
	                        conductance=unit("36:mS/cm2"),
	                        reversalpotential=unit("-77:mV"),
	                        statevars=kStateVars,
	                        mechanism_id="HH_K_CURRENT"
	                        )
	
	
	# Apply the channels uniformly over the cell
	apply_mechanism_everywhere_uniform(myCell, leakChannels )
	apply_mechanism_everywhere_uniform(myCell, sodiumChannels )
	apply_mechanism_everywhere_uniform(myCell, kChannels )
	apply_passive_everywhere_uniform(myCell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )
	
	# Get a cell_location on the cell:
	somaLoc = myCell.get_location("soma")
	
	# Create the stimulus and record the injected current:
	cc = mySim.create_currentclamp( name="Stim1", amp=unit("250:pA"), dur=unit("5:ms"), delay=unit("100:ms"), cell_location=somaLoc)
	mySim.record( cc, what=StandardTags.Current)
	
	
	
	# To record along the axon, we create a set of 'CellLocations', at the distances
	# specified (start,stop,
	for cell_location in CellLocator.get_locations_at_distances_away_from_dummy(cell=myCell, distances=range(9, 3000, 100) ):
	
	    print " -- ",cell_location.section
	    print " -- ",cell_location.sectionpos
	    print " -- ",cell_location.get_3d_position()
	
	    # Create a path along the morphology from the centre of the
	    # Soma
	    path = MorphPath( somaLoc, cell_location)
	    print "Distance to Soma Centre:", path.get_length()
	
	    mySim.record( myCell, what=StandardTags.Voltage, cell_location=cell_location, description="Distance Recording at %0.0f (um)"% path.get_length() )
	
	
	# Define what to record:
	mySim.record( myCell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = somaLoc )
	
	# run the simulation
	results = mySim.run()
	
	# Display the results:
	TagViewer([results], timeranges=[(97.5, 140)*pq.ms] )
	




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation060_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation060_out1.png>`






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
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
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
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.physics
	['name', 'simulation']
	 --  <SectionObject: [0.000000,0.000000,0.000000, r=9.000000] -> [18.000000,0.000000,0.000000, r=9.000000], Length: 18.00, Region:soma, idtag:soma, >
	 --  0.5
	 --  [ 9.  0.  0.]
	Distance to Soma Centre: 0.0
	 --  <SectionObject: [18.000000,0.000000,0.000000, r=9.000000] -> [168.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_1, >
	 --  0.606666666667
	 --  [ 109.    0.    0.]
	Distance to Soma Centre: 100.0
	 --  <SectionObject: [168.000000,0.000000,0.000000, r=0.150000] -> [318.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_2, >
	 --  0.273333333333
	 --  [ 209.    0.    0.]
	Distance to Soma Centre: 200.0
	 --  <SectionObject: [168.000000,0.000000,0.000000, r=0.150000] -> [318.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_2, >
	 --  0.94
	 --  [ 309.    0.    0.]
	Distance to Soma Centre: 300.0
	 --  <SectionObject: [318.000000,0.000000,0.000000, r=0.150000] -> [468.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_3, >
	 --  0.606666666667
	 --  [ 409.    0.    0.]
	Distance to Soma Centre: 400.0
	 --  <SectionObject: [468.000000,0.000000,0.000000, r=0.150000] -> [618.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_4, >
	 --  0.273333333333
	 --  [ 509.    0.    0.]
	Distance to Soma Centre: 500.0
	 --  <SectionObject: [468.000000,0.000000,0.000000, r=0.150000] -> [618.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_4, >
	 --  0.94
	 --  [ 609.    0.    0.]
	Distance to Soma Centre: 600.0
	 --  <SectionObject: [618.000000,0.000000,0.000000, r=0.150000] -> [768.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_5, >
	 --  0.606666666667
	 --  [ 709.    0.    0.]
	Distance to Soma Centre: 700.0
	 --  <SectionObject: [768.000000,0.000000,0.000000, r=0.150000] -> [918.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_6, >
	 --  0.273333333333
	 --  [ 809.    0.    0.]
	Distance to Soma Centre: 800.0
	 --  <SectionObject: [768.000000,0.000000,0.000000, r=0.150000] -> [918.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_6, >
	 --  0.94
	 --  [ 909.    0.    0.]
	Distance to Soma Centre: 900.0
	 --  <SectionObject: [918.000000,0.000000,0.000000, r=0.150000] -> [1068.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_7, >
	 --  0.606666666667
	 --  [ 1009.     0.     0.]
	Distance to Soma Centre: 1000.0
	 --  <SectionObject: [1068.000000,0.000000,0.000000, r=0.150000] -> [1218.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_8, >
	 --  0.273333333333
	 --  [ 1109.     0.     0.]
	Distance to Soma Centre: 1100.0
	 --  <SectionObject: [1068.000000,0.2012-07-15 15:57:08,062 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:08,062 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
	000000,0.000000, r=0.150000] -> [1218.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_8, >
	 --  0.94
	 --  [ 1209.     0.     0.]
	Distance to Soma Centre: 1200.0
	 --  <SectionObject: [1218.000000,0.000000,0.000000, r=0.150000] -> [1368.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_9, >
	 --  0.606666666667
	 --  [ 1309.     0.     0.]
	Distance to Soma Centre: 1300.0
	 --  <SectionObject: [1368.000000,0.000000,0.000000, r=0.150000] -> [1518.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_10, >
	 --  0.273333333333
	 --  [ 1409.     0.     0.]
	Distance to Soma Centre: 1400.0
	 --  <SectionObject: [1368.000000,0.000000,0.000000, r=0.150000] -> [1518.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_10, >
	 --  0.94
	 --  [ 1509.     0.     0.]
	Distance to Soma Centre: 1500.0
	 --  <SectionObject: [1518.000000,0.000000,0.000000, r=0.150000] -> [1668.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_11, >
	 --  0.606666666667
	 --  [ 1609.     0.     0.]
	Distance to Soma Centre: 1600.0
	 --  <SectionObject: [1668.000000,0.000000,0.000000, r=0.150000] -> [1818.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_12, >
	 --  0.273333333333
	 --  [ 1709.     0.     0.]
	Distance to Soma Centre: 1700.0
	 --  <SectionObject: [1668.000000,0.000000,0.000000, r=0.150000] -> [1818.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_12, >
	 --  0.94
	 --  [ 1809.     0.     0.]
	Distance to Soma Centre: 1800.0
	 --  <SectionObject: [1818.000000,0.000000,0.000000, r=0.150000] -> [1968.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_13, >
	 --  0.606666666667
	 --  [ 1909.     0.     0.]
	Distance to Soma Centre: 1900.0
	 --  <SectionObject: [1968.000000,0.000000,0.000000, r=0.150000] -> [2118.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_14, >
	 --  0.273333333333
	 --  [ 2009.     0.     0.]
	Distance to Soma Centre: 2000.0
	 --  <SectionObject: [1968.000000,0.000000,0.000000, r=0.150000] -> [2118.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_14, >
	 --  0.94
	 --  [ 2109.     0.     0.]
	Distance to Soma Centre: 2100.0
	 --  <SectionObject: [2118.000000,0.000000,0.000000, r=0.150000] -> [2268.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_15, >
	 --  0.606666666667
	 --  [ 2209.     0.     0.]
	Distance to Soma Centre: 2200.0
	 --  <SectionObject: [2268.000000,0.000000,0.000000, r=0.150000] -> [2418.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_16, >
	 --  0.273333333333
	 --  [ 2309.     0.     0.]
	Distance to Soma Centre: 2300.0
	 --  <SectionObject: [2268.000000,0.000000,0.000000, r=0.150000] -> [2418.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_16, >
	 --  0.94
	 --  [ 2409.     0.     0.]
	Distance to Soma Centre: 2400.0
	 --  <SectionObject: [2418.000000,0.000000,0.000000, r=0.150000] -> [2568.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_17, >
	 --  0.606666666667
	 --  [ 2509.     0.     0.]
	Distance to Soma Centre: 2500.0
	 --  <SectionObject: [2568.000000,0.000000,0.000000, r=0.150000] -> [2718.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_18, >
	 --  0.273333333333
	 --  [ 2609.     0.     0.]
	Distance to Soma Centre: 2600.0
	 --  <SectionObject: [2568.000000,0.000000,0.000000, r=0.150000] -> [2718.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_18, >
	 --  0.94
	 --  [ 2709.     0.     0.]
	Distance to Soma Centre: 2700.0
	 --  <SectionObject: [2718.000000,0.000000,0.000000, r=0.150000] -> [2868.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_19, >
	 --  0.606666666667
	 --  [ 2809.     0.     0.]
	Distance to Soma Centre: 2800.0
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa06decc>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa07b46c>
	Saving File _output/figures/singlecell_simulation060/eps/fig000_Autosave_figure_1.eps
	Saving File _output/figures/singlecell_simulation060/pdf/fig000_Autosave_figure_1.pdf
	Saving File _output/figures/singlecell_simulation060/png/fig000_Autosave_figure_1.png
	Saving File _output/figures/singlecell_simulation060/svg/fig000_Autosave_figure_1.svg
	




