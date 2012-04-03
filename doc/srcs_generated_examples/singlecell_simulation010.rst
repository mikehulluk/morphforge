
9. Single compartment with leak channels response to current injection
======================================================================



Single compartment with leak channels response to current injection.
In this example, we build a single section neuron, with passive channels,
and stimulate it with a current clamp


Code
~~~~

.. code-block:: python

	
	
	 
	 
	
	from morphforge.stdimports import *
	#from morphforgecontrib.stdimports import *
	from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmleak import MM_LeakChannel
	
	
	# Create the morphology for the cell:
	morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
	m1 = MorphologyTree.fromDictionary(morphDict1)
	
	# Create the environment:
	env = NeuronSimulationEnvironment()
	
	# Create the simulation:
	mySim = env.Simulation(name="TestSim1")
	
	
	# Create a cell:
	myCell = mySim.createCell(name="Cell1", morphology=m1)
	
	
	# Apply the mechanisms to the cells
	leakChannels = env.MembraneMechanism( MM_LeakChannel, 
	                         name="LkChl", 
	                         conductance=unit("0.25:mS/cm2"), 
	                         reversalpotential=unit("-51:mV"),
	                         mechanism_id = 'HULL12_DIN_LK_ID'
	                        )
	    
	shortcuts.ApplyMechanismEverywhereUniform(myCell, leakChannels )
	shortcuts.ApplyPassiveEverywhereUniform(myCell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )
	
	
	# Get a location on the cell:
	somaLoc = myCell.getLocation("soma")
	
	# Create the simulous:
	mySim.createCurrentClamp( name="Stim1", amp=unit("200:pA"), dur=unit("100:ms"), delay=unit("100:ms"), celllocation=somaLoc)
	
	
	# Define what to record:
	mySim.record( myCell, what=StdRec.MembraneVoltage, name="SomaVoltage", location = somaLoc ) #, description='Membrane Voltage')
	mySim.recordall( leakChannels, where=somaLoc)
	
	
	
	# Run the simulation
	results = mySim.Run()
	
	SimulationSummariser(simulationresult=results, filename="outBlha.pdf", make_graphs=True)
	# Display the results:
	TagViewer([results], timeranges=[(95, 200)*pq.ms], show=False )
	#import pylab
	#pylab.show()
	
	
	


Output
~~~~~~

.. code-block:: bash

    	Setting Random Seed: 15919
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//52/522007e4c05d114a4ac9abd9aa833201.bundle
	Setting Random Seed: 8374
	Time for Building Mod-Files:  0.0207109451294
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_c13fa0a8998fb81175e7d2e0b21af153.so
		1 
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0131168365479
	Time for Extracting Data: (3 records) 0.00168490409851
	Simulation Time Elapsed:  0.357455015182
	Suceeded
	Setting Random Seed: 8374
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x393ab10>
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x38e3310>
	Setting Time Range [  95.  200.] ms
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x38e7950>
	Setting Time Range [  95.  200.] ms
	Setting Yunit 1.0 mA/cm2
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x3908dd0>
	Setting Time Range [  95.  200.] ms
	Setting Yunit 0.001 S/cm2
	Saving File _output/figures/singlecell_simulation010/eps/fig000_None.eps
	Saving File _output/figures/singlecell_simulation010/pdf/fig000_None.pdf
	Saving File _output/figures/singlecell_simulation010/png/fig000_None.png
	Saving File _output/figures/singlecell_simulation010/svg/fig000_None.svg
	



Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation010_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation010_out1.png>`



