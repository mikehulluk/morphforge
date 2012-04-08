
13. Demonstrate using NEURON mod files directly in a simulation
===============================================================



Demonstrate using NEURON mod files directly in a simulation
We run two simulations, using 2 slightly different mod files, and plot the membrane voltage seen.




Code
~~~~

.. code-block:: python

	"""Demonstrate using NEURON mod files directly in a simulation
	We run two simulations, using 2 slightly different mod files, and plot the membrane voltage seen.
	
	"""
	
	
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
	    myCell = mySim.createCell(morphology=m1)
	    somaLoc = myCell.getLocation("soma")
	    
	    modChls = env.MembraneMechanism( SimulatorSpecificChannel, 
	                                     modfilename =  modfilename, 
	                                     mechanism_id='ID1')
	                                          
	    # Apply the mechanisms to the cells
	    ApplyMechanismEverywhereUniform(myCell, modChls )
	    
	    mySim.record( myCell, what=StdRec.MembraneVoltage, name="SomaVoltage", location = somaLoc, description='Membrane Voltage')
	    mySim.createCurrentClamp( name="Stim1", amp=unit("200:pA"), dur=unit("100:ms"), delay=unit("100:ms"), celllocation=somaLoc)
	    
	    results = mySim.Run()
	    return results
	
	
	
	mod3aFilename = Join(LocMgr.getTestModsPath(), "exampleChannels3a.mod")
	results3a = build_simulation( mod3aFilename )
	
	mod3bFilename = Join(LocMgr.getTestModsPath(), "exampleChannels3b.mod")
	results3b = build_simulation( mod3bFilename )
	
	TagViewer([results3a,results3b], timeranges=[(95, 200)*pq.ms] )
	
	try:
	    import os
	    print 'Differences between the two mod files:'
	    os.system("diff %s %s"%(mod3aFilename,mod3bFilename) )
	except:
	    print "<Can't run 'diff', so can't show differences!>"
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	


Output
~~~~~~

.. code-block:: bash

    	Setting Random Seed: 71470
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//28/281ffa067ff42a730ce491c02884cd06.bundle
	Setting Random Seed: 18744
	Time for Building Mod-Files:  0.000924825668335
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_b9e50529a8d1f686ed3955884ae081fa.so
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0191788673401
	Time for Extracting Data: (1 records) 0.000524997711182
	Simulation Time Elapsed:  0.135529994965
	Suceeded
	Setting Random Seed: 1954
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//3e/3ed67a09ee1f184f12e9d3b248c9cffd.bundle
	Setting Random Seed: 18744
	Time for Building Mod-Files:  0.000703096389771
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_5e54856fc3939091ebcff35b32cc9ab3.so
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0208940505981
	Time for Extracting Data: (1 records) 0.000429153442383
	Simulation Time Elapsed:  0.111531972885
	Suceeded
	15c15
	<         SUFFIX exampleChannels3a
	---
	>         SUFFIX exampleChannels3b
	28c28
	<         el = -64.3 (mV)
	---
	>         el = -44.3 (mV)
	Setting Random Seed: 18744
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x3d8bf10>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x3d8b8d0>
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x3d33350>
	Setting Time Range [  95.  200.] ms
	Saving File _output/figures/singlecell_simulation050/eps/fig000_None.eps
	Saving File _output/figures/singlecell_simulation050/pdf/fig000_None.pdf
	Saving File _output/figures/singlecell_simulation050/png/fig000_None.png
	Saving File _output/figures/singlecell_simulation050/svg/fig000_None.svg
	Differences between the two mod files:
	



Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation050_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation050_out1.png>`



