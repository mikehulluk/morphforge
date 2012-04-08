
10. Hodgkin-Huxley '52 neuron simulation
========================================



Hodgkin-Huxley '52 neuron simulation.

A simulation of the HodgkinHuxley52 neuron. We create 3 channels, Lk, Na, and K channels and apply them over the neuron. 
The morphforge backend takes care of building/compiling .mod-files from these,
and runs the simulation.
Note that the neurons reseting potentials have been shifted from 0mV to -65mV.



Code
~~~~

.. code-block:: python

	
	
	"""Hodgkin-Huxley '52 neuron simulation.
	
	A simulation of the HodgkinHuxley52 neuron. We create 3 channels, Lk, Na, and K channels and apply them over the neuron. 
	The morphforge backend takes care of building/compiling .mod-files from these,
	and runs the simulation.
	Note that the neurons reseting potentials have been shifted from 0mV to -65mV.
	"""
	
	 
	
	from morphforge.stdimports import *
	from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmleak import MM_LeakChannel
	from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmalphabeta import MM_AlphaBetaChannel
	
	
	# Create the environment:
	env = NeuronSimulationEnvironment()
	
	# Create the simulation:
	mySim = env.Simulation()
	
	
	# Create a cell:
	morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
	m1 = MorphologyTree.fromDictionary(morphDict1)
	myCell = mySim.createCell(name="Cell1", morphology=m1)
	
	
	leakChannels = env.MembraneMechanism( 
	                         MM_LeakChannel, 
	                         name="LkChl", 
	                         conductance=unit("0.3:mS/cm2"), 
	                         reversalpotential=unit("-54.3:mV"),
	                         mechanism_id = 'HULL12_DIN_LK_ID'
	                        )
	
	sodiumStateVars = { "m": { 
	                      "alpha":[-4.00,-0.10,-1.00,40.00,-10.00],
	                      "beta": [ 4.00, 0.00, 0.00,65.00, 18.00]},
	                    "h": { 
	                        "alpha":[0.07,0.00,0.00,65.00,20.00] ,
	                        "beta": [1.00,0.00,1.00,35.00,-10.00]} 
	                  }
	
	sodiumChannels = env.MembraneMechanism( 
	                        MM_AlphaBetaChannel,
	                        name="NaChl", ion="na",
	                        equation="m*m*m*h",
	                        conductance=unit("120:mS/cm2"),
	                        reversalpotential=unit("50:mV"),
	                        statevars=sodiumStateVars,
	                        mechanism_id="HH_NA_CURRENT"
	                        )
	kStateVars = { "n": { 
	                      "alpha":[-0.55,-0.01,-1.0,55.0,-10.0],
	                      "beta": [0.125,0,0,65,80]},
	                   }
	
	kChannels = env.MembraneMechanism( 
	                        MM_AlphaBetaChannel,
	                        name="KChl", ion="k",
	                        equation="n*n*n*n",
	                        conductance=unit("36:mS/cm2"),
	                        reversalpotential=unit("-77:mV"),
	                        statevars=kStateVars,
	                        mechanism_id="HH_K_CURRENT"
	                        )
	
	
	# Apply the channels uniformly over the cell
	ApplyMechanismEverywhereUniform(myCell, leakChannels )
	ApplyMechanismEverywhereUniform(myCell, sodiumChannels )
	ApplyMechanismEverywhereUniform(myCell, kChannels )
	ApplyPassiveEverywhereUniform(myCell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )
	
	# Get a location on the cell:
	somaLoc = myCell.getLocation("soma")
	
	# Create the stimulus and record the injected current:
	cc = mySim.createCurrentClamp( name="Stim1", amp=unit("250:pA"), dur=unit("100:ms"), delay=unit("100:ms"), celllocation=somaLoc)
	mySim.record( cc, what=StdRec.Current)
	# Define what to record:
	mySim.record( myCell, what=StdRec.MembraneVoltage, name="SomaVoltage", location = somaLoc ) 
	
	# Run the simulation
	results = mySim.Run()
	
	# Display the results:
	TagViewer([results], timeranges=[(50, 250)*pq.ms], show=True )
	


Output
~~~~~~

.. code-block:: bash

    	Setting Random Seed: 53346
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//b0/b0a7f8162b5939b41041ec66ed5a4f4a.bundle
	Setting Random Seed: 80520
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_24107a3909362c4bad4decdab973e591.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_24107a3909362c4bad4decdab973e591.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_24107a3909362c4bad4decdab973e591.lo tmp_24107a3909362c4bad4decdab973e591.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_24107a3909362c4bad4decdab973e591.la  -rpath /opt/nrn/x86_64/libs  tmp_24107a3909362c4bad4decdab973e591.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_3c7916bd99f54c4a22464bcd3c7c223b.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_3c7916bd99f54c4a22464bcd3c7c223b.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_3c7916bd99f54c4a22464bcd3c7c223b.lo tmp_3c7916bd99f54c4a22464bcd3c7c223b.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_3c7916bd99f54c4a22464bcd3c7c223b.la  -rpath /opt/nrn/x86_64/libs  tmp_3c7916bd99f54c4a22464bcd3c7c223b.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_38a8944c766fa751f7c9434c01ea48fb.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_38a8944c766fa751f7c9434c01ea48fb.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_38a8944c766fa751f7c9434c01ea48fb.lo tmp_38a8944c766fa751f7c9434c01ea48fb.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_38a8944c766fa751f7c9434c01ea48fb.la  -rpath /opt/nrn/x86_64/libs  tmp_38a8944c766fa751f7c9434c01ea48fb.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Time for Building Mod-Files:  1.63297009468
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_6a9024390484a2ca23db81d9eb0ba1de.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_c9363fb7f2e9afde70041ff6f549790e.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_9bf335229af6a5bc679edab09814d8de.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0373530387878
	Time for Extracting Data: (2 records) 0.000810861587524
	Simulation Time Elapsed:  1.94410085678
	Suceeded
	Setting Random Seed: 80520
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x39cce50>
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x38abf50>
	Setting Time Range [  50.  250.] ms
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x38c3e10>
	Setting Time Range [  50.  250.] ms
	Setting Yunit 1 pA (picoampere)
	Saving File _output/figures/singlecell_simulation020/eps/fig000_None.eps
	Saving File _output/figures/singlecell_simulation020/pdf/fig000_None.pdf
	Saving File _output/figures/singlecell_simulation020/png/fig000_None.png
	Saving File _output/figures/singlecell_simulation020/svg/fig000_None.svg
	



Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation020_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation020_out1.png>`



