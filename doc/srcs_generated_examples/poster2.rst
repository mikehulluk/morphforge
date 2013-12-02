
.. _example_poster2:

Example 23. Action potential propagation and synaptic transmission
==================================================================


Action potential propagation and synaptic transmission.
In this simulation, we create 3 neurons; Neuron 1 has an axon, and when the
soma is stimulated, we see the action potential propagate along it. Neuron 1
forms synapses onto cell2 and cell3 with different strengths and different
positions along the axon.

Code
~~~~

.. code-block:: python

    
    
    
    
    
    
    
    
    
    import matplotlib as mpl
    mpl.rcParams['font.size'] = 14
    
    
    from morphforge.stdimports import *
    from morphforgecontrib.stdimports import *
    
    # Create a cell:
    def build_cell(name, sim):
    
        my_morph = MorphologyBuilder.get_soma_axon_morph(axon_length=1500.0, axon_radius=0.3, soma_radius=10.0)
        my_cell = sim.create_cell(name=name, morphology=my_morph)
    
        na_chls = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Na", env=sim.environment)
        k_chls  = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="K",  env=sim.environment)
        lk_chls = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Lk", env=sim.environment)
    
        my_cell.apply_channel(lk_chls)
        my_cell.apply_channel(k_chls)
        my_cell.apply_channel(na_chls)
        my_cell.apply_channel(na_chls, where="axon", parameter_multipliers={'gScale':1.0})
        return my_cell
    
    
    # Create a simulation:
    env = NEURONEnvironment()
    sim = env.Simulation()
    
    # Two cells:
    cell1 = build_cell(name="cell1", sim=sim)
    cell2 = build_cell(name="cell2", sim=sim)
    cell3 = build_cell(name="cell3", sim=sim)
    
    
    # Connect with a synapse:
    simple_ampa_syn = """
    define_component syn_simple {
    
        g' = - g/g_tau
        i = gmax * (v-erev) * g
    
        gmax = 300pS * scale
        erev = 0mV
    
        g_tau = 10ms
        <=> INPUT     v: mV       METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
        <=> OUTPUT    i:(mA)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }
        <=> PARAMETER scale:()
        on on_event(){
            g = g + 1.0
        }
    }
    """
    
    
    post_syn_tmpl = env.PostSynapticMechTemplate(
            NeuroUnitEqnsetPostSynaptic,
            eqnset = simple_ampa_syn,
            default_parameters = { 'scale':1.0}
            )
    
    syn1 = sim.create_synapse(
            trigger =  env.SynapticTrigger(
                                        SynapticTriggerByVoltageThreshold,
                                            cell_location = CellLocator.get_location_at_distance_away_from_dummy(cell1, 300),
                                            voltage_threshold = qty("0:mV"),  delay=qty("0:ms"), 
                                       ),
            postsynaptic_mech = post_syn_tmpl.instantiate(cell_location = cell2.soma,), 
           )
    
    syn1 = sim.create_synapse(
            trigger =  env.SynapticTrigger(
                                        SynapticTriggerByVoltageThreshold,
                                        cell_location = CellLocator.get_location_at_distance_away_from_dummy(cell1, 700),
                                        voltage_threshold = qty("0:mV"),  delay = qty("0:ms"),
                                       ),
            postsynaptic_mech = post_syn_tmpl.instantiate(cell_location = cell3.soma, parameter_overrides={'scale':2.0} )  
           )
    
    # Record Voltages from axons:
    for loc in CellLocator.get_locations_at_distances_away_from_dummy(cell1, range(0, 1000, 50)):
        sim.record( what=StandardTags.Voltage, cell_location = loc, user_tags=['cell1'])
    sim.record(what=StandardTags.Voltage, cell_location = cell2.get_location("soma"), user_tags=['cell2'])
    sim.record(what=StandardTags.Voltage, cell_location = cell3.get_location("soma"), user_tags=['cell3'])
    
    # Create the stimulus and record the injected current:
    cc = sim.create_currentclamp(name="CC1", amp=qty("200:pA"), dur=qty("1:ms"), delay=qty("100:ms"), cell_location=cell1.get_location("soma"))
    sim.record(cc, what=StandardTags.Current)
    
    results = sim.run()
    TagViewer(results, timerange=(98, 120)*units.ms,
              fig_kwargs = {'figsize':(12, 10)},
              show=True,
              plots = [
                  TagPlot('Current', yunit=units.picoamp),
                  TagPlot('Voltage,cell1', yrange=(-80*units.mV, 50*units.mV), yunit=units.mV),
                  TagPlot('Voltage AND ANY{cell2,cell3}', yrange=(-70*units.mV, -55*units.mV), yunit=units.millivolt),
                 ],
               )
    
    
    




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/poster2_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/poster2_out1.png>`






Output
~~~~~~

.. code-block:: bash

        No handlers could be found for logger "neurounits"
    2013-12-01 17:16:17,706 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:16:17,707 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
    No handlers could be found for logger "neurounits"
    2013-12-01 17:16:20,322 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:16:20,322 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/53/53c6998e8827a28214a7ec15f50c6a65.bundle (48k) : 0.987 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_fe29ca000b1bf9f98f8a5a86da5768f4.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_4a46a0f70872d4114e6b6a454639c210.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_8e3462bc4d8c5799b1edfe26d70b04ec.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_e1d9b15c15cf730d6ad5de223a1b3007.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_8c477b241bf2d2faa9a7d850b7091542.hoc
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
    Running Simulation
    Time for Extracting Data: (23 records) 0.0401768684387
    Running simulation : 3.909 seconds
    Size of results file: 0.6 (MB)
    Post-processing : 0.055 seconds
    Entire load-run-save time : 4.952 seconds
    Suceeded
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    <Parameter [id:56178448] Symbol: 'scale' >
    scale
    iii 1.0 dimensionless <class 'quantities.quantity.Quantity'>
    iiii 1.0 <type 'float'>
    Output <StateVariable [id:56249808] Symbol: 'g' >
    None
    Output <AssignedVariable [id:56249168] Symbol: 'gmax' >
    None
    Output <AssignedVariable [id:56248528] Symbol: 'i' >
    {u'mf': {u'role': u'TRANSMEMBRANECURRENT'}}
    input <SuppliedValue [id:56262864] Symbol: 'v' >
    {u'mf': {u'role': u'MEMBRANEVOLTAGE'}}
    scale <class 'neurounits.ast.astobjects.Parameter'>
    gmax <class 'neurounits.ast.astobjects.AssignedVariable'>
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    g <class 'neurounits.ast.astobjects.StateVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:56248400] Symbol: gmax >
    scale <class 'neurounits.ast.astobjects.Parameter'>
    Writing assignment for:  <EqnAssignmentByRegime [id:56250000] Symbol: i >
    gmax <class 'neurounits.ast.astobjects.AssignedVariable'>
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    g <class 'neurounits.ast.astobjects.StateVariable'>
    g <class 'neurounits.ast.astobjects.StateVariable'>
    <neurounits.codegen.nmodl.MODLBuildParameters object at 0x3593610>
    g <class 'neurounits.ast.astobjects.StateVariable'>
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/53//53c6998e8827a28214a7ec15f50c6a65.neuronsim.results.pickle ]
    PlotManger saving:  _output/figures/poster2/{png,svg}/fig000_Autosave_figure_1.{png,svg}




