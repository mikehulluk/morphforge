
.. _example_test_all:

Example 29. <Missing Docstring>
===============================




Code
~~~~

.. code-block:: python

    
    from morphforge.stdimports import *
    from morphforgecontrib.stdimports import *
    
    
    
    
    
    def test_channels():
        #for every type of channel, lets make a cell with channel and some leak:
        for key,chlfunctor in ChannelLibrary._channels.items():
    
            def my_new_cell(sim):
                cell = CellLibrary.create_cell(
                        sim=sim,
                        modelsrc=StandardModels.SingleCompartmentPassive,
                        input_resistance=300*units.MOhm)
                
                chl = chlfunctor(env=env)
                cell.apply_channel(chl)
                return cell
            CellLibrary.register(celltype='%s'%str(key), modelsrc='None', cell_functor=my_new_cell)
            
    
    
    
    
        cell_sucesses = []
        cell_failures = []
        for key, cellfunctor in sorted(CellLibrary._cells.items()):
            
            try:
                # Record everything that we can!
                env = NEURONEnvironment()
                sim = env.Simulation(tstop=400*units.ms)
                cell = CellLibrary.create_cell(sim=sim, modelsrc=key[0], celltype=key[1])
                for chl in cell.get_biophysics().get_all_channels_applied_to_cell():
                    chl.record_all(sim=sim, cell_location=cell.soma)
    
                res = sim.run()    
                cell_sucesses.append( (key,res) )
                
            except Exception, e:
                print 'Error running:', key
                print e
                cell_failures.append( (key, str(e) ) )
    
        return cell_sucesses, cell_failures
    
    
    
    
    
    
    
    
    chl_sucesses, chl_failures = test_channels()
    import mredoc as mrd
    res_doc = mrd.Section('Simulation Results',
                mrd.SectionNewPage("Channels",
                    mrd.Section('Sucesses', mrd.Table(["Key"], [ c[0] for c in chl_sucesses] ) ),
                    mrd.Section('Failures', mrd.Table(["Key", 'Msg'], [(c[0],str(c[1])) for c in chl_failures] ) ),
    
                    mrd.Section('Sucess Details',
                        [ SimulationMRedoc.build(r[1]) for r in chl_sucesses ]
                        ),
                )
    )
    
        
    res_doc.to_html("output")
    
    




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/test_all_out27.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out27.png>`


.. figure:: /srcs_generated_examples/images/test_all_out7.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out7.png>`


.. figure:: /srcs_generated_examples/images/test_all_out12.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out12.png>`


.. figure:: /srcs_generated_examples/images/test_all_out25.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out25.png>`


.. figure:: /srcs_generated_examples/images/test_all_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out1.png>`


.. figure:: /srcs_generated_examples/images/test_all_out11.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out11.png>`


.. figure:: /srcs_generated_examples/images/test_all_out2.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out2.png>`


.. figure:: /srcs_generated_examples/images/test_all_out23.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out23.png>`


.. figure:: /srcs_generated_examples/images/test_all_out13.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out13.png>`


.. figure:: /srcs_generated_examples/images/test_all_out18.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out18.png>`


.. figure:: /srcs_generated_examples/images/test_all_out32.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out32.png>`


.. figure:: /srcs_generated_examples/images/test_all_out5.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out5.png>`


.. figure:: /srcs_generated_examples/images/test_all_out29.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out29.png>`


.. figure:: /srcs_generated_examples/images/test_all_out19.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out19.png>`


.. figure:: /srcs_generated_examples/images/test_all_out28.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out28.png>`


.. figure:: /srcs_generated_examples/images/test_all_out34.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out34.png>`


.. figure:: /srcs_generated_examples/images/test_all_out15.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out15.png>`


.. figure:: /srcs_generated_examples/images/test_all_out22.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out22.png>`


.. figure:: /srcs_generated_examples/images/test_all_out6.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out6.png>`


.. figure:: /srcs_generated_examples/images/test_all_out8.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out8.png>`


.. figure:: /srcs_generated_examples/images/test_all_out21.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out21.png>`


.. figure:: /srcs_generated_examples/images/test_all_out26.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out26.png>`


.. figure:: /srcs_generated_examples/images/test_all_out17.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out17.png>`


.. figure:: /srcs_generated_examples/images/test_all_out14.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out14.png>`


.. figure:: /srcs_generated_examples/images/test_all_out3.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out3.png>`


.. figure:: /srcs_generated_examples/images/test_all_out10.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out10.png>`


.. figure:: /srcs_generated_examples/images/test_all_out4.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out4.png>`


.. figure:: /srcs_generated_examples/images/test_all_out20.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out20.png>`


.. figure:: /srcs_generated_examples/images/test_all_out33.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out33.png>`


.. figure:: /srcs_generated_examples/images/test_all_out16.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out16.png>`


.. figure:: /srcs_generated_examples/images/test_all_out24.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out24.png>`


.. figure:: /srcs_generated_examples/images/test_all_out31.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out31.png>`


.. figure:: /srcs_generated_examples/images/test_all_out30.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out30.png>`


.. figure:: /srcs_generated_examples/images/test_all_out9.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/test_all_out9.png>`






Output
~~~~~~

.. code-block:: bash

        No handlers could be found for logger "neurounits"
    2013-12-01 17:16:43,352 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:16:43,352 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
    No handlers could be found for logger "neurounits"
    2013-12-01 17:16:45,480 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:16:45,480 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/1d/1dcc5a5dad3e0e09f69e94cf869960a7.bundle (13k) : 0.858 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_af84455a7bd10be7408061ecd02b589b.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_fb18cab9ab8db5d2c968f5e6fba6a942.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_e1d9b15c15cf730d6ad5de223a1b3007.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_1829dde01cefc211170b0cbf30e1af68.hoc
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
    Running Simulation
    Time for Extracting Data: (15 records) 0.0683908462524
    Running simulation : 0.439 seconds
    Size of results file: 0.1 (MB)
    Post-processing : 0.011 seconds
    Entire load-run-save time : 1.308 seconds
    Suceeded
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    
    ConductanceDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3e82650>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e75610>}
    
    CurrentDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3e82650>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e75610>}
    
    StateVariable
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3e82650>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e75610>}
    
    StateSteadyState
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3e82650>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e75610>}
    
    StateTimeConstant
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3e82650>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e75610>}
    
    ConductanceDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3e82a10>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e75610>}
    
    CurrentDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3e82a10>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e75610>}
    
    StateVariable
    {'state': 'h', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3e82a10>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e75610>}
    
    StateSteadyState
    {'state': 'h', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3e82a10>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e75610>}
    
    StateTimeConstant
    {'state': 'h', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3e82a10>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e75610>}
    
    StateVariable
    {'state': 'm', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3e82a10>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e75610>}
    
    StateSteadyState
    {'state': 'm', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3e82a10>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e75610>}
    
    StateTimeConstant
    {'state': 'm', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3e82a10>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e75610>}
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/1d//1dcc5a5dad3e0e09f69e94cf869960a7.neuronsim.results.pickle ]
    
    ConductanceDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3ea1890>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulationNo handlers could be found for logger "neurounits"
    2013-12-01 17:16:48,148 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:16:48,148 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/f2/f28e84d7bdf90d340edc74d9b6adbc3f.bundle (11k) : 0.837 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-60.0) * mV, '_name': 'AnonObj0017', '_simulation': None, 'conductance': array(3333333.3333333335) * 1/(m**2*MOhm)}
    
    Executing: /home/michael/opt//x86_64/bin/modlunit /mnt/scratch/tmp/morphforge/tmp/tmp_25329468b83730b87edd25d03e300c52.mod
    /mnt/scratch/tmp/morphforge/tmp/modbuild_24423
    Executing: /home/michael/opt//x86_64/bin/nocmodl tmp_25329468b83730b87edd25d03e300c52.mod
    Executing: /home/michael/opt//share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/home/michael/opt//include/nrn"  -I"/home/michael/opt//x86_64/lib"    -g -O2 -c -o tmp_25329468b83730b87edd25d03e300c52.lo tmp_25329468b83730b87edd25d03e300c52.c  
    Executing: /home/michael/opt//share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_25329468b83730b87edd25d03e300c52.la  -rpath /home/michael/opt//x86_64/libs  tmp_25329468b83730b87edd25d03e300c52.lo  -L/home/michael/opt//x86_64/lib -L/home/michael/opt//x86_64/lib  /home/michael/opt//x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
    OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/home/michael/opt//include/nrn -I/home/michael/opt//x86_64/lib -g -O2 -c tmp_25329468b83730b87edd25d03e300c52.c  -fPIC -DPIC -o .libs/tmp_25329468b83730b87edd25d03e300c52.o
    
    OP2: libtool: link: gcc -shared  -fPIC -DPIC  .libs/tmp_25329468b83730b87edd25d03e300c52.o   -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -L/home/michael/opt//x86_64/lib /home/michael/opt/x86_64/lib/libnrniv.so /home/michael/opt/x86_64/lib/libnrnoc.so /home/michael/opt/x86_64/lib/liboc.so /home/michael/opt/x86_64/lib/libmemacs.so /home/michael/opt/x86_64/lib/libnrnmpi.so /home/michael/opt/x86_64/lib/libscopmath.so /home/michael/opt/x86_64/lib/libsparse13.so -lreadline -lncurses /home/michael/opt/x86_64/lib/libivoc.so /home/michael/opt/x86_64/lib/libneuron_gnu.so /home/michael/opt/x86_64/lib/libmeschach.so /home/michael/opt/x86_64/lib/libsundials.so -lm -ldl  -O2   -pthread -Wl,-soname -Wl,tmp_25329468b83730b87edd25d03e300c52.so.0 -o .libs/tmp_25329468b83730b87edd25d03e300c52.so.0.0.0
    libtool: link: (cd ".libs" && rm -f "tmp_25329468b83730b87edd25d03e300c52.so.0" && ln -s "tmp_25329468b83730b87edd25d03e300c52.so.0.0.0" "tmp_25329468b83730b87edd25d03e300c52.so.0")
    libtool: link: (cd ".libs" && rm -f "tmp_25329468b83730b87edd25d03e300c52.so" && ln -s "tmp_25329468b83730b87edd25d03e300c52.so.0.0.0" "tmp_25329468b83730b87edd25d03e300c52.so")
    libtool: link: ( cd ".libs" && rm -f "tmp_25329468b83730b87edd25d03e300c52.la" && ln -s "../tmp_25329468b83730b87edd25d03e300c52.la" "tmp_25329468b83730b87edd25d03e300c52.la" )
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_4e9dd4f0dc9f56bdefe76c76e93a2c6a.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_979e51e8134d9ad14b8ff4498af4abcc.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_d3b1448d7022bb684b2c2116bd9224d2.hoc
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
    Time for Extracting Data: (7 records) 0.0422308444977
    Running simulation : 1.408 seconds
    Size of results file: 0.0 (MB)
    Post-processing : 0.008 seconds
    Entire load-run-save time : 2.253 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-12-01 17:16:51,765 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:16:51,766 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/1b/1be9a751b4475e9d67b09aaabf62bfe2.bundle (11k) : 0.841 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-60.0) * mV, '_name': 'AnonObj0026', '_simulation': None, 'conductance': array(3333333.3333333335) * 1/(m**2*MOhm)}
    
    Executing: /home/michael/opt//x86_64/bin/modlunit /mnt/scratch/tmp/morphforge/tmp/tmp_5c99b837a5a669b6ab6cfc67dc4435fe.mod
    /mnt/scratch/tmp/morphforge/tmp/modbuild_24615
    Executing: /home/michael/opt//x86_64/bin/nocmodl tmp_5c99b837a5a669b6ab6cfc67dc4435fe.mod
    Executing: /home/michael/opt//share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/home/michael/opt//include/nrn"  -I"/home/michael/opt//x86_64/lib"    -g -O2 -c -o tmp_5c99b837a5a669b6ab6cfc67dc4435fe.lo tmp_5c99b837a5a669b6ab6cfc67dc4435fe.c  
    Executing: /home/michael/opt//share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_5c99b837a5a669b6ab6cfc67dc4435fe.la  -rpath /home/michael/opt//x86_64/libs  tmp_5c99b837a5a669b6ab6cfc67dc4435fe.lo  -L/home/michael/opt//x86_64/lib -L/home/michael/opt//x86_64/lib  /home/michael/opt//x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
    OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/home/michael/opt//include/nrn -I/home/michael/opt//x86_64/lib -g -O2 -c tmp_5c99b837a5a669b6ab6cfc67dc4435fe.c  -fPIC -DPIC -o .libs/tmp_5c99b837a5a669b6ab6cfc67dc4435fe.o
    
    OP2: libtool: link: gcc -shared  -fPIC -DPIC  .libs/tmp_5c99b837a5a669b6ab6cfc67dc4435fe.o   -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -L/home/michael/opt//x86_64/lib /home/michael/opt/x86_64/lib/libnrniv.so /home/michael/opt/x86_64/lib/libnrnoc.so /home/michael/opt/x86_64/lib/liboc.so /home/michael/opt/x86_64/lib/libmemacs.so /home/michael/opt/x86_64/lib/libnrnmpi.so /home/michael/opt/x86_64/lib/libscopmath.so /home/michael/opt/x86_64/lib/libsparse13.so -lreadline -lncurses /home/michael/opt/x86_64/lib/libivoc.so /home/michael/opt/x86_64/lib/libneuron_gnu.so /home/michael/opt/x86_64/lib/libmeschach.so /home/michael/opt/x86_64/lib/libsundials.so -lm -ldl  -O2   -pthread -Wl,-soname -Wl,tmp_5c99b837a5a669b6ab6cfc67dc4435fe.so.0 -o .libs/tmp_5c99b837a5a669b6ab6cfc67dc4435fe.so.0.0.0
    libtool: link: (cd ".libs" && rm -f "tmp_5c99b837a5a669b6ab6cfc67dc4435fe.so.0" && ln -s "tmp_5c99b837a5a669b6ab6cfc67dc4435fe.so.0.0.0" "tmp_5c99b837a5a669b6ab6cfc67dc4435fe.so.0")
    libtool: link: (cd ".libs" && rm -f "tmp_5c99b837a5a669b6ab6cfc67dc4435fe.so" && ln -s "tmp_5c99b837a5a669b6ab6cfc67dc4435fe.so.0.0.0" "tmp_5c99b837a5a669b6ab6cfc67dc4435fe.so")
    libtool: link: ( cd ".libs" && rm -f "tmp_5c99b837a5a669b6ab6cfc67dc4435fe.la" && ln -s "../tmp_5c99b837a5a669b6ab6cfc67dc4435fe.la" "tmp_5c99b837a5a669b6ab6cfc67dc4435fe.la" )
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_cd12d11035e38d254242c6910f7785bc.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_08fd042f5617092e986b5453289c786a.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_e702e4624ce0c27fea2c1e4559cad759.hoc
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
    Time for Extracting Data: (7 records) 0.0412681102753
    Running simulation : 1.390 seconds
    Size of results file: 0.0 (MB)
    Post-processing : 0.008 seconds
    Entire load-run-save time : 2.239 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-12-01 17:16:55,429 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:16:55,432 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/7c/7c8661f823e7aadcf24889768185d961.bundle (11k) : 0.851 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-60.0) * mV, '_name': 'AnonObj0035', '_simulation': None, 'conductance': array(3333333.3333333335) * 1/(m**2*MOhm)}
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_441d00ac1d6ed2d478a432634287e05e.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_7107658b8d4baf45336a305e26f255ba.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_a147f012f28f0445641356aa6f5b1aec.hoc
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
    Time for Extracting Data: (7 records) 0.044881105423
    Running simulation : 0.422 seconds
    Size of results file: 0.0 (MB)
    Post-processing : 0.007 seconds
    Entire load-run-save time : 1.280 seconds
    Suceeded
    .NEURONSimulation object at 0x3e82e90>}
    
    CurrentDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3ea1890>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e82e90>}
    
    StateVariable
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3ea1890>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e82e90>}
    
    StateSteadyState
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3ea1890>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e82e90>}
    
    StateTimeConstant
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3ea1890>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e82e90>}
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/f2//f28e84d7bdf90d340edc74d9b6adbc3f.neuronsim.results.pickle ]
    
    ConductanceDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3ea4350>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e93750>}
    
    CurrentDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3ea4350>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e93750>}
    
    StateVariable
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3ea4350>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e93750>}
    
    StateSteadyState
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3ea4350>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e93750>}
    
    StateTimeConstant
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3ea4350>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e93750>}
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/1b//1be9a751b4475e9d67b09aaabf62bfe2.neuronsim.results.pickle ]
    
    ConductanceDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3eabad0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e93a10>}
    
    CurrentDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3eabad0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e93a10>}
    
    StateVariable
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3eabad0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e93a10>}
    
    StateSteadyState
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3eabad0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e93a10>}
    
    StateTimeConstant
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3eabad0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3e93a10>}
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/7c//7c8661f823e7aadcf24889768185d961.neuronsim.results.pickle ]
    
    ConductanceDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3eaa690>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3ea1090>}
    
    CurrentDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3eaa690>, 'simulation': <morphforge.simulation.neuron.No handlers could be found for logger "neurounits"
    2013-12-01 17:16:58,075 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:16:58,076 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/77/77e67e129668cf89c79ef3b5968069d1.bundle (11k) : 0.844 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-60.0) * mV, '_name': 'AnonObj0044', '_simulation': None, 'conductance': array(3333333.3333333335) * 1/(m**2*MOhm)}
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_2cbb14555250240a4c2eef70e413328d.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_47e8f16ebc67f13d01a7bd84be614581.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_f4921d870a5b7ece263280e92902b868.hoc
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
    Time for Extracting Data: (7 records) 0.0479950904846
    Running simulation : 0.401 seconds
    Size of results file: 0.0 (MB)
    Post-processing : 0.011 seconds
    Entire load-run-save time : 1.257 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-12-01 17:17:00,666 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:17:00,666 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/68/68f164f8c0dc83015b4865988d4dae4b.bundle (11k) : 0.827 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-60.0) * mV, '_name': 'AnonObj0053', '_simulation': None, 'conductance': array(3333333.3333333335) * 1/(m**2*MOhm)}
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_9abe11266d08d5deb2ab5aadeb8cea7e.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_6bc9ad269f3ed985cfb414f29b21f378.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_3be76bf44b400c8c090808f32b04dd91.hoc
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
    Time for Extracting Data: (7 records) 0.0425209999084
    Running simulation : 0.401 seconds
    Size of results file: 0.0 (MB)
    Post-processing : 0.006 seconds
    Entire load-run-save time : 1.235 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-12-01 17:17:03,309 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:17:03,309 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/6d/6d3b4d00ad14e2a1eac65f20e9521424.bundle (11k) : 0.837 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-60.0) * mV, '_name': 'AnonObj0062', '_simulation': None, 'conductance': array(3333333.3333333335) * 1/(m**2*MOhm)}
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_31e396204ee472ac314748e4803b5734.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_aff211156e65946ed8b14e421c7fb4a8.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_bbd2916c2b4ca4532c81ba9b767972b0.hoc
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
    Time for Extracting Data: (7 records) 0.0443441867828
    Running simulation : 0.414 seconds
    Size of results file: 0.0 (MB)
    Post-processing : 0.006 seconds
    Entire load-run-save time : 1.258 seconds
    Suceeded
    core.neuronsimulation.NEURONSimulation object at 0x3ea1090>}
    
    StateVariable
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3eaa690>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3ea1090>}
    
    StateSteadyState
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3eaa690>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3ea1090>}
    
    StateTimeConstant
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3eaa690>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3ea1090>}
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/77//77e67e129668cf89c79ef3b5968069d1.neuronsim.results.pickle ]
    
    ConductanceDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3eabdd0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3eaae50>}
    
    CurrentDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3eabdd0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3eaae50>}
    
    StateVariable
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3eabdd0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3eaae50>}
    
    StateSteadyState
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3eabdd0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3eaae50>}
    
    StateTimeConstant
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3eabdd0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3eaae50>}
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/68//68f164f8c0dc83015b4865988d4dae4b.neuronsim.results.pickle ]
    
    ConductanceDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3eb5a10>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3eaad90>}
    
    CurrentDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3eb5a10>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3eaad90>}
    
    StateVariable
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3eb5a10>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3eaad90>}
    
    StateSteadyState
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3eb5a10>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3eaad90>}
    
    StateTimeConstant
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3eb5a10>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3eaad90>}
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/6d//6d3b4d00ad14e2a1eac65f20e9521424.neuronsim.results.pickle ]
    
    ConductanceDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3f815d0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3eb1e90>}
    
    CurrentDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3f815d0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3eb1e90>}
    
    StateVariable
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3f815d0>, 'simulatioNo handlers could be found for logger "neurounits"
    2013-12-01 17:17:06,004 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:17:06,004 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/c0/c0067c7d9890bb351f7bd2063051d8b7.bundle (11k) : 0.834 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-60.0) * mV, '_name': 'AnonObj0071', '_simulation': None, 'conductance': array(3333333.3333333335) * 1/(m**2*MOhm)}
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_cd12d11035e38d254242c6910f7785bc.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_08fd042f5617092e986b5453289c786a.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_35cf65138cd66e6f2ccc749ea801d70e.hoc
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
    Time for Extracting Data: (7 records) 0.043261051178
    Running simulation : 0.497 seconds
    Size of results file: 0.0 (MB)
    Post-processing : 0.007 seconds
    Entire load-run-save time : 1.339 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-12-01 17:17:08,704 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:17:08,705 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/e9/e94a733b8fcbbd0389c8cc6088d38d0e.bundle (11k) : 0.846 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-60.0) * mV, '_name': 'AnonObj0080', '_simulation': None, 'conductance': array(3333333.3333333335) * 1/(m**2*MOhm)}
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_441d00ac1d6ed2d478a432634287e05e.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_7107658b8d4baf45336a305e26f255ba.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_bde51d3416c8a3afe58d928afc79b167.hoc
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
    Time for Extracting Data: (7 records) 0.0426919460297
    Running simulation : 0.449 seconds
    Size of results file: 0.0 (MB)
    Post-processing : 0.006 seconds
    Entire load-run-save time : 1.302 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-12-01 17:17:11,396 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:17:11,397 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/4c/4ceb4df87e22949c98b9db108929f036.bundle (11k) : 0.837 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-60.0) * mV, '_name': 'AnonObj0089', '_simulation': None, 'conductance': array(3333333.3333333335) * 1/(m**2*MOhm)}
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_4f036a7286a89bad29d3716090cdae31.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_2983a0d8adc4fa11c6750daedebe0aee.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_bf5f8cd199683faa3e75b95dca32294e.hoc
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
    Time for Extracting Data: (7 records) 0.0429339408875
    Running simulation : 0.470 seconds
    Size of results file: 0.0 (MB)
    Post-processing : 0.006 seconds
    Entire load-run-save time : 1.314 seconds
    Suceeded
    n': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3eb1e90>}
    
    StateSteadyState
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3f815d0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3eb1e90>}
    
    StateTimeConstant
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3f815d0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3eb1e90>}
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/c0//c0067c7d9890bb351f7bd2063051d8b7.neuronsim.results.pickle ]
    
    ConductanceDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3f85dd0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3eb1890>}
    
    CurrentDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3f85dd0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3eb1890>}
    
    StateVariable
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3f85dd0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3eb1890>}
    
    StateSteadyState
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3f85dd0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3eb1890>}
    
    StateTimeConstant
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3f85dd0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3eb1890>}
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/e9//e94a733b8fcbbd0389c8cc6088d38d0e.neuronsim.results.pickle ]
    
    ConductanceDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3eae8d0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3f85e50>}
    
    CurrentDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3eae8d0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3f85e50>}
    
    StateVariable
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3eae8d0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3f85e50>}
    
    StateSteadyState
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3eae8d0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3f85e50>}
    
    StateTimeConstant
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3eae8d0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3f85e50>}
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/4c//4ceb4df87e22949c98b9db108929f036.neuronsim.results.pickle ]
    
    ConductanceDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3f8d210>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3f81b50>}
    
    CurrentDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3f8d210>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3f81b50>}
    
    StateVariable
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3f8d210>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3f81b50>}
    
    StateSteadyState
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocaNo handlers could be found for logger "neurounits"
    2013-12-01 17:17:14,044 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:17:14,044 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/a9/a97a27ad6542c30513caa83b2b8df96f.bundle (11k) : 0.835 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-60.0) * mV, '_name': 'AnonObj0098', '_simulation': None, 'conductance': array(3333333.3333333335) * 1/(m**2*MOhm)}
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_cd12d11035e38d254242c6910f7785bc.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_08fd042f5617092e986b5453289c786a.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_2595ea1e8890274d7de738302bc03c83.hoc
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
    Time for Extracting Data: (7 records) 0.0403339862823
    Running simulation : 0.442 seconds
    Size of results file: 0.0 (MB)
    Post-processing : 0.006 seconds
    Entire load-run-save time : 1.284 seconds
    Suceeded
    tion object at 0x3f8d210>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3f81b50>}
    
    StateTimeConstant
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x3f8d210>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x3f81b50>}
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/a9//a97a27ad6542c30513caa83b2b8df96f.neuronsim.results.pickle ]
    Error running: ('Single Compartment Passive', None)
    build_passive_cell() takes at least 2 arguments (1 given)
    Warning: node 'AnonObj0001', graph 'graphname' size too small for label
    
    [(397.88735772973837, array([ 1.,  0.,  0.])), (0.0, array([ 0.,  1.,  0.])), (0.0, array([ 0.,  0.,  1.]))]
    Saving figure /home/michael/.mredoc/build/figs/opfile0002
    Saving figure /home/michael/.mredoc/build/figs/opfile0003
    Saving figure /home/michael/.mredoc/build/figs/opfile0004
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig000_Autosave_figure_1.{png,svg}
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig001_Autosave_figure_2.{png,svg}
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig002_Autosave_figure_3.{png,svg}
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig003_Autosave_figure_4.{png,svg}
    Saving figure /home/michael/.mredoc/build/figs/opfile0005
    Warning: node 'AnonObj0018', graph 'graphname' size too small for label
    
    [(79.577471545947674, array([ 1.,  0.,  0.])), (0.0, array([ 0.,  1.,  0.])), (0.0, array([ 0.,  0.,  1.]))]
    Saving figure /home/michael/.mredoc/build/figs/opfile0007
    Saving figure /home/michael/.mredoc/build/figs/opfile0008
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig004_Autosave_figure_5.{png,svg}
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig005_Autosave_figure_6.{png,svg}
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig006_Autosave_figure_7.{png,svg}
    Saving figure /home/michael/.mredoc/build/figs/opfile0009
    Warning: node 'AnonObj0027', graph 'graphname' size too small for label
    
    [(79.577471545947674, array([ 1.,  0.,  0.])), (0.0, array([ 0.,  1.,  0.])), (0.0, array([ 0.,  0.,  1.]))]
    Saving figure /home/michael/.mredoc/build/figs/opfile0011
    Saving figure /home/michael/.mredoc/build/figs/opfile0012
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig007_Autosave_figure_8.{png,svg}
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig008_Autosave_figure_9.{png,svg}
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig009_Autosave_figure_10.{png,svg}
    Saving figure /home/michael/.mredoc/build/figs/opfile0013
    Warning: node 'AnonObj0036', graph 'graphname' size too small for label
    
    [(79.577471545947674, array([ 1.,  0.,  0.])), (0.0, array([ 0.,  1.,  0.])), (0.0, array([ 0.,  0.,  1.]))]
    Saving figure /home/michael/.mredoc/build/figs/opfile0015
    Saving figure /home/michael/.mredoc/build/figs/opfile0016
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig010_Autosave_figure_11.{png,svg}
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig011_Autosave_figure_12.{png,svg}
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig012_Autosave_figure_13.{png,svg}
    Saving figure /home/michael/.mredoc/build/figs/opfile0017
    Warning: node 'AnonObj0045', graph 'graphname' size too small for label
    
    [(79.577471545947674, array([ 1.,  0.,  0.])), (0.0, array([ 0.,  1.,  0.])), (0.0, array([ 0.,  0.,  1.]))]
    Saving figure /home/michael/.mredoc/build/figs/opfile0019
    Saving figure /home/michael/.mredoc/build/figs/opfile0020
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig013_Autosave_figure_14.{png,svg}
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig014_Autosave_figure_15.{png,svg}
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig015_Autosave_figure_16.{png,svg}
    Saving figure /home/michael/.mredoc/build/figs/opfile0021
    Warning: node 'AnonObj0054', graph 'graphname' size too small for label
    
    [(79.577471545947674, array([ 1.,  0.,  0.])), (0.0, array([ 0.,  1.,  0.])), (0.0, array([ 0.,  0.,  1.]))]
    S/usr/bin/convert
    aving figure /home/michael/.mredoc/build/figs/opfile0023
    Saving figure /home/michael/.mredoc/build/figs/opfile0024
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig016_Autosave_figure_17.{png,svg}
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig017_Autosave_figure_18.{png,svg}
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig018_Autosave_figure_19.{png,svg}
    Saving figure /home/michael/.mredoc/build/figs/opfile0025
    Warning: node 'AnonObj0063', graph 'graphname' size too small for label
    
    [(79.577471545947674, array([ 1.,  0.,  0.])), (0.0, array([ 0.,  1.,  0.])), (0.0, array([ 0.,  0.,  1.]))]
    Saving figure /home/michael/.mredoc/build/figs/opfile0027
    Saving figure /home/michael/.mredoc/build/figs/opfile0028
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig019_Autosave_figure_20.{png,svg}
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig020_Autosave_figure_21.{png,svg}
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig021_Autosave_figure_22.{png,svg}
    Saving figure /home/michael/.mredoc/build/figs/opfile0029
    Warning: node 'AnonObj0072', graph 'graphname' size too small for label
    
    [(79.577471545947674, array([ 1.,  0.,  0.])), (0.0, array([ 0.,  1.,  0.])), (0.0, array([ 0.,  0.,  1.]))]
    Saving figure /home/michael/.mredoc/build/figs/opfile0031
    Saving figure /home/michael/.mredoc/build/figs/opfile0032
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig022_Autosave_figure_23.{png,svg}
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig023_Autosave_figure_24.{png,svg}
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig024_Autosave_figure_25.{png,svg}
    Saving figure /home/michael/.mredoc/build/figs/opfile0033
    Warning: node 'AnonObj0081', graph 'graphname' size too small for label
    
    [(79.577471545947674, array([ 1.,  0.,  0.])), (0.0, array([ 0.,  1.,  0.])), (0.0, array([ 0.,  0.,  1.]))]
    Saving figure /home/michael/.mredoc/build/figs/opfile0035
    Saving figure /home/michael/.mredoc/build/figs/opfile0036
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig025_Autosave_figure_26.{png,svg}
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig026_Autosave_figure_27.{png,svg}
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig027_Autosave_figure_28.{png,svg}
    Saving figure /home/michael/.mredoc/build/figs/opfile0037
    Warning: node 'AnonObj0090', graph 'graphname' size too small for label
    
    [(79.577471545947674, array([ 1.,  0.,  0.])), (0.0, array([ 0.,  1.,  0.])), (0.0, array([ 0.,  0.,  1.]))]
    Saving figure /home/michael/.mredoc/build/figs/opfile0039
    Saving figure /home/michael/.mredoc/build/figs/opfile0040
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig028_Autosave_figure_29.{png,svg}
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig029_Autosave_figure_30.{png,svg}
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig030_Autosave_figure_31.{png,svg}
    Saving figure /home/michael/.mredoc/build/figs/opfile0041
    Warning: node 'AnonObj0099', graph 'graphname' size too small for label
    
    [(79.577471545947674, array([ 1.,  0.,  0.])), (0.0, array([ 0.,  1.,  0.])), (0.0, array([ 0.,  0.,  1.]))]
    Saving figure /home/michael/.mredoc/build/figs/opfile0043
    Saving figure /home/michael/.mredoc/build/figs/opfile0044
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig031_Autosave_figure_32.{png,svg}
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig032_Autosave_figure_33.{png,svg}
    PlotManger saving:  _output/figures/test_all/{png,svg}/fig033_Autosave_figure_34.{png,svg}
    Saving figure /home/michael/.mredoc/build/figs/opfile0045
    Sucessfully written HTML to:  output




