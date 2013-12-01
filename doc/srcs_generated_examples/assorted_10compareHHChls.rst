
.. _example_assorted_10compareHHChls:

Example 21. Comparing simulations: the Hodgkin-Huxley '52 channels
==================================================================


Comparing simulations: the Hodgkin-Huxley '52 channels

This simulation compares the different ways of implementing the Hodgkin-Huxley channels;
we check that the Hodgkin-Huxley channels built-in to NEURON produce the same results as
when we create these channels with parameters as an StdChlAlphaBeta.

In you are not familiar with python, then this is an example of the one of
the advantages of the laanguage: functions are objects!

In "test_neuron", we create a neuron morphology, but put the code to add the channels
in a different function. This makes it easy to try out different channel types and
distributions easily and quickly.

Code
~~~~

.. code-block:: python

    
    
    
    
    
    
    
    from morphforgecontrib.simulation.channels.neuroml_via_neurounits.neuroml_via_neurounits_core import NeuroML_Via_NeuroUnits_Channel
    from morphforgecontrib.simulation.channels.neurounits.neuro_units_bridge import Neuron_NeuroUnitEqnsetMechanism
    
    from morphforge.stdimports import *
    from morphforgecontrib.simulation.channels.hh_style.core.mmleak import StdChlLeak
    from morphforgecontrib.simulation.channels.hh_style.core.mmalphabeta import StdChlAlphaBeta
    from morphforgecontrib.simulation.channels.simulatorbuiltin.sim_builtin_core import BuiltinChannel
    from morphforgecontrib.simulation.channels.neuroml_via_xsl.neuroml_via_xsl_core import NeuroML_Via_XSL_Channel
    
    import random as R
    
    
    variables = ['h', 'm', 'minf', 'mtau', 'm_alpha_rate', 'm_beta_rate']
    
    def apply_hh_chls_neurounits_direct(env, cell, sim):
    
        eqnset_txt_na = """
        define_component chlstd_hh_na {
            from std.math import exp
            i = g * (v-erev) * m**3*h
            minf = m_alpha_rate / (m_alpha_rate + m_beta_rate)
            mtau = 1.0 / (m_alpha_rate + m_beta_rate)
            m' = (minf-m) / mtau
            hinf = h_alpha_rate / (h_alpha_rate + h_beta_rate)
            htau = 1.0 / (h_alpha_rate + h_beta_rate)
            h' = (hinf-h) / htau
            StdFormAB(V, a1, a2, a3, a4, a5) = (a1 + a2*V)/(a3+exp((V+a4)/a5))
            m_alpha_rate = StdFormAB(V=v, a1=m_a1, a2=m_a2, a3=m_a3, a4=m_a4, a5=m_a5)
            m_beta_rate =  StdFormAB(V=v, a1=m_b1, a2=m_b2, a3=m_b3, a4=m_b4, a5=m_b5)
            h_alpha_rate = StdFormAB(V=v, a1=h_a1, a2=h_a2, a3=h_a3, a4=h_a4, a5=h_a5)
            h_beta_rate =  StdFormAB(V=v, a1=h_b1, a2=h_b2, a3=h_b3, a4=h_b4, a5=h_b5)
            m_a1 = {-4.00 ms-1}
            m_a2 = {-0.10 mV-1 ms-1}
            m_a3 = -1.00
            m_a4 = {40.00 mV}
            m_a5 = {-10.00 mV}
            m_b1 = {4.00 ms-1}
            m_b2 = {0.00 mV-1 ms-1}
            m_b3 = {0.00}
            m_b4 = {65.00 mV}
            m_b5 = {18.00 mV}
            h_a1 = {0.07 ms-1}
            h_a2 = {0.00 mV-1 ms-1}
            h_a3 = {0.00}
            h_a4 = {65.00 mV}
            h_a5 = {20.00 mV}
            h_b1 = {1.00  ms-1}
            h_b2 = {0.00  mV-1 ms-1}
            h_b3 = {1.00}
            h_b4 = {35.00  mV}
            h_b5 = {-10.00 mV}
            sg = {120.0mS/cm2}
            erev = {50.0mV}
            <=> PARAMETER g:(S/m2)
            <=> OUTPUT    i:(A/m2)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }
            <=> INPUT     v: V           METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
        }
        """
    
        eqnset_txt_k = """
        define_component chlstd_hh_k {
            from std.math import exp
            i = g * (v-erev) * n*n*n*n
            ninf = n_alpha_rate / (n_alpha_rate + n_beta_rate)
            ntau = 1.0 / (n_alpha_rate + n_beta_rate)
            n' = (ninf-n) / ntau
            StdFormAB(V, a1, a2, a3, a4, a5) = (a1 + a2*V)/(a3+exp((V+a4)/a5))
            n_alpha_rate = StdFormAB(V=v, a1=n_a1, a2=n_a2, a3=n_a3, a4=n_a4, a5=n_a5)
            n_beta_rate =  StdFormAB(V=v, a1=n_b1, a2=n_b2, a3=n_b3, a4=n_b4, a5=n_b5)
    
            n_a1 = {-0.55 ms-1}
            n_a2 = {-0.01 mV-1 ms-1}
            n_a3 = -1.00
            n_a4 = {55.00 mV}
            n_a5 = {-10.00 mV}
            n_b1 = {0.125 ms-1}
            n_b2 = {0.00 mV-1 ms-1}
            n_b3 = {0.00}
            n_b4 = {65.00 mV}
            n_b5 = {80.00 mV}
    
            g = {36.0mS/cm2}
            erev = {-77.0mV}
            <=> OUTPUT    i:(A/m2)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }
            <=> INPUT     v: V          METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
        }
        """
    
        eqnset_txt_lk = """
            define_component chlstd_hh_lk {
                i = g * (v-erev)
                g = {0.3 mS/cm2}
                erev = -54.3 mV
                <=> OUTPUT    i:(A/m2)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }
                <=> INPUT     v: V          METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
                }
        """
    
    
        na_chl = Neuron_NeuroUnitEqnsetMechanism(name="Chl1", eqnset=eqnset_txt_na, default_parameters={"g":qty("120:mS/cm2")}, )
        lk_chl = Neuron_NeuroUnitEqnsetMechanism(name="Chl2", eqnset=eqnset_txt_lk, )
        k_chl  = Neuron_NeuroUnitEqnsetMechanism(name="Chl3", eqnset=eqnset_txt_k,  )
    
    
        cell.apply_channel( na_chl)
        cell.apply_channel( lk_chl)
        cell.apply_channel( k_chl)
    
    
        sim.record(na_chl, what='m', cell_location= cell.soma, user_tags=[StandardTags.StateVariable])
        sim.record(na_chl, what='mtau', cell_location= cell.soma, user_tags=[StandardTags.StateTimeConstant])
    
        sim.record(na_chl, what='h', cell_location= cell.soma, user_tags=[StandardTags.StateVariable])
        sim.record(na_chl, what='htau', cell_location= cell.soma, user_tags=[StandardTags.StateTimeConstant])
    
        sim.record(k_chl, what='n', cell_location= cell.soma, user_tags=[StandardTags.StateVariable])
        sim.record(k_chl, what='ntau', cell_location= cell.soma, user_tags=[StandardTags.StateTimeConstant])
    
    
    
    
    def apply_hh_chls_neuroml_xsl(env, cell, sim):
    
    
    
        lk_chl = env.Channel(
            StdChlLeak,
            name="LkChl",
            conductance=qty("0.3:mS/cm2"),
            reversalpotential=qty("-54.3:mV"),
              )
    
        na_chl = env.Channel(NeuroML_Via_XSL_Channel,
            xml_filename = os.path.join(LocMgr.get_test_srcs_path(), "neuroml/channelml/NaChannel_HH.xml"),
            xsl_filename = os.path.join(LocMgr.get_test_srcs_path(), "neuroml/channelml/ChannelML_v1.8.1_NEURONmod.xsl"),
    
           )
    
        k_chl = env.Channel(NeuroML_Via_XSL_Channel,
            xml_filename = os.path.join(LocMgr.get_test_srcs_path(), "neuroml/channelml/KChannel_HH.xml"),
            xsl_filename = os.path.join(LocMgr.get_test_srcs_path(), "neuroml/channelml/ChannelML_v1.8.1_NEURONmod.xsl"),
           )
    
        cell.apply_channel( na_chl)
        cell.apply_channel( lk_chl)
        cell.apply_channel( k_chl)
    
    
    
    
    
    
    
    
    def apply_hh_chls_neuroml_neurounits(env, cell, sim):
    
    
    
        lk_chl = env.Channel(
                             StdChlLeak,
                             name="LkChl",
                             conductance=qty("0.3:mS/cm2"),
                             reversalpotential=qty("-54.3:mV"),
                               )
    
        na_chl = env.Channel(NeuroML_Via_NeuroUnits_Channel,
                                                xml_filename = os.path.join(LocMgr.get_test_srcs_path(), "neuroml/channelml/NaChannel_HH.xml"),
    
                                               )
    
        k_chl = env.Channel(NeuroML_Via_XSL_Channel,
            xml_filename = os.path.join(LocMgr.get_test_srcs_path(), "neuroml/channelml/KChannel_HH.xml"),
            xsl_filename = os.path.join(LocMgr.get_test_srcs_path(), "neuroml/channelml/ChannelML_v1.8.1_NEURONmod.xsl"),
                                               )
    
        cell.apply_channel( na_chl)
        cell.apply_channel( lk_chl)
        cell.apply_channel( k_chl)
    
    
    
    def apply_hh_chls_morphforge_format(env, cell, sim):
    
        lk_chl = env.Channel(
                                 StdChlLeak,
                                 name="LkChl",
                                 conductance=qty("0.3:mS/cm2"),
                                 reversalpotential=qty("-54.3:mV"),
                               )
    
        na_state_vars = { "m": {
                              "alpha":[-4.00, -0.10, -1.00, 40.00, -10.00],
                              "beta": [4.00, 0.00, 0.00, 65.00, 18.00]},
                        "h": {
                                "alpha":[0.07, 0.00, 0.00, 65.00, 20.00] ,
                                "beta": [1.00, 0.00, 1.00, 35.00, -10.00]}
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
                              "alpha":[-0.55, -0.01, -1.0, 55.0, -10.0],
                              "beta": [0.125, 0, 0, 65, 80]},
                           }
    
        k_chl = env.Channel(
                                StdChlAlphaBeta,
                                name="KChl", ion="k",
                                equation="n*n*n*n",
                                conductance=qty("36:mS/cm2"),
                                reversalpotential=qty("-77:mV"),
                                statevars=k_state_vars,
    
                               )
    
        cell.apply_channel( lk_chl)
        cell.apply_channel( na_chl)
        cell.apply_channel( k_chl)
    
    
    
    
    def apply_hh_chls_NEURON_builtin(env, cell, sim):
    
        hhChls = env.Channel(BuiltinChannel,  sim_chl_name="hh", )
        cell.apply_channel( hhChls)
    
    
    
    
    
    
    def simulate_chls_on_neuron(chl_applicator_functor):
        # Create the environment:
        env = NEURONEnvironment()
    
        # Create the simulation:
        sim = env.Simulation()
    
        # Create a cell:
        morphDict1 = {'root': {'length': 18.8, 'diam': 18.8, 'id':'soma'} }
        m1 = MorphologyTree.fromDictionary(morphDict1)
        cell = sim.create_cell(name="Cell1", morphology=m1)
    
        # Setup the HH-channels on the cell:
        chl_applicator_functor(env, cell, sim)
    
        # Setup passive channels:
        cell.set_passive( PassiveProperty.SpecificCapacitance, qty('1.0:uF/cm2'))
    
    
    
        # Create the stimulus and record the injected current:
        cc = sim.create_currentclamp(name="Stim1", amp=qty("100:pA"), dur=qty("100:ms"), delay=qty("100:ms") * R.uniform(0.95, 1.0), cell_location=cell.soma)
    
    
        # Define what to record:
        sim.record(cell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = cell.soma)
    
    
        # run the simulation
        results = sim.run()
        return results
    
    
    
    
    
    resultsA =None
    resultsB =None
    resultsC =None
    resultsD =None
    resultsE =None
    
    
    resultsA = simulate_chls_on_neuron(apply_hh_chls_morphforge_format)
    resultsB = simulate_chls_on_neuron(apply_hh_chls_NEURON_builtin)
    resultsC = simulate_chls_on_neuron(apply_hh_chls_neuroml_neurounits)
    resultsD = simulate_chls_on_neuron(apply_hh_chls_neuroml_xsl)
    resultsE = simulate_chls_on_neuron(apply_hh_chls_neurounits_direct)
    #
    trs = [resultsA, resultsB, resultsC, resultsD, resultsE]
    trs = [tr for tr in trs if tr is not None]
    TagViewer(trs, timerange=(95, 200)*units.ms, show=True)
    
    
    pylab.show()
    




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/assorted_10compareHHChls_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/assorted_10compareHHChls_out1.png>`






Output
~~~~~~

.. code-block:: bash

        No handlers could be found for logger "neurounits"
    2013-12-01 17:15:42,771 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:15:42,772 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
    No handlers could be found for logger "neurounits"
    2013-12-01 17:15:44,958 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:15:44,959 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/24/24bbdee3e0bb7fbe00cca5b220278f75.bundle (11k) : 0.832 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_af84455a7bd10be7408061ecd02b589b.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_fb18cab9ab8db5d2c968f5e6fba6a942.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_e1d9b15c15cf730d6ad5de223a1b3007.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_a60cccd31e5b3353f7d1bc7b22a8ecc6.hoc
    	1 
    	1 
    	0.01 
    	0 
    	1 
    	50000 
    	1 
    Running Simulation
    Time for Extracting Data: (1 records) 0.0017671585083
    Running simulation : 0.463 seconds
    Size of results file: 0.1 (MB)
    Post-processing : 0.007 seconds
    Entire load-run-save time : 1.303 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/31/31ef01e2512928ee7dbd4dac5084817f.bundle (9k) : 0.870 seconds
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_b55da11a3034a715142adfe4f135acec.hoc
    	1 
    	1 
    	0.01 
    	0 
    	1 
    	50000 
    	1 
    Running Simulation
    Time for Extracting Data: (1 records) 0.00233507156372
    Running simulation : 0.277 seconds
    Size of results file: 0.1 (MB)
    Post-processing : 0.008 seconds
    Entire load-run-save time : 1.155 seconds
    Suceeded
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/24//24bbdee3e0bb7fbe00cca5b220278f75.neuronsim.results.pickle ]
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/31//31ef01e2512928ee7dbd4dac5084817f.neuronsim.results.pickle ]
    Loading Channel Type: NaChannel
    [('m', 'm_inf'), ('h', 'h_inf')]
    CHECKING
    <Parameter [id:83571664] Symbol: 'GMAX' >
    GMAX
    iii 1.0 s**3*A**2/(kg*m**4) <class 'quantities.quantity.Quantity'>
    iiii 1200.0 s**3*A**2/(kg*m**4) <class 'quantities.quantity.Quantity'>
    OK
    
    CHECKING
    <Parameter [id:83572688] Symbol: 'VREV' >
    VREV
    iii 1.0 kg*m**2/(s**3*A) <class 'quantities.quantity.Quantity'>
    iiii 0.05 kg*m**2/(s**3*A) <class 'quantities.quantity.Quantity'>
    OK
    
    Output <StateVariable [id:83563088] Symbol: 'h' >
    None
    Output <StateVariable [id:83564240] Symbol: 'm' >
    None
    Output <AssignedVariable [id:83566480] Symbol: 'GATEPROP' >
    None
    Output <AssignedVariable [id:83565392] Symbol: 'I' >
    {u'mf': {u'role': u'TRANSMEMBRANECURRENT'}}
    Output <AssignedVariable [id:83565200] Symbol: 'g' >
    None
    Output <AssignedVariable [id:83551504] Symbol: 'h_alpha' >
    None
    Output <AssignedVariable [id:83570832] Symbol: 'h_beta' >
    None
    Output <AssignedVariable [id:83565776] Symbol: 'h_inf' >
    None
    Output <AssignedVariable [id:83565008] Symbol: 'h_tau' >
    None
    Output <AssignedVariable [id:83564624] Symbol: 'm_alpha' >
    None
    Output <AssignedVariable [id:83566160] Symbol: 'm_beta' >
    None
    Output <AssignedVariable [id:83564816] Symbol: 'm_inf' >
    None
    Output <AssignedVariable [id:83565968] Symbol: 'm_tau' >
    None
    input <SuppliedValue [id:83573904] Symbol: 'V' >
    {u'mf': {u'role': u'MEMBRANEVOLTAGE'}}
    m_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_beta <class 'neurounits.ast.astobjects.AssignedVariable'>
    m <class 'neurounits.ast.astobjects.StateVariable'>
    m <class 'neurounits.ast.astobjects.StateVariable'>
    m <class 'neurounits.ast.astobjects.StateVariable'>
    h <class 'neurounits.ast.astobjects.StateVariable'>
    GMAX <class 'neurounits.ast.astobjects.Parameter'>
    GATEPROP <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_beta <class 'neurounits.ast.astobjects.AssignedVariable'>
    T [<class 'neurounits.ast.astobjects.DivOp'>]
    V <class 'neurounits.ast.astobjects.SuppliedValue'>
    V <class 'neurounits.ast.astobjects.SuppliedValue'>
    T [<class 'neurounits.ast.astobjects.MulOp'>]
    V <class 'neurounits.ast.astobjects.SuppliedValue'>
    T [<class 'neurounits.ast.astobjects.DivOp'>]
    V <class 'neurounits.ast.astobjects.SuppliedValue'>
    T [<class 'neurounits.ast.astobjects.DivOp'>]
    V <class 'neurounits.ast.astobjects.SuppliedValue'>
    m_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_beta <class 'neurounits.ast.astobjects.AssignedVariable'>
    g <class 'neurounits.ast.astobjects.AssignedVariable'>
    V <class 'neurounits.ast.astobjects.SuppliedValue'>
    VREV <class 'neurounits.ast.astobjects.Parameter'>
    h_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_beta <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:83566288] Symbol: m_beta >
    T [<class 'neurounits.ast.astobjects.DivOp'>]
    V <class 'neurNo handlers could be found for logger "neurounits"
    2013-12-01 17:15:51,025 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:15:51,025 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/9f/9fb2f6f970d82de3f4ffd52f1994ca45.bundle (82k) : 1.053 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    Executing: /home/michael/opt//x86_64/bin/modlunit /mnt/scratch/tmp/morphforge/tmp/tmp_48cf10999f12f2749f4d65f33d3f5882.mod
    /mnt/scratch/tmp/morphforge/tmp/modbuild_23368
    Executing: /home/michael/opt//x86_64/bin/nocmodl tmp_48cf10999f12f2749f4d65f33d3f5882.mod
    Executing: /home/michael/opt//share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/home/michael/opt//include/nrn"  -I"/home/michael/opt//x86_64/lib"    -g -O2 -c -o tmp_48cf10999f12f2749f4d65f33d3f5882.lo tmp_48cf10999f12f2749f4d65f33d3f5882.c  
    Executing: /home/michael/opt//share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_48cf10999f12f2749f4d65f33d3f5882.la  -rpath /home/michael/opt//x86_64/libs  tmp_48cf10999f12f2749f4d65f33d3f5882.lo  -L/home/michael/opt//x86_64/lib -L/home/michael/opt//x86_64/lib  /home/michael/opt//x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
    OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/home/michael/opt//include/nrn -I/home/michael/opt//x86_64/lib -g -O2 -c tmp_48cf10999f12f2749f4d65f33d3f5882.c  -fPIC -DPIC -o .libs/tmp_48cf10999f12f2749f4d65f33d3f5882.o
    
    OP2: libtool: link: gcc -shared  -fPIC -DPIC  .libs/tmp_48cf10999f12f2749f4d65f33d3f5882.o   -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -L/home/michael/opt//x86_64/lib /home/michael/opt/x86_64/lib/libnrniv.so /home/michael/opt/x86_64/lib/libnrnoc.so /home/michael/opt/x86_64/lib/liboc.so /home/michael/opt/x86_64/lib/libmemacs.so /home/michael/opt/x86_64/lib/libnrnmpi.so /home/michael/opt/x86_64/lib/libscopmath.so /home/michael/opt/x86_64/lib/libsparse13.so -lreadline -lncurses /home/michael/opt/x86_64/lib/libivoc.so /home/michael/opt/x86_64/lib/libneuron_gnu.so /home/michael/opt/x86_64/lib/libmeschach.so /home/michael/opt/x86_64/lib/libsundials.so -lm -ldl  -O2   -pthread -Wl,-soname -Wl,tmp_48cf10999f12f2749f4d65f33d3f5882.so.0 -o .libs/tmp_48cf10999f12f2749f4d65f33d3f5882.so.0.0.0
    libtool: link: (cd ".libs" && rm -f "tmp_48cf10999f12f2749f4d65f33d3f5882.so.0" && ln -s "tmp_48cf10999f12f2749f4d65f33d3f5882.so.0.0.0" "tmp_48cf10999f12f2749f4d65f33d3f5882.so.0")
    libtool: link: (cd ".libs" && rm -f "tmp_48cf10999f12f2749f4d65f33d3f5882.so" && ln -s "tmp_48cf10999f12f2749f4d65f33d3f5882.so.0.0.0" "tmp_48cf10999f12f2749f4d65f33d3f5882.so")
    libtool: link: ( cd ".libs" && rm -f "tmp_48cf10999f12f2749f4d65f33d3f5882.la" && ln -s "../tmp_48cf10999f12f2749f4d65f33d3f5882.la" "tmp_48cf10999f12f2749f4d65f33d3f5882.la" )
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_1b9db84d43b77ec2fb2e53e206df6e31.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_595fd1e1e00ca2d9deba3e407f51424f.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_f0d9052fdfd19f720a7dd9bd9e578ef4.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_fadcccbfdf6c8eef1cde95e3ec5a28d2.hoc
    	1 
    	1 
    	0.01 
    	0 
    	1 
    	50000 
    	1 
    Running Simulation
    Time for Extracting Data: (1 records) 0.00188708305359
    Running simulation : 1.497 seconds
    Size of results file: 0.1 (MB)
    Post-processing : 0.027 seconds
    Entire load-run-save time : 2.577 seconds
    Suceeded
    No handlers could be found for logger "neurounits"
    2013-12-01 17:15:55,067 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:15:55,067 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/2a/2a9e13bbc911cf36dff438ab7625f7b4.bundle (20k) : 1.041 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_a290c9a645340023c23922c59afedba8.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_493e4afc99901274d3bc57b05062327c.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_f0d9052fdfd19f720a7dd9bd9e578ef4.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_00eb70358a20f499fd897c2d662fb660.hoc
    	1 
    	1 
    	0.01 
    	0 
    	1 
    	50000 
    	1 
    Running Simulation
    Time for Extracting Data: (1 records) 0.00178408622742
    Running simulation : 0.322 seconds
    Size of results file: 0.1 (MB)
    Post-processing : 0.008 seconds
    Entire load-run-save time : 1.372 seconds
    Suceeded
    ounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:83564752] Symbol: m_alpha >
    V <class 'neurounits.ast.astobjects.SuppliedValue'>
    T [<class 'neurounits.ast.astobjects.MulOp'>]
    V <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:83566096] Symbol: m_tau >
    m_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_beta <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:83564944] Symbol: m_inf >
    m_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_beta <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:83570960] Symbol: h_beta >
    T [<class 'neurounits.ast.astobjects.DivOp'>]
    V <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:83566416] Symbol: h_alpha >
    T [<class 'neurounits.ast.astobjects.DivOp'>]
    V <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:83565904] Symbol: h_inf >
    h_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_beta <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:83570768] Symbol: GATEPROP >
    m <class 'neurounits.ast.astobjects.StateVariable'>
    m <class 'neurounits.ast.astobjects.StateVariable'>
    m <class 'neurounits.ast.astobjects.StateVariable'>
    h <class 'neurounits.ast.astobjects.StateVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:83565328] Symbol: g >
    GMAX <class 'neurounits.ast.astobjects.Parameter'>
    GATEPROP <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:83565520] Symbol: I >
    g <class 'neurounits.ast.astobjects.AssignedVariable'>
    V <class 'neurounits.ast.astobjects.SuppliedValue'>
    VREV <class 'neurounits.ast.astobjects.Parameter'>
    Writing assignment for:  <EqnAssignmentByRegime [id:83565136] Symbol: h_tau >
    h_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_beta <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_inf <class 'neurounits.ast.astobjects.AssignedVariable'>
    m <class 'neurounits.ast.astobjects.StateVariable'>
    m_tau <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_inf <class 'neurounits.ast.astobjects.AssignedVariable'>
    h <class 'neurounits.ast.astobjects.StateVariable'>
    h_tau <class 'neurounits.ast.astobjects.AssignedVariable'>
    Loading Channel Type: KConductance
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/9f//9fb2f6f970d82de3f4ffd52f1994ca45.neuronsim.results.pickle ]
    Loading Channel Type: NaChannel
    Loading Channel Type: KConductance
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/2a//2a9e13bbc911cf36dff438ab7625f7b4.neuronsim.results.pickle ]
    CHECKING
    <Parameter [id:87654096] Symbol: 'g' >
    g
    iii 1.0 s**3*A**2/(kg*m**4) <class 'quantities.quantity.Quantity'>
    iiii 1200.0 s**3*A**2/(kg*m**4) <class 'quantities.quantity.Quantity'>
    OK
    
    Output <StateVariable [id:87651600] Symbol: 'h' >
    None
    Output <StateVariable [id:87664080] Symbol: 'm' >
    None
    Output <AssignedVariable [id:87664784] Symbol: 'h_alpha_rate' >
    None
    Output <AssignedVariable [id:87664592] Symbol: 'h_beta_rate' >
    None
    Output <AssignedVariable [id:87670864] Symbol: 'hinf' >
    None
    Output <AssignedVariable [id:87666512] Symbol: 'htau' >
    None
    Output <AssignedVariable [id:87672592] Symbol: 'i' >
    {u'mf': {u'role': u'TRANSMEMBRANECURRENT'}}
    Output <AssignedVariable [id:87666128] Symbol: 'm_alpha_rate' >
    None
    Output <AssignedVariable [id:87672976] Symbol: 'm_beta_rate' >
    None
    Output <AssignedVariable [id:87664208] Symbol: 'minf' >
    None
    Output <AssignedVariable [id:87664976] Symbol: 'mtau' >
    None
    input <SuppliedValue [id:87673232] Symbol: 'v' >
    {u'mf': {u'role': u'MEMBRANEVOLTAGE'}}
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    h_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    g <class 'neurounits.ast.astobjects.Parameter'>
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    m <class 'neurounits.ast.astobjects.StateVariable'>
    h <class 'neurounits.ast.astobjects.StateVariable'>
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:87664720] Symbol: h_beta_rate >
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:87664912] Symbol: h_alpha_rate >
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:87670992] Symbol: hinf >
    h_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:87666256] Symbol: m_alpha_rate >
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:87673104] Symbol: m_beta_rate >
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:87665104] Symbol: mtau >
    m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:87672720] Symbol: i >
    g <class 'neurounits.ast.astobjects.Parameter'>
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    m <class 'neurounits.ast.astobjects.StateVariable'>
    h <class 'neurounits.ast.astobjects.StateVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:87666640] Symbol: htau >
    h_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:87664336] Symbol: minf >
    m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    minf <class 'neurounits.ast.astobjects.AssignedVariable'>
    m <class 'neurounits.ast.astobjects.StateVariable'>
    mtau <class 'neurounits.ast.astobjects.AssignedVariable'>
    hinf <class 'neurounits.ast.astobjects.AssignedVariable'>
    h <class 'neurounits.ast.astobjects.StateVariable'>
    htau <class 'neurounits.ast.astobjects.AssignedVariable'>
    a1 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    a2 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    V <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    a3 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    T [<class 'neurounits.ast.astobjects.DivOp'>]
    V <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    a4 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    a5 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    Output <AssignedVariable [id:87598992] Symbol: 'i' >
    {u'mf': {u'role': u'TRANSMEMBRANECURRENT'}}
    input <SuppliedValue [id:87630096] Symbol: 'v' >
    {u'mf': {u'role': u'MEMBRANEVOLTAGE'}}
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:87599568] Symbol: i >
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    Output <StateVariable [id:87547280] Symbol: 'n' >
    None
    Output <AssignedVariable [id:87532304] Symbol: 'i' >
    {u'mf': {u'role': u'TRANSMEMBRANECURRENT'}}
    Output <AssignedVariable [id:87547152] Symbol: 'n_alpha_rate' >
    None
    Output <AssignedVariable [id:87534032] Symbol: 'n_beta_rate' >
    None
    Output <AssignedVariable [id:87533648] Symbol: 'ninf' >
    None
    Output <AssignedVariable [id:87544976] Symbol: 'ntau' >
    None
    input <SuppliedValue [id:87535120] Symbol: 'v' >
    {u'mf': {u'role': u'MEMBRANEVOLTAGE'}}
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    n_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    n_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    n <class 'neurounits.ast.astobjects.StateVariable'>
    No handlers could be found for logger "neurounits"
    2013-12-01 17:15:59,651 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:15:59,652 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/6d/6da8c32e20d060372d72edb98dcfc7e6.bundle (139k) : 0.986 seconds
    Executing: /home/michael/opt//x86_64/bin/modlunit /mnt/scratch/tmp/morphforge/tmp/tmp_6c4edc63e462f424e4c70e8cbcc883a0.mod
    /mnt/scratch/tmp/morphforge/tmp/modbuild_23593
    Executing: /home/michael/opt//x86_64/bin/nocmodl tmp_6c4edc63e462f424e4c70e8cbcc883a0.mod
    Executing: /home/michael/opt//share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/home/michael/opt//include/nrn"  -I"/home/michael/opt//x86_64/lib"    -g -O2 -c -o tmp_6c4edc63e462f424e4c70e8cbcc883a0.lo tmp_6c4edc63e462f424e4c70e8cbcc883a0.c  
    Executing: /home/michael/opt//share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_6c4edc63e462f424e4c70e8cbcc883a0.la  -rpath /home/michael/opt//x86_64/libs  tmp_6c4edc63e462f424e4c70e8cbcc883a0.lo  -L/home/michael/opt//x86_64/lib -L/home/michael/opt//x86_64/lib  /home/michael/opt//x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
    OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/home/michael/opt//include/nrn -I/home/michael/opt//x86_64/lib -g -O2 -c tmp_6c4edc63e462f424e4c70e8cbcc883a0.c  -fPIC -DPIC -o .libs/tmp_6c4edc63e462f424e4c70e8cbcc883a0.o
    
    OP2: libtool: link: gcc -shared  -fPIC -DPIC  .libs/tmp_6c4edc63e462f424e4c70e8cbcc883a0.o   -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -L/home/michael/opt//x86_64/lib /home/michael/opt/x86_64/lib/libnrniv.so /home/michael/opt/x86_64/lib/libnrnoc.so /home/michael/opt/x86_64/lib/liboc.so /home/michael/opt/x86_64/lib/libmemacs.so /home/michael/opt/x86_64/lib/libnrnmpi.so /home/michael/opt/x86_64/lib/libscopmath.so /home/michael/opt/x86_64/lib/libsparse13.so -lreadline -lncurses /home/michael/opt/x86_64/lib/libivoc.so /home/michael/opt/x86_64/lib/libneuron_gnu.so /home/michael/opt/x86_64/lib/libmeschach.so /home/michael/opt/x86_64/lib/libsundials.so -lm -ldl  -O2   -pthread -Wl,-soname -Wl,tmp_6c4edc63e462f424e4c70e8cbcc883a0.so.0 -o .libs/tmp_6c4edc63e462f424e4c70e8cbcc883a0.so.0.0.0
    libtool: link: (cd ".libs" && rm -f "tmp_6c4edc63e462f424e4c70e8cbcc883a0.so.0" && ln -s "tmp_6c4edc63e462f424e4c70e8cbcc883a0.so.0.0.0" "tmp_6c4edc63e462f424e4c70e8cbcc883a0.so.0")
    libtool: link: (cd ".libs" && rm -f "tmp_6c4edc63e462f424e4c70e8cbcc883a0.so" && ln -s "tmp_6c4edc63e462f424e4c70e8cbcc883a0.so.0.0.0" "tmp_6c4edc63e462f424e4c70e8cbcc883a0.so")
    libtool: link: ( cd ".libs" && rm -f "tmp_6c4edc63e462f424e4c70e8cbcc883a0.la" && ln -s "../tmp_6c4edc63e462f424e4c70e8cbcc883a0.la" "tmp_6c4edc63e462f424e4c70e8cbcc883a0.la" )
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_b710d7b3064eaabef925f2922f85b448.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_7e798569f10b7cd5b42e75f7cea8a7ea.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_02fe20696304be49ae774511a85392b8.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_4c11f22d9eebc78affb275e22ffe435e.hoc
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
    Time for Extracting Data: (7 records) 0.0116751194
    Running simulation : 1.488 seconds
    Size of results file: 0.3 (MB)
    Post-processing : 0.048 seconds
    Entire load-run-save time : 2.522 seconds
    Suceeded
    n <class 'neurounits.ast.astobjects.StateVariable'>
    n <class 'neurounits.ast.astobjects.StateVariable'>
    n <class 'neurounits.ast.astobjects.StateVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:87534160] Symbol: n_beta_rate >
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:87532048] Symbol: n_alpha_rate >
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:87533776] Symbol: ninf >
    n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    n_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:87532432] Symbol: i >
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    n <class 'neurounits.ast.astobjects.StateVariable'>
    n <class 'neurounits.ast.astobjects.StateVariable'>
    n <class 'neurounits.ast.astobjects.StateVariable'>
    n <class 'neurounits.ast.astobjects.StateVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:87544592] Symbol: ntau >
    n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    n_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    ninf <class 'neurounits.ast.astobjects.AssignedVariable'>
    n <class 'neurounits.ast.astobjects.StateVariable'>
    ntau <class 'neurounits.ast.astobjects.AssignedVariable'>
    a1 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    a2 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    V <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    a3 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    T [<class 'neurounits.ast.astobjects.DivOp'>]
    V <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    a4 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    a5 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/6d//6da8c32e20d060372d72edb98dcfc7e6.neuronsim.results.pickle ]
    PlotManger saving:  _output/figures/assorted_10compareHHChls/{png,svg}/fig000_Autosave_figure_1.{png,svg}




