
.. _example_multicell_simulation010:

Example 18. 2 cells connected with an AMPA synapse
==================================================


2 cells connected with an AMPA synapse.

Timed input into a cell causes an action potential, which causes an EPSP in
another cell via an excitatry synapse.

Code
~~~~

.. code-block:: python

    
    
    
    
    from morphforgecontrib.stdimports import SynapticTriggerAtTimes
    from morphforgecontrib.stdimports import SynapticTriggerByVoltageThreshold
    
    
    from morphforgecontrib.simulation.synapse_templates.neurounit import *
    from morphforgecontrib.simulation.synapse_templates.exponential_form.expsyn.core import *
    from morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core import *
    from morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core import *
    
    
    from morphforge.stdimports import *
    #from morphforgecontrib.simulation.channels.simulatorbuiltin.sim_builtin_core import BuiltinChannel
    from morphforgecontrib.data_library.stdmodels import StandardModels
    
    
    def simulate_chls_on_neuron():
    
    
        # Create the environment:
        env = NEURONEnvironment()
        sim = env.Simulation()
    
        # Create a cell:
        cell1 = CellLibrary.create_cell(celltype=None, modelsrc=StandardModels.HH52, sim=sim)
        cell2 = CellLibrary.create_cell(celltype=None, modelsrc=StandardModels.HH52, sim=sim)
    
    
        exp2template = env.PostSynapticMechTemplate(
            PostSynapticMech_Exp2SynNMDA_Base,
            template_name='expsyn2tmpl',
            tau_open = 5 * units.ms, tau_close=20*units.ms, e_rev=0 * units.mV, popening=1.0, peak_conductance = qty("1:nS"),  vdep=False,
            )
    
    
    
        syn = sim.create_synapse(
                trigger = env.SynapticTrigger(
                                         SynapticTriggerAtTimes,
                                         time_list =   (100,105,110,112,115, 115,115) * units.ms ,
                                         ),
                postsynaptic_mech = exp2template.instantiate(cell_location = cell1.soma, ),
               )
    
        syn = sim.create_synapse(
                trigger = env.SynapticTrigger(
                                         SynapticTriggerByVoltageThreshold,
                                         cell_location=cell1.soma,
                                         voltage_threshold=qty("0:mV"),
                                         delay=qty('1:ms'),
                                         ),
                postsynaptic_mech = exp2template.instantiate(cell_location = cell2.soma, ),
               )
    
    
    
    
        # Define what to record:
        sim.record(what=StandardTags.Voltage, name="SomaVoltage1", cell_location = cell1.soma)
        sim.record(what=StandardTags.Voltage, name="SomaVoltage2", cell_location = cell2.soma)
    
    
        # run the simulation
        results = sim.run()
        return results
    
    
    results = simulate_chls_on_neuron()
    SimulationMRedoc.build( results ).to_pdf(__file__ + '.pdf')
    
    TagViewer(results, timerange=(95, 200)*units.ms, show=True)
    
    




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/multicell_simulation010_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/multicell_simulation010_out1.png>`


.. figure:: /srcs_generated_examples/images/multicell_simulation010_out2.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/multicell_simulation010_out2.png>`


.. figure:: /srcs_generated_examples/images/multicell_simulation010_out5.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/multicell_simulation010_out5.png>`


.. figure:: /srcs_generated_examples/images/multicell_simulation010_out6.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/multicell_simulation010_out6.png>`


.. figure:: /srcs_generated_examples/images/multicell_simulation010_out3.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/multicell_simulation010_out3.png>`


.. figure:: /srcs_generated_examples/images/multicell_simulation010_out4.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/multicell_simulation010_out4.png>`






Output
~~~~~~

