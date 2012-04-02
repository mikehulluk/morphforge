
8. Single compartment with leak channels response to current injection
======================================================================



Single compartment with leak channels response to current injection.
In this example, we build a single section neuron, with passive channels,
and stimulate it with a current clamp


Code
~~~~

.. code-block:: python

	
	
	 
	 
	
	from morphforge.stdimports import *
	from morphforgecontrib.stdimports import *
	
	
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
	#pylab.show()
	
	
	


Output
~~~~~~

.. code-block:: bash

    	Setting Random Seed: 16720
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//46/463f110ab3ff6e45b20768a66ce616c6.bundle
	Setting Random Seed: 57232
	Time for Building Mod-Files:  0.0592141151428
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_513f173ceab2f0d74a008de097f4cfcf.so
		1 
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0188381671906
	Time for Extracting Data: (3 records) 0.00119209289551
	Simulation Time Elapsed:  0.541245222092
	Suceeded
	Setting Random Seed: 57232
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x4fe9a10>
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x3e4c590>
	Setting Time Range [  95.  200.] ms
	[array(1.0) * s, array(1.0) * kg*m**2/(s**3*A)]
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x3e53950>
	Setting Time Range [  95.  200.] ms
	Setting Yunit 1.0 mA/cm2
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x3e6c290>
	Setting Time Range [  95.  200.] ms
	Setting Yunit 0.001 S/cm2
	Saving File _output/figures/simulation10/eps/fig000_None.eps
	Saving File _output/figures/simulation10/pdf/fig000_None.pdf
	Saving File _output/figures/simulation10/png/fig000_None.png
	Saving File _output/figures/simulation10/svg/fig000_None.svg
	



Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/simulation10_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/simulation10_out1.png>`



