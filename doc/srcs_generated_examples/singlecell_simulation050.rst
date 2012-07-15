
13. Demonstrate using NEURON mod files directly in a simulation
===============================================================


Demonstrate using NEURON mod files directly in a simulation
We run two simulations, using 2 slightly different mod files, and plot the membrane voltage seen.

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
	from morphforgecontrib.simulation.membranemechanisms.exisitingmodfile.core import SimulatorSpecificChannel
	
	
	def build_simulation(modfilename):
	    # Create the morphology for the cell:
	    morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
	    m1 = MorphologyTree.fromDictionary(morphDict1)
	
	
	    # Create the environment:
	    env = NeuronSimulationEnvironment()
	
	    # Create the simulation:
	    mySim = env.Simulation()
	    myCell = mySim.create_cell(morphology=m1)
	    somaLoc = myCell.get_location("soma")
	
	    modChls = env.MembraneMechanism( SimulatorSpecificChannel,
	                                     modfilename =  modfilename,
	                                     mechanism_id='ID1')
	
	    # Apply the mechanisms to the cells
	    apply_mechanism_everywhere_uniform(myCell, modChls )
	
	    mySim.record( myCell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = somaLoc, description='Membrane Voltage')
	    mySim.create_currentclamp( name="Stim1", amp=unit("200:pA"), dur=unit("100:ms"), delay=unit("100:ms"), cell_location=somaLoc)
	
	    results = mySim.run()
	    return results
	
	
	
	mod3aFilename = Join(LocMgr.get_test_mods_path(), "exampleChannels3a.mod")
	results3a = build_simulation( mod3aFilename )
	
	mod3bFilename = Join(LocMgr.get_test_mods_path(), "exampleChannels3b.mod")
	results3b = build_simulation( mod3bFilename )
	
	TagViewer([results3a,results3b], timeranges=[(95, 200)*pq.ms] )
	
	try:
	    import os
	    print 'Differences between the two mod files:'
	    os.system("diff %s %s"%(mod3aFilename,mod3bFilename) )
	except:
	    print "<Can't run 'diff', so can't show differences!>"
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation050_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation050_out1.png>`






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
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <cla2012-07-15 15:57:05,099 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:05,099 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
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
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <cla2012-07-15 15:57:05,713 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:05,713 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
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
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.physics
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/dd/dd6566715a28c8feffdc3637513e65f5.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_AnonObj0001', 'recVecName': 'SomaVoltage'}
	Time for Building Mod-Files:  0.00122499465942
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_b9e50529a8d1f686ed3955884ae081fa.so
		1 
		1 
		1 
		50000 
		1 
	Running Simulation
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xab8084c> t= 495.0 ms
	Time for Simulation:  0.0374028682709
	Time for Extracting Data: (1 records) 0.014310836792
	Simulation Time Elapsed:  0.164366006851
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
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
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
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
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
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <cla2012-07-15 15:57:06,474 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:06,474 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	ss 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
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
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.physics
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/7a/7a980a494a3c8f1f278c062d105aafd4.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_AnonObj0002', 'recVecName': 'SomaVoltage'}
	Time for Building Mod-Files:  0.000720024108887
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_5e54856fc3939091ebcff35b32cc9ab3.so
		1 
		1 
		1 
		50000 
		1 
	Running Simulation
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7ac84c> t= 495.0 ms
	Time for Simulation:  0.0321161746979
	Time for Extracting Data: (1 records) 0.0144851207733
	Simulation Time Elapsed:  0.144726037979
	Suceeded
	15c15
	<         SUFFIX exampleChannels3a
	---
	>         SUFFIX exampleChannels3b
	28c28
	<         el = -64.3 (mV)
	---
	>         el = -44.3 (mV)
	ss 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.neuro
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.physics
	['name', 'simulation']
	['name', 'simulation']
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x9f88c0c>
	Saving File _output/figures/singlecell_simulation050/eps/fig000_Autosave_figure_1.eps
	Saving File _output/figures/singlecell_simulation050/pdf/fig000_Autosave_figure_1.pdf
	Saving File _output/figures/singlecell_simulation050/png/fig000_Autosave_figure_1.png
	Saving File _output/figures/singlecell_simulation050/svg/fig000_Autosave_figure_1.svg
	Differences between the two mod files:
	




