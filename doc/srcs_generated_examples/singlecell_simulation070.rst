
15. None
========



None


Code
~~~~

.. code-block:: python

	
	from morphforge.traces.tagviewer.tagviewer import DefaultPlotSpec
	
	
	"""Visualising the internal states of a neuron 
	
	We look at the internal states of an HH neuron, and plot the properties on 
	different graphs.
	
	"""
	
	
	from morphforge.stdimports import *
	from morphforgecontrib.data_library.stdmodels import StandardModels
	
	
	
	# Create the environment:
	env = NeuronSimulationEnvironment()
	
	# Create the simulation:
	mySim = env.Simulation()
	
	
	# Create a cell:
	morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
	m1 = MorphologyTree.fromDictionary(morphDict1)
	myCell = mySim.createCell(name="Cell1", morphology=m1)
	
	
	lkChannels = ChannelLibrary.getChannel(modelsrc=StandardModels.HH52, channeltype="Lk", env=env)
	naChannels = ChannelLibrary.getChannel(modelsrc=StandardModels.HH52, channeltype="Na", env=env) 
	kChannels = ChannelLibrary.getChannel(modelsrc=StandardModels.HH52, channeltype="K", env=env) 
	 
	
	# Apply the channels uniformly over the cell
	ApplyMechanismEverywhereUniform(myCell, lkChannels )
	ApplyMechanismEverywhereUniform(myCell, naChannels )
	ApplyMechanismEverywhereUniform(myCell, kChannels )
	ApplyPassiveEverywhereUniform(myCell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )
	
	# Get a location on the cell:
	somaLoc = myCell.getLocation("soma")
	
	# Create the stimulus and record the injected current:
	cc = mySim.createCurrentClamp( name="Stim1", amp=unit("250:pA"), dur=unit("100:ms"), delay=unit("100:ms"), celllocation=somaLoc)
	mySim.record( cc, what=StdRec.Current)
	# Define what to record:
	mySim.record( myCell, what=StdRec.MembraneVoltage, name="SomaVoltage", location = somaLoc ) 
	
	
	mySim.record( lkChannels, where = somaLoc, what=StdRec.ConductanceDensity )
	mySim.record( naChannels, where = somaLoc, what=StdRec.ConductanceDensity )
	mySim.record( kChannels,  where = somaLoc, what=StdRec.ConductanceDensity )
	
	mySim.record( lkChannels, where = somaLoc,what=StdRec.CurrentDensity )
	mySim.record( naChannels, where = somaLoc,what=StdRec.CurrentDensity )
	mySim.record( kChannels,  where = somaLoc, what=StdRec.CurrentDensity )
	
	
	mySim.record( naChannels, where = somaLoc, what=StdRec.StateVariable, state="m" )
	mySim.record( naChannels, where = somaLoc, what=StdRec.StateVariable, state="h" )
	mySim.record( kChannels,  where = somaLoc, what=StdRec.StateVariable, state="n" )
	
	
	# Also:
	#mySim.record( naChannels, where = somaLoc, what=StdRec.StateVarTimeConstant, state="m" )
	#mySim.record( naChannels, where = somaLoc, what=StdRec.StateVarTimeConstant, state="h" )
	#mySim.record( kChannels,  where = somaLoc, what=StdRec.StateVarTimeConstant, state="n" )
	
	#mySim.record( naChannels, where = somaLoc, what=StdRec.StateVarSteadyState, state="m" )
	#mySim.record( naChannels, where = somaLoc, what=StdRec.StateVarSteadyState, state="h" )
	#mySim.record( kChannels,  where = somaLoc, what=StdRec.StateVarSteadyState, state="n" )
	
	
	# Run the simulation
	results = mySim.Run()
	
	
	# Display the results, there is a lot of info for one graph, so lets split it up:
	TagViewer([results], timeranges=[(50, 250)*pq.ms], show=False )
	
	
	TagViewer([results], timeranges=[(50, 250)*pq.ms], show=False, 
	          plotspecs = [
	                       DefaultPlotSpec.Voltage, 
	                       DefaultPlotSpec.Current,
	                       DefaultPlotSpec.CurrentDensity,
	                       ] )
	
	
	TagViewer([results], timeranges=[(100, 120)*pq.ms], show=True, 
	          plotspecs = [
	                       DefaultPlotSpec.Voltage, 
	                       DefaultPlotSpec.ConductanceDensity,
	                       DefaultPlotSpec.StateVariable,
	                       ] )
	


Output
~~~~~~

.. code-block:: bash

    	Setting Random Seed: 69236
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//59/594778de483d91f17c597a4cd353ac8e.bundle
	Setting Random Seed: 45492
	Time for Building Mod-Files:  0.000993013381958
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_859a1d9737d5211246550de95c1fd4fd.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_948eaa7278919dda7237824a9dcc37cc.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_80a8e4fa82aa6d9aeeba91346ef5e628.so
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0330519676208
	Time for Extracting Data: (11 records) 0.00479102134705
	Simulation Time Elapsed:  0.383481025696
	Suceeded
	Setting Random Seed: 45492
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x27bda10>
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x2764550>
	Setting Time Range [  50.  250.] ms
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x276bc50>
	Setting Time Range [  50.  250.] ms
	Setting Yunit 1.0 mA/cm2
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x2788ed0>
	Setting Time Range [  50.  250.] ms
	Setting Yunit 1 pA (picoampere)
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x27a0ad0>
	Setting Time Range [  50.  250.] ms
	Setting Yunit 0.001 S/cm2
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x2799550>
	Setting Time Range [  50.  250.] ms
	Saving File _output/figures/singlecell_simulation070/eps/fig000_None.eps
	Saving File _output/figures/singlecell_simulation070/pdf/fig000_None.pdf
	Saving File _output/figures/singlecell_simulation070/png/fig000_None.png
	Saving File _output/figures/singlecell_simulation070/svg/fig000_None.svg
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x27bda10>
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x2764550>
	Setting Time Range [  50.  250.] ms
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x2788ed0>
	Setting Time Range [  50.  250.] ms
	Setting Yunit 1 pA (picoampere)
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x276bc50>
	Setting Time Range [  50.  250.] ms
	Setting Yunit 1.0 mA/cm2
	Saving File _output/figures/singlecell_simulation070/eps/fig001_None.eps
	Saving File _output/figures/singlecell_simulation070/pdf/fig001_None.pdf
	Saving File _output/figures/singlecell_simulation070/png/fig001_None.png
	Saving File _output/figures/singlecell_simulation070/svg/fig001_None.svg
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x27bda10>
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x2764550>
	Setting Time Range [ 100.  120.] ms
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x27a0ad0>
	Setting Time Range [ 100.  120.] ms
	Setting Yunit 0.001 S/cm2
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x2799550>
	Setting Time Range [ 100.  120.] ms
	Saving File _output/figures/singlecell_simulation070/eps/fig002_None.eps
	Saving File _output/figures/singlecell_simulation070/pdf/fig002_None.pdf
	Saving File _output/figures/singlecell_simulation070/png/fig002_None.png
	Saving File _output/figures/singlecell_simulation070/svg/fig002_None.svg
	



Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation070_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation070_out1.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation070_out2.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation070_out2.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation070_out3.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation070_out3.png>`



