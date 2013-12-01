
.. _example_singlecell_simulation065:

Example 13. Using a channel library to reduce duplication
=========================================================


Using a channel library to reduce duplication.

We define functions that produce morphology and channel objects for our simulations.
We could stop here, and simply import and use the functions in our simulations, but
we go a step further, and register them with  "ChannelLibrary" and "MorphologyLibrary".
These are basically glorified dictionaries, that do the lookup for the appropriate functors
based on a key from the tuple~(modelsrc, celltype, channeltype). The advantage for doing this is that
there is single repository for morphologies and channels.

There is not really anythin clever going on here, and you can run simulations completely ignorantly
of these classes, I just included it because it made life much easier for me, when I had to start managing
lots of channel definitions.

Code
~~~~

.. code-block:: python

    
    
    
    
    
    
    
    
    from morphforge.stdimports import *
    from morphforgecontrib.stdimports import StdChlLeak,StdChlAlphaBeta
    
    
    
    
    # This can be put into a file that is loaded on
    # you path somewhere:
    
    # ======================================================
    def getSimpleMorphology():
    
        mDict  = {'root': { 'length': 17.5, 'diam': 17.5, 'id':'soma', 'region':'soma',   } }
        return  MorphologyTree.fromDictionary(mDict)
    
    
    def get_sample_lk(env):
        lk_chl = env.Channel(
                             StdChlLeak,
                             name="LkChl",
                             conductance=qty("0.3:mS/cm2"),
                             reversalpotential=qty("-54.3:mV"),
                           )
        return lk_chl
    
    
    def get_sample_na(env):
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
        return na_chl
    
    
    def get_sample_k(env):
        k_state_vars = { "n": { "alpha":[-0.55,-0.01,-1.0,55.0,-10.0],
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
        return k_chl
    
    
    
    MorphologyLibrary.register_morphology(modelsrc="Sample", celltype="Cell1", morph_functor=getSimpleMorphology)
    ChannelLibrary.register_channel(modelsrc="Sample", celltype="Cell1", channeltype="Na", chl_functor=get_sample_na)
    ChannelLibrary.register_channel(modelsrc="Sample", celltype="Cell1", channeltype="K", chl_functor=get_sample_k)
    ChannelLibrary.register_channel(modelsrc="Sample", celltype="Cell1", channeltype="Lk", chl_functor=get_sample_lk)
    
    # =============================================================
    
    
    
    
    
    
    
    
    
    # Now in our script elsewhere, we can use them as:
    modelsrc = "Sample"
    celltype="Cell1"
    
    # Create the environment:
    env = NEURONEnvironment()
    
    # Create the simulation:
    sim = env.Simulation()
    
    # Create a cell:
    morphology=MorphologyLibrary.get_morphology(modelsrc=modelsrc, celltype=celltype)
    cell = sim.create_cell(morphology=morphology)
    
    # Apply the channels uniformly over the cell
    na_chl = ChannelLibrary.get_channel(modelsrc=modelsrc, celltype=celltype, channeltype="Na", env=env)
    k_chl  = ChannelLibrary.get_channel(modelsrc=modelsrc, celltype=celltype, channeltype="K", env=env)
    lk_chl = ChannelLibrary.get_channel(modelsrc=modelsrc, celltype=celltype, channeltype="Lk", env=env)
    
    cell.apply_channel( na_chl)
    cell.apply_channel( k_chl )
    cell.apply_channel( lk_chl)
    
    cell.set_passive( PassiveProperty.SpecificCapacitance, qty('1.0:uF/cm2'))
    
    # Create the stimulus and record the injected current:
    cc = sim.create_currentclamp(name="Stim1", amp=qty("150:pA"), dur=qty("5:ms"), delay=qty("100:ms"), cell_location=cell.soma)
    
    sim.record(cc, what=StandardTags.Current)
    sim.record(cell, what=StandardTags.Voltage, cell_location=cell.soma)
    
    
    # run the simulation
    results = sim.run()
    
    # Display the results:
    TagViewer([results], timerange=(97.5, 140)*units.ms)
    




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation065_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation065_out1.png>`






Output
~~~~~~

.. code-block:: bash

        No handlers could be found for logger "neurounits"
    2013-12-01 17:11:37,257 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:11:37,258 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
    No handlers could be found for logger "neurounits"
    2013-12-01 17:11:39,470 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:11:39,471 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/c1/c1265244a5fb5b4ff9665635277c60da.bundle (11k) : 0.844 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    Executing: /home/michael/opt//x86_64/bin/modlunit /mnt/scratch/tmp/morphforge/tmp/tmp_77f4939b62aa0aee20909846754ab5d2.mod
    /mnt/scratch/tmp/morphforge/tmp/modbuild_21153
    Executing: /home/michael/opt//x86_64/bin/nocmodl tmp_77f4939b62aa0aee20909846754ab5d2.mod
    Executing: /home/michael/opt//share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/home/michael/opt//include/nrn"  -I"/home/michael/opt//x86_64/lib"    -g -O2 -c -o tmp_77f4939b62aa0aee20909846754ab5d2.lo tmp_77f4939b62aa0aee20909846754ab5d2.c  
    Executing: /home/michael/opt//share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_77f4939b62aa0aee20909846754ab5d2.la  -rpath /home/michael/opt//x86_64/libs  tmp_77f4939b62aa0aee20909846754ab5d2.lo  -L/home/michael/opt//x86_64/lib -L/home/michael/opt//x86_64/lib  /home/michael/opt//x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
    OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/home/michael/opt//include/nrn -I/home/michael/opt//x86_64/lib -g -O2 -c tmp_77f4939b62aa0aee20909846754ab5d2.c  -fPIC -DPIC -o .libs/tmp_77f4939b62aa0aee20909846754ab5d2.o
    
    OP2: libtool: link: gcc -shared  -fPIC -DPIC  .libs/tmp_77f4939b62aa0aee20909846754ab5d2.o   -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -L/home/michael/opt//x86_64/lib /home/michael/opt/x86_64/lib/libnrniv.so /home/michael/opt/x86_64/lib/libnrnoc.so /home/michael/opt/x86_64/lib/liboc.so /home/michael/opt/x86_64/lib/libmemacs.so /home/michael/opt/x86_64/lib/libnrnmpi.so /home/michael/opt/x86_64/lib/libscopmath.so /home/michael/opt/x86_64/lib/libsparse13.so -lreadline -lncurses /home/michael/opt/x86_64/lib/libivoc.so /home/michael/opt/x86_64/lib/libneuron_gnu.so /home/michael/opt/x86_64/lib/libmeschach.so /home/michael/opt/x86_64/lib/libsundials.so -lm -ldl  -O2   -pthread -Wl,-soname -Wl,tmp_77f4939b62aa0aee20909846754ab5d2.so.0 -o .libs/tmp_77f4939b62aa0aee20909846754ab5d2.so.0.0.0
    libtool: link: (cd ".libs" && rm -f "tmp_77f4939b62aa0aee20909846754ab5d2.so.0" && ln -s "tmp_77f4939b62aa0aee20909846754ab5d2.so.0.0.0" "tmp_77f4939b62aa0aee20909846754ab5d2.so.0")
    libtool: link: (cd ".libs" && rm -f "tmp_77f4939b62aa0aee20909846754ab5d2.so" && ln -s "tmp_77f4939b62aa0aee20909846754ab5d2.so.0.0.0" "tmp_77f4939b62aa0aee20909846754ab5d2.so")
    libtool: link: ( cd ".libs" && rm -f "tmp_77f4939b62aa0aee20909846754ab5d2.la" && ln -s "../tmp_77f4939b62aa0aee20909846754ab5d2.la" "tmp_77f4939b62aa0aee20909846754ab5d2.la" )
    
    Executing: /home/michael/opt//x86_64/bin/modlunit /mnt/scratch/tmp/morphforge/tmp/tmp_50636df53ea0c4b8840c60f57dd7bf9a.mod
    /mnt/scratch/tmp/morphforge/tmp/modbuild_21153
    Executing: /home/michael/opt//x86_64/bin/nocmodl tmp_50636df53ea0c4b8840c60f57dd7bf9a.mod
    Executing: /home/michael/opt//share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/homeNEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    /michael/opt//include/nrn"  -I"/home/michael/opt//x86_64/lib"    -g -O2 -c -o tmp_50636df53ea0c4b8840c60f57dd7bf9a.lo tmp_50636df53ea0c4b8840c60f57dd7bf9a.c  
    Executing: /home/michael/opt//share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_50636df53ea0c4b8840c60f57dd7bf9a.la  -rpath /home/michael/opt//x86_64/libs  tmp_50636df53ea0c4b8840c60f57dd7bf9a.lo  -L/home/michael/opt//x86_64/lib -L/home/michael/opt//x86_64/lib  /home/michael/opt//x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
    OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/home/michael/opt//include/nrn -I/home/michael/opt//x86_64/lib -g -O2 -c tmp_50636df53ea0c4b8840c60f57dd7bf9a.c  -fPIC -DPIC -o .libs/tmp_50636df53ea0c4b8840c60f57dd7bf9a.o
    
    OP2: libtool: link: gcc -shared  -fPIC -DPIC  .libs/tmp_50636df53ea0c4b8840c60f57dd7bf9a.o   -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -L/home/michael/opt//x86_64/lib /home/michael/opt/x86_64/lib/libnrniv.so /home/michael/opt/x86_64/lib/libnrnoc.so /home/michael/opt/x86_64/lib/liboc.so /home/michael/opt/x86_64/lib/libmemacs.so /home/michael/opt/x86_64/lib/libnrnmpi.so /home/michael/opt/x86_64/lib/libscopmath.so /home/michael/opt/x86_64/lib/libsparse13.so -lreadline -lncurses /home/michael/opt/x86_64/lib/libivoc.so /home/michael/opt/x86_64/lib/libneuron_gnu.so /home/michael/opt/x86_64/lib/libmeschach.so /home/michael/opt/x86_64/lib/libsundials.so -lm -ldl  -O2   -pthread -Wl,-soname -Wl,tmp_50636df53ea0c4b8840c60f57dd7bf9a.so.0 -o .libs/tmp_50636df53ea0c4b8840c60f57dd7bf9a.so.0.0.0
    libtool: link: (cd ".libs" && rm -f "tmp_50636df53ea0c4b8840c60f57dd7bf9a.so.0" && ln -s "tmp_50636df53ea0c4b8840c60f57dd7bf9a.so.0.0.0" "tmp_50636df53ea0c4b8840c60f57dd7bf9a.so.0")
    libtool: link: (cd ".libs" && rm -f "tmp_50636df53ea0c4b8840c60f57dd7bf9a.so" && ln -s "tmp_50636df53ea0c4b8840c60f57dd7bf9a.so.0.0.0" "tmp_50636df53ea0c4b8840c60f57dd7bf9a.so")
    libtool: link: ( cd ".libs" && rm -f "tmp_50636df53ea0c4b8840c60f57dd7bf9a.la" && ln -s "../tmp_50636df53ea0c4b8840c60f57dd7bf9a.la" "tmp_50636df53ea0c4b8840c60f57dd7bf9a.la" )
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_fe29ca000b1bf9f98f8a5a86da5768f4.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_250f079a9019e4d528955aa6190f2826.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_4a46a0f70872d4114e6b6a454639c210.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_126abe6c4d84a6d91e731bb5e7be3f37.hoc
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
    Time for Extracting Data: (2 records) 0.00391411781311
    Running simulation : 2.607 seconds
    Size of results file: 0.0 (MB)
    Post-processing : 0.009 seconds
    Entire load-run-save time : 3.460 seconds
    Suceeded
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/c1//c1265244a5fb5b4ff9665635277c60da.neuronsim.results.pickle ]
    PlotManger saving:  _output/figures/singlecell_simulation065/{png,svg}/fig000_Autosave_figure_1.{png,svg}




