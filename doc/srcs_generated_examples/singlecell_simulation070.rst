
14. Visualising the internal states of a neuron
===============================================


Visualising the internal states of a neuron

We look at the internal states of an HH neuron, and plot the properties on
different graphs.

Code
~~~~

.. code-block:: python

    
    
    
    
    
    
    from morphforge.stdimports import *
    from morphforgecontrib.stdimports import *
    
    
    
    # Create the environment:
    env = NEURONEnvironment()
    
    # Create the simulation:
    sim = env.Simulation()
    
    
    # Create a cell:
    morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
    m1 = MorphologyTree.fromDictionary(morphDict1)
    cell = sim.create_cell(name="Cell1", morphology=m1)
    
    
    lk_chl = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Lk", env=env)
    na_chl = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Na", env=env)
    k_chl = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="K", env=env)
    
    
    # Apply the channels uniformly over the cell
    cell.apply_channel( lk_chl)
    cell.apply_channel( na_chl)
    cell.apply_channel( k_chl)
    cell.set_passive( PassiveProperty.SpecificCapacitance, qty('1.0:uF/cm2'))
    
    # Get a cell_location on the cell:
    
    
    # Create the stimulus and record the injected current:
    cc = sim.create_currentclamp(name="Stim1", amp=qty("250:pA"), dur=qty("100:ms"), delay=qty("100:ms"), cell_location=cell.soma)
    sim.record(cc, what=StandardTags.Current)
    # Define what to record:
    sim.record(cell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = cell.soma)
    
    
    sim.record(lk_chl, cell_location = cell.soma, what=StandardTags.ConductanceDensity)
    sim.record(na_chl, cell_location = cell.soma, what=StandardTags.ConductanceDensity)
    sim.record(k_chl,  cell_location = cell.soma, what=StandardTags.ConductanceDensity)
    
    sim.record(lk_chl, cell_location = cell.soma, what=StandardTags.CurrentDensity)
    sim.record(na_chl, cell_location = cell.soma, what=StandardTags.CurrentDensity)
    sim.record(k_chl,  cell_location = cell.soma, what=StandardTags.CurrentDensity)
    
    
    sim.record(na_chl, cell_location = cell.soma, what=StandardTags.StateVariable, state="m")
    sim.record(na_chl, cell_location = cell.soma, what=StandardTags.StateVariable, state="h")
    sim.record(k_chl,  cell_location = cell.soma, what=StandardTags.StateVariable, state="n")
    
    
    # Also:
    #sim.record(na_chl, where = cell.soma, what=StandardTags.StateTimeConstant, state="m")
    #sim.record(na_chl, where = cell.soma, what=StandardTags.StateTimeConstant, state="h")
    #sim.record(k_chl,  where = cell.soma, what=StandardTags.StateTimeConstant, state="n")
    
    #sim.record(na_chl, where = cell.soma, what=StandardTags.StateSteadyState, state="m")
    #sim.record(na_chl, where = cell.soma, what=StandardTags.StateSteadyState, state="h")
    #sim.record(k_chl,  where = cell.soma, what=StandardTags.StateSteadyState, state="n")
    
    
    # run the simulation
    results = sim.run()
    
    
    # Display the results, there is a lot of info for one graph, so lets split it up:
    TagViewer([results], timerange=(50, 250)*units.ms, show=False)
    
    
    TagViewer([results], timerange=(50, 250)*units.ms, show=False,
              plots = [
                           DefaultTagPlots.Voltage,
                           DefaultTagPlots.Current,
                           DefaultTagPlots.CurrentDensity,
                          ])
    
    
    TagViewer([results], timerange=(100, 120)*units.ms, show=True,
              plots = [
                           DefaultTagPlots.Voltage,
                           DefaultTagPlots.ConductanceDensity,
                           DefaultTagPlots.StateVariable,
                          ])
    




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation070_out2.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation070_out2.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation070_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation070_out1.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation070_out3.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation070_out3.png>`






Output
~~~~~~

.. code-block:: bash

        No handlers could be found for logger "neurounits"
    2013-10-19 15:40:40,588 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:40:40,589 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
    No handlers could be found for logger "neurounits"
    2013-10-19 15:40:42,181 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:40:42,181 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/ec/ecf2dde0447333de8ee0864e7877ff6e.bundle (13k) : 0.775 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_468d766f8a3c48bce3bbb5aa16488aa9.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_10528623af7b919560a2e2606bf0cd9c.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_e53416588be6b02ed52a843da0f43a15.so
    	1 
    	1 
    	0.01 
    	0 
    	1 
    	50000 
    	1 
    	50000 
    	1 
    	50000 
    	1 
    	50000 
    	1 
    	50000 
    	1 
    	50000 
    	1 
    	50000 
    	1 
    	50000 
    	1 
    	50000 
    	1 
    	50000 
    	1 
    	50000 
    	1 
    Running Simulation
    Time for Extracting Data: (11 records) 0.0158488750458
    Running simulation : 0.145 seconds
    Post-processing : 0.014 seconds
    Entire load-run-save time : 0.934 seconds
    Suceeded
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    PlotMnager:Saving  _output/figures/singlecell_simulation070/{png,svg}/fig000_Autosave_figure_1.{png,svg}
    PlotMnager:Saving  _output/figures/singlecell_simulation070/{png,svg}/fig001_Autosave_figure_2.{png,svg}
    PlotMnager:Saving  _output/figures/singlecell_simulation070/{png,svg}/fig002_Autosave_figure_3.{png,svg}




