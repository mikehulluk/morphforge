
.. _example_singlecell_simulation010:

Example 7. The response of a single compartment neuron with leak channels to step current injection
===================================================================================================


The response of a single compartment neuron with leak channels to step current injection.
In this example, we build a single section neuron, with passive channels,
and stimulate it with a step current clamp of 200pA for 100ms starting at t=100ms.
We also create a summary pdf of the simulation.

Code
~~~~

.. code-block:: python

    
    
    
    
    
    
    
    from morphforge.stdimports import *
    from morphforgecontrib.stdimports import StdChlLeak
    
    
    # Create the morphology for the cell:
    morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
    m1 = MorphologyTree.fromDictionary(morphDict1)
    
    # Create the environment:
    env = NEURONEnvironment()
    
    # Create the simulation:
    sim = env.Simulation()
    
    
    # Create a cell:
    cell = sim.create_cell(name="Cell1", morphology=m1)
    
    
    # Apply the mechanisms to the cells
    lk_chl = env.Channel(StdChlLeak,
                             name="LkChl",
                             conductance=qty("0.25:mS/cm2"),
                             reversalpotential=qty("-51:mV"),
                           )
    
    cell.apply_channel( lk_chl)
    cell.set_passive( PassiveProperty.SpecificCapacitance, qty('1.0:uF/cm2'))
    
    
    
    # Create the stimulus and record the injected current:
    cc = sim.create_currentclamp(name="Stim1", amp=qty("200:pA"), dur=qty("100:ms"), delay=qty("100:ms"), cell_location=cell.soma)
    
    
    # Define what to record:
    sim.record(cell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = cell.soma)
    sim.recordall(lk_chl, cell_location=cell.soma)
    
    
    # run the simulation
    results = sim.run()
    
    # Create an output .pdf
    SimulationMRedoc.build( sim ).to_pdf(__file__ + '.pdf')
    
    
    # Display the results:
    TagViewer([results], figtitle="The response of a neuron to step current injection", timerange=(95, 200)*units.ms, show=True)
    
    
    
    




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation010_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation010_out1.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation010_out2.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation010_out2.png>`






Output
~~~~~~

.. code-block:: bash

        No handlers could be found for logger "neurounits"
    2013-12-01 17:10:07,798 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:10:07,799 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
    No handlers could be found for logger "neurounits"
    2013-12-01 17:10:09,880 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:10:09,881 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/e8/e8833a46ab6c914215b975766ffc53a2.bundle (10k) : 0.843 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-51.0) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(2.5) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_640025bfcb95dabed2220b5e874a64e1.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_26a2e296238b62afeb4fd164ef368096.hoc
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
    Time for Extracting Data: (3 records) 0.0272469520569
    Running simulation : 0.407 seconds
    Size of results file: 0.0 (MB)
    Post-processing : 0.006 seconds
    Entire load-run-save time : 1.257 seconds
    Suceeded
    /usr/bin/pdflatex
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/e8//e8833a46ab6c914215b975766ffc53a2.neuronsim.results.pickle ]
    Warning: node 'Cell1', graph 'graphname' size too small for label
    Warning: node 'Stim1', graph 'graphname' size too small for label
    
    [(100.0, array([ 1.,  0.,  0.])), (0.0, array([ 0.,  1.,  0.])), (0.0, array([ 0.,  0.,  1.]))]
    Saving figure /home/michael/.mredoc/build/figs/opfile0002
    Tex File: /home/michael/.mredoc/build/pdflatex/eqnset.tex
    Successfully written PDF to:  /mnt/scratch/tmp/morphforge/tmp/mf_doc_build/singlecell_simulation010.py.pdf
    PlotManger saving:  _output/figures/singlecell_simulation010/{png,svg}/fig000_Autosave_figure_1.{png,svg}
    PlotManger saving:  _output/figures/singlecell_simulation010/{png,svg}/fig001_Autosave_figure_2.{png,svg}




