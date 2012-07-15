
13. Demonstrate using NEURON mod files directly in a simulation
===============================================================


Demonstrate using NEURON mod files directly in a simulation
We run two simulations, using 2 slightly different mod files, and plot the membrane voltage seen.

Code
~~~~

.. code-block:: python

	
	
	
	
	
	
	
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

    	2012-07-15 16:21:40,271 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 16:21:40,271 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
	2012-07-15 16:21:40,854 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 16:21:40,854 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/f7/f78a7ff8cda9a0e85f72144e79adc8ea.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_AnonObj0001', 'recVecName': 'SomaVoltage'}
	Time for Building Mod-Files:  0.00067400932312
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_b9e50529a8d1f686ed3955884ae081fa.so
		1 
		1 
		1 
		50000 
		1 
	Running Simulation
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa7c284c> t= 495.0 ms
	Time for Simulation:  0.0292630195618
	Time for Extracting Data: (1 records) 0.0140027999878
	Simulation Time Elapsed:  0.138566017151
	Suceeded
	2012-07-15 16:21:41,717 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 16:21:41,718 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/de/de09183d8c713c07020db5df0421aec6.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_AnonObj0002', 'recVecName': 'SomaVoltage'}
	Time for Building Mod-Files:  0.000704050064087
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_5e54856fc3939091ebcff35b32cc9ab3.so
		1 
		1 
		1 
		50000 
		1 
	Running Simulation
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xac5684c> t= 495.0 ms
	Time for Simulation:  0.0317208766937
	Time for Extracting Data: (1 records) 0.014536857605
	Simulation Time Elapsed:  0.142915964127
	Suceeded
	15c15
	<         SUFFIX exampleChannels3a
	---
	>         SUFFIX exampleChannels3b
	28c28
	<         el = -64.3 (mV)
	---
	>         el = -44.3 (mV)
	['name', 'simulation']
	['name', 'simulation']
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa16bc0c>
	Saving File _output/figures/singlecell_simulation050/eps/fig000_Autosave_figure_1.eps
	Saving File _output/figures/singlecell_simulation050/pdf/fig000_Autosave_figure_1.pdf
	Saving File _output/figures/singlecell_simulation050/png/fig000_Autosave_figure_1.png
	Saving File _output/figures/singlecell_simulation050/svg/fig000_Autosave_figure_1.svg
	Differences between the two mod files:
	




