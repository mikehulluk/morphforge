
9. The response of a single compartment neuron with leak channels to step current injection
===========================================================================================



The response of a single compartment neuron with leak channels to step current injection.
In this example, we build a single section neuron, with passive channels,
and stimulate it with a step current clamp of 200pA for 100ms starting at t=100ms.  
We also create a summary pdf of the simulation. 



Code
~~~~

.. code-block:: python

	
	"""The response of a single compartment neuron with leak channels to step current injection.
	In this example, we build a single section neuron, with passive channels,
	and stimulate it with a step current clamp of 200pA for 100ms starting at t=100ms.  
	We also create a summary pdf of the simulation. 
	"""
	 
	 
	
	from morphforge.stdimports import *
	from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmleak import MM_LeakChannel
	
	
	# Create the morphology for the cell:
	morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
	m1 = MorphologyTree.fromDictionary(morphDict1)
	
	# Create the environment:
	env = NeuronSimulationEnvironment()
	
	# Create the simulation:
	mySim = env.Simulation()
	
	
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
	
	# Create the stimulus and record the injected current:
	cc = mySim.createCurrentClamp( name="Stim1", amp=unit("200:pA"), dur=unit("100:ms"), delay=unit("100:ms"), celllocation=somaLoc)
	
	
	# Define what to record:
	mySim.record( myCell, what=StdRec.MembraneVoltage, name="SomaVoltage", location = somaLoc ) 
	mySim.recordall( leakChannels, where=somaLoc)
	
	
	# Run the simulation
	results = mySim.Run()
	
	# Create an output .pdf
	SimulationSummariser(simulationresult=results, filename="Simulation010Output.pdf", make_graphs=True)
	
	# Display the results:
	TagViewer([results], figtitle="The response of a neuron to step current injection", timeranges=[(95, 200)*pq.ms], show=True )
	
	
	
	


Output
~~~~~~

.. code-block:: bash

    	Setting Random Seed: 89933
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//bb/bbf0028ba2a0424680cb813ac5fd9d4b.bundle
	Setting Random Seed: 27763
	Time for Building Mod-Files:  0.161846160889
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_e6a1c9496e8e65aa950509b29828a683.so
		1 
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0252041816711
	Time for Extracting Data: (3 records) 0.0017101764679
	Simulation Time Elapsed:  0.804562091827
	Suceeded
	Setting Random Seed: 27763
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x4148b10>
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x40f1390>
	Setting Time Range [  95.  200.] ms
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x40f59d0>
	Setting Time Range [  95.  200.] ms
	Setting Yunit 1.0 mA/cm2
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x4124e50>
	Setting Time Range [  95.  200.] ms
	Setting Yunit 0.001 S/cm2
	Saving File _output/figures/singlecell_simulation010/eps/fig000_The response of a neuron to step current injection.eps
	Saving File _output/figures/singlecell_simulation010/pdf/fig000_The response of a neuron to step current injection.pdf
	Saving File _output/figures/singlecell_simulation010/png/fig000_The response of a neuron to step current injection.png
	Saving File _output/figures/singlecell_simulation010/svg/fig000_The response of a neuron to step current injection.svg
	



Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation010_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation010_out1.png>`



