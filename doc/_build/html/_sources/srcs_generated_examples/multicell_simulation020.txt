
17. The responses of two cells connected by a gap junction to a step current injection into the first
=====================================================================================================


The responses of two cells connected by a gap junction to a step current injection into the first

Code
~~~~

.. code-block:: python

    
    
    
    
    
    
    import morphforge.stdimports as mf
    import morphforgecontrib.stdimports as mfc
    from morphforge.stdimports import units as U
    
    # The simulation:
    env = mf.NEURONEnvironment()
    sim = env.Simulation(cvode=True)
    cell1 = sim.create_cell(area=5000 * U.um2, initial_voltage=0*U.mV, name='Cell1')
    lk_chl1 = env.Channel(mfc.StdChlLeak,
                    conductance=0.66  * U.mS/U.cm2,
                    reversalpotential=0*U.mV )
    
    cell1.apply_channel(lk_chl1)
    cell1.set_passive(mf.PassiveProperty.SpecificCapacitance, (1e-3) * U.uF / U.cm2)
    
    
    cell2 = sim.create_cell(area=20000 * U.um2, initial_voltage=0*U.mV, name='Cell2')
    lk_chl2 = env.Channel(mfc.StdChlLeak,
                    conductance=0.01* U.mS/U.cm2,
                    reversalpotential=0*U.mV
                    )
    
    cell2.apply_channel(lk_chl2)
    cell2.set_passive(mf.PassiveProperty.SpecificCapacitance, (1e-3) * U.uF / U.cm2)
    
    gj = sim.create_gapjunction(
        celllocation1 = cell1.soma,
        celllocation2 = cell2.soma,
        resistance = 100 * mf.units.MOhm
        )
    
    cc = sim.create_currentclamp(cell_location=cell1.soma,
                            amp=200 * U.pA,
                            delay=100*U.ms,
                            dur=250*U.ms)
    
    
    
    sim.record(cell1, what=mf.StandardTags.Voltage)
    sim.record(cell2, what=mf.StandardTags.Voltage)
    sim.record(cc, what=mf.StandardTags.Current)
    
    res = sim.run()
    
    
    mf.TagViewer(res)
    
    
    




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/multicell_simulation020_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/multicell_simulation020_out1.png>`






Output
~~~~~~

.. code-block:: bash

        No handlers could be found for logger "neurounits"
    2013-10-19 15:41:17,070 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:41:17,071 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
    No handlers could be found for logger "neurounits"
    2013-10-19 15:41:18,612 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:41:18,612 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/1b/1bed7227061cb40c17119e4fd3b22f62.bundle (13k) : 0.784 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(0.0) * mV, '_name': 'AnonObj0001', '_simulation': None, 'conductance': array(0.66) * mS/cm2}
    
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(0.0) * mV, '_name': 'AnonObj0002', '_simulation': None, 'conductance': array(0.01) * mS/cm2}
    
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_eaaebbdf61a1f3f1e8c370f0d9775f7b.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_7254a011c6a75f1920b34df02c1d8135.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_e57913d7cc35b32450d483afb87ad8fc.so
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
    Running Simulation
    Time for Extracting Data: (3 records) 0.00183081626892
    Running simulation : 0.212 seconds
    Post-processing : 0.050 seconds
    Entire load-run-save time : 1.046 seconds
    Suceeded
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    PlotMnager:Saving  _output/figures/multicell_simulation020/{png,svg}/fig000_Autosave_figure_1.{png,svg}




