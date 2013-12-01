
.. _example_multicell_simulation020:

Example 19. The responses of two cells connected by a gap junction to a step current injection into the first
=============================================================================================================


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
    
    # Create an output .pdf
    mf.SimulationMRedoc.build( sim ).to_pdf(__file__ + '.pdf')
    
    mf.TagViewer(res)
    
    
    




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/multicell_simulation020_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/multicell_simulation020_out1.png>`


.. figure:: /srcs_generated_examples/images/multicell_simulation020_out2.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/multicell_simulation020_out2.png>`


.. figure:: /srcs_generated_examples/images/multicell_simulation020_out3.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/multicell_simulation020_out3.png>`






Output
~~~~~~

.. code-block:: bash

        No handlers could be found for logger "neurounits"
    2013-12-01 17:14:10,691 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:14:10,692 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
    No handlers could be found for logger "neurounits"
    2013-12-01 17:14:12,857 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:14:12,858 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/ba/babc3e04df03ed230a636ec1d32cbdee.bundle (13k) : 0.847 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(0.0) * mV, '_name': 'AnonObj0001', '_simulation': None, 'conductance': array(0.66) * mS/cm2}
    
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(0.0) * mV, '_name': 'AnonObj0002', '_simulation': None, 'conductance': array(0.01) * mS/cm2}
    
    Executing: /home/michael/opt//x86_64/bin/modlunit /mnt/scratch/tmp/morphforge/tmp/tmp_fc0fe82d3cc8e757c40cdb2b0ba7a7bc.mod
    /mnt/scratch/tmp/morphforge/tmp/modbuild_22531
    Executing: /home/michael/opt//x86_64/bin/nocmodl tmp_fc0fe82d3cc8e757c40cdb2b0ba7a7bc.mod
    Executing: /home/michael/opt//share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/home/michael/opt//include/nrn"  -I"/home/michael/opt//x86_64/lib"    -g -O2 -c -o tmp_fc0fe82d3cc8e757c40cdb2b0ba7a7bc.lo tmp_fc0fe82d3cc8e757c40cdb2b0ba7a7bc.c  
    Executing: /home/michael/opt//share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_fc0fe82d3cc8e757c40cdb2b0ba7a7bc.la  -rpath /home/michael/opt//x86_64/libs  tmp_fc0fe82d3cc8e757c40cdb2b0ba7a7bc.lo  -L/home/michael/opt//x86_64/lib -L/home/michael/opt//x86_64/lib  /home/michael/opt//x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
    OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/home/michael/opt//include/nrn -I/home/michael/opt//x86_64/lib -g -O2 -c tmp_fc0fe82d3cc8e757c40cdb2b0ba7a7bc.c  -fPIC -DPIC -o .libs/tmp_fc0fe82d3cc8e757c40cdb2b0ba7a7bc.o
    
    OP2: libtool: link: gcc -shared  -fPIC -DPIC  .libs/tmp_fc0fe82d3cc8e757c40cdb2b0ba7a7bc.o   -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -L/home/michael/opt//x86_64/lib /home/michael/opt/x86_64/lib/libnrniv.so /home/michael/opt/x86_64/lib/libnrnoc.so /home/michael/opt/x86_64/lib/liboc.so /home/michael/opt/x86_64/lib/libmemacs.so /home/michael/opt/x86_64/lib/libnrnmpi.so /home/michael/opt/x86_64/lib/libscopmath.so /home/michael/opt/x86_64/lib/libsparse13.so -lreadline -lncurses /home/michael/opt/x86_64/lib/libivoc.so /home/michael/opt/x86_64/lib/libneuron_gnu.so /home/michael/opt/x86_64/lib/libmeschach.so /home/michael/opt/x86_64/lib/libsundials.so -lm -ldl  -O2   -pthread -Wl,-soname -Wl,tmp_fc0fe82d3cc8e757c40cdb2b0ba7a7bc.so.0 -o .libs/tmp_fc0fe82d3cc8e757c40cdb2b0ba7a7bc.so.0.0.0
    libtool: link: (cd ".libs" && rm -f "tmp_fc0fe82d3cc8e757c40cdb2b0ba7a7bc.so.0" && ln -s "tmp_fc0fe82d3cc8e757c40cdb2b0ba7a7bc.so.0.0.0" "tmp_fc0fe82d3cc8e757c40cdb2b0ba7a7bc.so.0")
    libtool: link: (cd ".libs" && rm -f "tmp_fc0fe82d3cc8e757c40cdb2b0ba7a7bc.so" && ln -s "tmp_fc0fe82d3cc8e757c40cdb2b0ba7a7bc.so.0.0.0" "tmp_fc0fe82d3cc8e757c40cdb2b0ba7a7bc.so")
    libtool: link: ( cd ".libs" && rm -f "tmp_fc0fe82d3cc8e757c40cdb2b0ba7a7bc.la" && ln -s "../tmp_fc0fe82d3cc8e757c40cdb2b0ba7a7bc.la" "tmp_fc0fe82d3cc8e757c40cdb2b0ba7a7bc.la" )
    
    Executing: /home/michael/opt//x86_64/bin/modlunit /mnt/scratch/tmp/morphforge/tmp/tmp_b0b5995b5693c940bd9065348d7750d6.mod
    /mnt/scratch/tmp/morphforgeNEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    /tmp/modbuild_22531
    Executing: /home/michael/opt//x86_64/bin/nocmodl tmp_b0b5995b5693c940bd9065348d7750d6.mod
    Executing: /home/michael/opt//share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/home/michael/opt//include/nrn"  -I"/home/michael/opt//x86_64/lib"    -g -O2 -c -o tmp_b0b5995b5693c940bd9065348d7750d6.lo tmp_b0b5995b5693c940bd9065348d7750d6.c  
    Executing: /home/michael/opt//share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_b0b5995b5693c940bd9065348d7750d6.la  -rpath /home/michael/opt//x86_64/libs  tmp_b0b5995b5693c940bd9065348d7750d6.lo  -L/home/michael/opt//x86_64/lib -L/home/michael/opt//x86_64/lib  /home/michael/opt//x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
    OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/home/michael/opt//include/nrn -I/home/michael/opt//x86_64/lib -g -O2 -c tmp_b0b5995b5693c940bd9065348d7750d6.c  -fPIC -DPIC -o .libs/tmp_b0b5995b5693c940bd9065348d7750d6.o
    
    OP2: libtool: link: gcc -shared  -fPIC -DPIC  .libs/tmp_b0b5995b5693c940bd9065348d7750d6.o   -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -L/home/michael/opt//x86_64/lib /home/michael/opt/x86_64/lib/libnrniv.so /home/michael/opt/x86_64/lib/libnrnoc.so /home/michael/opt/x86_64/lib/liboc.so /home/michael/opt/x86_64/lib/libmemacs.so /home/michael/opt/x86_64/lib/libnrnmpi.so /home/michael/opt/x86_64/lib/libscopmath.so /home/michael/opt/x86_64/lib/libsparse13.so -lreadline -lncurses /home/michael/opt/x86_64/lib/libivoc.so /home/michael/opt/x86_64/lib/libneuron_gnu.so /home/michael/opt/x86_64/lib/libmeschach.so /home/michael/opt/x86_64/lib/libsundials.so -lm -ldl  -O2   -pthread -Wl,-soname -Wl,tmp_b0b5995b5693c940bd9065348d7750d6.so.0 -o .libs/tmp_b0b5995b5693c940bd9065348d7750d6.so.0.0.0
    libtool: link: (cd ".libs" && rm -f "tmp_b0b5995b5693c940bd9065348d7750d6.so.0" && ln -s "tmp_b0b5995b5693c940bd9065348d7750d6.so.0.0.0" "tmp_b0b5995b5693c940bd9065348d7750d6.so.0")
    libtool: link: (cd ".libs" && rm -f "tmp_b0b5995b5693c940bd9065348d7750d6.so" && ln -s "tmp_b0b5995b5693c940bd9065348d7750d6.so.0.0.0" "tmp_b0b5995b5693c940bd9065348d7750d6.so")
    libtool: link: ( cd ".libs" && rm -f "tmp_b0b5995b5693c940bd9065348d7750d6.la" && ln -s "../tmp_b0b5995b5693c940bd9065348d7750d6.la" "tmp_b0b5995b5693c940bd9065348d7750d6.la" )
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_7254a011c6a75f1920b34df02c1d8135.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_557fe3244eff2b73a1c55382b6d548ca.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_5b9a22e0fb647ffe8cc542351a1e4456.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_d3680f34f28faf75923997034724a1a2.hoc
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
    Time for Extracting Data: (3 records) 0.00642418861389
    Running simulation : 2.617 seconds
    Size of results file: 1.3 (MB)
    Post-processing : 0.098 seconds
    Entire load-run-save time : 3.562 seconds
    Suceeded
    /usr/bin/pdflatex
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/ba//babc3e04df03ed230a636ec1d32cbdee.neuronsim.results.pickle ]
    Warning: node 'Cell1', graph 'graphname' size too small for label
    Warning: node 'Cell2', graph 'graphname' size too small for label
    Warning: node 'AnonObj0004', graph 'graphname' size too small for label
    
    [(397.88735772973837, array([ 1.,  0.,  0.])), (0.0, array([ 0.,  1.,  0.])), (0.0, array([ 0.,  0.,  1.]))]
    Saving figure /home/michael/.mredoc/build/figs/opfile0002
    [(1591.5494309189535, array([ 1.,  0.,  0.])), (0.0, array([ 0.,  1.,  0.])), (0.0, array([ 0.,  0.,  1.]))]
    Saving figure /home/michael/.mredoc/build/figs/opfile0003
    Tex File: /home/michael/.mredoc/build/pdflatex/eqnset.tex
    Successfully written PDF to:  /mnt/scratch/tmp/morphforge/tmp/mf_doc_build/multicell_simulation020.py.pdf
    PlotManger saving:  _output/figures/multicell_simulation020/{png,svg}/fig000_Autosave_figure_1.{png,svg}
    PlotManger saving:  _output/figures/multicell_simulation020/{png,svg}/fig001_Autosave_figure_2.{png,svg}
    PlotManger saving:  _output/figures/multicell_simulation020/{png,svg}/fig002_Autosave_figure_3.{png,svg}




