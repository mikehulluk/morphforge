
.. _example_singlecell_simulation040:

Example 10. Investigating the rheobase of a neuron with a parameter sweep
=========================================================================


Investigating the rheobase of a neuron with a parameter sweep

WARNING: The automatic naming and linkage between grpah colors is currently under a refactor; what is done in this script is not representing the best possible solution, or even something that will reliably work in the future!

The aim of this script is just to show that it is possible to run multiple simulations from a single script!

Code
~~~~

.. code-block:: python

    
    
    
    
    
    
    
    from morphforge.stdimports import *
    from morphforgecontrib.stdimports import StdChlLeak, StdChlAlphaBeta
    
    
    @cached_functor
    def get_Na_Channels(env):
        na_state_vars = {"m":
                        {"alpha": [13.01,0,4,-1.01,-12.56], "beta": [5.73,0,1,9.01,9.69] },
                       "h":
                        {"alpha": [0.06,0,0,30.88,26], "beta": [3.06,0,1,-7.09,-10.21]}
                       }
    
        return  env.Channel(
                                StdChlAlphaBeta,
                                name="NaChl", ion="na",
                                equation="m*m*m*h",
                                conductance=qty("210:nS") / qty("400:um2"),
                                reversalpotential=qty("50.0:mV"),
                                statevars=na_state_vars,
                               )
    
    @cached_functor
    def get_Ks_Channels(env):
        kf_state_vars = {"ks": {"alpha": [0.2,0,1,-6.96,-7.74 ], "beta": [0.05,0,2,-18.07,6.1 ] } }
    
        return  env.Channel(
                                StdChlAlphaBeta,
                                name="KsChl", ion="ks",
                                equation="ks*ks*ks*ks",
                                conductance=qty("3:nS") / qty("400:um2"),
                                reversalpotential=qty("-80.0:mV"),
                                statevars=kf_state_vars,
                               )
    
    @cached_functor
    def get_Kf_Channels(env):
        kf_state_vars = {"kf": {"alpha": [ 3.1,0,1,-31.5,-9.3], "beta": [0.44,0,1,4.98,16.19 ] } }
    
        return  env.Channel(
                                StdChlAlphaBeta,
                                name="KfChl", ion="kf",
                                equation="kf*kf*kf*kf",
                                conductance=qty("0.5:nS") / qty("400:um2") ,
                                reversalpotential=qty("-80.0:mV"),
                                statevars=kf_state_vars,
                               )
    
    @cached_functor
    def get_Lk_Channels(env):
        lk_chl = env.Channel(
                             StdChlLeak,
                             name="LkChl",
                             conductance=qty("3.6765:nS") / qty("400:um2"),
                             reversalpotential=qty("-51:mV"),
                           )
        return lk_chl
    
    
    
    
    def simulate(current_inj_level):
        # Create the environment:
        env = NEURONEnvironment()
    
        # Create the simulation:
        sim = env.Simulation(name="AA")
    
    
        # Create a cell:
        morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
        morph = MorphologyTree.fromDictionary(morphDict1)
        cell = sim.create_cell(name="Cell1", morphology=morph)
    
        lk_chl = get_Lk_Channels(env)
        na_chl = get_Na_Channels(env)
        potFastChannels = get_Kf_Channels(env)
        potSlowChannels = get_Ks_Channels(env)
    
        cell.apply_channel( lk_chl)
        cell.apply_channel( na_chl)
        cell.apply_channel( potFastChannels)
        cell.apply_channel( potSlowChannels)
        cell.set_passive( PassiveProperty.SpecificCapacitance, qty('2.0:uF/cm2'))
    
    
    
        # Create the stimulus and record the injected current:
        cc = sim.create_currentclamp(amp=current_inj_level, dur=qty("100:ms"), delay=qty("100:ms"), cell_location=cell.soma)
        sim.record(cc, what=StandardTags.Current)
    
        # Define what to record:
        sim.record(cell, what=StandardTags.Voltage, cell_location = cell.soma)
    
        # run the simulation
        results = sim.run()
    
        return results
    
    
    # Display the results:
    #results = [simulate(current_inj_level='%d:pA' % i) for i in [50,100,150,200, 250, 300]  ]
    results = [simulate(current_inj_level='%d:pA' % i) for i in [50]  ]
    
    
    # Create an output .pdf of the first simulation:
    SimulationMRedoc.build( results[0] ).to_pdf(__file__ + '.pdf')
    
    TagViewer(results, timerange=(95, 200)*units.ms, show=True)
    
    
    
    




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation040_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation040_out1.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation040_out2.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation040_out2.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation040_out5.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation040_out5.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation040_out6.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation040_out6.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation040_out3.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation040_out3.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation040_out4.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation040_out4.png>`






Output
~~~~~~

.. code-block:: bash

        No handlers could be found for logger "neurounits"
    2013-12-01 17:10:52,111 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:10:52,111 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
    No handlers could be found for logger "neurounits"
    2013-12-01 17:10:54,239 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:10:54,239 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/5b/5b26463f7871798c2f37d8f819bb039a.bundle (12k) : 0.826 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-51.0) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(9.19125) * S/m**2}
    
    Executing: /home/michael/opt//x86_64/bin/modlunit /mnt/scratch/tmp/morphforge/tmp/tmp_35ef696eee624ddddad719ec8975e2b8.mod
    /mnt/scratch/tmp/morphforge/tmp/modbuild_20285
    Executing: /home/michael/opt//x86_64/bin/nocmodl tmp_35ef696eee624ddddad719ec8975e2b8.mod
    Executing: /home/michael/opt//share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/home/michael/opt//include/nrn"  -I"/home/michael/opt//x86_64/lib"    -g -O2 -c -o tmp_35ef696eee624ddddad719ec8975e2b8.lo tmp_35ef696eee624ddddad719ec8975e2b8.c  
    Executing: /home/michael/opt//share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_35ef696eee624ddddad719ec8975e2b8.la  -rpath /home/michael/opt//x86_64/libs  tmp_35ef696eee624ddddad719ec8975e2b8.lo  -L/home/michael/opt//x86_64/lib -L/home/michael/opt//x86_64/lib  /home/michael/opt//x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
    OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/home/michael/opt//include/nrn -I/home/michael/opt//x86_64/lib -g -O2 -c tmp_35ef696eee624ddddad719ec8975e2b8.c  -fPIC -DPIC -o .libs/tmp_35ef696eee624ddddad719ec8975e2b8.o
    
    OP2: libtool: link: gcc -shared  -fPIC -DPIC  .libs/tmp_35ef696eee624ddddad719ec8975e2b8.o   -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -L/home/michael/opt//x86_64/lib /home/michael/opt/x86_64/lib/libnrniv.so /home/michael/opt/x86_64/lib/libnrnoc.so /home/michael/opt/x86_64/lib/liboc.so /home/michael/opt/x86_64/lib/libmemacs.so /home/michael/opt/x86_64/lib/libnrnmpi.so /home/michael/opt/x86_64/lib/libscopmath.so /home/michael/opt/x86_64/lib/libsparse13.so -lreadline -lncurses /home/michael/opt/x86_64/lib/libivoc.so /home/michael/opt/x86_64/lib/libneuron_gnu.so /home/michael/opt/x86_64/lib/libmeschach.so /home/michael/opt/x86_64/lib/libsundials.so -lm -ldl  -O2   -pthread -Wl,-soname -Wl,tmp_35ef696eee624ddddad719ec8975e2b8.so.0 -o .libs/tmp_35ef696eee624ddddad719ec8975e2b8.so.0.0.0
    libtool: link: (cd ".libs" && rm -f "tmp_35ef696eee624ddddad719ec8975e2b8.so.0" && ln -s "tmp_35ef696eee624ddddad719ec8975e2b8.so.0.0.0" "tmp_35ef696eee624ddddad719ec8975e2b8.so.0")
    libtool: link: (cd ".libs" && rm -f "tmp_35ef696eee624ddddad719ec8975e2b8.so" && ln -s "tmp_35ef696eee624ddddad719ec8975e2b8.so.0.0.0" "tmp_35ef696eee624ddddad719ec8975e2b8.so")
    libtool: link: ( cd ".libs" && rm -f "tmp_35ef696eee624ddddad719ec8975e2b8.la" && ln -s "../tmp_35ef696eee624ddddad719ec8975e2b8.la" "tmp_35ef696eee624ddddad719ec8975e2b8.la" )
    
    Executing: /home/michael/opt//x86_64/bin/modlunit /mnt/scratch/tmp/morphforge/tmp/tmp_948523052657a5cf46d1539c09528f1c.mod
    /mnt/scratch/tmp/morphforge/tmp/modbuild_20285
    Executing: /home/michael/opt//x86_64/bin/nocmodl tmp_948523052657a5cf46d1539c09528f1c.mod
    Executing: /home/michael/opt//share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/home/michael/opt//include/nrn"  -I"/home/michael/opt//x86_64/lib"    -g -O2 -c -o tmp_948523052657a5cf46d1539c09528f1c.lo tmp_948523052657a5cf46d1539c09528f1c.c  
    Executing: /home/michael/opt//share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_948523052657a5cf46d1539c09528f1c.la  -rpath /home/michael/opt//x86_64/libs  tmp_948523052657a5cf46d1539c09528f1c.lo  -L/home/michael/opt//x86_64/lib -L/home/michael/opt//x86_64/lib  /home/michael/opt//x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
    OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/home/michael/opt//include/nrn -I/home/michael/opt//x86_64/lib -g -O2 -c tmp_948523052657a5cf46d1539c09528f1c.c  -fPIC -DPIC -o .libs/tmp_948523052657a5cf46d1539c09528f1c.o
    
    OP2: libtool: link: gcc -shared  -fPIC -DPIC  .libs/tmp_948523052657a5cf46d1539c09528f1c.o   -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -L/home/michael/opt//x86_64/lib /home/michael/opt/x86_64/lib/libnrniv.so /home/michael/opt/x86_64/lib/libnrnoc.so /home/michael/opt/x86_64/lib/liboc.so /home/michael/opt/x86_64/lib/libmemacs.so /home/michael/opt/x86_64/lib/libnrnmpi.so /home/michael/opt/x86_64/lib/libscopmath.so /home/michael/opt/x86_64/lib/libsparse13.so -lreadline -lncurses /home/michael/opt/x86_64/lib/libivoc.so /home/michael/opt/x86_64/lib/libneuron_gnu.so /home/michael/opt/x86_64/lib/libmeschach.so /home/michael/opt/x86_64/lib/libsundials.so -lm -ldl  -O2   -pthread -Wl,-soname -Wl,tmp_948523052657a5cf46d1539c09528f1c.so.0 -o .libs/tmp_948523052657a5cf46d1539c09528f1c.so.0.0.0
    libtool: link: (cd ".libs" && rm -f "tmp_948523052657a5cf46d1539c09528f1c.so.0" && ln -s "tmp_948523052657a5cf46d1539c09528f1c.so.0.0.0" "tmp_948523052657a5cf46d1539c09528f1c.so.0")
    libtool: link: (cd ".libs" && rm -f "tmp_948523052657a5cf46d1539c09528f1c.so" && ln -s "tmp_948523052657a5cf46d1539c09528f1c.so.0.0.0" "tmp_948523052657a5cf46d1539c09528f1c.so")
    libtool: link: ( cd ".libs" && rm -f "tmp_948523052657a5cf46d1539c09528f1c.la" && ln -s "../tmp_948523052657a5cf46d1539c09528f1c.la" "tmp_948523052657a5cf46d1539c09528f1c.la" )
    
    Executing: /home/michael/opt//x86_64/bin/modlunit /mnt/scratch/tmp/morphforge/tmp/tmp_8e3f1017ae86fad13f965c3855e4c53b.mod
    /mnt/scratch/tmp/morphforge/tmp/modbuild_20285
    Executing: /home/michael/opt//x86_64/bin/nocmodl tmp_8e3f1017ae86fad13f965c3855e4c53b.mod
    Executing: /home/michael/opt//share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/home/michael/opt//include/nrn"  -I"/home/michael/opt//x86_64/lib"    -g -O2 -c -o tmp_8e3f1017ae86fad13f965c3855e4c53b.lo tmp_8e3f1017ae86fad13f965c3855e4c53b.c  
    Executing: /home/michael/opt//share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_8e3f1017ae86fad13f965c3855e4c53b.la  -rpath /home/michael/opt//x86_64/libs  tmp_8e3f1017ae86fad13f965c3855e4c53b.lo  -L/home/michael/opt//x86_64/lib -L/home/michael/opt//x86_64/lib  /home/michael/opt//x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
    OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/home/michael/opt//include/nrn -I/home/michael/opt//x86_64/lib -g -O2 -c tmp_8e3f1017ae86fad13f965c3855e4c53b.c  -fPIC -DPIC -o .libs/tmp_8e3f1017ae86fad13f965c3855e4c53b.o
    
    OP2: libtool: link: gcc -shared  -fPIC -DPIC  .libs/tmp_8e3f1017ae86fad13f965c3855e4c53b.o   -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -L/home/michael/opt//x86_64/lib /home/michael/opt/x86_64/lib/libnrniv.so /home/michael/opt/x86_64/lib/libnrnoc.so /home/michael/opt/x86_64/lib/liboc.so /home/michael/opt/x86_64/lib/libmemacs.so /home/michael/opt/x86_64/lib/libnrnmpi.so /home/michael/opt/x86_64/lib/libscopmath.so /home/michael/opt/x86_64/lib/libsparse13.so -lreadline -lncurses /home/michael/opt/x86_64/lib/libivoc.so /home/michael/opt/x86_64/lib/libneuron_gnu.so /home/michael/opt/x86_64/lib/libmeschach.so /home/michael/opt/x86_64/lib/NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    libsundials.so -lm -ldl  -O2   -pthread -Wl,-soname -Wl,tmp_8e3f1017ae86fad13f965c3855e4c53b.so.0 -o .libs/tmp_8e3f1017ae86fad13f965c3855e4c53b.so.0.0.0
    libtool: link: (cd ".libs" && rm -f "tmp_8e3f1017ae86fad13f965c3855e4c53b.so.0" && ln -s "tmp_8e3f1017ae86fad13f965c3855e4c53b.so.0.0.0" "tmp_8e3f1017ae86fad13f965c3855e4c53b.so.0")
    libtool: link: (cd ".libs" && rm -f "tmp_8e3f1017ae86fad13f965c3855e4c53b.so" && ln -s "tmp_8e3f1017ae86fad13f965c3855e4c53b.so.0.0.0" "tmp_8e3f1017ae86fad13f965c3855e4c53b.so")
    libtool: link: ( cd ".libs" && rm -f "tmp_8e3f1017ae86fad13f965c3855e4c53b.la" && ln -s "../tmp_8e3f1017ae86fad13f965c3855e4c53b.la" "tmp_8e3f1017ae86fad13f965c3855e4c53b.la" )
    
    Executing: /home/michael/opt//x86_64/bin/modlunit /mnt/scratch/tmp/morphforge/tmp/tmp_f81186f7d53550cac65242285b734fe5.mod
    /mnt/scratch/tmp/morphforge/tmp/modbuild_20285
    Executing: /home/michael/opt//x86_64/bin/nocmodl tmp_f81186f7d53550cac65242285b734fe5.mod
    Executing: /home/michael/opt//share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/home/michael/opt//include/nrn"  -I"/home/michael/opt//x86_64/lib"    -g -O2 -c -o tmp_f81186f7d53550cac65242285b734fe5.lo tmp_f81186f7d53550cac65242285b734fe5.c  
    Executing: /home/michael/opt//share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_f81186f7d53550cac65242285b734fe5.la  -rpath /home/michael/opt//x86_64/libs  tmp_f81186f7d53550cac65242285b734fe5.lo  -L/home/michael/opt//x86_64/lib -L/home/michael/opt//x86_64/lib  /home/michael/opt//x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
    OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/home/michael/opt//include/nrn -I/home/michael/opt//x86_64/lib -g -O2 -c tmp_f81186f7d53550cac65242285b734fe5.c  -fPIC -DPIC -o .libs/tmp_f81186f7d53550cac65242285b734fe5.o
    
    OP2: libtool: link: gcc -shared  -fPIC -DPIC  .libs/tmp_f81186f7d53550cac65242285b734fe5.o   -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -L/home/michael/opt//x86_64/lib /home/michael/opt/x86_64/lib/libnrniv.so /home/michael/opt/x86_64/lib/libnrnoc.so /home/michael/opt/x86_64/lib/liboc.so /home/michael/opt/x86_64/lib/libmemacs.so /home/michael/opt/x86_64/lib/libnrnmpi.so /home/michael/opt/x86_64/lib/libscopmath.so /home/michael/opt/x86_64/lib/libsparse13.so -lreadline -lncurses /home/michael/opt/x86_64/lib/libivoc.so /home/michael/opt/x86_64/lib/libneuron_gnu.so /home/michael/opt/x86_64/lib/libmeschach.so /home/michael/opt/x86_64/lib/libsundials.so -lm -ldl  -O2   -pthread -Wl,-soname -Wl,tmp_f81186f7d53550cac65242285b734fe5.so.0 -o .libs/tmp_f81186f7d53550cac65242285b734fe5.so.0.0.0
    libtool: link: (cd ".libs" && rm -f "tmp_f81186f7d53550cac65242285b734fe5.so.0" && ln -s "tmp_f81186f7d53550cac65242285b734fe5.so.0.0.0" "tmp_f81186f7d53550cac65242285b734fe5.so.0")
    libtool: link: (cd ".libs" && rm -f "tmp_f81186f7d53550cac65242285b734fe5.so" && ln -s "tmp_f81186f7d53550cac65242285b734fe5.so.0.0.0" "tmp_f81186f7d53550cac65242285b734fe5.so")
    libtool: link: ( cd ".libs" && rm -f "tmp_f81186f7d53550cac65242285b734fe5.la" && ln -s "../tmp_f81186f7d53550cac65242285b734fe5.la" "tmp_f81186f7d53550cac65242285b734fe5.la" )
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_88205c8a06bba8a0808d415d4b9b191d.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_40e684618b2cbfb23d3322a61c77b689.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_df6b8521f579e1ad2aeec575b6207104.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_7600478d01e0b9510e7cb196c284fe70.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_60f36e17742108a7264754d6c012af7b.hoc
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
    Time for Extracting Data: (2 records) 0.0036289691925
    Running simulation : 4.696 seconds
    Size of results file: 0.0 (MB)
    Post-processing : 0.007 seconds
    Entire load-run-save time : 5.529 seconds
    Suceeded
    /usr/bin/pdflatex
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/5b//5b26463f7871798c2f37d8f819bb039a.neuronsim.results.pickle ]
    Warning: node 'Cell1', graph 'graphname' size too small for label
    Warning: node 'AnonObj0001', graph 'graphname' size too small for label
    
    [(100.0, array([ 1.,  0.,  0.])), (0.0, array([ 0.,  1.,  0.])), (0.0, array([ 0.,  0.,  1.]))]
    Saving figure /home/michael/.mredoc/build/figs/opfile0002
    Saving figure /home/michael/.mredoc/build/figs/opfile0003
    Saving figure /home/michael/.mredoc/build/figs/opfile0004
    Saving figure /home/michael/.mredoc/build/figs/opfile0005
    PlotManger saving:  _output/figures/singlecell_simulation040/{png,svg}/fig000_Autosave_figure_1.{png,svg}
    PlotManger saving:  _output/figures/singlecell_simulation040/{png,svg}/fig001_Autosave_figure_2.{png,svg}
    PlotManger saving:  _output/figures/singlecell_simulation040/{png,svg}/fig002_Autosave_figure_3.{png,svg}
    PlotManger saving:  _output/figures/singlecell_simulation040/{png,svg}/fig003_Autosave_figure_4.{png,svg}
    PlotManger saving:  _output/figures/singlecell_simulation040/{png,svg}/fig004_Autosave_figure_5.{png,svg}
    Saving figure /home/michael/.mredoc/build/figs/opfile0006
    Tex File: /home/michael/.mredoc/build/pdflatex/eqnset.tex
    Successfully written PDF to:  /mnt/scratch/tmp/morphforge/tmp/mf_doc_build/singlecell_simulation040.py.pdf
    PlotManger saving:  _output/figures/singlecell_simulation040/{png,svg}/fig005_Autosave_figure_6.{png,svg}




