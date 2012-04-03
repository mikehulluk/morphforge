
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
	
	#SimulationSummariser(simulationresult=results, filename="/home/michael/Desktop/outBlha.pdf", make_graphs=True)
	# Display the results:
	TagViewer([results], timeranges=[(95, 200)*pq.ms], show=False )
	#import pylab
	#pylab.show()
	
	
	


Output
~~~~~~

.. code-block:: bash

    	Setting Random Seed: 85703
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//dc/dc9b6341cdc7ee771d8983c234ec7f8b.bundle
	Setting Random Seed: 70159
	Time for Building Mod-Files:  0.000668048858643
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_a2d2ff7f838ea7ab5d497051e4e86a49.so
		1 
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.00986313819885
	Time for Extracting Data: (3 records) 0.00323700904846
	Simulation Time Elapsed:  0.325742006302
	Suceeded
	Setting Random Seed: 70159
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x3895b10>
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x383e310>
	Setting Time Range [  95.  200.] ms
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x3842950>
	Setting Time Range [  95.  200.] ms
	Setting Yunit 1.0 mA/cm2
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x3863dd0>
	Setting Time Range [  95.  200.] ms
	Setting Yunit 0.001 S/cm2
	Saving File _output/figures/singlecell_simulation10/eps/fig000_None.eps
	Saving File _output/figures/singlecell_simulation10/pdf/fig000_None.pdf
	Saving File _output/figures/singlecell_simulation10/png/fig000_None.png
	Saving File _output/figures/singlecell_simulation10/svg/fig000_None.svg
	



Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation10_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation10_out1.png>`



