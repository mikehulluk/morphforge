
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
	from morphforgecontrib.stdimports import SimulatorSpecificChannel
	
	
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

    	15c15
	<         SUFFIX exampleChannels3a
	---
	>         SUFFIX exampleChannels3b
	28c28
	<         el = -64.3 (mV)
	---
	>         el = -44.3 (mV)
	Setting Random Seed: 96235
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x3b5c350>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x3b5cbd0>
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x2f013d0>
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



