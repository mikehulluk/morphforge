
11. Hodgkin-Huxley '52 neuron simulation with automatic summary pdf generation
==============================================================================



 Hodgkin-Huxley '52 neuron simulation with automatic summary pdf generation. 

AS BEFORE: A simulation of the HodgkinHuxley52 neuron. Same Caveeat! 
MIKE: TODO!

Whats nice is that adding a single line, generates a pdf output of the simulation! 

SimulationSummariser(simulationresult=results, filename="SimulationOutput.pdf", make_graphs=True)

You can do this one any simulation.
 



Code
~~~~

.. code-block:: python

	
	
	""" Hodgkin-Huxley '52 neuron simulation with automatic summary pdf generation. 
	
	AS BEFORE: A simulation of the HodgkinHuxley52 neuron. Same Caveeat! 
	MIKE: TODO!
	
	Whats nice is that adding a single line, generates a pdf output of the simulation! 
	
	SimulationSummariser(simulationresult=results, filename="SimulationOutput.pdf", make_graphs=True)
	
	You can do this one any simulation.
	 
	"""
	
	 
	
	from morphforge.stdimports import *
	from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmleak import MM_LeakChannel
	from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmalphabeta import MM_AlphaBetaChannel
	
	# Create the morphology for the cell:
	
	
	# Create the environment:
	env = NeuronSimulationEnvironment()
	
	# Create the simulation:
	mySim = env.Simulation()
	
	
	# Create a cell:
	morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
	m1 = MorphologyTree.fromDictionary(morphDict1)
	
	myCell = mySim.createCell(name="Cell1", morphology=m1)
	
	
	# Apply the mechanisms to the cells
	leakChannels = env.MembraneMechanism( 
	                         MM_LeakChannel, 
	                         name="LkChl", 
	                         conductance=unit("0.3:mS/cm2"), 
	                         reversalpotential=unit("0:mV"),
	                         mechanism_id = 'HULL12_DIN_LK_ID'
	                        )
	
	sodiumStateVars = { "m": { 
	                      "alpha":[2.5, -0.1, -1.0, -25,-10],
	                      "beta": [4.0, 0.0, 0.0, 0.0, 18  ]},
	                "h": { 
	                        "alpha":[0.07, 0.0, 0.0, 0.0, 20.0] ,
	                        "beta": [1.0, 0.0, 1.0, -30.0, -10]} 
	                  } 
	sodiumChannels = env.MembraneMechanism( 
	                        MM_AlphaBetaChannel,
	                        name="NaChl", ion="na",
	                        equation="m*m*m*h",
	                        conductance=unit("120:mS/cm2"),
	                        reversalpotential=unit("115.0:mV"),
	                        statevars=sodiumStateVars,
	                        mechanism_id="HH_NA_CURRENT"
	                        )
	kStateVars = { "n": { 
	                      "alpha":[0.1,-0.01,-1,-10,-10],
	                      "beta": [0.125,0,0,0,80]},
	                   }
	kChannels = env.MembraneMechanism( 
	                        MM_AlphaBetaChannel,
	                        name="KChl", ion="k",
	                        equation="n*n*n*n",
	                        conductance=unit("36:mS/cm2"),
	                        reversalpotential=unit("-12.0:mV"),
	                        statevars=kStateVars,
	                        mechanism_id="HH_K_CURRENT"
	                        )
	
	shortcuts.ApplyMechanismEverywhereUniform(myCell, leakChannels )
	shortcuts.ApplyMechanismEverywhereUniform(myCell, sodiumChannels )
	shortcuts.ApplyMechanismEverywhereUniform(myCell, kChannels )
	shortcuts.ApplyPassiveEverywhereUniform(myCell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )
	
	
	# Get a location on the cell:
	somaLoc = myCell.getLocation("soma")
	
	# Create the stimulus and record the injected current:
	cc = mySim.createCurrentClamp( name="Stim1", amp=unit("250:pA"), dur=unit("100:ms"), delay=unit("100:ms"), celllocation=somaLoc)
	
	
	# Define what to record:
	mySim.record( myCell, what=StdRec.MembraneVoltage, name="SomaVoltage", location = somaLoc ) 
	mySim.recordall( leakChannels, where=somaLoc)
	mySim.recordall( sodiumChannels,state="m", where=somaLoc)
	mySim.recordall( sodiumChannels,state="h", where=somaLoc)
	
	
	# Run the simulation
	results = mySim.Run()
	
	SimulationSummariser(simulationresult=results, filename="SimulationOutput.pdf", make_graphs=True)
	
	# Display the results:
	TagViewer([results], timeranges=[(95, 200)*pq.ms], show=True )
	


Output
~~~~~~

.. code-block:: bash

    	Setting Random Seed: 4479
	[0.07, 0.0, 0.0, 0.0, 20.0]
	
	[1.0, 0.0, 1.0, -30.0, -10]
	
	[2.5, -0.1, -1.0, -25, -10]
	
	[4.0, 0.0, 0.0, 0.0, 18]
	
	[0.1, -0.01, -1, -10, -10]
	
	[0.125, 0, 0, 0, 80]
	
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x34eaa50>
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x34953d0>
	Setting Time Range [  95.  200.] ms
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x3499a10>
	Setting Time Range [  95.  200.] ms
	Setting Yunit 1.0 mA/cm2
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x34c7f10>
	Setting Time Range [  95.  200.] ms
	Setting Yunit 0.001 S/cm2
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x34cf1d0>
	Setting Time Range [  95.  200.] ms
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x34ccd50>
	Setting Time Range [  95.  200.] ms
	Setting Yunit 1 ms (millisecond)
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x34da2d0>
	Setting Time Range [  95.  200.] ms
	Saving File _output/figures/singlecell_simulation030/eps/fig000_None.eps
	Saving File _output/figures/singlecell_simulation030/pdf/fig000_None.pdf
	Saving File _output/figures/singlecell_simulation030/png/fig000_None.png
	Saving File _output/figures/singlecell_simulation030/svg/fig000_None.svg
	



Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation030_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation030_out1.png>`



