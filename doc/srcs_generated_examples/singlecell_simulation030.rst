
9. Hodgkin-Huxley '52 neuron simulation with automatic summary pdf generation
=============================================================================


Hodgkin-Huxley '52 neuron simulation with automatic summary pdf generation.

The same simulation of the HodgkinHuxley52 neuron as before, but by adding
a single line, we can generate a pdf output of the simulation! (You can do this
on any simulation.)

.. code-block:: python

    SimulationSummariser(simulationresult=results, filename="SimulationOutput.pdf", make_graphs=True)


TODO: THIS IS NOT WORKING  - DISABLED TO ALLOW runnnign during pdf gen refactor

Code
~~~~

.. code-block:: python

    
    
    
    
    
    
    
    
    
    from morphforge.stdimports import *
    from morphforgecontrib.simulation.channels.hh_style.core.mmleak import StdChlLeak
    from morphforgecontrib.simulation.channels.hh_style.core.mmalphabeta import StdChlAlphaBeta
    
    
    # Create the environment:
    env = NEURONEnvironment()
    
    # Create the simulation:
    sim = env.Simulation()
    
    
    # Create a cell:
    morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
    m1 = MorphologyTree.fromDictionary(morphDict1)
    cell = sim.create_cell(name="Cell1", morphology=m1)
    
    
    lk_chl = env.Channel(
                             StdChlLeak,
                             name="LkChl",
                             conductance=qty("0.3:mS/cm2"),
                             reversalpotential=qty("-54.3:mV"),
                           )
    
    na_state_vars = { "m": {
                          "alpha":[-4.00,-0.10,-1.00,40.00,-10.00],
                          "beta": [4.00, 0.00, 0.00,65.00, 18.00]},
                        "h": {
                            "alpha":[0.07,0.00,0.00,65.00,20.00] ,
                            "beta": [1.00,0.00,1.00,35.00,-10.00]}
                      }
    
    na_chl = env.Channel(
                            StdChlAlphaBeta,
                            name="NaChl", ion="na",
                            equation="m*m*m*h",
                            conductance=qty("120:mS/cm2"),
                            reversalpotential=qty("50:mV"),
                            statevars=na_state_vars,
                           )
    k_state_vars = { "n": {
                          "alpha":[-0.55,-0.01,-1.0,55.0,-10.0],
                          "beta": [0.125,0,0,65,80]},
                       }
    
    k_chl = env.Channel(
                            StdChlAlphaBeta,
                            name="KChl", ion="k",
                            equation="n*n*n*n",
                            conductance=qty("36:mS/cm2"),
                            reversalpotential=qty("-77:mV"),
                            statevars=k_state_vars,
                            
                           )
    
    
    # Apply the channels uniformly over the cell
    cell.apply_channel( lk_chl)
    cell.apply_channel( na_chl)
    cell.apply_channel( k_chl)
    cell.set_passive( PassiveProperty.SpecificCapacitance, qty('1.0:uF/cm2'))
    
    
    # Create the stimulus and record the injected current:
    cc = sim.create_currentclamp(name="Stim1", amp=qty("250:pA"), dur=qty("100:ms"), delay=qty("100:ms"), cell_location=cell.soma)
    sim.record(cc, what=StandardTags.Current)
    # Define what to record:
    sim.record(cell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = cell.soma)
    
    # run the simulation
    results = sim.run()
    
    #SimulationSummariser(simulationresult=results, filename="SimulationOutput.pdf", make_graphs=True)
    
    # Display the results:
    TagViewer([results], timerange=(50, 250)*units.ms, show=True)
    
    
    #summary = SimulationMRedoc.build(sim)
    #summary.to_pdf('~/Desktop/pdfs/%s.pdf'%__file__.split('/')[-1])
    




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation030_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation030_out1.png>`






Output
~~~~~~

.. code-block:: bash

        No handlers could be found for logger "neurounits"
    2013-10-19 15:40:08,201 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:40:08,201 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
    No handlers could be found for logger "neurounits"
    2013-10-19 15:40:09,777 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:40:09,777 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/e4/e4562dba33da1e886d7661ced4cc5a28.bundle (11k) : 0.781 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_0b082b636334d63b27417ca014016a90.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_0399d8f72ddafed0d172aeb0b7707773.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_67de8ab4c215459909d3fb83ce6b7aa5.so
    	1 
    	1 
    	0.01 
    	0 
    	1 
    	50000 
    	1 
    	50000 
    	1 
    Running Simulation
    Time for Extracting Data: (2 records) 0.00107216835022
    Running simulation : 0.129 seconds
    Post-processing : 0.005 seconds
    Entire load-run-save time : 0.915 seconds
    Suceeded
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    PlotMnager:Saving  _output/figures/singlecell_simulation030/{png,svg}/fig000_Autosave_figure_1.{png,svg}




