
20. The response of a single compartment neuron with leak channels to step current injection
============================================================================================



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
	    
	ApplyMechanismEverywhereUniform(myCell, leakChannels )
	ApplyPassiveEverywhereUniform(myCell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )
	
	
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

    	Setting Random Seed: 13884
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//cb/cbbe3a6de645e817a1f43ee7ad921b65.bundle
	Setting Random Seed: 8809
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_27a24a6c6e585f71d3d88b5172de79d9.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_27a24a6c6e585f71d3d88b5172de79d9.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_27a24a6c6e585f71d3d88b5172de79d9.lo tmp_27a24a6c6e585f71d3d88b5172de79d9.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_27a24a6c6e585f71d3d88b5172de79d9.la  -rpath /opt/nrn/x86_64/libs  tmp_27a24a6c6e585f71d3d88b5172de79d9.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Time for Building Mod-Files:  0.452130079269
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_38182cdfb96724bab91b81e2b9014344.so
		1 
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.00867795944214
	Time for Extracting Data: (3 records) 0.00119590759277
	Simulation Time Elapsed:  0.680875062943
	Suceeded
	Setting Random Seed: 8809
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x2569c10>
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x2514950>
	Setting Time Range [  95.  200.] ms
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x251ad10>
	Setting Time Range [  95.  200.] ms
	Setting Yunit 1.0 mA/cm2
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x254ddd0>
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



