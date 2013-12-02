
.. _example_singlecell_simulation030:

Example 9. Hodgkin-Huxley '52 neuron simulation with automatic summary pdf generation
=====================================================================================


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
    from morphforgecontrib.stdimports import StdChlLeak, StdChlAlphaBeta
    
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
    
    
    # Create an output .pdf
    SimulationMRedoc.build( sim ).to_pdf(__file__ + '.pdf')
    
    # Display the results:
    TagViewer([results], timerange=(50, 250)*units.ms, show=True)
    
    
    




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation030_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation030_out1.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation030_out2.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation030_out2.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation030_out3.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation030_out3.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation030_out4.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation030_out4.png>`






Output
~~~~~~

.. code-block:: bash

        No handlers could be found for logger "neurounits"
    2013-12-01 17:10:35,102 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:10:35,102 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
    No handlers could be found for logger "neurounits"
    2013-12-01 17:10:37,250 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:10:37,250 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/26/2607e3e2726bea30b32ea1330fbe6aa2.bundle (11k) : 0.831 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_af84455a7bd10be7408061ecd02b589b.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_fb18cab9ab8db5d2c968f5e6fba6a942.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_e1d9b15c15cf730d6ad5de223a1b3007.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_f9eabaec748627fc36116940a8512cba.hoc
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
    Time for Extracting Data: (2 records) 0.00352597236633
    Running simulation : 0.449 seconds
    Size of results file: 0.1 (MB)
    Post-processing : 0.011 seconds
    Entire load-run-save time : 1.291 seconds
    Suceeded
    /usr/bin/pdflatex
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/26//2607e3e2726bea30b32ea1330fbe6aa2.neuronsim.results.pickle ]
    Warning: node 'Cell1', graph 'graphname' size too small for label
    Warning: node 'Stim1', graph 'graphname' size too small for label
    
    [(100.0, array([ 1.,  0.,  0.])), (0.0, array([ 0.,  1.,  0.])), (0.0, array([ 0.,  0.,  1.]))]
    Saving figure /home/michael/.mredoc/build/figs/opfile0002
    Saving figure /home/michael/.mredoc/build/figs/opfile0003
    Saving figure /home/michael/.mredoc/build/figs/opfile0004
    Tex File: /home/michael/.mredoc/build/pdflatex/eqnset.tex
    Successfully written PDF to:  /mnt/scratch/tmp/morphforge/tmp/mf_doc_build/singlecell_simulation030.py.pdf
    PlotManger saving:  _output/figures/singlecell_simulation030/{png,svg}/fig000_Autosave_figure_1.{png,svg}
    PlotManger saving:  _output/figures/singlecell_simulation030/{png,svg}/fig001_Autosave_figure_2.{png,svg}
    PlotManger saving:  _output/figures/singlecell_simulation030/{png,svg}/fig002_Autosave_figure_3.{png,svg}
    PlotManger saving:  _output/figures/singlecell_simulation030/{png,svg}/fig003_Autosave_figure_4.{png,svg}