.. code-block:: bash

        No handlers could be found for logger "neurounits"
    2013-12-01 17:13:49,540 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:13:49,541 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
    No handlers could be found for logger "neurounits"
    2013-12-01 17:13:51,753 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:13:51,754 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/de/de5b931255c0cccab3fb89ed3dff0c7e.bundle (17k) : 0.857 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    Executing: /home/michael/opt//x86_64/bin/modlunit /mnt/scratch/tmp/morphforge/tmp/tmp_02e8edf95aed821ddbf229dca157da35.mod
    /mnt/scratch/tmp/morphforge/tmp/modbuild_22303
    Executing: /home/michael/opt//x86_64/bin/nocmodl tmp_02e8edf95aed821ddbf229dca157da35.mod
    Executing: /home/michael/opt//share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/home/michael/opt//include/nrn"  -I"/home/michael/opt//x86_64/lib"    -g -O2 -c -o tmp_02e8edf95aed821ddbf229dca157da35.lo tmp_02e8edf95aed821ddbf229dca157da35.c  
    Executing: /home/michael/opt//share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_02e8edf95aed821ddbf229dca157da35.la  -rpath /home/michael/opt//x86_64/libs  tmp_02e8edf95aed821ddbf229dca157da35.lo  -L/home/michael/opt//x86_64/lib -L/home/michael/opt//x86_64/lib  /home/michael/opt//x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
    OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/home/michael/opt//include/nrn -I/home/michael/opt//x86_64/lib -g -O2 -c tmp_02e8edf95aed821ddbf229dca157da35.c  -fPIC -DPIC -o .libs/tmp_02e8edf95aed821ddbf229dca157da35.o
    
    OP2: libtool: link: gcc -shared  -fPIC -DPIC  .libs/tmp_02e8edf95aed821ddbf229dca157da35.o   -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -L/home/michael/opt//x86_64/lib /home/michael/opt/x86_64/lib/libnrniv.so /home/michael/opt/x86_64/lib/libnrnoc.so /home/michael/opt/x86_64/lib/liboc.so /home/michael/opt/x86_64/lib/libmemacs.so /home/michael/opt/x86_64/lib/libnrnmpi.so /home/michael/opt/x86_64/lib/libscopmath.so /home/michael/opt/x86_64/lib/libsparse13.so -lreadline -lncurses /home/michael/opt/x86_64/lib/libivoc.so /home/michael/opt/x86_64/lib/libneuron_gnu.so /home/michael/opt/x86_64/lib/libmeschach.so /home/michael/opt/x86_64/lib/libsundials.so -lm -ldl  -O2   -pthread -Wl,-soname -Wl,tmp_02e8edf95aed821ddbf229dca157da35.so.0 -o .libs/tmp_02e8edf95aed821ddbf229dca157da35.so.0.0.0
    libtool: link: (cd ".libs" && rm -f "tmp_02e8edf95aed821ddbf229dca157da35.so.0" && ln -s "tmp_02e8edf95aed821ddbf229dca157da35.so.0.0.0" "tmp_02e8edf95aed821ddbf229dca157da35.so.0")
    libtool: link: (cd ".libs" && rm -f "tmp_02e8edf95aed821ddbf229dca157da35.so" && ln -s "tmp_02e8edf95aed821ddbf229dca157da35.so.0.0.0" "tmp_02e8edf95aed821ddbf229dca157da35.so")
    libtool: link: ( cd ".libs" && rm -f "tmp_02e8edf95aed821ddbf229dca157da35.la" && ln -s "../tmp_02e8edf95aed821ddbf229dca157da35.la" "tmp_02e8edf95aed821ddbf229dca157da35.la" )
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_e1d9b15c15cf730d6ad5de223a1b3007.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_4a46a0f70872d4114e6b6a454639c210.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_0ac427c36425efb444e1407927e6186e.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_fe29ca000b1bf9f98f8a5a86da5768f4.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_b49c7a5b742595377840c8e946528676.hoc
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
    Time for Extracting Data: (2 records) 0.00368809700012
    Running simulation : 1.654 seconds
    Size of results file: 0.0 (MB)
    Post-processing : 0.011 seconds
    Entire load-run-save time : 2.523 seconds
    Suceeded
    /usr/bin/pdflatex
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/de//de5b931255c0cccab3fb89ed3dff0c7e.neuronsim.results.pickle ]
    Warning: node 'AnonObj0001', graph 'graphname' size too small for label
    Warning: node 'AnonObj0002', graph 'graphname' size too small for label
    
    [(397.88735772973837, array([ 1.,  0.,  0.])), (0.0, array([ 0.,  1.,  0.])), (0.0, array([ 0.,  0.,  1.]))]
    Saving figure /home/michael/.mredoc/build/figs/opfile0002
    [(397.88735772973837, array([ 1.,  0.,  0.])), (0.0, array([ 0.,  1.,  0.])), (0.0, array([ 0.,  0.,  1.]))]
    Saving figure /home/michael/.mredoc/build/figs/opfile0003
    Saving figure /home/michael/.mredoc/build/figs/opfile0004
    Saving figure /home/michael/.mredoc/build/figs/opfile0005
    True
    True
    PlotManger saving:  _output/figures/multicell_simulation010/{png,svg}/fig000_Autosave_figure_1.{png,svg}
    PlotManger saving:  _output/figures/multicell_simulation010/{png,svg}/fig001_Autosave_figure_2.{png,svg}
    PlotManger saving:  _output/figures/multicell_simulation010/{png,svg}/fig002_Autosave_figure_3.{png,svg}
    PlotManger saving:  _output/figures/multicell_simulation010/{png,svg}/fig003_Autosave_figure_4.{png,svg}
    PlotManger saving:  _output/figures/multicell_simulation010/{png,svg}/fig004_Autosave_figure_5.{png,svg}
    Saving figure /home/michael/.mredoc/build/figs/opfile0006
    Remove paragraph? (no)
    Tex File: /home/michael/.mredoc/build/pdflatex/eqnset.tex
    Successfully written PDF to:  /mnt/scratch/tmp/morphforge/tmp/mf_doc_build/multicell_simulation010.py.pdf
    PlotManger saving:  _output/figures/multicell_simulation010/{png,svg}/fig005_Autosave_figure_6.{png,svg}




