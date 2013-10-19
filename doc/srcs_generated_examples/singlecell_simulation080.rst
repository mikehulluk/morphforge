
15. Applying different channel densities over a cell
====================================================


Applying different channel densities over a cell.
We start with a cell with a long axon, and then apply Hodgkin-Huxley channels over the surface. We look at the effect of changing the density of leak and sodium channels in just the axon of the neuron (not the soma)

This example also shows the use of tags; 300 traces are recorded in this experiment; but we don't ever need to get
involved in managing them directly. We can just specify that all traces recorded on simulation X should be tagged with "SIMY", and
then tell the TagViewer to plot everything with a tag 'SIMY'

Code
~~~~

.. code-block:: python

    
    
    
    
    
    
    
    
    from morphforge.stdimports import *
    from morphforgecontrib.data_library.stdmodels import StandardModels
    
    
    def sim(glk_multiplier, gna_multiplier, tag):
        # Create the environment:
        env = NEURONEnvironment()
    
        # Create the simulation:
        sim = env.Simulation()
    
        # Create a cell:
        morph = MorphologyBuilder.get_soma_axon_morph(axon_length=3000.0, axon_radius=0.3, soma_radius=9.0, axon_sections=20)
        cell = sim.create_cell(name="Cell1", morphology=morph)
    
    
        lk_chl = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Lk", env=env)
        na_chl = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Na", env=env)
        k_chl  = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="K", env=env)
    
        # Apply the channels uniformly over the cell
        cell.apply_channel(lk_chl)
        cell.apply_channel(na_chl)
        cell.apply_channel(k_chl)
    
        # Over-ride the parameters in the axon:
        cell.apply_channel(channel=lk_chl, where="axon", parameter_multipliers={'gScale':glk_multiplier})
        cell.apply_channel(channel=na_chl, where="axon", parameter_multipliers={'gScale':gna_multiplier})
    
        cell.set_passive( PassiveProperty.SpecificCapacitance, qty('1.0:uF/cm2'))
    
    
        for cell_location in CellLocator.get_locations_at_distances_away_from_dummy(cell=cell, distances=range(9, 3000, 100)):
            sim.record(cell, what=StandardTags.Voltage, cell_location=cell_location, user_tags=[tag])
    
        # Create the stimulus and record the injected current:
        cc = sim.create_currentclamp(name="Stim1", amp=qty("250:pA"), dur=qty("5:ms"), delay=qty("100:ms"), cell_location=cell.soma)
        sim.record(cc, what=StandardTags.Current)
    
        # run the simulation
        return sim.run()
    
    
    # Display the results:
    results_a = [
        sim(glk_multiplier=0.1, gna_multiplier=1.0, tag="SIM1"),
        sim(glk_multiplier=0.5, gna_multiplier=1.0, tag="SIM2"),
        sim(glk_multiplier=1.0, gna_multiplier=1.0, tag="SIM3"),
        sim(glk_multiplier=5.0, gna_multiplier=1.0, tag="SIM4"),
        sim(glk_multiplier=10.0, gna_multiplier=1.0, tag="SIM5"),
    ]
    
    TagViewer(results_a, timerange=(97.5, 140)*units.ms, show=False,
              plots = [
                        TagPlot("ALL{Voltage,SIM1}", ylabel='gLeak: 0.1\nVoltage', yrange=(-80, 50)*units.mV, legend_labeller=None),
                        TagPlot("ALL{Voltage,SIM2}", ylabel='gLeak: 0.5\nVoltage', yrange=(-80, 50)*units.mV, legend_labeller=None),
                        TagPlot("ALL{Voltage,SIM3}", ylabel='gLeak: 1.0\nVoltage', yrange=(-80, 50)*units.mV, legend_labeller=None),
                        TagPlot("ALL{Voltage,SIM4}", ylabel='gLeak: 5.0\nVoltage', yrange=(-80, 50)*units.mV, legend_labeller=None),
                        TagPlot("ALL{Voltage,SIM5}", ylabel='gLeak: 10.0\nVoltage',yrange=(-80, 50)*units.mV, legend_labeller=None),
                           ])
    
    results_b = [
        sim(gna_multiplier=0.1,  glk_multiplier=1.0, tag="SIM6"),
        sim(gna_multiplier=0.5,  glk_multiplier=1.0, tag="SIM7"),
        sim(gna_multiplier=0.75,  glk_multiplier=1.0, tag="SIM8"),
        sim(gna_multiplier=1.0,  glk_multiplier=1.0, tag="SIM9"),
    ]
    
    TagViewer(results_b, timerange=(97.5, 140)*units.ms, show=True,
              plots = [
                        TagPlot("ALL{Voltage,SIM6}", ylabel='gNa: 0.10\nVoltage', yrange=(-80, 50)*units.mV, legend_labeller=None),
                        TagPlot("ALL{Voltage,SIM7}", ylabel='gNa: 0.50\nVoltage', yrange=(-80, 50)*units.mV, legend_labeller=None),
                        TagPlot("ALL{Voltage,SIM8}", ylabel='gNa: 0.75\nVoltage', yrange=(-80, 50)*units.mV, legend_labeller=None),
                        TagPlot("ALL{Voltage,SIM9}", ylabel='gNa: 1.00\nVoltage', yrange=(-80, 50)*units.mV, legend_labeller=None),
                           ])
    
    




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation080_out2.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation080_out2.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation080_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation080_out1.png>`






Output
~~~~~~

.. code-block:: bash

        No handlers could be found for logger "neurounits"
    2013-10-19 15:40:46,704 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:40:46,704 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
    No handlers could be found for logger "neurounits"
    2013-10-19 15:40:48,332 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:40:48,332 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/75/75b3b2b9bd9b587a14653b96392f3151.bundle (23k) : 0.785 seconds
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
    Time for Extracting Data: (30 records) 0.0145881175995
    Running simulation : 0.787 seconds
    Post-processing : 0.024 seconds
    Entire load-run-save time : 1.596 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-10-19 15:40:50,867 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:40:50,867 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/3c/3c25eb16c1ba2f8ae55c84332b3d42d2.bundle (23k) : 0.804 seconds
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
    Time for Extracting Data: (30 records) 0.0151150226593
    Running simulation : 0.691 seconds
    Post-processing : 0.022 seconds
    Entire load-run-save time : 1.517 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-10-19 15:40:53,338 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:40:53,338 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/23/233cfd4eff4b963e94e2c95a824a2ae2.bundle (23k) : 0.780 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_78a9a6f61ad61db32f7e0812457f0b19.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_3bf774ddb40d01137fc04e1ccf2cc5ab.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_618809ca886acf30497c7377b8787d22.so
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
    Time for Extracting Data: (30 records) 0.0145320892334
    Running simulation : 0.676 seconds
    Post-processing : 0.019 seconds
    Entire load-run-save time : 1.476 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-10-19 15:40:55,740 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:40:55,740 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/f9/f99535fae803f8bd6a2aa1ac28fcc754.bundle (23k) : 0.788 seconds
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
    Time for Extracting Data: (30 records) 0.0144238471985
    Running simulation : 0.769 seconds
    Post-processing : 0.022 seconds
    Entire load-run-save time : 1.580 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-10-19 15:40:58,258 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:40:58,259 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/f8/f85e809d30b5749eef61273a9aee0212.bundle (23k) : 0.792 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_5b27604449f43a74a5cedaba068a8082.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_493e4afc99901274d3bc57b05062327c.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_74bacce0ccfd6b62a1f2810b7a3c436d.so
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
    Time for Extracting Data: (30 records) 0.015095949173
    Running simulation : 0.590 seconds
    Post-processing : 0.018 seconds
    Entire load-run-save time : 1.401 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-10-19 15:41:01,070 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:41:01,070 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/2d/2d6928d0568f9815c65992777fabc702.bundle (23k) : 0.801 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_6e4ef82af6252a644c640713bba2c767.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_dba81496a6a5bee537c52f9be5e61f23.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_8253857f8f84368b878abf70fcf25462.so
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
    Time for Extracting Data: (30 records) 0.014200925827
    Running simulation : 0.477 seconds
    Post-processing : 0.012 seconds
    Entire load-run-save time : 1.290 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-10-19 15:41:03,264 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:41:03,264 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/6d/6d5e44f13a4d4f153138a5cf6bd30ca6.bundle (23k) : 0.786 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_73cae5515813b8c78e05ae21b69025ee.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_e8de507bed64a7a182e7bb3108a43a37.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_e1d9b15c15cf730d6ad5de223a1b3007.so
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
    Time for Extracting Data: (30 records) 0.0146231651306
    Running simulation : 0.771 seconds
    Post-processing : 0.023 seconds
    Entire load-run-save time : 1.579 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-10-19 15:41:05,777 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:41:05,778 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/95/9578be9c9b7def3f4320b4ff22c375da.bundle (23k) : 0.787 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_73cae5515813b8c78e05ae21b69025ee.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_e8de507bed64a7a182e7bb3108a43a37.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_e1d9b15c15cf730d6ad5de223a1b3007.so
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
    Time for Extracting Data: (30 records) 0.0145888328552
    Running simulation : 0.715 seconds
    Post-processing : 0.020 seconds
    Entire load-run-save time : 1.522 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-10-19 15:41:08,194 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-10-19 15:41:08,194 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/a7/a70c607e497c72a1bae8a43867106a84.bundle (23k) : 0.779 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_c224cc126ae7a2714f42b5c551e02fa6.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_bb9b6fbbfd7217f10a29e5a4c138dd75.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_5163084cbe5b6d3cdf0bea4ed32ff8fc.so
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
    Time for Extracting Data: (30 records) 0.0145931243896
    Running simulation : 0.666 seconds
    Post-processing : 0.020 seconds
    Entire load-run-save time : 1.465 seconds
    Suceeded
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    PlotMnager:Saving  _output/figures/singlecell_simulation080/{png,svg}/fig000_Autosave_figure_1.{png,svg}
    PlotMnager:Saving  _output/figures/singlecell_simulation080/{png,svg}/fig001_Autosave_figure_2.{png,svg}




