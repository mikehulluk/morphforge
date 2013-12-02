
.. _example_singlecell_simulation100:

Example 17. Specifying the different types of current clamps
============================================================


Specifying the different types of current clamps.
A simulation in which a passve neuron is stimulated with different
types of current-clamps.

Code
~~~~

.. code-block:: python

    
    
    
    
    
    from morphforge.stdimports import *
    from morphforgecontrib.stdimports import *
    
    # Create the environment:
    env = NEURONEnvironment()
    sim = env.Simulation()
    
    # Create a cell:
    m1 = MorphologyTree.fromDictionary({'root': {'length': 20, 'diam': 40, 'id':'soma'} })
    cell = sim.create_cell(name="Cell1", morphology=m1)
    
    # Apply the channels uniformly over the cell
    lk_chl = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Lk", env=env)
    cell.apply_channel( lk_chl)
    
    # Create a selection of current clamps
    cc0 = sim.create_currentclamp(name='CC0', amp=750*units.pA, dur=40*units.ms, delay=40*units.ms, cell_location=cell.soma)
    cc1 = sim.create_currentclamp(name='CC1', amp=200*units.pA, dur=40*units.ms, delay=100*units.ms, cell_location=cell.soma)
    
    cc2 = sim.create_currentclamp(protocol=CurrentClampSinwave, name='CC2', 
                amp=150*units.pA, freq=100*units.Hz, 
                delay=150*units.ms, bias = 0*units.pA, duration=40*units.ms, cell_location=cell.soma)
    cc3 = sim.create_currentclamp(protocol=CurrentClampSinwave, name='CC3', 
                amp=250*units.pA, freq=250*units.Hz,
                delay=200*units.ms, bias = 200*units.pA, duration=40*units.ms, cell_location=cell.soma)
    
    cc4 = sim.create_currentclamp(protocol=CurrentClampRamp, name='CC4', 
                amp0=0*units.pA, amp1=100*units.pA, 
                time0=250*units.ms, time1=280*units.ms, time2=290*units.ms, cell_location=cell.soma)
    cc5 = sim.create_currentclamp(protocol=CurrentClampRamp, name='CC5',
                amp0=-50*units.pA, amp1=-100*units.pA, 
                time0=300*units.ms, time1=330*units.ms, time2=340*units.ms, cell_location=cell.soma)
    
    for cc in [cc0,cc1,cc2,cc3, cc4, cc5]:
        sim.record(cc, what=StandardTags.Current)
    sim.record(cell, what=StandardTags.Voltage, cell_location = cell.soma)
    
    results = sim.run()
    TagViewer(results, timerange=(30, 500)*units.ms )
    
    




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation100_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation100_out1.png>`






Output
~~~~~~

.. code-block:: bash

        No handlers could be found for logger "neurounits"
    2013-12-01 17:13:42,493 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:13:42,494 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
    No handlers could be found for logger "neurounits"
    2013-12-01 17:13:44,716 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:13:44,716 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/a1/a19789440c4b3c2a33a833aad2b92d91.bundle (15k) : 0.865 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_66970b4f6bd9d1781c5471f1e35ea623.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_dfae3bc9af5308acf4eaccb4bf0c1922.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_e1d9b15c15cf730d6ad5de223a1b3007.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_5a1ef2e02626a8464fb9327ebb72cf24.hoc
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
    Running Simulation
    Time for Extracting Data: (7 records) 0.011402130127
    Running simulation : 0.480 seconds
    Size of results file: 0.2 (MB)
    Post-processing : 0.021 seconds
    Entire load-run-save time : 1.366 seconds
    Suceeded
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/a1//a19789440c4b3c2a33a833aad2b92d91.neuronsim.results.pickle ]
    PlotManger saving:  _output/figures/singlecell_simulation100/{png,svg}/fig000_Autosave_figure_1.{png,svg}




