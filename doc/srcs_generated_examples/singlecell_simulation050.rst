
.. _example_singlecell_simulation050:

Example 11. Demonstrate using NEURON mod files directly in a simulation
=======================================================================


Demonstrate using NEURON mod files directly in a simulation
We run two simulations, using 2 slightly different mod files, and plot the membrane voltage seen.

Code
~~~~

.. code-block:: python

    
    
    
    
    
    
    
    from morphforge.stdimports import *
    from morphforgecontrib.simulation.channels.exisitingmodfile.core import SimulatorSpecificChannel
    
    
    def build_simulation(modfilename):
        # Create the morphology for the cell:
        morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
        m1 = MorphologyTree.fromDictionary(morphDict1)
    
    
        # Create the environment:
        env = NEURONEnvironment()
    
        # Create the simulation:
        sim = env.Simulation()
        cell = sim.create_cell(morphology=m1)
    
    
        modChls = env.Channel(SimulatorSpecificChannel, modfilename=modfilename)
    
        # Apply the mechanisms to the cells
        cell.apply_channel( modChls)
    
        sim.record(cell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = cell.soma, description='Membrane Voltage')
        sim.create_currentclamp(name="Stim1", amp=qty("200:pA"), dur=qty("100:ms"), delay=qty("100:ms"), cell_location=cell.soma)
    
        results = sim.run()
        return results
    
    
    
    mod3aFilename = Join(LocMgr.get_test_mods_path(), "exampleChannels3a.mod")
    results3a = build_simulation(mod3aFilename)
    
    mod3bFilename = Join(LocMgr.get_test_mods_path(), "exampleChannels3b.mod")
    results3b = build_simulation(mod3bFilename)
    
    TagViewer([results3a, results3b], timerange=(95, 200)*units.ms)
    
    try:
        import os
        print 'Differences between the two mod files:'
        os.system("diff %s %s"%(mod3aFilename, mod3bFilename))
    except:
        print "<Can't run 'diff', so can't show differences!>"
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation050_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation050_out1.png>`






Output
~~~~~~

.. code-block:: bash

        No handlers could be found for logger "neurounits"
    2013-12-01 17:11:18,167 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:11:18,168 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
    No handlers could be found for logger "neurounits"
    2013-12-01 17:11:20,153 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:11:20,154 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/20/2007868be371f03d6c270907ca8fb379.bundle (11k) : 0.828 seconds
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_b9e50529a8d1f686ed3955884ae081fa.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_0b471241e9da39b7cf3360eac4bafab3.hoc
    	1 
    	1 
    	0.01 
    	0 
    	1 
    	50000 
    	1 
    Running Simulation
    Time for Extracting Data: (1 records) 0.00195908546448
    Running simulation : 0.312 seconds
    Size of results file: 0.1 (MB)
    Post-processing : 0.007 seconds
    Entire load-run-save time : 1.147 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-12-01 17:11:22,715 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:11:22,715 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/b1/b1363a8e60c10cd92c6ee878e802fcf9.bundle (11k) : 0.844 seconds
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_5e54856fc3939091ebcff35b32cc9ab3.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_5088290ab0782eb50e572e2dfe44dba8.hoc
    	1 
    	1 
    	0.01 
    	0 
    	1 
    	50000 
    	1 
    Running Simulation
    Time for Extracting Data: (1 records) 0.00190591812134
    Running simulation : 0.330 seconds
    Size of results file: 0.1 (MB)
    Post-processing : 0.007 seconds
    Entire load-run-save time : 1.181 seconds
    Suceeded
    15c15
    <         SUFFIX exampleChannels3a
    ---
    >         SUFFIX exampleChannels3b
    28c28
    <         el = -64.3 (mV)
    ---
    >         el = -44.3 (mV)
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/20//2007868be371f03d6c270907ca8fb379.neuronsim.results.pickle ]
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/b1//b1363a8e60c10cd92c6ee878e802fcf9.neuronsim.results.pickle ]
    PlotManger saving:  _output/figures/singlecell_simulation050/{png,svg}/fig000_Autosave_figure_1.{png,svg}
    Differences between the two mod files:




