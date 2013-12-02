
.. _example_singlecell_simulation080:

Example 15. Applying different channel densities over a cell
============================================================


Applying different channel densities over a cell.
We start with a cell with a long axon, and then apply Hodgkin-Huxley channels over the surface. We look at the effect of changing the density of leak and sodium channels in just the axon of the neuron (not the soma)

This example also shows the use of tags; 300 traces are recorded in this experiment; but we don't ever need to get
involved in managing them directly. We can just specify that all traces recorded on simulation X should be tagged with "SIMY", and
then tell the TagViewer to plot everything with a tag 'SIMY'

Code
~~~~

.. code-block:: python

    
    
    
    
    
    
    
    
    from morphforge.stdimports import *
    from morphforgecontrib.stdimports import StandardModels
    
    
    def sim(glk_multiplier, gna_multiplier, tag):
        
        env = NEURONEnvironment()
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
        sim(gna_multiplier=0.75, glk_multiplier=1.0, tag="SIM8"),
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


.. figure:: /srcs_generated_examples/images/singlecell_simulation080_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation080_out1.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation080_out2.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation080_out2.png>`






Output
~~~~~~

.. code-block:: bash

        No handlers could be found for logger "neurounits"
    2013-12-01 17:11:58,226 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:11:58,226 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
    No handlers could be found for logger "neurounits"
    2013-12-01 17:12:00,529 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:12:00,529 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/37/37fe410751d68ab77348d725093b9a37.bundle (23k) : 0.843 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_af84455a7bd10be7408061ecd02b589b.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_fb18cab9ab8db5d2c968f5e6fba6a942.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_250f079a9019e4d528955aa6190f2826.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_8be294eccf854380121f9cc2534c9637.hoc
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
    Time for Extracting Data: (30 records) 0.0491099357605
    Running simulation : 2.325 seconds
    Size of results file: 0.6 (MB)
    Post-processing : 0.052 seconds
    Entire load-run-save time : 3.221 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-12-01 17:12:05,427 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:12:05,427 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/9b/9ba409992e7a26e50ed93b6987b21266.bundle (23k) : 0.844 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    Executing: /home/michael/opt//x86_64/bin/modlunit /mnt/scratch/tmp/morphforge/tmp/tmp_5c515003560d11f7f6c5bf95994063d3.mod
    /mnt/scratch/tmp/morphforge/tmp/modbuild_21627
    Executing: /home/michael/opt//x86_64/bin/nocmodl tmp_5c515003560d11f7f6c5bf95994063d3.mod
    Executing: /home/michael/opt//share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/home/michael/opt//include/nrn"  -I"/home/michael/opt//x86_64/lib"    -g -O2 -c -o tmp_5c515003560d11f7f6c5bf95994063d3.lo tmp_5c515003560d11f7f6c5bf95994063d3.c  
    Executing: /home/michael/opt//share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_5c515003560d11f7f6c5bf95994063d3.la  -rpath /home/michael/opt//x86_64/libs  tmp_5c515003560d11f7f6c5bf95994063d3.lo  -L/home/michael/opt//x86_64/lib -L/home/michael/opt//x86_64/lib  /home/michael/opt//x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
    OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/home/michael/opt//include/nrn -I/home/michael/opt//x86_64/lib -g -O2 -c tmp_5c515003560d11f7f6c5bf95994063d3.c  -fPIC -DPIC -o .libs/tmp_5c515003560d11f7f6c5bf95994063d3.o
    
    OP2: libtool: link: gcc -shared  -fPIC -DPIC  .libs/tmp_5c515003560d11f7f6c5bf95994063d3.o   -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -L/home/michael/opt//x86_64/lib /home/michael/opt/x86_64/lib/libnrniv.so /home/michael/opt/x86_64/lib/libnrnoc.so /home/michael/opt/x86_64/lib/liboc.so /home/michael/opt/x86_64/lib/libmemacs.so /home/michael/opt/x86_64/lib/libnrnmpi.so /home/michael/opt/x86_64/lib/libscopmath.so /home/michael/opt/x86_64/lib/libsparse13.so -lreadline -lncurses /home/michael/opt/x86_64/lib/libivoc.so /home/michael/opt/x86_64/lib/libneuron_gnu.so /home/michael/opt/x86_64/lib/libmeschach.so /home/michael/opt/x86_64/lib/libsundials.so -lm -ldl  -O2   -pthread -Wl,-soname -Wl,tmp_5c515003560d11f7f6c5bf95994063d3.so.0 -o .libs/tmp_5c515003560d11f7f6c5bf95994063d3.so.0.0.0
    libtool: link: (cd ".libs" && rm -f "tmp_5c515003560d11f7f6c5bf95994063d3.so.0" && ln -s "tmp_5c515003560d11f7f6c5bf95994063d3.so.0.0.0" "tmp_5c515003560d11f7f6c5bf95994063d3.so.0")
    libtool: link: (cd ".libs" && rm -f "tmp_5c515003560d11f7f6c5bf95994063d3.so" && ln -s "tmp_5c515003560d11f7f6c5bf95994063d3.so.0.0.0" "tmp_5c515003560d11f7f6c5bf95994063d3.so")
    libtool: link: ( cd ".libs" && rm -f "tmp_5c515003560d11f7f6c5bf95994063d3.la" && ln -s "../tmp_5c515003560d11f7f6c5bf95994063d3.la" "tmp_5c515003560d11f7f6c5bf95994063d3.la" )
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_9ecf8f39fd9146b277ff6177749299c6.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_62a4ddcd4ac772510aa6813825f854fa.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_979e51e8134d9ad14b8ff4498af4abcc.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_982d1751e1efe1e2df1ad423178619e6.hoc
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
    Time for Extracting Data: (30 records) 0.053050994873
    Running simulation : 3.140 seconds
    Size of results file: 0.5 (MB)
    Post-processing : 0.049 seconds
    Entire load-run-save time : 4.033 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-12-01 17:12:11,057 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:12:11,057 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/b9/b9013013773c24d5cb34879f5a07e148.bundle (23k) : 0.834 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_1b9db84d43b77ec2fb2e53e206df6e31.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_08fd042f5617092e986b5453289c786a.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_7df4c149812c25e673966e04c457447e.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_747cfe823e9c27c230ee7a5d068a636a.hoc
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
    Time for Extracting Data: (30 records) 0.053318977356
    Running simulation : 2.098 seconds
    Size of results file: 0.4 (MB)
    Post-processing : 0.042 seconds
    Entire load-run-save time : 2.974 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-12-01 17:12:15,696 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:12:15,697 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/05/05ce1c77cbabd00648e2abc7f8391d8f.bundle (23k) : 0.873 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_441d00ac1d6ed2d478a432634287e05e.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_20f6d2c3344f354cb5e5fc2759b4552b.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_493e4afc99901274d3bc57b05062327c.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_ab5326e2b7e5a80e09ceb3cda3d380a2.hoc
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
    Time for Extracting Data: (30 records) 0.0526940822601
    Running simulation : 2.221 seconds
    Size of results file: 0.5 (MB)
    Post-processing : 0.048 seconds
    Entire load-run-save time : 3.142 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-12-01 17:12:20,444 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:12:20,445 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/55/551abb27e0b05b74fe936ec535604fdb.bundle (23k) : 0.842 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_47e8f16ebc67f13d01a7bd84be614581.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_3bf774ddb40d01137fc04e1ccf2cc5ab.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_5163cbad7d6a5b01abf1db214c811de2.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_57e8f09677241bc3ffbeb65dd47e5da7.hoc
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
    Time for Extracting Data: (30 records) 0.0506639480591
    Running simulation : 1.787 seconds
    Size of results file: 0.4 (MB)
    Post-processing : 0.039 seconds
    Entire load-run-save time : 2.668 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-12-01 17:12:26,290 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:12:26,291 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/ee/eef320ba24fd739d08f1e52ea52b8bb4.bundle (23k) : 0.837 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_b251ce27fbf299b74853400c6fb7030f.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_9abe11266d08d5deb2ab5aadeb8cea7e.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_7e273289d9d064fd79deb81dcb7d1f60.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_cef3a3ebf3889987f4800510c3b97a3b.hoc
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
    Time for Extracting Data: (30 records) 0.0505378246307
    Running simulation : 1.485 seconds
    Size of results file: 0.2 (MB)
    Post-processing : 0.028 seconds
    Entire load-run-save time : 2.351 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-12-01 17:12:30,214 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:12:30,215 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/49/49df28cc76631862075e306b4486c18a.bundle (23k) : 0.842 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_b251ce27fbf299b74853400c6fb7030f.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_9abe11266d08d5deb2ab5aadeb8cea7e.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_7e273289d9d064fd79deb81dcb7d1f60.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_8d0569e097af1813e8d243c911b97f95.hoc
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
    Time for Extracting Data: (30 records) 0.0514340400696
    Running simulation : 2.368 seconds
    Size of results file: 0.5 (MB)
    Post-processing : 0.048 seconds
    Entire load-run-save time : 3.259 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-12-01 17:12:35,154 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:12:35,155 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/6a/6aa4576fdf0900bef97ea9ddd1ac210e.bundle (23k) : 0.836 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_1b9db84d43b77ec2fb2e53e206df6e31.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_08fd042f5617092e986b5453289c786a.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_7df4c149812c25e673966e04c457447e.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_a3731a3d542f6133f77d4d744ce6fefb.hoc
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
    Time for Extracting Data: (30 records) 0.0515050888062
    Running simulation : 2.148 seconds
    Size of results file: 0.5 (MB)
    Post-processing : 0.043 seconds
    Entire load-run-save time : 3.027 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-12-01 17:12:39,802 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:12:39,803 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/5d/5d07db38cbcf52ca1b197aab262034d1.bundle (23k) : 0.833 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_441d00ac1d6ed2d478a432634287e05e.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_20f6d2c3344f354cb5e5fc2759b4552b.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_493e4afc99901274d3bc57b05062327c.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_d13e0a86595a3af5720616e82c522fba.hoc
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
    Time for Extracting Data: (30 records) 0.0521669387817
    Running simulation : 2.084 seconds
    Size of results file: 0.4 (MB)
    Post-processing : 0.041 seconds
    Entire load-run-save time : 2.959 seconds
    Suceeded
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/37//37fe410751d68ab77348d725093b9a37.neuronsim.results.pickle ]
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/9b//9ba409992e7a26e50ed93b6987b21266.neuronsim.results.pickle ]
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/b9//b9013013773c24d5cb34879f5a07e148.neuronsim.results.pickle ]
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/05//05ce1c77cbabd00648e2abc7f8391d8f.neuronsim.results.pickle ]
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/55//551abb27e0b05b74fe936ec535604fdb.neuronsim.results.pickle ]
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/ee//eef320ba24fd739d08f1e52ea52b8bb4.neuronsim.results.pickle ]
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/49//49df28cc76631862075e306b4486c18a.neuronsim.results.pickle ]
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/6a//6aa4576fdf0900bef97ea9ddd1ac210e.neuronsim.results.pickle ]
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/5d//5d07db38cbcf52ca1b197aab262034d1.neuronsim.results.pickle ]
    PlotManger saving:  _output/figures/singlecell_simulation080/{png,svg}/fig000_Autosave_figure_1.{png,svg}
    PlotManger saving:  _output/figures/singlecell_simulation080/{png,svg}/fig001_Autosave_figure_2.{png,svg}




