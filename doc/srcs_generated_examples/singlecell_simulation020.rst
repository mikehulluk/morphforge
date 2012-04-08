
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

    	Setting Random Seed: 31242
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x36c8e90>
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x36732d0>
	Setting Time Range [  50.  250.] ms
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x3694ad0>
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



