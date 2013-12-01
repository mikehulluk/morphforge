
.. _example_assorted_10compareHHChls:

Example 20. Comparing simulations: the Hodgkin-Huxley '52 channels
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

        WARNING: Symbol 'quantity_expr' is unreachable
    WARNING: Symbol 'quantity_term' is unreachable
    WARNING: Symbol 'quantity_factor' is unreachable
    Generating LALR tables
    WARNING: 1 shift/reduce conflict
    WARNING: 1 reduce/reduce conflict
    WARNING: reduce/reduce conflict in state 97 resolved using rule (empty -> <empty>)
    WARNING: rejected rule (alphanumtoken -> ALPHATOKEN) in state 97
    ConfigOoptins {'BATCHRUN': None}
    ['BLUESPEC', 'BLUESPECDIR', 'CDPATH', 'COLORTERM', 'DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DISPLAY', 'EAGLEDIR', 'ECAD', 'ECAD_LICENSES', 'ECAD_LOCAL', 'EDITOR', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'HISTFILE', 'HISTSIZE', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'KRB5CCNAME', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LD_RUN_PATH', 'LESS', 'LM_LICENSE_FILE', 'LOGNAME', 'LSCOLORS', 'MAKEFLAGS', 'MAKELEVEL', 'MANDATORY_PATH', 'MFLAGS', 'MGLS_LICENSE_FILE', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PRINTER', 'PWD', 'PYTHONPATH', 'QUARTUS_64BIT', 'QUARTUS_BIT_TYPE', 'QUARTUS_ROOTDIR', 'SHELL', 'SHLVL', 'SOPC_KIT_NIOS2', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TEMP', 'TERM', 'TMP', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CACHE_HOME', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Parsing: library std.math {
    pi = 3.141592653;
    e =  2.718281828;
    sin(x) = __sin__(x);
    cos(x) = __cos__(x);
    tan(x) = __tan__(x);
    sinh(x) = __sinh__(x);
    cosh(x) = __cosh__(x);
    tanh(x) = __tanh__(x);
    asin(x) = __asin__(x);
    acos(x) = __acos__(x);
    atan(x) = __atan__(x);
    atan2(x,y) = __atan2__(x=x,y=y);
    exp(x) = __exp__(x);
    ln(x) = __ln__(x);
    log2(x) = __log2__(x);
    log10(x) = __log10__(x);
    abs(x) = __abs__(x);
    pow(base,exp) = __pow__(base=base,exp=exp);
    ceil(x) = __ceil__(x);
    fabs(x) = __fabs__(x);
    floor(x) = __floor__(x);
    };
    library std.geom {
    from std.math import pi;
    area_of_sphere(r:{m}) = 4 * pi * r*r;
    volume_of_sphere(r:{m}) = 4.0/3.0 * pi * r*r *r;
    };
    library std.neuro {
    from std.math import pi,pow;
    r_a(R_i:{ohm m}, d:{m}) = (4*R_i)/(pi*d*d);
    space_constant(Rm:{ohm m2},Ri:{ohm m},d:{m}) = pow(base=(( (Rm/Ri)*(d/4) )/{1m2}),exp=0.5) * {1m};
    Rinf_sealed_end(Rm:{ohm m2},d:{m}) = (4*Rm/(pi*d*d) );
    RateConstant5(V:{V},a1:{s-1} ,a2:{V-1 s-1}, a3:{},a4:{V},a5:{V} ) = (a1 + a2*V)/(a3+std.math.exp( (V+a4)/a5) );
    };
    library std.physics {
    F = 96485.3365 coulomb mole-1;
    Na = 6.02214129e23 mole-1;
    k = 1.380648e-23 joule kelvin-1;
    e =  1.602176565 coulomb;
    R = 8.3144621 J mole-1 kelvin-1;
    };
    p_lhs! <ConstValue [id:75197520] Value: '3.141592653' >
    p_lhs! <ConstValue [id:75197840] Value: '2.718281828' >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74993744] {__sin__( <id:x:75198224>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74994320] {__cos__( <id:x:74993808>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74994896] {__tan__( <id:x:74994256>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74995472] {__sinh__( <id:x:74994832>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74996048] {__cosh__( <id:x:74995408>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74996624] {__tanh__( <id:x:74995984>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74997200] {__asin__( <id:x:74996560>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:75358288] {__acos__( <id:x:74997136>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:75358864] {__atan__( <id:x:75358352>)} >
    p_lhs! params: {'y': <FunctionDefParameterInstantiation: y >, 'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:75359568] {__atan2__( <id:y:75359440,x:75359376>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:75360336] {__exp__( <id:x:75359760>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:75360912] {__ln__( <id:x:75360272>)} >
    p_lhs! params: {'x': <FuWARNING: Symbol 'ns_dot_name' is unreachable
    WARNING: Symbol 'time_derivative' is unreachable
    WARNING: Symbol 'ns_name_list' is unreachable
    WARNING: Symbol 'import_target_list' is unreachable
    WARNING: Symbol 'compound_line' is unreachable
    WARNING: Symbol 'multiport_direction' is unreachable
    WARNING: Symbol 'on_transition' is unreachable
    WARNING: Symbol 'quantity_expr' is unreachable
    WARNING: Symbol 'nineml_file' is unreachable
    WARNING: Symbol 'rv_modes' is unreachable
    WARNING: Symbol 'quantity_term' is unreachable
    WARNING: Symbol 'func_call_params_l3' is unreachable
    WARNING: Symbol 'componentlinecontents' is unreachable
    WARNING: Symbol 'function_def_param' is unreachable
    WARNING: Symbol 'open_transition_scope' is unreachable
    WARNING: Symbol 'compoundport_event_param' is unreachable
    WARNING: Symbol 'magnitude' is unreachable
    WARNING: Symbol 'transition_actions' is unreachable
    WARNING: Symbol 'event_call_param_l3' is unreachable
    WARNING: Symbol 'library_name' is unreachable
    WARNING: Symbol 'bool_term' is unreachable
    WARNING: Symbol 'localsymbol' is unreachable
    WARNING: Symbol 'open_funcdef_scope' is unreachable
    WARNING: Symbol 'externalsymbol' is unreachable
    WARNING: Symbol 'function_call_l3' is unreachable
    WARNING: Symbol 'regime_block' is unreachable
    WARNING: Symbol 'libraryline' is unreachable
    WARNING: Symbol 'import' is unreachable
    WARNING: Symbol 'library_def' is unreachable
    WARNING: Symbol 'component_name' is unreachable
    WARNING: Symbol 'compound_port_def' is unreachable
    WARNING: Symbol 'rhs_term' is unreachable
    WARNING: Symbol 'ar_model' is unreachable
    WARNING: Symbol 'compound_port_def_line' is unreachable
    WARNING: Symbol 'librarycontents' is unreachable
    WARNING: Symbol 'on_event_def_param' is unreachable
    WARNING: Symbol 'rhs_generic' is unreachable
    WARNING: Symbol 'random_variable' is unreachable
    WARNING: Symbol 'compoundcontents' is unreachable
    WARNING: Symbol 'crosses_expr' is unreachable
    WARNING: Symbol 'rt_name' is unreachable
    WARNING: Symbol 'lhs_symbol' is unreachable
    WARNING: Symbol 'component_def' is unreachable
    WARNING: Symbol 'transition_action' is unreachable
    WARNING: Symbol 'alphanumtoken' is unreachable
    WARNING: Symbol 'compound_port_def_contents' is unreachable
    WARNING: Symbol 'empty' is unreachable
    WARNING: Symbol 'namespace_def' is unreachable
    WARNING: Symbol 'compound_port_inst' is unreachable
    WARNING: Symbol 'bool_expr' is unreachable
    WARNING: Symbol 'namespace_name' is unreachable
    WARNING: Symbol 'regimecontents' is unreachable
    WARNING: Symbol 'rv_param' is unreachable
    WARNING: Symbol 'rtgraph_contents' is unreachable
    WARNING: Symbol 'namespaceblocks' is unreachable
    WARNING: Symbol 'compoundport_event_param_list' is unreachable
    WARNING: Symbol 'ns_name' is unreachable
    WARNING: Symbol 'initial_block' is unreachable
    WARNING: Symbol 'compound_port_def_direction_arrow' is unreachable
    WARNING: Symbol 'rv_mode' is unreachable
    WARNING: Symbol 'initial_expr_block' is unreachable
    WARNING: Symbol 'regime_name' is unreachable
    WARNING: Symbol 'top_level_block' is unreachable
    WARNING: Symbol 'compound_port_inst_constents' is unreachable
    WARNING: Symbol 'transition_to' is unreachable
    WARNING: Symbol 'on_event_def_params' is unreachable
    WARNING: Symbol 'regimecontentsline' is unreachable
    WARNING: Symbol 'namespace' is unreachable
    WARNING: Symbol 'rv_params' is unreachable
    WARNING: Symbol 'compound_component_def' is unreachable
    WARNING: Symbol 'function_def_params' is unreachable
    WARNING: Symbol 'function_def' is unreachable
    WARNING: Symbol 'assignment' is unreachable
    WARNING: Symbol 'componentcontents' is unreachable
    WARNING: Symbol 'rhs_variable' is unreachable
    WARNING: Symbol 'event_call_params_l3' is unreachable
    WARNING: Symbol 'compondport_inst_line' is unreachable
    WARNING: Symbol 'func_call_param_l3' is unreachable
    WARNING: Symbol 'rhs_symbol' is unreachable
    WARNING: Symbol 'quantity_factor' is unreachable
    WARNING: Symbol 'rhs_quantity_expr' is unreachable
    WARNING: Symbol 'quantity' is unreachable
    Generating LALR tables
    2013-11-30 18:14:35,996 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-11-30 18:14:35,996 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
    WARNING: Symbol 'quantity_expr' is unreachable
    WARNING: Symbol 'quantity_term' is unreachable
    WARNING: Symbol 'quantity_factor' is unreachable
    Generating LALR tables
    WARNING: 1 shift/reduce conflict
    WARNING: 1 reduce/reduce conflict
    WARNING: reduce/reduce conflict in state 97 resolved using rule (empty -> <empty>)
    WARNING: rejected rule (alphanumtoken -> ALPHATOKEN) in state 97
    ConfigOoptins {'BATCHRUN': None}
    ['BLUESPEC', 'BLUESPECDIR', 'CDPATH', 'COLORTERM', 'DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DISPLAY', 'EAGLEDIR', 'ECAD', 'ECAD_LICENSES', 'ECAD_LOCAL', 'EDITOR', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'HISTFILE', 'HISTSIZE', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'KRB5CCNAME', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LD_RUN_PATH', 'LESS', 'LM_LICENSE_FILE', 'LOGNAME', 'LSCOLORS', 'MAKEFLAGS', 'MAKELEVEL', 'MANDATORY_PATH', 'MFLAGS', 'MGLS_LICENSE_FILE', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PRINTER', 'PWD', 'PYTHONPATH', 'QUARTUS_64BIT', 'QUARTUS_BIT_TYPE', 'QUARTUS_ROOTDIR', 'SHELL', 'SHLVL', 'SOPC_KIT_NIOS2', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TEMP', 'TERM', 'TMP', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CACHE_HOME', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Parsing: library std.math {
    pi = 3.141592653;
    e =  2.718281828;
    sin(x) = __sin__(x);
    cos(x) = __cos__(x);
    tan(x) = __tan__(x);
    sinh(x) = __sinh__(x);
    cosh(x) = __cosh__(x);
    tanh(x) = __tanh__(x);
    asin(x) = __asin__(x);
    acos(x) = __acos__(x);
    atan(x) = __atan__(x);
    atan2(x,y) = __atan2__(x=x,y=y);
    exp(x) = __exp__(x);
    ln(x) = __ln__(x);
    log2(x) = __log2__(x);
    log10(x) = __log10__(x);
    abs(x) = __abs__(x);
    pow(base,exp) = __pow__(base=base,exp=exp);
    ceil(x) = __ceil__(x);
    fabs(x) = __fabs__(x);
    floor(x) = __floor__(x);
    };
    library std.geom {
    from std.math import pi;
    area_of_sphere(r:{m}) = 4 * pi * r*r;
    volume_of_sphere(r:{m}) = 4.0/3.0 * pi * r*r *r;
    };
    library std.neuro {
    from std.math import pi,pow;
    r_a(R_i:{ohm m}, d:{m}) = (4*R_i)/(pi*d*d);
    space_constant(Rm:{ohm m2},Ri:{ohm m},d:{m}) = pow(base=(( (Rm/Ri)*(d/4) )/{1m2}),exp=0.5) * {1m};
    Rinf_sealed_end(Rm:{ohm m2},d:{m}) = (4*Rm/(pi*d*d) );
    RateConstant5(V:{V},a1:{s-1} ,a2:{V-1 s-1}, a3:{},a4:{V},a5:{V} ) = (a1 + a2*V)/(a3+std.math.exp( (V+a4)/a5) );
    };
    library std.physics {
    F = 96485.3365 coulomb mole-1;
    Na = 6.02214129e23 mole-1;
    k = 1.380648e-23 joule kelvin-1;
    e =  1.602176565 coulomb;
    R = 8.3144621 J mole-1 kelvin-1;
    };
    p_lhs! <ConstValue [id:72313168] Value: '3.141592653' >
    p_lhs! <ConstValue [id:72313488] Value: '2.718281828' >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:72314128] {__sin__( <id:x:72313872>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:72314704] {__cos__( <id:x:72314064>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:72319440] {__tan__( <id:x:72319248>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:72320016] {__sinh__( <id:x:72319376>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:72320592] {__cosh__( <id:x:72319952>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:72321168] {__tanh__( <id:x:72320528>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:72321744] {__asin__( <id:x:72321104>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:72322320] {__acos__( <id:x:72321680>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:72322896] {__atan__( <id:x:72322256>)} >
    p_lhs! params: {'y': <FunctionDefParameterInstantiation: y >, 'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:72323664] {__atan2__( <id:y:72323536,x:72323600>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:72324432] {__exp__( <id:x:72323856>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:72325008] {__ln__( <id:x:72324368>)} >
    p_lhs! params: {'x': <FuWARNING: Symbol 'ns_dot_name' is unreachable
    WARNING: Symbol 'time_derivative' is unreachable
    WARNING: Symbol 'ns_name_list' is unreachable
    WARNING: Symbol 'import_target_list' is unreachable
    WARNING: Symbol 'compound_line' is unreachable
    WARNING: Symbol 'multiport_direction' is unreachable
    WARNING: Symbol 'on_transition' is unreachable
    WARNING: Symbol 'quantity_expr' is unreachable
    WARNING: Symbol 'nineml_file' is unreachable
    WARNING: Symbol 'rv_modes' is unreachable
    WARNING: Symbol 'quantity_term' is unreachable
    WARNING: Symbol 'func_call_params_l3' is unreachable
    WARNING: Symbol 'componentlinecontents' is unreachable
    WARNING: Symbol 'function_def_param' is unreachable
    WARNING: Symbol 'open_transition_scope' is unreachable
    WARNING: Symbol 'compoundport_event_param' is unreachable
    WARNING: Symbol 'magnitude' is unreachable
    WARNING: Symbol 'transition_actions' is unreachable
    WARNING: Symbol 'event_call_param_l3' is unreachable
    WARNING: Symbol 'library_name' is unreachable
    WARNING: Symbol 'bool_term' is unreachable
    WARNING: Symbol 'localsymbol' is unreachable
    WARNING: Symbol 'open_funcdef_scope' is unreachable
    WARNING: Symbol 'externalsymbol' is unreachable
    WARNING: Symbol 'function_call_l3' is unreachable
    WARNING: Symbol 'regime_block' is unreachable
    WARNING: Symbol 'libraryline' is unreachable
    WARNING: Symbol 'import' is unreachable
    WARNING: Symbol 'library_def' is unreachable
    WARNING: Symbol 'component_name' is unreachable
    WARNING: Symbol 'compound_port_def' is unreachable
    WARNING: Symbol 'rhs_term' is unreachable
    WARNING: Symbol 'ar_model' is unreachable
    WARNING: Symbol 'compound_port_def_line' is unreachable
    WARNING: Symbol 'librarycontents' is unreachable
    WARNING: Symbol 'on_event_def_param' is unreachable
    WARNING: Symbol 'rhs_generic' is unreachable
    WARNING: Symbol 'random_variable' is unreachable
    WARNING: Symbol 'compoundcontents' is unreachable
    WARNING: Symbol 'crosses_expr' is unreachable
    WARNING: Symbol 'rt_name' is unreachable
    WARNING: Symbol 'lhs_symbol' is unreachable
    WARNING: Symbol 'component_def' is unreachable
    WARNING: Symbol 'transition_action' is unreachable
    WARNING: Symbol 'alphanumtoken' is unreachable
    WARNING: Symbol 'compound_port_def_contents' is unreachable
    WARNING: Symbol 'empty' is unreachable
    WARNING: Symbol 'namespace_def' is unreachable
    WARNING: Symbol 'compound_port_inst' is unreachable
    WARNING: Symbol 'bool_expr' is unreachable
    WARNING: Symbol 'namespace_name' is unreachable
    WARNING: Symbol 'regimecontents' is unreachable
    WARNING: Symbol 'rv_param' is unreachable
    WARNING: Symbol 'rtgraph_contents' is unreachable
    WARNING: Symbol 'namespaceblocks' is unreachable
    WARNING: Symbol 'compoundport_event_param_list' is unreachable
    WARNING: Symbol 'ns_name' is unreachable
    WARNING: Symbol 'initial_block' is unreachable
    WARNING: Symbol 'compound_port_def_direction_arrow' is unreachable
    WARNING: Symbol 'rv_mode' is unreachable
    WARNING: Symbol 'initial_expr_block' is unreachable
    WARNING: Symbol 'regime_name' is unreachable
    WARNING: Symbol 'top_level_block' is unreachable
    WARNING: Symbol 'compound_port_inst_constents' is unreachable
    WARNING: Symbol 'transition_to' is unreachable
    WARNING: Symbol 'on_event_def_params' is unreachable
    WARNING: Symbol 'regimecontentsline' is unreachable
    WARNING: Symbol 'namespace' is unreachable
    WARNING: Symbol 'rv_params' is unreachable
    WARNING: Symbol 'compound_component_def' is unreachable
    WARNING: Symbol 'function_def_params' is unreachable
    WARNING: Symbol 'function_def' is unreachable
    WARNING: Symbol 'assignment' is unreachable
    WARNING: Symbol 'componentcontents' is unreachable
    WARNING: Symbol 'rhs_variable' is unreachable
    WARNING: Symbol 'event_call_params_l3' is unreachable
    WARNING: Symbol 'compondport_inst_line' is unreachable
    WARNING: Symbol 'func_call_param_l3' is unreachable
    WARNING: Symbol 'rhs_symbol' is unreachable
    WARNING: Symbol 'quantity_factor' is unreachable
    WARNING: Symbol 'rhs_quantity_expr' is unreachable
    WARNING: Symbol 'quantity' is unreachable
    Generating LALR tables
    2013-11-30 18:14:37,576 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-11-30 18:14:37,576 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    nctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:72325584] {__log2__( <id:x:72325520>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:72326160] {__log10__( <id:x:72326096>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:72326736] {__abs__( <id:x:72324944>)} >
    p_lhs! params: {'base': <FunctionDefParameterInstantiation: base >, 'exp': <FunctionDefParameterInstantiation: exp >}
    <FunctionDefBuiltInInstantiation [id:72327504] {__pow__( <id:base:72327440,exp:72327248>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:72328272] {__ceil__( <id:x:72327696>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:72328848] {__fabs__( <id:x:72328208>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:72329424] {__floor__( <id:x:72328784>)} >
    p_lhs! <MulOp [id:72343760] [??] >
    p_lhs! <MulOp [id:74395984] [??] >
    p_lhs! <DivOp [id:74335120] [??] >
    p_lhs! <MulOp [id:74336720] [??] >
    p_lhs! <DivOp [id:74336272] [??] >
    p_lhs! <DivOp [id:74404432] [??] >
    p_lhs! <ConstValue [id:74379408] Value: '96485.3365e0 s  A  mol ' >
    p_lhs! <ConstValue [id:74382800] Value: '6.02214129e+23e0 mol ' >
    p_lhs! <ConstValue [id:74379728] Value: '1.380648e-23e0 m 2 kg  s  K ' >
    p_lhs! <ConstValue [id:74383184] Value: '1.602176565e0 s  A ' >
    p_lhs! <ConstValue [id:74383056] Value: '8.3144621e0 m 2 kg  s  K  mol ' >
    Parsing: ms
    Parsing: ms
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/23/2301083af38ef722a2c44293a32a7bf4.bundle (11k) : 0.789 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    Executing: /opt/nrn//x86_64/bin/modlunit /local/scratch/mh735/tmp/morphforge/tmp/tmp_3921e7faec6eb201a604a59c06ea8e00.mod
    /local/scratch/mh735/tmp/morphforge/tmp/modbuild_4940
    Executing: /opt/nrn//x86_64/bin/nocmodl tmp_3921e7faec6eb201a604a59c06ea8e00.mod
    Executing: /opt/nrn//share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn//include/nrn"  -I"/opt/nrn//x86_64/lib"    -g -O2 -c -o tmp_3921e7faec6eb201a604a59c06ea8e00.lo tmp_3921e7faec6eb201a604a59c06ea8e00.c  
    Executing: /opt/nrn//share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_3921e7faec6eb201a604a59c06ea8e00.la  -rpath /opt/nrn//x86_64/libs  tmp_3921e7faec6eb201a604a59c06ea8e00.lo  -L/opt/nrn//x86_64/lib -L/opt/nrn//x86_64/lib  /opt/nrn//x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
    OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/opt/nrn//include/nrn -I/opt/nrn//x86_64/lib -g -O2 -c tmp_3921e7faec6eb201a604a59c06ea8e00.c  -fPIC -DPIC -o .libs/tmp_3921e7faec6eb201a604a59c06ea8e00.o
    
    OP2: libtool: link: gcc -shared  .libs/tmp_3921e7faec6eb201a604a59c06ea8e00.o   -Wl,-rpath -Wl,/opt/nrn/x86_64/lib -Wl,-rpath -Wl,/opt/nrn/x86_64/lib -L/opt/nrn//x86_64/lib /opt/nrn/x86_64/lib/libnrniv.so /opt/nrn/x86_64/lib/libnrnoc.so /opt/nrn/x86_64/lib/liboc.so /opt/nrn/x86_64/lib/libmemacs.so /opt/nrn/x86_64/lib/libnrnmpi.so /opt/nrn/x86_64/lib/libscopmath.so /opt/nrn/x86_64/lib/libsparse13.so -lreadline -lncurses /opt/nrn/x86_64/lib/libivoc.so /opt/nrn/x86_64/lib/libneuron_gnu.so /opt/nrn/x86_64/lib/libmeschach.so /opt/nrn/x86_64/lib/libsundials.so -lm -ldl    -pthread -Wl,-soname -Wl,tmp_3921e7faec6eb201a604a59c06ea8e00.so.0 -o .libs/tmp_3921e7faec6eb201a604a59c06ea8e00.so.0.0.0
    libtool: link: (cd ".libs" && rm -f "tmp_3921e7faec6eb201a604a59c06ea8e00.so.0" && ln -s "tmp_3921e7faec6eb201a604a59c06ea8e00.so.0.0.0" "tmp_3921e7faec6eb201a604a59c06ea8e00.so.0")
    libtool: link: (cd ".libs" && rm -f "tmp_3921e7faec6eb201a604a59c06ea8e00.so" && ln -s "tmp_3921e7faec6eb201a604a59c06eaNEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    8e00.so.0.0.0" "tmp_3921e7faec6eb201a604a59c06ea8e00.so")
    libtool: link: ( cd ".libs" && rm -f "tmp_3921e7faec6eb201a604a59c06ea8e00.la" && ln -s "../tmp_3921e7faec6eb201a604a59c06ea8e00.la" "tmp_3921e7faec6eb201a604a59c06ea8e00.la" )
    
    Executing: /opt/nrn//x86_64/bin/modlunit /local/scratch/mh735/tmp/morphforge/tmp/tmp_df613e962532e3fa96089ed20b5db0d0.mod
    /local/scratch/mh735/tmp/morphforge/tmp/modbuild_4940
    Executing: /opt/nrn//x86_64/bin/nocmodl tmp_df613e962532e3fa96089ed20b5db0d0.mod
    Executing: /opt/nrn//share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn//include/nrn"  -I"/opt/nrn//x86_64/lib"    -g -O2 -c -o tmp_df613e962532e3fa96089ed20b5db0d0.lo tmp_df613e962532e3fa96089ed20b5db0d0.c  
    Executing: /opt/nrn//share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_df613e962532e3fa96089ed20b5db0d0.la  -rpath /opt/nrn//x86_64/libs  tmp_df613e962532e3fa96089ed20b5db0d0.lo  -L/opt/nrn//x86_64/lib -L/opt/nrn//x86_64/lib  /opt/nrn//x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
    OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/opt/nrn//include/nrn -I/opt/nrn//x86_64/lib -g -O2 -c tmp_df613e962532e3fa96089ed20b5db0d0.c  -fPIC -DPIC -o .libs/tmp_df613e962532e3fa96089ed20b5db0d0.o
    
    OP2: libtool: link: gcc -shared  .libs/tmp_df613e962532e3fa96089ed20b5db0d0.o   -Wl,-rpath -Wl,/opt/nrn/x86_64/lib -Wl,-rpath -Wl,/opt/nrn/x86_64/lib -L/opt/nrn//x86_64/lib /opt/nrn/x86_64/lib/libnrniv.so /opt/nrn/x86_64/lib/libnrnoc.so /opt/nrn/x86_64/lib/liboc.so /opt/nrn/x86_64/lib/libmemacs.so /opt/nrn/x86_64/lib/libnrnmpi.so /opt/nrn/x86_64/lib/libscopmath.so /opt/nrn/x86_64/lib/libsparse13.so -lreadline -lncurses /opt/nrn/x86_64/lib/libivoc.so /opt/nrn/x86_64/lib/libneuron_gnu.so /opt/nrn/x86_64/lib/libmeschach.so /opt/nrn/x86_64/lib/libsundials.so -lm -ldl    -pthread -Wl,-soname -Wl,tmp_df613e962532e3fa96089ed20b5db0d0.so.0 -o .libs/tmp_df613e962532e3fa96089ed20b5db0d0.so.0.0.0
    libtool: link: (cd ".libs" && rm -f "tmp_df613e962532e3fa96089ed20b5db0d0.so.0" && ln -s "tmp_df613e962532e3fa96089ed20b5db0d0.so.0.0.0" "tmp_df613e962532e3fa96089ed20b5db0d0.so.0")
    libtool: link: (cd ".libs" && rm -f "tmp_df613e962532e3fa96089ed20b5db0d0.so" && ln -s "tmp_df613e962532e3fa96089ed20b5db0d0.so.0.0.0" "tmp_df613e962532e3fa96089ed20b5db0d0.so")
    libtool: link: ( cd ".libs" && rm -f "tmp_df613e962532e3fa96089ed20b5db0d0.la" && ln -s "../tmp_df613e962532e3fa96089ed20b5db0d0.la" "tmp_df613e962532e3fa96089ed20b5db0d0.la" )
    
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_878229359c61787dea115bc3b72984d5.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_4563344e61d3d666e79216fc708ef694.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_2dc2af8bb733b303221c732ec0afa7de.so
    	1 
    	1 
    	0.01 
    	0 
    	1 
    	50000 
    	1 
    Running Simulation
    Time for Extracting Data: (1 records) 0.000679016113281
    Running simulation : 1.075 seconds
    Post-processing : 0.004 seconds
    Entire load-run-save time : 1.867 seconds
    Suceeded
    WARNING: Symbol 'quantity_expr' is unreachable
    WARNING: Symbol 'quantity_term' is unreachable
    WARNING: Symbol 'quantity_factor' is unreachable
    Generating LALR tables
    WARNING: 1 shift/reduce conflict
    WARNING: 1 reduce/reduce conflict
    WARNING: reduce/reduce conflict in state 97 resolved using rule (empty -> <empty>)
    WARNING: rejected rule (alphanumtoken -> ALPHATOKEN) in state 97
    ConfigOoptins {'BATCHRUN': None}
    ['BLUESPEC', 'BLUESPECDIR', 'CDPATH', 'COLORTERM', 'DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DISPLAY', 'EAGLEDIR', 'ECAD', 'ECAD_LICENSES', 'ECAD_LOCAL', 'EDITOR', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'HISTFILE', 'HISTSIZE', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'KRB5CCNAME', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LD_RUN_PATH', 'LESS', 'LM_LICENSE_FILE', 'LOGNAME', 'LSCOLORS', 'MAKEFLAGS', 'MAKELEVEL', 'MANDATORY_PATH', 'MFLAGS', 'MGLS_LICENSE_FILE', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PRINTER', 'PWD', 'PYTHONPATH', 'QUARTUS_64BIT', 'QUARTUS_BIT_TYPE', 'QUARTUS_ROOTDIR', 'SHELL', 'SHLVL', 'SOPC_KIT_NIOS2', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TEMP', 'TERM', 'TMP', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CACHE_HOME', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Parsing: library std.math {
    pi = 3.141592653;
    e =  2.718281828;
    sin(x) = __sin__(x);
    cos(x) = __cos__(x);
    tan(x) = __tan__(x);
    sinh(x) = __sinh__(x);
    cosh(x) = __cosh__(x);
    tanh(x) = __tanh__(x);
    asin(x) = __asin__(x);
    acos(x) = __acos__(x);
    atan(x) = __atan__(x);
    atan2(x,y) = __atan2__(x=x,y=y);
    exp(x) = __exp__(x);
    ln(x) = __ln__(x);
    log2(x) = __log2__(x);
    log10(x) = __log10__(x);
    abs(x) = __abs__(x);
    pow(base,exp) = __pow__(base=base,exp=exp);
    ceil(x) = __ceil__(x);
    fabs(x) = __fabs__(x);
    floor(x) = __floor__(x);
    };
    library std.geom {
    from std.math import pi;
    area_of_sphere(r:{m}) = 4 * pi * r*r;
    volume_of_sphere(r:{m}) = 4.0/3.0 * pi * r*r *r;
    };
    library std.neuro {
    from std.math import pi,pow;
    r_a(R_i:{ohm m}, d:{m}) = (4*R_i)/(pi*d*d);
    space_constant(Rm:{ohm m2},Ri:{ohm m},d:{m}) = pow(base=(( (Rm/Ri)*(d/4) )/{1m2}),exp=0.5) * {1m};
    Rinf_sealed_end(Rm:{ohm m2},d:{m}) = (4*Rm/(pi*d*d) );
    RateConstant5(V:{V},a1:{s-1} ,a2:{V-1 s-1}, a3:{},a4:{V},a5:{V} ) = (a1 + a2*V)/(a3+std.math.exp( (V+a4)/a5) );
    };
    library std.physics {
    F = 96485.3365 coulomb mole-1;
    Na = 6.02214129e23 mole-1;
    k = 1.380648e-23 joule kelvin-1;
    e =  1.602176565 coulomb;
    R = 8.3144621 J mole-1 kelvin-1;
    };
    p_lhs! <ConstValue [id:55761232] Value: '3.141592653' >
    p_lhs! <ConstValue [id:55761552] Value: '2.718281828' >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:55762192] {__sin__( <id:x:55761936>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:55762768] {__cos__( <id:x:55762128>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:55796176] {__tan__( <id:x:55795984>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:55796752] {__sinh__( <id:x:55796112>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:55797328] {__cosh__( <id:x:55796688>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:55797904] {__tanh__( <id:x:55797264>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:55798480] {__asin__( <id:x:55797840>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:55799056] {__acos__( <id:x:55798416>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:55799632] {__atan__( <id:x:55798992>)} >
    p_lhs! params: {'y': <FunctionDefParameterInstantiation: y >, 'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:55804496] {__atan2__( <id:y:55804368,x:55804432>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:55805264] {__exp__( <id:x:55804688>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:55805840] {__ln__( <id:x:55805200>)} >
    p_lhs! params: {'x': <FuWARNING: Symbol 'ns_dot_name' is unreachable
    WARNING: Symbol 'time_derivative' is unreachable
    WARNING: Symbol 'ns_name_list' is unreachable
    WARNING: Symbol 'import_target_list' is unreachable
    WARNING: Symbol 'compound_line' is unreachable
    WARNING: Symbol 'multiport_direction' is unreachable
    WARNING: Symbol 'on_transition' is unreachable
    WARNING: Symbol 'quantity_expr' is unreachable
    WARNING: Symbol 'nineml_file' is unreachable
    WARNING: Symbol 'rv_modes' is unreachable
    WARNING: Symbol 'quantity_term' is unreachable
    WARNING: Symbol 'func_call_params_l3' is unreachable
    WARNING: Symbol 'componentlinecontents' is unreachable
    WARNING: Symbol 'function_def_param' is unreachable
    WARNING: Symbol 'open_transition_scope' is unreachable
    WARNING: Symbol 'compoundport_event_param' is unreachable
    WARNING: Symbol 'magnitude' is unreachable
    WARNING: Symbol 'transition_actions' is unreachable
    WARNING: Symbol 'event_call_param_l3' is unreachable
    WARNING: Symbol 'library_name' is unreachable
    WARNING: Symbol 'bool_term' is unreachable
    WARNING: Symbol 'localsymbol' is unreachable
    WARNING: Symbol 'open_funcdef_scope' is unreachable
    WARNING: Symbol 'externalsymbol' is unreachable
    WARNING: Symbol 'function_call_l3' is unreachable
    WARNING: Symbol 'regime_block' is unreachable
    WARNING: Symbol 'libraryline' is unreachable
    WARNING: Symbol 'import' is unreachable
    WARNING: Symbol 'library_def' is unreachable
    WARNING: Symbol 'component_name' is unreachable
    WARNING: Symbol 'compound_port_def' is unreachable
    WARNING: Symbol 'rhs_term' is unreachable
    WARNING: Symbol 'ar_model' is unreachable
    WARNING: Symbol 'compound_port_def_line' is unreachable
    WARNING: Symbol 'librarycontents' is unreachable
    WARNING: Symbol 'on_event_def_param' is unreachable
    WARNING: Symbol 'rhs_generic' is unreachable
    WARNING: Symbol 'random_variable' is unreachable
    WARNING: Symbol 'compoundcontents' is unreachable
    WARNING: Symbol 'crosses_expr' is unreachable
    WARNING: Symbol 'rt_name' is unreachable
    WARNING: Symbol 'lhs_symbol' is unreachable
    WARNING: Symbol 'component_def' is unreachable
    WARNING: Symbol 'transition_action' is unreachable
    WARNING: Symbol 'alphanumtoken' is unreachable
    WARNING: Symbol 'compound_port_def_contents' is unreachable
    WARNING: Symbol 'empty' is unreachable
    WARNING: Symbol 'namespace_def' is unreachable
    WARNING: Symbol 'compound_port_inst' is unreachable
    WARNING: Symbol 'bool_expr' is unreachable
    WARNING: Symbol 'namespace_name' is unreachable
    WARNING: Symbol 'regimecontents' is unreachable
    WARNING: Symbol 'rv_param' is unreachable
    WARNING: Symbol 'rtgraph_contents' is unreachable
    WARNING: Symbol 'namespaceblocks' is unreachable
    WARNING: Symbol 'compoundport_event_param_list' is unreachable
    WARNING: Symbol 'ns_name' is unreachable
    WARNING: Symbol 'initial_block' is unreachable
    WARNING: Symbol 'compound_port_def_direction_arrow' is unreachable
    WARNING: Symbol 'rv_mode' is unreachable
    WARNING: Symbol 'initial_expr_block' is unreachable
    WARNING: Symbol 'regime_name' is unreachable
    WARNING: Symbol 'top_level_block' is unreachable
    WARNING: Symbol 'compound_port_inst_constents' is unreachable
    WARNING: Symbol 'transition_to' is unreachable
    WARNING: Symbol 'on_event_def_params' is unreachable
    WARNING: Symbol 'regimecontentsline' is unreachable
    WARNING: Symbol 'namespace' is unreachable
    WARNING: Symbol 'rv_params' is unreachable
    WARNING: Symbol 'compound_component_def' is unreachable
    WARNING: Symbol 'function_def_params' is unreachable
    WARNING: Symbol 'function_def' is unreachable
    WARNING: Symbol 'assignment' is unreachable
    WARNING: Symbol 'componentcontents' is unreachable
    WARNING: Symbol 'rhs_variable' is unreachable
    WARNING: Symbol 'event_call_params_l3' is unreachable
    WARNING: Symbol 'compondport_inst_line' is unreachable
    WARNING: Symbol 'func_call_param_l3' is unreachable
    WARNING: Symbol 'rhs_symbol' is unreachable
    WARNING: Symbol 'quantity_factor' is unreachable
    WARNING: Symbol 'rhs_quantity_expr' is unreachable
    WARNING: Symbol 'quantity' is unreachable
    Generating LALR tables
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    nctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:55806416] {__log2__( <id:x:55806352>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:55806992] {__log10__( <id:x:55806928>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:55807568] {__abs__( <id:x:55805776>)} >
    p_lhs! params: {'base': <FunctionDefParameterInstantiation: base >, 'exp': <FunctionDefParameterInstantiation: exp >}
    <FunctionDefBuiltInInstantiation [id:55787856] {__pow__( <id:base:55787792,exp:55787600>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:55788624] {__ceil__( <id:x:55788048>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:55789200] {__fabs__( <id:x:55788560>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:55789776] {__floor__( <id:x:55789136>)} >
    p_lhs! <MulOp [id:55779536] [??] >
    p_lhs! <MulOp [id:57778512] [??] >
    p_lhs! <DivOp [id:57861008] [??] >
    p_lhs! <MulOp [id:57862608] [??] >
    p_lhs! <DivOp [id:57862160] [??] >
    p_lhs! <DivOp [id:57852496] [??] >
    p_lhs! <ConstValue [id:57806992] Value: '96485.3365e0 s  A  mol ' >
    p_lhs! <ConstValue [id:57810384] Value: '6.02214129e+23e0 mol ' >
    p_lhs! <ConstValue [id:57807312] Value: '1.380648e-23e0 m 2 kg  s  K ' >
    p_lhs! <ConstValue [id:57810768] Value: '1.602176565e0 s  A ' >
    p_lhs! <ConstValue [id:57810640] Value: '8.3144621e0 m 2 kg  s  K  mol ' >
    Parsing: ms
    Parsing: ms
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/3b/3bc3f7e81070fab0f5b8ae827488ee22.bundle (9k) : 0.790 seconds
    	1 
    	1 
    	0.01 
    	0 
    	1 
    	50000 
    	1 
    Running Simulation
    Time for Extracting Data: (1 records) 0.00061821937561
    Running simulation : 0.069 seconds
    Post-processing : 0.003 seconds
    Entire load-run-save time : 0.862 seconds
    Suceeded
    WARNING: Symbol 'ns_dot_name' is unreachable
    WARNING: Symbol 'time_derivative' is unreachable
    WARNING: Symbol 'ns_name_list' is unreachable
    WARNING: Symbol 'import_target_list' is unreachable
    WARNING: Symbol 'compound_line' is unreachable
    WARNING: Symbol 'multiport_direction' is unreachable
    WARNING: Symbol 'on_transition' is unreachable
    WARNING: Symbol 'nineml_file' is unreachable
    WARNING: Symbol 'rv_modes' is unreachable
    WARNING: Symbol 'func_call_params_l3' is unreachable
    WARNING: Symbol 'componentlinecontents' is unreachable
    WARNING: Symbol 'function_def_param' is unreachable
    WARNING: Symbol 'open_transition_scope' is unreachable
    WARNING: Symbol 'compoundport_event_param' is unreachable
    WARNING: Symbol 'transition_actions' is unreachable
    WARNING: Symbol 'event_call_param_l3' is unreachable
    WARNING: Symbol 'library_name' is unreachable
    WARNING: Symbol 'bool_term' is unreachable
    WARNING: Symbol 'localsymbol' is unreachable
    WARNING: Symbol 'open_funcdef_scope' is unreachable
    WARNING: Symbol 'externalsymbol' is unreachable
    WARNING: Symbol 'function_call_l3' is unreachable
    WARNING: Symbol 'regime_block' is unreachable
    WARNING: Symbol 'libraryline' is unreachable
    WARNING: Symbol 'import' is unreachable
    WARNING: Symbol 'library_def' is unreachable
    WARNING: Symbol 'component_name' is unreachable
    WARNING: Symbol 'compound_port_def' is unreachable
    WARNING: Symbol 'rhs_term' is unreachable
    WARNING: Symbol 'ar_model' is unreachable
    WARNING: Symbol 'compound_port_def_line' is unreachable
    WARNING: Symbol 'librarycontents' is unreachable
    WARNING: Symbol 'on_event_def_param' is unreachable
    WARNING: Symbol 'rhs_generic' is unreachable
    WARNING: Symbol 'random_variable' is unreachable
    WARNING: Symbol 'compoundcontents' is unreachable
    WARNING: Symbol 'crosses_expr' is unreachable
    WARNING: Symbol 'rt_name' is unreachable
    WARNING: Symbol 'lhs_symbol' is unreachable
    WARNING: Symbol 'component_def' is unreachable
    WARNING: Symbol 'transition_action' is unreachable
    WARNING: Symbol 'alphanumtoken' is unreachable
    WARNING: Symbol 'compound_port_def_contents' is unreachable
    WARNING: Symbol 'empty' is unreachable
    WARNING: Symbol 'namespace_def' is unreachable
    WARNING: Symbol 'compound_port_inst' is unreachable
    WARNING: Symbol 'bool_expr' is unreachable
    WARNING: Symbol 'namespace_name' is unreachable
    WARNING: Symbol 'regimecontents' is unreachable
    WARNING: Symbol 'rv_param' is unreachable
    WARNING: Symbol 'rtgraph_contents' is unreachable
    WARNING: Symbol 'namespaceblocks' is unreachable
    WARNING: Symbol 'compoundport_event_param_list' is unreachable
    WARNING: Symbol 'ns_name' is unreachable
    WARNING: Symbol 'initial_block' is unreachable
    WARNING: Symbol 'compound_port_def_direction_arrow' is unreachable
    WARNING: Symbol 'rv_mode' is unreachable
    WARNING: Symbol 'initial_expr_block' is unreachable
    WARNING: Symbol 'regime_name' is unreachable
    WARNING: Symbol 'top_level_block' is unreachable
    WARNING: Symbol 'compound_port_inst_constents' is unreachable
    WARNING: Symbol 'transition_to' is unreachable
    WARNING: Symbol 'on_event_def_params' is unreachable
    WARNING: Symbol 'regimecontentsline' is unreachable
    WARNING: Symbol 'namespace' is unreachable
    WARNING: Symbol 'rv_params' is unreachable
    WARNING: Symbol 'compound_component_def' is unreachable
    WARNING: Symbol 'function_def_params' is unreachable
    WARNING: Symbol 'function_def' is unreachable
    WARNING: Symbol 'assignment' is unreachable
    WARNING: Symbol 'componentcontents' is unreachable
    WARNING: Symbol 'rhs_variable' is unreachable
    WARNING: Symbol 'event_call_params_l3' is unreachable
    WARNING: Symbol 'compondport_inst_line' is unreachable
    WARNING: Symbol 'func_call_param_l3' is unreachable
    WARNING: Symbol 'rhs_symbol' is unreachable
    WARNING: Symbol 'rhs_quantity_expr' is unreachable
    Generating LALR tables
    nctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:75361488] {__log2__( <id:x:75361424>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:75362064] {__log10__( <id:x:75362000>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:75362704] {__abs__( <id:x:75362512>)} >
    p_lhs! params: {'base': <FunctionDefParameterInstantiation: base >, 'exp': <FunctionDefParameterInstantiation: exp >}
    <FunctionDefBuiltInInstantiation [id:75363408] {__pow__( <id:base:75362768,exp:75363152>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:75364176] {__ceil__( <id:x:75363600>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:75364752] {__fabs__( <id:x:75364112>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:75365328] {__floor__( <id:x:75364688>)} >
    p_lhs! <MulOp [id:75371472] [??] >
    p_lhs! <MulOp [id:74450128] [??] >
    p_lhs! <DivOp [id:74445968] [??] >
    p_lhs! <MulOp [id:74445840] [??] >
    p_lhs! <DivOp [id:74473808] [??] >
    p_lhs! <DivOp [id:74473936] [??] >
    p_lhs! <ConstValue [id:74462096] Value: '96485.3365e0 s  A  mol ' >
    p_lhs! <ConstValue [id:74463888] Value: '6.02214129e+23e0 mol ' >
    p_lhs! <ConstValue [id:74463632] Value: '1.380648e-23e0 m 2 kg  s  K ' >
    p_lhs! <ConstValue [id:74465168] Value: '1.602176565e0 s  A ' >
    p_lhs! <ConstValue [id:74463184] Value: '8.3144621e0 m 2 kg  s  K  mol ' >
    Parsing: ms
    Parsing: ms
    Parsing: mA/cm2
    Parsing: nA
    Parsing: mV
    Parsing: ms
    Parsing: K
    Parsing: ms
    Parsing: ms
    Parsing: mS/cm2
    Parsing: mS/cm2
    Parsing: mS/cm2
    Parsing: uF/cm2
    Parsing: ms
    Loading Channel Type: NaChannel
    [('m', 'm_inf'), ('h', 'h_inf')]
    Parsing: define_component NaChannel{
    from std.math import exp;
    from std.math import pow;
    from std.math import fabs;
    temp_adj  = 1.0;
    temp_adj_m = temp_adj;
    temp_adj_h = temp_adj;
    g =  GMAX * GATEPROP;
    I =  g * ( ((V)) - (VREV) );
    GATEPROP = m*m*m*h;
    m_alpha =  ({1.000000} * ( (((V )/{1mV}) - {-40.000000}) / {10.000000}) / (1 - exp( -1.0 * ((((V )/{1mV}) - {-40.000000})/{10.000000}) )) ) * (1/{1ms});
    m_beta =  ( {4.000000} * exp ( 1.0 * (((V )/{1mV})- {-65.000000})/{-18.000000} ) ) * (1/{1ms});
    m_tau =  1/(temp_adj_m* (m_alpha+m_beta));
    m_inf =  m_alpha/(m_alpha+m_beta);
    m' = (m_inf-m)/(m_tau);
    h_alpha =  ( {0.070000} * exp ( 1.0 * (((V )/{1mV})- {-65.000000})/{-20.000000} ) ) * (1/{1ms});
    h_beta =  ( (1 * {1.000000}) / ( 1.0 + exp ( (((V )/{1mV}) - {-35.000000})/{-10.000000}  ) ) ) * (1/{1ms});
    h_tau =  1/(temp_adj_h* (h_alpha+h_beta));
    h_inf =  h_alpha/(h_alpha+h_beta);
    h' = (h_inf-h)/(h_tau);
    initial {
    m=0.0;
    h=0.0;
    };
    <=> PARAMETER    GMAX : (S/m2);
    <=> PARAMETER    VREV : (mV);
    <=> OUTPUT       I :(A/m2)    METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} };
    <=> INPUT        V:(V)       METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} };
    <=> INPUT        celsius :(K) METADATA {"mf":{"role":"TEMPERATURE"} };
    };
    p_lhs! <ConstValue [id:82162384] Value: '1.0' >
    p_lhs! <Symbol Proxy: 4926313>
    p_lhs! <Symbol Proxy: 4926313>
    p_lhs! <MulOp [id:82162832] [??] >
    p_lhs! <MulOp [id:82163344] [??] >
    p_lhs! <MulOp [id:82163472] [??] >
    p_lhs! <MulOp [id:82165520] [??] >
    p_lhs! <MulOp [id:82144976] [??] >
    p_lhs! <DivOp [id:82159312] [??] >
    p_lhs! <DivOp [id:82158032] [??] >
    p_lhs! <DivOp [id:82158160] [??] >
    p_lhs! <MulOp [id:82161040] [??] >
    p_lhs! <MulOp [id:82131088] [??] >
    p_lhs! <DivOp [id:82132816] [??] >
    p_lhs! <DivOp [id:82132944] [??] >
    p_lhs! <DivOp [id:82130448] [??] >
    p_lhs! <ConstValue [id:82133136] Value: '0.0' >
    p_lhs! <ConstValue [id:82133072] Value: '0.0' >
    Parsing: (S/m2)
    Parsing: (mV)
    Parsing: (A/m2)
    Parsing: (V)
    Parsing: (K)
    Parsing: 120 mS/cm2
    Parsing: 50 mV
    Parsing: 120 S/m2
    Parsing: 50 V
    CHECKING
    <Parameter [id:82136720] Symbol: 'VREV' >
    VREV
    iii 1.0 kg*m**2/(s**3*A) <class 'quantities.quantity.Quantity'>
    iiii 0.05 kg*m**2/(s**3*A) <class 'quantities.quantity.Quantity'>
    OK
    
    CHECKING
    <Parameter [id:82136336] Symbol: 'GMAX' >
    GMAX
    iii 1.0 s**3*A**2/(kg*m**4) <class 'quantities.quantity.Quantity'>
    iiii 1200.0 s**3*A**2/(kg*m**4) <class 'quantities.quantity.Quantity'>
    OK
    
    Output <StateVariable [id:82132176] Symbol: 'h' >
    None
    Output <StateVariable [id:82133392] Symbol: 'm' >
    None
    Output <AssignedVariable [id:82135696] Symbol: 'GATEPROP' >
    None
    Output <AssignedVariable [id:82134544] Symbol: 'I' >
    {u'mf': {u'role': u'TRANSMEMBRANECURRENT'}}
    Output <AssignedVariable [id:82134352] Symbol: 'g' >
    None
    Output <AssignedVariable [id:82135504] Symbol: 'h_alpha' >
    None
    Output <AssignedVariable [id:82135888] Symbol: 'h_beta' >
    None
    Output <AssignedVariable [id:82134928] Symbol: 'h_inf' >
    None
    Output <AssignedVariable [id:82134160] Symbol: 'h_tau' >
    None
    Output <AssignedVariable [id:82133776] Symbol: 'm_alpha' >
    None
    Output <AssignedVariable [id:82135312] Symbol: 'm_beta' >
    None
    Output <AssignedVariable [id:82133968] Symbol: 'm_inf' >
    None
    Output <AssignedVariable [id:82135120] Symbol: 'm_tau' >
    None
    input <SuppliedValue [id:82121296] Symbol: 'V' >
    {u'mf': {u'role': u'MEMBRANEVOLTAGE'}}
    h_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_beta <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_beta <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_beta <class 'neurounits.ast.astobjects.AssignedVariable'>
    g <class 'neurounits.ast.astobjects.AssignedVariable'>
    V <class 'neurounits.ast.astobjects.SuppliedValue'>
    VREV <class 'neurounits.ast.astobjects.Parameter'>
    m_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_beta <class 'neurounits.ast.astobjects.AssignedVariable'>
    T [<class 'neurounits.ast.astobjects.DivOp'>]
    V <class 'neurounits.ast.astobjects.SuppliedValue'>
    m <class 'neurounits.ast.astobjects.StateVariable'>
    m <class 'neurounits.ast.astobjects.StateVariable'>
    m <class 'neurounits.ast.astobjects.StateVariable'>
    h <class 'neurounits.ast.astobjects.StateVariable'>
    V <class 'neurounits.ast.astobjects.SuppliedValue'>
    T [<class 'neurounits.ast.astobjects.MulOp'>]
    V <class 'neurounits.ast.astobjects.SuppliedValue'>
    T [<class 'neurounits.ast.astobjects.DivOp'>]
    V <class 'neurounits.ast.astobjects.SuppliedValue'>
    GMAX <class 'neurounits.ast.astobjects.Parameter'>
    GATEPROP <class 'neurounits.ast.astobjects.AssignedVariable'>
    T [<class 'neurounits.ast.astobjects.DivOp'>]
    V <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:82135824] Symbol: GATEPROP >
    m <class 'neurounits.ast.astobjects.StateVariable'>
    m <class 'neurounits.ast.astobjects.StateVariable'>
    m <class 'neurounits.ast.astobjects.StateVariable'>
    h <class 'neurounits.ast.astobjects.StateVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:82134480] Symbol: g >
    GMAX <class 'neurounits.ast.astobjects.Parameter'>
    GATEPROP <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:82134672] Symbol: I >
    g <class 'neurounits.ast.astobjects.AssignedVariable'>
    V <class 'neurounits.ast.astobjects.SuppliedValue'>
    VREV <class 'neurounits.ast.astobjects.Parameter'>
    Writing assignment for:  <EqnAssignmentByRegime [id:82135440] Symbol: m_beta >
    T [<class 'neurounits.ast.astobjects.DivOp'>]
    V <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:82133904] Symbol: m_alpha >
    V <class 'neurounits.ast.astobjects.SuppliedValue'>
    T [<class 'neurounits.ast.astobjects.MulOp'>]
    V <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:82135248] Symbol: m_tau >
    m_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_beta <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:82134096] Symbol: m_inf >
    m_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_alpha <class 'neurounits.ast.astobjectsWARNING: Symbol 'quantity_expr' is unreachable
    WARNING: Symbol 'quantity_term' is unreachable
    WARNING: Symbol 'quantity_factor' is unreachable
    Generating LALR tables
    WARNING: 1 shift/reduce conflict
    WARNING: 1 reduce/reduce conflict
    WARNING: reduce/reduce conflict in state 97 resolved using rule (empty -> <empty>)
    WARNING: rejected rule (alphanumtoken -> ALPHATOKEN) in state 97
    ConfigOoptins {'BATCHRUN': None}
    ['BLUESPEC', 'BLUESPECDIR', 'CDPATH', 'COLORTERM', 'DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DISPLAY', 'EAGLEDIR', 'ECAD', 'ECAD_LICENSES', 'ECAD_LOCAL', 'EDITOR', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'HISTFILE', 'HISTSIZE', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'KRB5CCNAME', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LD_RUN_PATH', 'LESS', 'LM_LICENSE_FILE', 'LOGNAME', 'LSCOLORS', 'MAKEFLAGS', 'MAKELEVEL', 'MANDATORY_PATH', 'MFLAGS', 'MGLS_LICENSE_FILE', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PRINTER', 'PWD', 'PYTHONPATH', 'QUARTUS_64BIT', 'QUARTUS_BIT_TYPE', 'QUARTUS_ROOTDIR', 'SHELL', 'SHLVL', 'SOPC_KIT_NIOS2', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TEMP', 'TERM', 'TMP', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CACHE_HOME', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Parsing: library std.math {
    pi = 3.141592653;
    e =  2.718281828;
    sin(x) = __sin__(x);
    cos(x) = __cos__(x);
    tan(x) = __tan__(x);
    sinh(x) = __sinh__(x);
    cosh(x) = __cosh__(x);
    tanh(x) = __tanh__(x);
    asin(x) = __asin__(x);
    acos(x) = __acos__(x);
    atan(x) = __atan__(x);
    atan2(x,y) = __atan2__(x=x,y=y);
    exp(x) = __exp__(x);
    ln(x) = __ln__(x);
    log2(x) = __log2__(x);
    log10(x) = __log10__(x);
    abs(x) = __abs__(x);
    pow(base,exp) = __pow__(base=base,exp=exp);
    ceil(x) = __ceil__(x);
    fabs(x) = __fabs__(x);
    floor(x) = __floor__(x);
    };
    library std.geom {
    from std.math import pi;
    area_of_sphere(r:{m}) = 4 * pi * r*r;
    volume_of_sphere(r:{m}) = 4.0/3.0 * pi * r*r *r;
    };
    library std.neuro {
    from std.math import pi,pow;
    r_a(R_i:{ohm m}, d:{m}) = (4*R_i)/(pi*d*d);
    space_constant(Rm:{ohm m2},Ri:{ohm m},d:{m}) = pow(base=(( (Rm/Ri)*(d/4) )/{1m2}),exp=0.5) * {1m};
    Rinf_sealed_end(Rm:{ohm m2},d:{m}) = (4*Rm/(pi*d*d) );
    RateConstant5(V:{V},a1:{s-1} ,a2:{V-1 s-1}, a3:{},a4:{V},a5:{V} ) = (a1 + a2*V)/(a3+std.math.exp( (V+a4)/a5) );
    };
    library std.physics {
    F = 96485.3365 coulomb mole-1;
    Na = 6.02214129e23 mole-1;
    k = 1.380648e-23 joule kelvin-1;
    e =  1.602176565 coulomb;
    R = 8.3144621 J mole-1 kelvin-1;
    };
    p_lhs! <ConstValue [id:74434896] Value: '3.141592653' >
    p_lhs! <ConstValue [id:74435216] Value: '2.718281828' >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74435856] {__sin__( <id:x:74435600>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74436432] {__cos__( <id:x:74435792>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74437072] {__tan__( <id:x:74436880>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74437648] {__sinh__( <id:x:74437008>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74438224] {__cosh__( <id:x:74437584>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74438800] {__tanh__( <id:x:74438160>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74439376] {__asin__( <id:x:74438736>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74439952] {__acos__( <id:x:74439312>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74440528] {__atan__( <id:x:74439888>)} >
    p_lhs! params: {'y': <FunctionDefParameterInstantiation: y >, 'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74502736] {__atan2__( <id:y:74502608,x:74502672>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74503504] {__exp__( <id:x:74502928>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74504080] {__ln__( <id:x:74503440>)} >
    p_lhs! params: {'x': <FuWARNING: Symbol 'ns_dot_name' is unreachable
    WARNING: Symbol 'time_derivative' is unreachable
    WARNING: Symbol 'ns_name_list' is unreachable
    WARNING: Symbol 'import_target_list' is unreachable
    WARNING: Symbol 'compound_line' is unreachable
    WARNING: Symbol 'multiport_direction' is unreachable
    WARNING: Symbol 'on_transition' is unreachable
    WARNING: Symbol 'quantity_expr' is unreachable
    WARNING: Symbol 'nineml_file' is unreachable
    WARNING: Symbol 'rv_modes' is unreachable
    WARNING: Symbol 'quantity_term' is unreachable
    WARNING: Symbol 'func_call_params_l3' is unreachable
    WARNING: Symbol 'componentlinecontents' is unreachable
    WARNING: Symbol 'function_def_param' is unreachable
    WARNING: Symbol 'open_transition_scope' is unreachable
    WARNING: Symbol 'compoundport_event_param' is unreachable
    WARNING: Symbol 'magnitude' is unreachable
    WARNING: Symbol 'transition_actions' is unreachable
    WARNING: Symbol 'event_call_param_l3' is unreachable
    WARNING: Symbol 'library_name' is unreachable
    WARNING: Symbol 'bool_term' is unreachable
    WARNING: Symbol 'localsymbol' is unreachable
    WARNING: Symbol 'open_funcdef_scope' is unreachable
    WARNING: Symbol 'externalsymbol' is unreachable
    WARNING: Symbol 'function_call_l3' is unreachable
    WARNING: Symbol 'regime_block' is unreachable
    WARNING: Symbol 'libraryline' is unreachable
    WARNING: Symbol 'import' is unreachable
    WARNING: Symbol 'library_def' is unreachable
    WARNING: Symbol 'component_name' is unreachable
    WARNING: Symbol 'compound_port_def' is unreachable
    WARNING: Symbol 'rhs_term' is unreachable
    WARNING: Symbol 'ar_model' is unreachable
    WARNING: Symbol 'compound_port_def_line' is unreachable
    WARNING: Symbol 'librarycontents' is unreachable
    WARNING: Symbol 'on_event_def_param' is unreachable
    WARNING: Symbol 'rhs_generic' is unreachable
    WARNING: Symbol 'random_variable' is unreachable
    WARNING: Symbol 'compoundcontents' is unreachable
    WARNING: Symbol 'crosses_expr' is unreachable
    WARNING: Symbol 'rt_name' is unreachable
    WARNING: Symbol 'lhs_symbol' is unreachable
    WARNING: Symbol 'component_def' is unreachable
    WARNING: Symbol 'transition_action' is unreachable
    WARNING: Symbol 'alphanumtoken' is unreachable
    WARNING: Symbol 'compound_port_def_contents' is unreachable
    WARNING: Symbol 'empty' is unreachable
    WARNING: Symbol 'namespace_def' is unreachable
    WARNING: Symbol 'compound_port_inst' is unreachable
    WARNING: Symbol 'bool_expr' is unreachable
    WARNING: Symbol 'namespace_name' is unreachable
    WARNING: Symbol 'regimecontents' is unreachable
    WARNING: Symbol 'rv_param' is unreachable
    WARNING: Symbol 'rtgraph_contents' is unreachable
    WARNING: Symbol 'namespaceblocks' is unreachable
    WARNING: Symbol 'compoundport_event_param_list' is unreachable
    WARNING: Symbol 'ns_name' is unreachable
    WARNING: Symbol 'initial_block' is unreachable
    WARNING: Symbol 'compound_port_def_direction_arrow' is unreachable
    WARNING: Symbol 'rv_mode' is unreachable
    WARNING: Symbol 'initial_expr_block' is unreachable
    WARNING: Symbol 'regime_name' is unreachable
    WARNING: Symbol 'top_level_block' is unreachable
    WARNING: Symbol 'compound_port_inst_constents' is unreachable
    WARNING: Symbol 'transition_to' is unreachable
    WARNING: Symbol 'on_event_def_params' is unreachable
    WARNING: Symbol 'regimecontentsline' is unreachable
    WARNING: Symbol 'namespace' is unreachable
    WARNING: Symbol 'rv_params' is unreachable
    WARNING: Symbol 'compound_component_def' is unreachable
    WARNING: Symbol 'function_def_params' is unreachable
    WARNING: Symbol 'function_def' is unreachable
    WARNING: Symbol 'assignment' is unreachable
    WARNING: Symbol 'componentcontents' is unreachable
    WARNING: Symbol 'rhs_variable' is unreachable
    WARNING: Symbol 'event_call_params_l3' is unreachable
    WARNING: Symbol 'compondport_inst_line' is unreachable
    WARNING: Symbol 'func_call_param_l3' is unreachable
    WARNING: Symbol 'rhs_symbol' is unreachable
    WARNING: Symbol 'quantity_factor' is unreachable
    WARNING: Symbol 'rhs_quantity_expr' is unreachable
    WARNING: Symbol 'quantity' is unreachable
    Generating LALR tables
    2013-11-30 18:14:42,354 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-11-30 18:14:42,354 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    nctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74504656] {__log2__( <id:x:74504592>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74505232] {__log10__( <id:x:74505168>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74505808] {__abs__( <id:x:74504016>)} >
    p_lhs! params: {'base': <FunctionDefParameterInstantiation: base >, 'exp': <FunctionDefParameterInstantiation: exp >}
    <FunctionDefBuiltInInstantiation [id:74445136] {__pow__( <id:base:74445072,exp:74444880>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74445904] {__ceil__( <id:x:74445328>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74446480] {__fabs__( <id:x:74445840>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74447056] {__floor__( <id:x:74446416>)} >
    p_lhs! <MulOp [id:74440912] [??] >
    p_lhs! <MulOp [id:76550480] [??] >
    p_lhs! <DivOp [id:76542864] [??] >
    p_lhs! <MulOp [id:76544464] [??] >
    p_lhs! <DivOp [id:76544016] [??] >
    p_lhs! <DivOp [id:76436048] [??] >
    p_lhs! <ConstValue [id:76538000] Value: '96485.3365e0 s  A  mol ' >
    p_lhs! <ConstValue [id:76541392] Value: '6.02214129e+23e0 mol ' >
    p_lhs! <ConstValue [id:76538320] Value: '1.380648e-23e0 m 2 kg  s  K ' >
    p_lhs! <ConstValue [id:76541776] Value: '1.602176565e0 s  A ' >
    p_lhs! <ConstValue [id:76541648] Value: '8.3144621e0 m 2 kg  s  K  mol ' >
    Parsing: ms
    Parsing: ms
    Parsing: mA/cm2
    Parsing: nA
    Parsing: mV
    Parsing: ms
    Parsing: K
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/7f/7fc5e77b2afd9894aa09fd6404e03569.bundle (81k) : 0.846 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    Executing: /opt/nrn//x86_64/bin/modlunit /local/scratch/mh735/tmp/morphforge/tmp/tmp_ff30b89cd7aeba7bffb466dd713985af.mod
    /local/scratch/mh735/tmp/morphforge/tmp/modbuild_5798
    Executing: /opt/nrn//x86_64/bin/nocmodl tmp_ff30b89cd7aeba7bffb466dd713985af.mod
    Executing: /opt/nrn//share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn//include/nrn"  -I"/opt/nrn//x86_64/lib"    -g -O2 -c -o tmp_ff30b89cd7aeba7bffb466dd713985af.lo tmp_ff30b89cd7aeba7bffb466dd713985af.c  
    Executing: /opt/nrn//share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_ff30b89cd7aeba7bffb466dd713985af.la  -rpath /opt/nrn//x86_64/libs  tmp_ff30b89cd7aeba7bffb466dd713985af.lo  -L/opt/nrn//x86_64/lib -L/opt/nrn//x86_64/lib  /opt/nrn//x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
    OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/opt/nrn//include/nrn -I/opt/nrn//x86_64/lib -g -O2 -c tmp_ff30b89cd7aeba7bffb466dd713985af.c  -fPIC -DPIC -o .libs/tmp_ff30b89cd7aeba7bffb466dd713985af.o
    
    OP2: libtool: link: gcc -shared  .libs/tmp_ff30b89cd7aeba7bffb466dd713985af.o   -Wl,-rpath -Wl,/opt/nrn/x86_64/lib -Wl,-rpath -Wl,/opt/nrn/x86_64/lib -L/opt/nrn//x86_64/lib /opt/nrn/x86_64/lib/libnrniv.so /opt/nrn/x86_64/lib/libnrnoc.so /opt/nrn/x86_64/lib/liboc.so /opt/nrn/x86_64/lib/libmemacs.so /opt/nrn/x86_64/lib/libnrnmpi.so /opt/nrn/x86_64/lib/libscopmath.so /opt/nrn/x86_64/lib/libsparse13.so -lreadline -lncurses /opt/nrn/x86_64/lib/libivoc.so /opt/nrn/x86_64/lib/libneuron_gnu.so /opt/nrn/x86_64/lib/libmeschach.so /opt/nrn/x86_64/lib/libsundials.so -lm -ldl    -pthread -Wl,-soname -Wl,tmp_ff30b89cd7aeba7bffb466dd713985af.so.0 -o .libs/tmp_ff30b89cd7aeba7bffb466dd713985af.so.0.0.0
    libtool: link: (cd ".libs" && rm -f "tmp_ff30b89cd7aeba7bffb466dd713985af.so.0" && ln -s "tmp_ff30b89cd7aeba7bffb466dd713985af.so.0.0.0" "tmp_ff30b89cd7aeba7bffb466dd713985af.so.0")
    libtool: link: (cd ".libs" && rm -f "tmp_ff30b89cd7aeba7bNEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    ffb466dd713985af.so" && ln -s "tmp_ff30b89cd7aeba7bffb466dd713985af.so.0.0.0" "tmp_ff30b89cd7aeba7bffb466dd713985af.so")
    libtool: link: ( cd ".libs" && rm -f "tmp_ff30b89cd7aeba7bffb466dd713985af.la" && ln -s "../tmp_ff30b89cd7aeba7bffb466dd713985af.la" "tmp_ff30b89cd7aeba7bffb466dd713985af.la" )
    
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_2e7b88320311eb54c5cd28c09e7ede5d.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_f0d9052fdfd19f720a7dd9bd9e578ef4.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_6b3bea54728962db867b1823185340ac.so
    	1 
    	1 
    	0.01 
    	0 
    	1 
    	50000 
    	1 
    Running Simulation
    Time for Extracting Data: (1 records) 0.000631093978882
    Running simulation : 0.624 seconds
    Post-processing : 0.011 seconds
    Entire load-run-save time : 1.481 seconds
    Suceeded
    WARNING: Symbol 'quantity_expr' is unreachable
    WARNING: Symbol 'quantity_term' is unreachable
    WARNING: Symbol 'quantity_factor' is unreachable
    Generating LALR tables
    WARNING: 1 shift/reduce conflict
    WARNING: 1 reduce/reduce conflict
    WARNING: reduce/reduce conflict in state 97 resolved using rule (empty -> <empty>)
    WARNING: rejected rule (alphanumtoken -> ALPHATOKEN) in state 97
    ConfigOoptins {'BATCHRUN': None}
    ['BLUESPEC', 'BLUESPECDIR', 'CDPATH', 'COLORTERM', 'DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DISPLAY', 'EAGLEDIR', 'ECAD', 'ECAD_LICENSES', 'ECAD_LOCAL', 'EDITOR', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'HISTFILE', 'HISTSIZE', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'KRB5CCNAME', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LD_RUN_PATH', 'LESS', 'LM_LICENSE_FILE', 'LOGNAME', 'LSCOLORS', 'MAKEFLAGS', 'MAKELEVEL', 'MANDATORY_PATH', 'MFLAGS', 'MGLS_LICENSE_FILE', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PRINTER', 'PWD', 'PYTHONPATH', 'QUARTUS_64BIT', 'QUARTUS_BIT_TYPE', 'QUARTUS_ROOTDIR', 'SHELL', 'SHLVL', 'SOPC_KIT_NIOS2', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TEMP', 'TERM', 'TMP', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CACHE_HOME', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Parsing: library std.math {
    pi = 3.141592653;
    e =  2.718281828;
    sin(x) = __sin__(x);
    cos(x) = __cos__(x);
    tan(x) = __tan__(x);
    sinh(x) = __sinh__(x);
    cosh(x) = __cosh__(x);
    tanh(x) = __tanh__(x);
    asin(x) = __asin__(x);
    acos(x) = __acos__(x);
    atan(x) = __atan__(x);
    atan2(x,y) = __atan2__(x=x,y=y);
    exp(x) = __exp__(x);
    ln(x) = __ln__(x);
    log2(x) = __log2__(x);
    log10(x) = __log10__(x);
    abs(x) = __abs__(x);
    pow(base,exp) = __pow__(base=base,exp=exp);
    ceil(x) = __ceil__(x);
    fabs(x) = __fabs__(x);
    floor(x) = __floor__(x);
    };
    library std.geom {
    from std.math import pi;
    area_of_sphere(r:{m}) = 4 * pi * r*r;
    volume_of_sphere(r:{m}) = 4.0/3.0 * pi * r*r *r;
    };
    library std.neuro {
    from std.math import pi,pow;
    r_a(R_i:{ohm m}, d:{m}) = (4*R_i)/(pi*d*d);
    space_constant(Rm:{ohm m2},Ri:{ohm m},d:{m}) = pow(base=(( (Rm/Ri)*(d/4) )/{1m2}),exp=0.5) * {1m};
    Rinf_sealed_end(Rm:{ohm m2},d:{m}) = (4*Rm/(pi*d*d) );
    RateConstant5(V:{V},a1:{s-1} ,a2:{V-1 s-1}, a3:{},a4:{V},a5:{V} ) = (a1 + a2*V)/(a3+std.math.exp( (V+a4)/a5) );
    };
    library std.physics {
    F = 96485.3365 coulomb mole-1;
    Na = 6.02214129e23 mole-1;
    k = 1.380648e-23 joule kelvin-1;
    e =  1.602176565 coulomb;
    R = 8.3144621 J mole-1 kelvin-1;
    };
    p_lhs! <ConstValue [id:46696784] Value: '3.141592653' >
    p_lhs! <ConstValue [id:46697104] Value: '2.718281828' >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:46697744] {__sin__( <id:x:46697488>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:46698320] {__cos__( <id:x:46697680>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:46707152] {__tan__( <id:x:46706960>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:46707728] {__sinh__( <id:x:46707088>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:46708304] {__cosh__( <id:x:46707664>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:46708880] {__tanh__( <id:x:46708240>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:46709456] {__asin__( <id:x:46708816>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:46710032] {__acos__( <id:x:46709392>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:46710608] {__atan__( <id:x:46709968>)} >
    p_lhs! params: {'y': <FunctionDefParameterInstantiation: y >, 'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:46703184] {__atan2__( <id:y:46703056,x:46703120>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:46703952] {__exp__( <id:x:46703376>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:46704528] {__ln__( <id:x:46703888>)} >
    p_lhs! params: {'x': <FuWARNING: Symbol 'ns_dot_name' is unreachable
    WARNING: Symbol 'time_derivative' is unreachable
    WARNING: Symbol 'ns_name_list' is unreachable
    WARNING: Symbol 'import_target_list' is unreachable
    WARNING: Symbol 'compound_line' is unreachable
    WARNING: Symbol 'multiport_direction' is unreachable
    WARNING: Symbol 'on_transition' is unreachable
    WARNING: Symbol 'quantity_expr' is unreachable
    WARNING: Symbol 'nineml_file' is unreachable
    WARNING: Symbol 'rv_modes' is unreachable
    WARNING: Symbol 'quantity_term' is unreachable
    WARNING: Symbol 'func_call_params_l3' is unreachable
    WARNING: Symbol 'componentlinecontents' is unreachable
    WARNING: Symbol 'function_def_param' is unreachable
    WARNING: Symbol 'open_transition_scope' is unreachable
    WARNING: Symbol 'compoundport_event_param' is unreachable
    WARNING: Symbol 'magnitude' is unreachable
    WARNING: Symbol 'transition_actions' is unreachable
    WARNING: Symbol 'event_call_param_l3' is unreachable
    WARNING: Symbol 'library_name' is unreachable
    WARNING: Symbol 'bool_term' is unreachable
    WARNING: Symbol 'localsymbol' is unreachable
    WARNING: Symbol 'open_funcdef_scope' is unreachable
    WARNING: Symbol 'externalsymbol' is unreachable
    WARNING: Symbol 'function_call_l3' is unreachable
    WARNING: Symbol 'regime_block' is unreachable
    WARNING: Symbol 'libraryline' is unreachable
    WARNING: Symbol 'import' is unreachable
    WARNING: Symbol 'library_def' is unreachable
    WARNING: Symbol 'component_name' is unreachable
    WARNING: Symbol 'compound_port_def' is unreachable
    WARNING: Symbol 'rhs_term' is unreachable
    WARNING: Symbol 'ar_model' is unreachable
    WARNING: Symbol 'compound_port_def_line' is unreachable
    WARNING: Symbol 'librarycontents' is unreachable
    WARNING: Symbol 'on_event_def_param' is unreachable
    WARNING: Symbol 'rhs_generic' is unreachable
    WARNING: Symbol 'random_variable' is unreachable
    WARNING: Symbol 'compoundcontents' is unreachable
    WARNING: Symbol 'crosses_expr' is unreachable
    WARNING: Symbol 'rt_name' is unreachable
    WARNING: Symbol 'lhs_symbol' is unreachable
    WARNING: Symbol 'component_def' is unreachable
    WARNING: Symbol 'transition_action' is unreachable
    WARNING: Symbol 'alphanumtoken' is unreachable
    WARNING: Symbol 'compound_port_def_contents' is unreachable
    WARNING: Symbol 'empty' is unreachable
    WARNING: Symbol 'namespace_def' is unreachable
    WARNING: Symbol 'compound_port_inst' is unreachable
    WARNING: Symbol 'bool_expr' is unreachable
    WARNING: Symbol 'namespace_name' is unreachable
    WARNING: Symbol 'regimecontents' is unreachable
    WARNING: Symbol 'rv_param' is unreachable
    WARNING: Symbol 'rtgraph_contents' is unreachable
    WARNING: Symbol 'namespaceblocks' is unreachable
    WARNING: Symbol 'compoundport_event_param_list' is unreachable
    WARNING: Symbol 'ns_name' is unreachable
    WARNING: Symbol 'initial_block' is unreachable
    WARNING: Symbol 'compound_port_def_direction_arrow' is unreachable
    WARNING: Symbol 'rv_mode' is unreachable
    WARNING: Symbol 'initial_expr_block' is unreachable
    WARNING: Symbol 'regime_name' is unreachable
    WARNING: Symbol 'top_level_block' is unreachable
    WARNING: Symbol 'compound_port_inst_constents' is unreachable
    WARNING: Symbol 'transition_to' is unreachable
    WARNING: Symbol 'on_event_def_params' is unreachable
    WARNING: Symbol 'regimecontentsline' is unreachable
    WARNING: Symbol 'namespace' is unreachable
    WARNING: Symbol 'rv_params' is unreachable
    WARNING: Symbol 'compound_component_def' is unreachable
    WARNING: Symbol 'function_def_params' is unreachable
    WARNING: Symbol 'function_def' is unreachable
    WARNING: Symbol 'assignment' is unreachable
    WARNING: Symbol 'componentcontents' is unreachable
    WARNING: Symbol 'rhs_variable' is unreachable
    WARNING: Symbol 'event_call_params_l3' is unreachable
    WARNING: Symbol 'compondport_inst_line' is unreachable
    WARNING: Symbol 'func_call_param_l3' is unreachable
    WARNING: Symbol 'rhs_symbol' is unreachable
    WARNING: Symbol 'quantity_factor' is unreachable
    WARNING: Symbol 'rhs_quantity_expr' is unreachable
    WARNING: Symbol 'quantity' is unreachable
    Generating LALR tables
    2013-11-30 18:14:44,742 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-11-30 18:14:44,743 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    nctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:46705104] {__log2__( <id:x:46705040>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:46705680] {__log10__( <id:x:46705616>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:46706256] {__abs__( <id:x:46704464>)} >
    p_lhs! params: {'base': <FunctionDefParameterInstantiation: base >, 'exp': <FunctionDefParameterInstantiation: exp >}
    <FunctionDefBuiltInInstantiation [id:46711120] {__pow__( <id:base:46711056,exp:46710864>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:46711888] {__ceil__( <id:x:46711312>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:46712464] {__fabs__( <id:x:46711824>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:46713040] {__floor__( <id:x:46712400>)} >
    p_lhs! <MulOp [id:46719184] [??] >
    p_lhs! <MulOp [id:48767312] [??] >
    p_lhs! <DivOp [id:48731024] [??] >
    p_lhs! <MulOp [id:48732624] [??] >
    p_lhs! <DivOp [id:48732176] [??] >
    p_lhs! <DivOp [id:48788048] [??] >
    p_lhs! <ConstValue [id:48681104] Value: '96485.3365e0 s  A  mol ' >
    p_lhs! <ConstValue [id:48684496] Value: '6.02214129e+23e0 mol ' >
    p_lhs! <ConstValue [id:48681424] Value: '1.380648e-23e0 m 2 kg  s  K ' >
    p_lhs! <ConstValue [id:48684880] Value: '1.602176565e0 s  A ' >
    p_lhs! <ConstValue [id:48684752] Value: '8.3144621e0 m 2 kg  s  K  mol ' >
    Parsing: ms
    Parsing: ms
    Parsing: mA/cm2
    Parsing: nA
    Parsing: mV
    Parsing: ms
    Parsing: K
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/04/04c8cd744c89c5682cdc3080e7b86a4e.bundle (20k) : 0.850 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    Executing: /opt/nrn//x86_64/bin/modlunit /local/scratch/mh735/tmp/morphforge/tmp/tmp_aa4950b44f831595132d4996be87c8bd.mod
    /local/scratch/mh735/tmp/morphforge/tmp/modbuild_6227
    Executing: /opt/nrn//x86_64/bin/nocmodl tmp_aa4950b44f831595132d4996be87c8bd.mod
    Executing: /opt/nrn//share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn//include/nrn"  -I"/opt/nrn//x86_64/lib"    -g -O2 -c -o tmp_aa4950b44f831595132d4996be87c8bd.lo tmp_aa4950b44f831595132d4996be87c8bd.c  
    Executing: /opt/nrn//share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_aa4950b44f831595132d4996be87c8bd.la  -rpath /opt/nrn//x86_64/libs  tmp_aa4950b44f831595132d4996be87c8bd.lo  -L/opt/nrn//x86_64/lib -L/opt/nrn//x86_64/lib  /opt/nrn//x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
    OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/opt/nrn//include/nrn -I/opt/nrn//x86_64/lib -g -O2 -c tmp_aa4950b44f831595132d4996be87c8bd.c  -fPIC -DPIC -o .libs/tmp_aa4950b44f831595132d4996be87c8bd.o
    
    OP2: libtool: link: gcc -shared  .libs/tmp_aa4950b44f831595132d4996be87c8bd.o   -Wl,-rpath -Wl,/opt/nrn/x86_64/lib -Wl,-rpath -Wl,/opt/nrn/x86_64/lib -L/opt/nrn//x86_64/lib /opt/nrn/x86_64/lib/libnrniv.so /opt/nrn/x86_64/lib/libnrnoc.so /opt/nrn/x86_64/lib/liboc.so /opt/nrn/x86_64/lib/libmemacs.so /opt/nrn/x86_64/lib/libnrnmpi.so /opt/nrn/x86_64/lib/libscopmath.so /opt/nrn/x86_64/lib/libsparse13.so -lreadline -lncurses /opt/nrn/x86_64/lib/libivoc.so /opt/nrn/x86_64/lib/libneuron_gnu.so /opt/nrn/x86_64/lib/libmeschach.so /opt/nrn/x86_64/lib/libsundials.so -lm -ldl    -pthread -Wl,-soname -Wl,tmp_aa4950b44f831595132d4996be87c8bd.so.0 -o .libs/tmp_aa4950b44f831595132d4996be87c8bd.so.0.0.0
    libtool: link: (cd ".libs" && rm -f "tmp_aa4950b44f831595132d4996be87c8bd.so.0" && ln -s "tmp_aa4950b44f831595132d4996be87c8bd.so.0.0.0" "tmp_aa4950b44f831595132d4996be87c8bd.so.0")
    libtool: link: (cd ".libs" && rm -f "tmp_aa4950b44f831595NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    132d4996be87c8bd.so" && ln -s "tmp_aa4950b44f831595132d4996be87c8bd.so.0.0.0" "tmp_aa4950b44f831595132d4996be87c8bd.so")
    libtool: link: ( cd ".libs" && rm -f "tmp_aa4950b44f831595132d4996be87c8bd.la" && ln -s "../tmp_aa4950b44f831595132d4996be87c8bd.la" "tmp_aa4950b44f831595132d4996be87c8bd.la" )
    
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_93beb3592d2be6b8a6884f9f5cda6c23.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_a290c9a645340023c23922c59afedba8.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_f0d9052fdfd19f720a7dd9bd9e578ef4.so
    	1 
    	1 
    	0.01 
    	0 
    	1 
    	50000 
    	1 
    Running Simulation
    Time for Extracting Data: (1 records) 0.00062894821167
    Running simulation : 0.563 seconds
    Post-processing : 0.005 seconds
    Entire load-run-save time : 1.418 seconds
    Suceeded
    .AssignedVariable'>
    m_beta <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:82136016] Symbol: h_beta >
    T [<class 'neurounits.ast.astobjects.DivOp'>]
    V <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:82135632] Symbol: h_alpha >
    T [<class 'neurounits.ast.astobjects.DivOp'>]
    V <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:82134288] Symbol: h_tau >
    h_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_beta <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:82135056] Symbol: h_inf >
    h_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_beta <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_inf <class 'neurounits.ast.astobjects.AssignedVariable'>
    h <class 'neurounits.ast.astobjects.StateVariable'>
    h_tau <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_inf <class 'neurounits.ast.astobjects.AssignedVariable'>
    m <class 'neurounits.ast.astobjects.StateVariable'>
    m_tau <class 'neurounits.ast.astobjects.AssignedVariable'>
    Loading Channel Type: KConductance
    Loading Channel Type: NaChannel
    Loading Channel Type: KConductance
    Parsing: define_component chlstd_hh_na {
    from std.math import exp;
    i = g * (v-erev) * m**3*h;
    minf = m_alpha_rate / (m_alpha_rate + m_beta_rate);
    mtau = 1.0 / (m_alpha_rate + m_beta_rate);
    m' = (minf-m) / mtau;
    hinf = h_alpha_rate / (h_alpha_rate + h_beta_rate);
    htau = 1.0 / (h_alpha_rate + h_beta_rate);
    h' = (hinf-h) / htau;
    StdFormAB(V, a1, a2, a3, a4, a5) = (a1 + a2*V)/(a3+exp((V+a4)/a5));
    m_alpha_rate = StdFormAB(V=v, a1=m_a1, a2=m_a2, a3=m_a3, a4=m_a4, a5=m_a5);
    m_beta_rate =  StdFormAB(V=v, a1=m_b1, a2=m_b2, a3=m_b3, a4=m_b4, a5=m_b5);
    h_alpha_rate = StdFormAB(V=v, a1=h_a1, a2=h_a2, a3=h_a3, a4=h_a4, a5=h_a5);
    h_beta_rate =  StdFormAB(V=v, a1=h_b1, a2=h_b2, a3=h_b3, a4=h_b4, a5=h_b5);
    m_a1 = {-4.00 ms-1};
    m_a2 = {-0.10 mV-1 ms-1};
    m_a3 = -1.00;
    m_a4 = {40.00 mV};
    m_a5 = {-10.00 mV};
    m_b1 = {4.00 ms-1};
    m_b2 = {0.00 mV-1 ms-1};
    m_b3 = {0.00};
    m_b4 = {65.00 mV};
    m_b5 = {18.00 mV};
    h_a1 = {0.07 ms-1};
    h_a2 = {0.00 mV-1 ms-1};
    h_a3 = {0.00};
    h_a4 = {65.00 mV};
    h_a5 = {20.00 mV};
    h_b1 = {1.00  ms-1};
    h_b2 = {0.00  mV-1 ms-1};
    h_b3 = {1.00};
    h_b4 = {35.00  mV};
    h_b5 = {-10.00 mV};
    sg = {120.0mS/cm2};
    erev = {50.0mV};
    <=> PARAMETER g:(S/m2);
    <=> OUTPUT    i:(A/m2)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} };
    <=> INPUT     v: V           METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} };
    };
    p_lhs! <MulOp [id:86359504] [??] >
    p_lhs! <DivOp [id:86359312] [??] >
    p_lhs! <DivOp [id:86357584] [??] >
    p_lhs! <DivOp [id:86358736] [??] >
    p_lhs! <DivOp [id:86357328] [??] >
    p_lhs! <DivOp [id:86358288] [??] >
    p_lhs! <DivOp [id:86357520] [??] >
    p_lhs! <DivOp [id:86362832] [??] >
    p_lhs! <FunctionDefUserInstantiation [id:86363792] [??] >
    p_lhs! <FunctionDefUserInstantiation [id:86274576] [??] >
    p_lhs! <FunctionDefUserInstantiation [id:86275408] [??] >
    p_lhs! <FunctionDefUserInstantiation [id:86276240] [??] >
    p_lhs! <ConstValue [id:86276688] Value: '-4.0e3 s ' >
    p_lhs! <ConstValue [id:86277328] Value: '-0.1e6 m  kg  s 2 A ' >
    p_lhs! <ConstValue [id:86277200] Value: '-1.0' >
    p_lhs! <ConstValue [id:86276752] Value: '40.0e-3 m 2 kg  s  A ' >
    p_lhs! <ConstValue [id:86277264] Value: '-10.0e-3 m 2 kg  s  A ' >
    p_lhs! <ConstValue [id:86365520] Value: '4.0e3 s ' >
    p_lhs! <ConstValue [id:86366096] Value: '0.0e6 m  kg  s 2 A ' >
    p_lhs! <ConstValue [id:86364752] Value: '0.0' >
    p_lhs! <ConstValue [id:86366032] Value: '65.0e-3 m 2 kg  s  A ' >
    p_lhs! <ConstValue [id:86364304] Value: '18.0e-3 m 2 kg  s  A ' >
    p_lhs! <ConstValue [id:86364560] Value: '0.07e3 s ' >
    p_lhs! <ConstValue [id:86367696] Value: '0.0e6 m  kg  s 2 A ' >
    p_lhs! <ConstValue [id:86367312] Value: '0.0' >
    p_lhs! <ConstValue [id:86367632] Value: '65.0e-3 m 2 kg  s  A ' >
    p_lhs! <ConstValue [id:86366800] Value: '20.0e-3 m 2 kg  s  A ' >
    p_lhs! <ConstValue [id:86366480] Value: '1.0e3 s ' >
    p_lhs! <ConstValue [id:86365136] Value: '0.0e6 m  kg  s 2 A ' >
    p_lhs! <ConstValue [id:86364432] Value: '1.0' >
    p_lhs! <ConstValue [id:86372944] Value: '35.0e-3 m 2 kg  s  A ' >
    p_lhs! <ConstValue [id:86372688] Value: '-10.0e-3 m 2 kg  s  A ' >
    p_lhs! <ConstValue [id:86373456] Value: '120.0e1 m  kg  s 3 A 2' >
    p_lhs! <ConstValue [id:86373072] Value: '50.0e-3 m 2 kg  s  A ' >
    Parsing: (S/m2)
    Parsing: (A/m2)
    Parsing: V
    CHECKING
    <Parameter [id:86375184] Symbol: 'g' >
    g
    iii 1.0 s**3*A**2/(kg*m**4) <class 'quantities.quantity.Quantity'>
    iiii 1200.0 s**3*A**2/(kg*m**4) <class 'quantities.quantity.Quantity'>
    OK
    
    Output <StateVariable [id:86375056] Symbol: 'h' >
    None
    Output <StateVariable [id:86374928] Symbol: 'm' >
    None
    Output <AssignedVariable [id:86376016] Symbol: 'h_alpha_rate' >
    None
    Output <AssignedVariable [id:86375824] Symbol: 'h_beta_rate' >
    None
    Output <AssignedVariable [id:86382096] Symbol: 'hinf' >
    None
    Output <AssignedVariable [id:86381904] Symbol: 'htau' >
    None
    Output <AssignedVariable [id:86383824] Symbol: 'i' >
    {u'mf': {u'role': u'TRANSMEMBRANECURRENT'}}
    Output <AssignedVariable [id:86381520] Symbol: 'm_alpha_rate' >
    None
    Output <AssignedVariable [id:86384208] Symbol: 'm_beta_rate' >
    None
    Output <AssignedVariable [id:86375440] Symbol: 'minf' >
    None
    Output <AssignedVariable [id:86376208] Symbol: 'mtau' >
    None
    input <SuppliedValue [id:86367760] Symbol: 'v' >
    {u'mf': {u'role': u'MEMBRANEVOLTAGE'}}
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    h_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    g <class 'neurounits.ast.astobjects.Parameter'>
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    m <class 'neurounits.ast.astobjects.StateVariable'>
    h <class 'neurounits.ast.astobjects.StateVariable'>
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    h_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:86376144] Symbol: h_alpha_rate >
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:86375952] Symbol: h_beta_rate >
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:86382224] Symbol: hinf >
    h_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:86384336] Symbol: m_beta_rate >
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:86381648] Symbol: m_alpha_rate >
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:86375568] Symbol: minf >
    m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:86383952] Symbol: i >
    g <class 'neurounits.ast.astobjects.Parameter'>
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    m <class 'neurounits.ast.astobjects.StateVariable'>
    h <class 'neurounits.ast.astobjects.StateVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:86376336] Symbol: mtau >
    m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:86382032] Symbol: htau >
    h_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
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
    Parsing: define_component chlstd_hh_lk {
    i = g * (v-erev);
    g = {0.3 mS/cm2};
    erev = -54.3 mV;
    <=> OUTPUT    i:(A/m2)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} };
    <=> INPUT     v: V          METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} };
    };
    p_lhs! <MulOp [id:86222096] [??] >
    p_lhs! <ConstValue [id:83712272] Value: '0.3e1 m  kg  s 3 A 2' >
    p_lhs! <ConstValue [id:83714000] Value: '-54.3e-3 m 2 kg  s  A ' >
    Parsing: (A/m2)
    Parsing: V
    Output <AssignedVariable [id:83712720] Symbol: 'i' >
    {u'mf': {u'role': u'TRANSMEMBRANECURRENT'}}
    input <SuppliedValue [id:83710608] Symbol: 'v' >
    {u'mf': {u'role': u'MEMBRANEVOLTAGE'}}
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:83712848] Symbol: i >
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    Parsing: define_component chlstd_hh_k {
    from std.math import exp;
    i = g * (v-erev) * n*n*n*n;
    ninf = n_alpha_rate / (n_alpha_rate + n_beta_rate);
    ntau = 1.0 / (n_alpha_rate + n_beta_rate);
    n' = (ninf-n) / ntau;
    StdFormAB(V, a1, a2, a3, a4, a5) = (a1 + a2*V)/(a3+exp((V+a4)/a5));
    n_alpha_rate = StdFormAB(V=v, a1=n_a1, a2=n_a2, a3=n_a3, a4=n_a4, a5=n_a5);
    n_beta_rate =  StdFormAB(V=v, a1=n_b1, a2=n_b2, a3=n_b3, a4=n_b4, a5=n_b5);
    n_a1 = {-0.55 ms-1};
    n_a2 = {-0.01 mV-1 ms-1};
    n_a3 = -1.00;
    n_a4 = {55.00 mV};
    n_a5 = {-10.00 mV};
    n_b1 = {0.125 ms-1};
    n_b2 = {0.00 mV-1 ms-1};
    n_b3 = {0.00};
    n_b4 = {65.00 mV};
    n_b5 = {80.00 mV};
    g = {36.0mS/cm2};
    erev = {-77.0mV};
    <=> OUTPUT    i:(A/m2)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} };
    <=> INPUT     v: V          METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} };
    };
    p_lhs! <MulOp [id:86388880] [??] >
    p_lhs! <DivOp [id:86312208] [??] >
    p_lhs! <DivOp [id:86312336] [??] >
    p_lhs! <DivOp [id:86311376] [??] >
    p_lhs! <DivOp [id:86367952] [??] >
    p_lhs! <FunctionDefUserInstantiation [id:83711184] [??] >
    p_lhs! <FunctionDefUserInstantiation [id:86221520] [??] >
    p_lhs! <ConstValue [id:86223376] Value: '-0.55e3 s ' >
    p_lhs! <ConstValue [id:86221712] Value: '-0.01e6 m  kg  s 2 A ' >
    p_lhs! <ConstValue [id:86224848] Value: '-1.0' >
    p_lhs! <ConstValue [id:86391056] Value: '55.0e-3 m 2 kg  s  A ' >
    p_lhs! <ConstValue [id:86391248] Value: '-10.0e-3 m 2 kg  s  A ' >
    p_lhs! <ConstValue [id:86390928] Value: '0.125e3 s ' >
    p_lhs! <ConstValue [id:86390992] Value: '0.0e6 m  kg  s 2 A ' >
    p_lhs! <ConstValue [id:86391312] Value: '0.0' >
    p_lhs! <ConstValue [id:86391184] Value: '65.0e-3 m 2 kg  s  A ' >
    p_lhs! <ConstValue [id:86391952] Value: '80.0e-3 m 2 kg  s  A ' >
    p_lhs! <ConstValue [id:86295888] Value: '36.0e1 m  kg  s 3 A 2' >
    p_lhs! <ConstValue [id:86295952] Value: '-77.0e-3 m 2 kg  s  A ' >
    Parsing: (A/m2)
    Parsing: V
    Output <StateVariable [id:86294992] Symbol: 'n' >
    None
    Output <AssignedVariable [id:86296784] Symbol: 'i' >
    {u'mf': {u'role': u'TRANSMEMBRANECURRENT'}}
    Output <AssignedVariable [id:86295440] Symbol: 'n_alpha_rate' >
    None
    Output <AssignedVariable [id:86298512] Symbol: 'n_beta_rate' >
    None
    Output <AssignedVariable [id:86298128] Symbol: 'ninf' >
    None
    Output <AssignedVariable [id:86294672] Symbol: 'ntau' >
    None
    input <SuppliedValue [id:86296272] Symbol: 'v' >
    {u'mf': {u'role': u'MEMBRANEVOLTAGE'}}
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    n_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    n <class 'neurounits.ast.astobjects.StateVariable'>
    n <class 'neurounits.ast.astobjects.StateVariable'>
    n <class 'neurounits.ast.astobjects.StateVariable'>
    n <class 'neurounits.ast.astobjects.StateVariable'>
    n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    n_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:86296016] Symbol: n_alpha_rateWARNING: Symbol 'quantity_expr' is unreachable
    WARNING: Symbol 'quantity_term' is unreachable
    WARNING: Symbol 'quantity_factor' is unreachable
    Generating LALR tables
    WARNING: 1 shift/reduce conflict
    WARNING: 1 reduce/reduce conflict
    WARNING: reduce/reduce conflict in state 97 resolved using rule (empty -> <empty>)
    WARNING: rejected rule (alphanumtoken -> ALPHATOKEN) in state 97
    ConfigOoptins {'BATCHRUN': None}
    ['BLUESPEC', 'BLUESPECDIR', 'CDPATH', 'COLORTERM', 'DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DISPLAY', 'EAGLEDIR', 'ECAD', 'ECAD_LICENSES', 'ECAD_LOCAL', 'EDITOR', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'HISTFILE', 'HISTSIZE', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'KRB5CCNAME', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LD_RUN_PATH', 'LESS', 'LM_LICENSE_FILE', 'LOGNAME', 'LSCOLORS', 'MAKEFLAGS', 'MAKELEVEL', 'MANDATORY_PATH', 'MFLAGS', 'MGLS_LICENSE_FILE', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PRINTER', 'PWD', 'PYTHONPATH', 'QUARTUS_64BIT', 'QUARTUS_BIT_TYPE', 'QUARTUS_ROOTDIR', 'SHELL', 'SHLVL', 'SOPC_KIT_NIOS2', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TEMP', 'TERM', 'TMP', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CACHE_HOME', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Parsing: library std.math {
    pi = 3.141592653;
    e =  2.718281828;
    sin(x) = __sin__(x);
    cos(x) = __cos__(x);
    tan(x) = __tan__(x);
    sinh(x) = __sinh__(x);
    cosh(x) = __cosh__(x);
    tanh(x) = __tanh__(x);
    asin(x) = __asin__(x);
    acos(x) = __acos__(x);
    atan(x) = __atan__(x);
    atan2(x,y) = __atan2__(x=x,y=y);
    exp(x) = __exp__(x);
    ln(x) = __ln__(x);
    log2(x) = __log2__(x);
    log10(x) = __log10__(x);
    abs(x) = __abs__(x);
    pow(base,exp) = __pow__(base=base,exp=exp);
    ceil(x) = __ceil__(x);
    fabs(x) = __fabs__(x);
    floor(x) = __floor__(x);
    };
    library std.geom {
    from std.math import pi;
    area_of_sphere(r:{m}) = 4 * pi * r*r;
    volume_of_sphere(r:{m}) = 4.0/3.0 * pi * r*r *r;
    };
    library std.neuro {
    from std.math import pi,pow;
    r_a(R_i:{ohm m}, d:{m}) = (4*R_i)/(pi*d*d);
    space_constant(Rm:{ohm m2},Ri:{ohm m},d:{m}) = pow(base=(( (Rm/Ri)*(d/4) )/{1m2}),exp=0.5) * {1m};
    Rinf_sealed_end(Rm:{ohm m2},d:{m}) = (4*Rm/(pi*d*d) );
    RateConstant5(V:{V},a1:{s-1} ,a2:{V-1 s-1}, a3:{},a4:{V},a5:{V} ) = (a1 + a2*V)/(a3+std.math.exp( (V+a4)/a5) );
    };
    library std.physics {
    F = 96485.3365 coulomb mole-1;
    Na = 6.02214129e23 mole-1;
    k = 1.380648e-23 joule kelvin-1;
    e =  1.602176565 coulomb;
    R = 8.3144621 J mole-1 kelvin-1;
    };
    p_lhs! <ConstValue [id:65395024] Value: '3.141592653' >
    p_lhs! <ConstValue [id:65395344] Value: '2.718281828' >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:65395984] {__sin__( <id:x:65395728>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:65396560] {__cos__( <id:x:65395920>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:65397200] {__tan__( <id:x:65397008>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:65397776] {__sinh__( <id:x:65397136>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:65398352] {__cosh__( <id:x:65397712>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:65398928] {__tanh__( <id:x:65398288>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:65399504] {__asin__( <id:x:65398864>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:65400080] {__acos__( <id:x:65399440>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:65400656] {__atan__( <id:x:65400016>)} >
    p_lhs! params: {'y': <FunctionDefParameterInstantiation: y >, 'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:65401424] {__atan2__( <id:y:65401296,x:65401360>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:65402192] {__exp__( <id:x:65401616>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:65402768] {__ln__( <id:x:65402128>)} >
    p_lhs! params: {'x': <FuWARNING: Symbol 'ns_dot_name' is unreachable
    WARNING: Symbol 'time_derivative' is unreachable
    WARNING: Symbol 'ns_name_list' is unreachable
    WARNING: Symbol 'import_target_list' is unreachable
    WARNING: Symbol 'compound_line' is unreachable
    WARNING: Symbol 'multiport_direction' is unreachable
    WARNING: Symbol 'on_transition' is unreachable
    WARNING: Symbol 'quantity_expr' is unreachable
    WARNING: Symbol 'nineml_file' is unreachable
    WARNING: Symbol 'rv_modes' is unreachable
    WARNING: Symbol 'quantity_term' is unreachable
    WARNING: Symbol 'func_call_params_l3' is unreachable
    WARNING: Symbol 'componentlinecontents' is unreachable
    WARNING: Symbol 'function_def_param' is unreachable
    WARNING: Symbol 'open_transition_scope' is unreachable
    WARNING: Symbol 'compoundport_event_param' is unreachable
    WARNING: Symbol 'magnitude' is unreachable
    WARNING: Symbol 'transition_actions' is unreachable
    WARNING: Symbol 'event_call_param_l3' is unreachable
    WARNING: Symbol 'library_name' is unreachable
    WARNING: Symbol 'bool_term' is unreachable
    WARNING: Symbol 'localsymbol' is unreachable
    WARNING: Symbol 'open_funcdef_scope' is unreachable
    WARNING: Symbol 'externalsymbol' is unreachable
    WARNING: Symbol 'function_call_l3' is unreachable
    WARNING: Symbol 'regime_block' is unreachable
    WARNING: Symbol 'libraryline' is unreachable
    WARNING: Symbol 'import' is unreachable
    WARNING: Symbol 'library_def' is unreachable
    WARNING: Symbol 'component_name' is unreachable
    WARNING: Symbol 'compound_port_def' is unreachable
    WARNING: Symbol 'rhs_term' is unreachable
    WARNING: Symbol 'ar_model' is unreachable
    WARNING: Symbol 'compound_port_def_line' is unreachable
    WARNING: Symbol 'librarycontents' is unreachable
    WARNING: Symbol 'on_event_def_param' is unreachable
    WARNING: Symbol 'rhs_generic' is unreachable
    WARNING: Symbol 'random_variable' is unreachable
    WARNING: Symbol 'compoundcontents' is unreachable
    WARNING: Symbol 'crosses_expr' is unreachable
    WARNING: Symbol 'rt_name' is unreachable
    WARNING: Symbol 'lhs_symbol' is unreachable
    WARNING: Symbol 'component_def' is unreachable
    WARNING: Symbol 'transition_action' is unreachable
    WARNING: Symbol 'alphanumtoken' is unreachable
    WARNING: Symbol 'compound_port_def_contents' is unreachable
    WARNING: Symbol 'empty' is unreachable
    WARNING: Symbol 'namespace_def' is unreachable
    WARNING: Symbol 'compound_port_inst' is unreachable
    WARNING: Symbol 'bool_expr' is unreachable
    WARNING: Symbol 'namespace_name' is unreachable
    WARNING: Symbol 'regimecontents' is unreachable
    WARNING: Symbol 'rv_param' is unreachable
    WARNING: Symbol 'rtgraph_contents' is unreachable
    WARNING: Symbol 'namespaceblocks' is unreachable
    WARNING: Symbol 'compoundport_event_param_list' is unreachable
    WARNING: Symbol 'ns_name' is unreachable
    WARNING: Symbol 'initial_block' is unreachable
    WARNING: Symbol 'compound_port_def_direction_arrow' is unreachable
    WARNING: Symbol 'rv_mode' is unreachable
    WARNING: Symbol 'initial_expr_block' is unreachable
    WARNING: Symbol 'regime_name' is unreachable
    WARNING: Symbol 'top_level_block' is unreachable
    WARNING: Symbol 'compound_port_inst_constents' is unreachable
    WARNING: Symbol 'transition_to' is unreachable
    WARNING: Symbol 'on_event_def_params' is unreachable
    WARNING: Symbol 'regimecontentsline' is unreachable
    WARNING: Symbol 'namespace' is unreachable
    WARNING: Symbol 'rv_params' is unreachable
    WARNING: Symbol 'compound_component_def' is unreachable
    WARNING: Symbol 'function_def_params' is unreachable
    WARNING: Symbol 'function_def' is unreachable
    WARNING: Symbol 'assignment' is unreachable
    WARNING: Symbol 'componentcontents' is unreachable
    WARNING: Symbol 'rhs_variable' is unreachable
    WARNING: Symbol 'event_call_params_l3' is unreachable
    WARNING: Symbol 'compondport_inst_line' is unreachable
    WARNING: Symbol 'func_call_param_l3' is unreachable
    WARNING: Symbol 'rhs_symbol' is unreachable
    WARNING: Symbol 'quantity_factor' is unreachable
    WARNING: Symbol 'rhs_quantity_expr' is unreachable
    WARNING: Symbol 'quantity' is unreachable
    Generating LALR tables
    2013-11-30 18:14:47,617 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-11-30 18:14:47,617 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    nctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:65403344] {__log2__( <id:x:65403280>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:65403920] {__log10__( <id:x:65403856>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:65404496] {__abs__( <id:x:65402704>)} >
    p_lhs! params: {'base': <FunctionDefParameterInstantiation: base >, 'exp': <FunctionDefParameterInstantiation: exp >}
    <FunctionDefBuiltInInstantiation [id:65433936] {__pow__( <id:base:65433872,exp:65433680>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:65434704] {__ceil__( <id:x:65434128>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:65435280] {__fabs__( <id:x:65434640>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:65435856] {__floor__( <id:x:65435216>)} >
    p_lhs! <MulOp [id:65429712] [??] >
    p_lhs! <MulOp [id:67432784] [??] >
    p_lhs! <DivOp [id:67404688] [??] >
    p_lhs! <MulOp [id:67406288] [??] >
    p_lhs! <DivOp [id:67405840] [??] >
    p_lhs! <DivOp [id:67494480] [??] >
    p_lhs! <ConstValue [id:67383440] Value: '96485.3365e0 s  A  mol ' >
    p_lhs! <ConstValue [id:67386832] Value: '6.02214129e+23e0 mol ' >
    p_lhs! <ConstValue [id:67383760] Value: '1.380648e-23e0 m 2 kg  s  K ' >
    p_lhs! <ConstValue [id:67387216] Value: '1.602176565e0 s  A ' >
    p_lhs! <ConstValue [id:67387088] Value: '8.3144621e0 m 2 kg  s  K  mol ' >
    Parsing: ms
    Parsing: ms
    Parsing: mA/cm2
    Parsing: nA
    Parsing: mV
    Parsing: ms
    Parsing: K
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/c7/c789d13ed8a12a331a3284ab5629373b.bundle (138k) : 0.858 seconds
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_b710d7b3064eaabef925f2922f85b448.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_9b74760aa9e9f61c04285c95f21d2945.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_6ee2fa9b55ab06b967686bbadb32a44b.so
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
    Time for Extracting Data: (7 records) 0.00348687171936
    Running simulation : 0.097 seconds
    Post-processing : 0.022 seconds
    Entire load-run-save time : 0.978 seconds
    Suceeded
     >
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:86265936] Symbol: n_beta_rate >
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:86298256] Symbol: ninf >
    n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    n_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:86294928] Symbol: ntau >
    n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    n_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:86296912] Symbol: i >
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    n <class 'neurounits.ast.astobjects.StateVariable'>
    n <class 'neurounits.ast.astobjects.StateVariable'>
    n <class 'neurounits.ast.astobjects.StateVariable'>
    n <class 'neurounits.ast.astobjects.StateVariable'>
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
    PlotManger saving:  _output/figures/assorted_10compareHHChls/{png,svg}/fig000_Autosave_figure_1.{png,svg}




