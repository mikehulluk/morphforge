
9. The response of a single compartment neuron with leak channels to step current injection
===========================================================================================


The response of a single compartment neuron with leak channels to step current injection.
In this example, we build a single section neuron, with passive channels,
and stimulate it with a step current clamp of 200pA for 100ms starting at t=100ms.
We also create a summary pdf of the simulation.

Code
~~~~

.. code-block:: python

	
	
	
	
	
	
	
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
	myCell = mySim.create_cell(name="Cell1", morphology=m1)
	
	
	# Apply the mechanisms to the cells
	leakChannels = env.MembraneMechanism( MM_LeakChannel,
	                         name="LkChl",
	                         conductance=unit("0.25:mS/cm2"),
	                         reversalpotential=unit("-51:mV"),
	                         mechanism_id = 'HULL12_DIN_LK_ID'
	                        )
	
	apply_mechanism_everywhere_uniform(myCell, leakChannels )
	apply_passive_everywhere_uniform(myCell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )
	
	
	# Get a cell_location on the cell:
	somaLoc = myCell.get_location("soma")
	
	# Create the stimulus and record the injected current:
	cc = mySim.create_currentclamp( name="Stim1", amp=unit("200:pA"), dur=unit("100:ms"), delay=unit("100:ms"), cell_location=somaLoc)
	
	
	# Define what to record:
	mySim.record( myCell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = somaLoc )
	mySim.recordall( leakChannels, cell_location=somaLoc)
	
	
	# run the simulation
	results = mySim.run()
	
	# Create an output .pdf
	SimulationSummariser(simulationresult=results, filename="Simulation010Output.pdf", make_graphs=True)
	
	# Display the results:
	TagViewer([results], figtitle="The response of a neuron to step current injection", timeranges=[(95, 200)*pq.ms], show=True )
	
	
	
	




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation010_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation010_out1.png>`






Output
~~~~~~

.. code-block:: bash

    	2012-07-15 16:21:32,517 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 16:21:32,517 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
	['name', 'simulation']
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa579c4c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa5887ec>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa5884ac>
	Saving File _output/figures/singlecell_simulation010/eps/fig000_Autosave_figure_1.eps
	Saving File _output/figures/singlecell_simulation010/pdf/fig000_Autosave_figure_1.pdf
	Saving File _output/figures/singlecell_simulation010/png/fig000_Autosave_figure_1.png
	Saving File _output/figures/singlecell_simulation010/svg/fig000_Autosave_figure_1.svg
	




