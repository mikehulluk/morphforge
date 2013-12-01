
.. _example_singlecell_simulation070:

Example 14. Visualising the internal states of a neuron
=======================================================


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






Output
~~~~~~

.. code-block:: bash

        No handlers could be found for logger "neurounits"
    2013-12-01 17:11:46,028 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:11:46,029 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
    No handlers could be found for logger "neurounits"
    2013-12-01 17:11:48,279 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:11:48,280 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/d3/d3a0a230d78d6c9f4a15ea8cc8cad730.bundle (13k) : 0.840 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_af84455a7bd10be7408061ecd02b589b.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_fb18cab9ab8db5d2c968f5e6fba6a942.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_250f079a9019e4d528955aa6190f2826.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_695590c978377002c1fd6c3e9fde85d0.hoc
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
    Time for Extracting Data: (11 records) 0.0535809993744
    Running simulation : 0.553 seconds
    Size of results file: 0.3 (MB)
    Post-processing : 0.028 seconds
    Entire load-run-save time : 1.422 seconds
    Suceeded
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    
    ConductanceDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3847610>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3801790>}
    
    ConductanceDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3847f50>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3801790>}
    
    CurrentDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3847190>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3801790>}
    
    CurrentDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3847c50>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3801790>}
    
    StateVariable
    {'state': 'm', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x385b050>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3801790>}
    
    StateVariable
    {'state': 'h', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x385b110>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3801790>}
    
    StateVariable
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x385b210>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3801790>}
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/d3//d3a0a230d78d6c9f4a15ea8cc8cad730.neuronsim.results.pickle ]
    PlotManger saving:  _output/figures/singlecell_simulation070/{png,svg}/fig000_Autosave_figure_1.{png,svg}
    PlotManger saving:  _output/figures/singlecell_simulation070/{png,svg}/fig001_Autosave_figure_2.{png,svg}
    PlotManger saving:  _output/figures/singlecell_simulation070/{png,svg}/fig002_Autosave_figure_3.{png,svg}




