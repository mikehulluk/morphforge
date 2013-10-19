
13. Using a channel library to reduce duplication
=================================================


Using a channel library to reduce duplication.

We define functions that produce morphology and channel objects for our simulations.
We could stop here, and simply import and use the functions in our simulations, but
we go a step further, and register them with  "ChannelLibrary" and "MorphologyLibrary".
These are basically glorified dictionaries, that do the lookup for the appropriate functors
based on a key from the tuple~(modelsrc, celltype, channeltype). The advantage for doing this is that
there is single repository for morphologies and channels.

There is not really anythin clever going on here, and you can run simulations completely ignorantly
of these classes, I just included it because it made life much easier for me, when I had to start managing
lots of channel definitions.

Code
~~~~

.. code-block:: python

    
    
    
    
    
    
    
    
    from morphforge.stdimports import *
    from morphforgecontrib.simulation.channels.hh_style.core.mmleak import StdChlLeak
    from morphforgecontrib.simulation.channels.hh_style.core.mmalphabeta import StdChlAlphaBeta
    
    
    
    # This can be put into a file that is loaded on
    # you path somewhere:
    
    # ======================================================
    def getSimpleMorphology():
    
        mDict  = {'root': { 'length': 17.5, 'diam': 17.5, 'id':'soma', 'region':'soma',   } }
        return  MorphologyTree.fromDictionary(mDict)
    
    
    def get_sample_lk(env):
        lk_chl = env.Channel(
                             StdChlLeak,
                             name="LkChl",
                             conductance=qty("0.3:mS/cm2"),
                             reversalpotential=qty("-54.3:mV"),
                           )
        return lk_chl
    
    
    def get_sample_na(env):
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
        return na_chl
    
    
    def get_sample_k(env):
        k_state_vars = { "n": { "alpha":[-0.55,-0.01,-1.0,55.0,-10.0],
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
        return k_chl
    
    
    
    MorphologyLibrary.register_morphology(modelsrc="Sample", celltype="Cell1", morph_functor=getSimpleMorphology)
    ChannelLibrary.register_channel(modelsrc="Sample", celltype="Cell1", channeltype="Na", chl_functor=get_sample_na)
    ChannelLibrary.register_channel(modelsrc="Sample", celltype="Cell1", channeltype="K", chl_functor=get_sample_k)
    ChannelLibrary.register_channel(modelsrc="Sample", celltype="Cell1", channeltype="Lk", chl_functor=get_sample_lk)
    
    # =============================================================
    
    
    
    
    
    
    
    
    
    # Now in our script elsewhere, we can use them as:
    modelsrc = "Sample"
    celltype="Cell1"
    
    # Create the environment:
    env = NEURONEnvironment()
    
    # Create the simulation:
    sim = env.Simulation()
    
    # Create a cell:
    morphology=MorphologyLibrary.get_morphology(modelsrc=modelsrc, celltype=celltype)
    cell = sim.create_cell(morphology=morphology)
    
    # Apply the channels uniformly over the cell
    na_chl = ChannelLibrary.get_channel(modelsrc=modelsrc, celltype=celltype, channeltype="Na", env=env)
    k_chl  = ChannelLibrary.get_channel(modelsrc=modelsrc, celltype=celltype, channeltype="K", env=env)
    lk_chl = ChannelLibrary.get_channel(modelsrc=modelsrc, celltype=celltype, channeltype="Lk", env=env)
    
    cell.apply_channel( na_chl)
    cell.apply_channel( k_chl )
    cell.apply_channel( lk_chl)
    
    cell.set_passive( PassiveProperty.SpecificCapacitance, qty('1.0:uF/cm2'))
    
    # Create the stimulus and record the injected current:
    cc = sim.create_currentclamp(name="Stim1", amp=qty("150:pA"), dur=qty("5:ms"), delay=qty("100:ms"), cell_location=cell.soma)
    
    sim.record(cc, what=StandardTags.Current)
    sim.record(cell, what=StandardTags.Voltage, cell_location=cell.soma)
    
    
    # run the simulation
    results = sim.run()
    
    # Display the results:
    TagViewer([results], timerange=(97.5, 140)*units.ms)
    




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation065_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation065_out1.png>`






Output
~~~~~~

.. code-block:: bash

        No handlers could be found for logger "neurounits"
    2013-10-19 15:40:36,351 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:40:36,351 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
    No handlers could be found for logger "neurounits"
    2013-10-19 15:40:37,934 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:40:37,934 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/b4/b41741d4d1311e8b1110b97dbab2fb28.bundle (11k) : 0.788 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_5fb53d86906bb0ff9a3f8f78e06c7a5b.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_14a5557d418242e3ab463bb7bc1b7cc3.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_5a503145b0c1cde6262b198883e45437.so
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
    Time for Extracting Data: (2 records) 0.00104999542236
    Running simulation : 0.128 seconds
    Post-processing : 0.003 seconds
    Entire load-run-save time : 0.919 seconds
    Suceeded
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    PlotMnager:Saving  _output/figures/singlecell_simulation065/{png,svg}/fig000_Autosave_figure_1.{png,svg}




