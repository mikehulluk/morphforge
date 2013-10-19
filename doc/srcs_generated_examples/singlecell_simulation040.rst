
10. Investigating the rheobase of a neuron with a parameter sweep
=================================================================


Investigating the rheobase of a neuron with a parameter sweep

WARNING: The automatic naming and linkage between grpah colors is currently under a refactor; what is done in this script is not representing the best possible solution, or even something that will reliably work in the future!

The aim of this script is just to show that it is possible to run multiple simulations from a single script!

Code
~~~~

.. code-block:: python

    
    
    
    
    
    
    
    from morphforge.stdimports import *
    from morphforgecontrib.simulation.channels.hh_style.core.mmleak import StdChlLeak
    from morphforgecontrib.simulation.channels.hh_style.core.mmalphabeta import StdChlAlphaBeta
    
    
    
    @cached_functor
    def get_Na_Channels(env):
        na_state_vars = {"m":
                        {"alpha": [13.01,0,4,-1.01,-12.56], "beta": [5.73,0,1,9.01,9.69] },
                       "h":
                        {"alpha": [0.06,0,0,30.88,26], "beta": [3.06,0,1,-7.09,-10.21]}
                       }
    
        return  env.Channel(
                                StdChlAlphaBeta,
                                name="NaChl", ion="na",
                                equation="m*m*m*h",
                                conductance=qty("210:nS") / qty("400:um2"),
                                reversalpotential=qty("50.0:mV"),
                                statevars=na_state_vars,
                               )
    
    @cached_functor
    def get_Ks_Channels(env):
        kf_state_vars = {"ks": {"alpha": [0.2,0,1,-6.96,-7.74 ], "beta": [0.05,0,2,-18.07,6.1 ] } }
    
        return  env.Channel(
                                StdChlAlphaBeta,
                                name="KsChl", ion="ks",
                                equation="ks*ks*ks*ks",
                                conductance=qty("3:nS") / qty("400:um2"),
                                reversalpotential=qty("-80.0:mV"),
                                statevars=kf_state_vars,
                               )
    
    @cached_functor
    def get_Kf_Channels(env):
        kf_state_vars = {"kf": {"alpha": [ 3.1,0,1,-31.5,-9.3], "beta": [0.44,0,1,4.98,16.19 ] } }
    
        return  env.Channel(
                                StdChlAlphaBeta,
                                name="KfChl", ion="kf",
                                equation="kf*kf*kf*kf",
                                conductance=qty("0.5:nS") / qty("400:um2") ,
                                reversalpotential=qty("-80.0:mV"),
                                statevars=kf_state_vars,
                               )
    
    @cached_functor
    def get_Lk_Channels(env):
        lk_chl = env.Channel(
                             StdChlLeak,
                             name="LkChl",
                             conductance=qty("3.6765:nS") / qty("400:um2"),
                             reversalpotential=qty("-51:mV"),
                           )
        return lk_chl
    
    
    
    
    def simulate(current_inj_level):
        # Create the environment:
        env = NEURONEnvironment()
    
        # Create the simulation:
        sim = env.Simulation(name="AA")
    
    
        # Create a cell:
        morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
        morph = MorphologyTree.fromDictionary(morphDict1)
        cell = sim.create_cell(name="Cell1", morphology=morph)
    
        lk_chl = get_Lk_Channels(env)
        na_chl = get_Na_Channels(env)
        potFastChannels = get_Kf_Channels(env)
        potSlowChannels = get_Ks_Channels(env)
    
        cell.apply_channel( lk_chl)
        cell.apply_channel( na_chl)
        cell.apply_channel( potFastChannels)
        cell.apply_channel( potSlowChannels)
        cell.set_passive( PassiveProperty.SpecificCapacitance, qty('2.0:uF/cm2'))
    
    
    
        # Create the stimulus and record the injected current:
        cc = sim.create_currentclamp(amp=current_inj_level, dur=qty("100:ms"), delay=qty("100:ms"), cell_location=cell.soma)
        sim.record(cc, what=StandardTags.Current)
    
        # Define what to record:
        sim.record(cell, what=StandardTags.Voltage, cell_location = cell.soma)
    
        # run the simulation
        results = sim.run()
    
        return results
    
    
    # Display the results:
    results = [simulate(current_inj_level='%d:pA' % i) for i in [50,100,150,200, 250, 300]  ]
    TagViewer(results, timerange=(95, 200)*units.ms, show=True)
    
    
    
    




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation040_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation040_out1.png>`






Output
~~~~~~

.. code-block:: bash

        No handlers could be found for logger "neurounits"
    2013-10-19 15:40:12,263 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:40:12,263 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
    No handlers could be found for logger "neurounits"
    2013-10-19 15:40:13,866 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:40:13,866 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/a2/a26b9f834d42fb9df2b663d2fd1fdba7.bundle (11k) : 0.794 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-51.0) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(9.19125) * S/m**2}
    
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_8c985bc4d78348c5e6b5020db7c84b33.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_4a11c42a24cf8094e8128eb36ed4454b.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_d441f583160e57ff5401cbe672e7a2fc.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_f840dc4d53912ca489cb83065e2ac90a.so
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
    Time for Extracting Data: (2 records) 0.00105500221252
    Running simulation : 0.131 seconds
    Post-processing : 0.002 seconds
    Entire load-run-save time : 0.927 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-10-19 15:40:15,614 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:40:15,615 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/a5/a5f2760136d0500d16e585edd8781b53.bundle (11k) : 0.798 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-51.0) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(9.19125) * S/m**2}
    
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_8c985bc4d78348c5e6b5020db7c84b33.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_4a11c42a24cf8094e8128eb36ed4454b.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_d441f583160e57ff5401cbe672e7a2fc.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_f840dc4d53912ca489cb83065e2ac90a.so
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
    Time for Extracting Data: (2 records) 0.0010449886322
    Running simulation : 0.119 seconds
    Post-processing : 0.003 seconds
    Entire load-run-save time : 0.920 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-10-19 15:40:17,343 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:40:17,343 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/a1/a149219849962767fc3ba050fe64fcb0.bundle (11k) : 0.798 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-51.0) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(9.19125) * S/m**2}
    
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_3491b26d83ce944c4a48bec588249988.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_10db04e695bde49229cd91f80837e678.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_a7e581760ab76fb7fd4364df6a5cb525.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_cdb90d18701a6ac6f42dafa8f8d2b68b.so
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
    Time for Extracting Data: (2 records) 0.00107979774475
    Running simulation : 0.118 seconds
    Post-processing : 0.002 seconds
    Entire load-run-save time : 0.918 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-10-19 15:40:19,067 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:40:19,067 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/b7/b718a0d40179ae8cd838abaf66951199.bundle (11k) : 0.787 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-51.0) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(9.19125) * S/m**2}
    
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_bb71ec78e6dab19dcf87e15fc17561eb.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_788287c244f7438044a89398129f898b.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_7408cd406bc1adf0811143f9ef2231f3.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_0b6ff728b56729ca8f05449ed9e44a97.so
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
    Time for Extracting Data: (2 records) 0.00105285644531
    Running simulation : 0.308 seconds
    Post-processing : 0.003 seconds
    Entire load-run-save time : 1.098 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-10-19 15:40:20,988 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:40:20,989 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/da/da53d39cbdc1efb254446b84a99fc168.bundle (11k) : 0.785 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-51.0) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(9.19125) * S/m**2}
    
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_7610f582ad2abbe48c35a53ca9916058.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_316a63d7a1569a19442d0738a9081666.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_5b95d930087f6bce4c78cdc261821c6a.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_2f3f9ea398f72a5862674d83f114a245.so
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
    Time for Extracting Data: (2 records) 0.00104308128357
    Running simulation : 0.118 seconds
    Post-processing : 0.003 seconds
    Entire load-run-save time : 0.906 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-10-19 15:40:22,789 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:40:22,790 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/c6/c6bc427811a04eb29cb45f46c697a32d.bundle (11k) : 0.799 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-51.0) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(9.19125) * S/m**2}
    
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_762ecdcc92fc56510ed63f453d729fcd.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_c5a5a97cc17f8f6d60395eae5a0c67ed.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_3ccc28a6e495081d0fd8d62d7dc20e60.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_c489958483f5e120000734ea6f939099.so
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
    Time for Extracting Data: (2 records) 0.00104308128357
    Running simulation : 0.127 seconds
    Post-processing : 0.003 seconds
    Entire load-run-save time : 0.929 seconds
    Suceeded
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    PlotMnager:Saving  _output/figures/singlecell_simulation040/{png,svg}/fig000_Autosave_figure_1.{png,svg}




