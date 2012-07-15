
22. 2 cells connected with an AMPA synapse
==========================================


2 cells connected with an AMPA synapse.

Timed input into a cell causes an action potential, which causes an EPSP in
another cell via an excitatry synapse.

Code
~~~~

.. code-block:: python

	
	
	
	
	from neurounits import NeuroUnitParser
	
	from morphforgecontrib.simulation.synapses.core.presynaptic_mechanisms import PreSynapticMech_TimeList
	from morphforgecontrib.simulation.synapses.core.presynaptic_mechanisms import PreSynapticMech_VoltageThreshold
	from morphforgecontrib.simulation.synapses_neurounit import NeuroUnitEqnsetPostSynaptic
	
	
	from morphforge.stdimports import *
	from morphforgecontrib.simulation.membranemechanisms.simulatorbuiltin.sim_builtin_core import BuiltinChannel
	
	def simulate_chls_on_neuron():
	    # Create the environment:
	    env = NeuronSimulationEnvironment()
	
	    # Create the simulation:
	    mySim = env.Simulation()
	
	    # Create a cell:
	    morphDict1 = {'root': {'length': 18.8, 'diam': 18.8, 'id':'soma'} }
	    m1 = MorphologyTree.fromDictionary(morphDict1)
	    myCell1 = mySim.create_cell(name="Cell1", morphology=m1)
	    apply_mechanism_everywhere_uniform( myCell1, env.MembraneMechanism(BuiltinChannel,  sim_chl_name="hh", mechanism_id="IDA" ) )
	    apply_passive_everywhere_uniform(myCell1, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )
	
	    m2 = MorphologyTree.fromDictionary(morphDict1)
	    myCell2 = mySim.create_cell(name="Cell2", morphology=m2)
	    apply_mechanism_everywhere_uniform( myCell2, env.MembraneMechanism(BuiltinChannel,  sim_chl_name="hh", mechanism_id="IDA" ) )
	    apply_passive_everywhere_uniform(myCell2, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )
	
	    # Get a cell_location on the cell:
	    somaLoc1 = myCell1.get_location("soma")
	    somaLoc2 = myCell2.get_location("soma")
	
	
	    eqnsetfile = "/home/michael/hw_to_come/libs/NeuroUnits/src/test_data/eqnsets/syn_simple.eqn"
	    syn = mySim.create_synapse(
	            presynaptic_mech =  env.PreSynapticMechanism(
	                                     PreSynapticMech_TimeList,
	                                     time_list =   (100,105,110,112,115, 115,115) * pq.ms ,
	                                     weight = unit("1:nS")),
	            postsynaptic_mech = env.PostSynapticMechanism(
	                                     NeuroUnitEqnsetPostSynaptic,
	                                     name = "mYName1",
	                                     eqnset = NeuroUnitParser.EqnSet(open(eqnsetfile).read()),
	                                     cell_location = somaLoc1
	                                     )
	            )
	
	    syn = mySim.create_synapse(
	            presynaptic_mech =  env.PreSynapticMechanism(
	                                     PreSynapticMech_VoltageThreshold,
	                                     cell_location=somaLoc1,
	                                     voltage_threshold=unit("0:mV"),
	                                     delay=unit('1:ms'),
	                                     weight = unit("1:nS")),
	            postsynaptic_mech = env.PostSynapticMechanism(
	                                     NeuroUnitEqnsetPostSynaptic,
	                                     name = "mYName1",
	                                     eqnset = NeuroUnitParser.EqnSet(open(eqnsetfile).read()),
	                                     cell_location = somaLoc2
	                                     )
	            )
	
	
	    # Define what to record:
	    mySim.record( what=StandardTags.Voltage, name="SomaVoltage1", cell_location = somaLoc1 )
	    mySim.record( what=StandardTags.Voltage, name="SomaVoltage2", cell_location = somaLoc2 )
	
	
	    # run the simulation
	    results = mySim.run()
	    return results
	
	
	results = simulate_chls_on_neuron()
	TagViewer(results, timeranges=[(95, 200)*pq.ms], show=True )
	#
	




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/multicell_simulation010_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/multicell_simulation010_out1.png>`






Output
~~~~~~

.. code-block:: bash

    	2012-07-15 16:21:59,105 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 16:21:59,105 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
	2012-07-15 16:21:59,729 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 16:21:59,729 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/6a/6afb7727d36f64e63079948f97eee8ef.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'SomaVoltage1'}
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell2', 'recVecName': 'SomaVoltage2'}
	Time for Building Mod-Files:  0.000709056854248
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_7d5db4858728c6cc383af7299a2380bf.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_963693d3ef1730a096a530e3b524ab68.so
		1 
		1 
		1 
		50000 
		1 
		50000 
		1 
	Running Simulation
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xad72ecc> t= 495.0 ms
	Time for Simulation:  0.0251410007477
	Time for Extracting Data: (2 records) 0.0163860321045
	Simulation Time Elapsed:  0.155837059021
	Suceeded
	Reading JSON: {"mf":{"role":"MEMBRANEVOLTAGE"}}
	Reading JSON: {"mf":{"role":"TRANSMEMBRANECURRENT"}}
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	g <class 'neurounits.ast.astobjects.StateVariable'>
	Deps; set([])
	g <class 'neurounits.ast.astobjects.StateVariable'>
	g <class 'neurounits.ast.astobjects.StateVariable'>
	Reading JSON: {"mf":{"role":"MEMBRANEVOLTAGE"}}
	Reading JSON: {"mf":{"role":"TRANSMEMBRANECURRENT"}}
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	g <class 'neurounits.ast.astobjects.StateVariable'>
	Deps; set([])
	g <class 'neurounits.ast.astobjects.StateVariable'>
	g <class 'neurounits.ast.astobjects.StateVariable'>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xade8c8c>
	Saving File _output/figures/multicell_simulation010/eps/fig000_Autosave_figure_1.eps
	Saving File _output/figures/multicell_simulation010/pdf/fig000_Autosave_figure_1.pdf
	Saving File _output/figures/multicell_simulation010/png/fig000_Autosave_figure_1.png
	Saving File _output/figures/multicell_simulation010/svg/fig000_Autosave_figure_1.svg
	




