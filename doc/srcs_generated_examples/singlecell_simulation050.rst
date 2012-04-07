
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
	    mySim = env.Simulation(name="TestSim1")
	    myCell = mySim.createCell(name="Cell1", morphology=m1)
	    somaLoc = myCell.getLocation("soma")
	    
	    modChls = env.MembraneMechanism( SimulatorSpecificChannel, modfilename =  modfilename, mechanism_id='ID1')
	                                          
	    # Apply the mechanisms to the cells
	    shortcuts.ApplyMechanismEverywhereUniform(myCell, modChls )
	    
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

    	Setting Random Seed: 27442
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//5a/5ac7ffb647202db607b728d3c48144a9.bundle
	Setting Random Seed: 64154
	Time for Building Mod-Files:  0.000705003738403
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_b9e50529a8d1f686ed3955884ae081fa.so
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0171499252319
	Time for Extracting Data: (1 records) 0.000407934188843
	Simulation Time Elapsed:  0.105490922928
	Suceeded
	Setting Random Seed: 43972
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//2f/2f80893bdedbaee7a56c589b7276ea12.bundle
	Setting Random Seed: 64154
	Time for Building Mod-Files:  0.000780820846558
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_5e54856fc3939091ebcff35b32cc9ab3.so
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0243318080902
	Time for Extracting Data: (1 records) 0.000430822372437
	Simulation Time Elapsed:  0.116508960724
	Suceeded
	15c15
	<         SUFFIX exampleChannels3a
	---
	>         SUFFIX exampleChannels3b
	28c28
	<         el = -64.3 (mV)
	---
	>         el = -44.3 (mV)
	Setting Random Seed: 64154
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x349ac10>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x349a490>
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x34435d0>
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



