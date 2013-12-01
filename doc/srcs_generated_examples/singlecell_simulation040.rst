
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
    from morphforgecontrib.simulation.channels.hh_style.core.mmleak import StdChlLeak
    from morphforgecontrib.simulation.channels.hh_style.core.mmalphabeta import StdChlAlphaBeta
    
    
    
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


.. figure:: /srcs_generated_examples/images/singlecell_simulation040_out6.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation040_out6.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation040_out2.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation040_out2.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation040_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation040_out1.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation040_out4.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation040_out4.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation040_out5.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation040_out5.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation040_out3.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation040_out3.png>`






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
    p_lhs! <ConstValue [id:51461328] Value: '3.141592653' >
    p_lhs! <ConstValue [id:51461648] Value: '2.718281828' >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:51486928] {__sin__( <id:x:51462032>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:51487504] {__cos__( <id:x:51486864>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:51488080] {__tan__( <id:x:51487440>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:51488656] {__sinh__( <id:x:51488016>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:51489232] {__cosh__( <id:x:51488592>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:51489808] {__tanh__( <id:x:51489168>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:51490384] {__asin__( <id:x:51489744>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:51482832] {__acos__( <id:x:51490320>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:51483408] {__atan__( <id:x:51482768>)} >
    p_lhs! params: {'y': <FunctionDefParameterInstantiation: y >, 'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:51484112] {__atan2__( <id:y:51483984,x:51483920>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:51484880] {__exp__( <id:x:51484304>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:51485456] {__ln__( <id:x:51484816>)} >
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
    2013-11-30 18:13:20,169 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-11-30 18:13:20,169 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
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
    p_lhs! <ConstValue [id:63314256] Value: '3.141592653' >
    p_lhs! <ConstValue [id:63314576] Value: '2.718281828' >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:63315216] {__sin__( <id:x:63314960>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:63315792] {__cos__( <id:x:63315152>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:63353296] {__tan__( <id:x:63353104>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:63353872] {__sinh__( <id:x:63353232>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:63354448] {__cosh__( <id:x:63353808>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:63355024] {__tanh__( <id:x:63354384>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:63355600] {__asin__( <id:x:63354960>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:63356176] {__acos__( <id:x:63355536>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:63356752] {__atan__( <id:x:63356112>)} >
    p_lhs! params: {'y': <FunctionDefParameterInstantiation: y >, 'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:63328848] {__atan2__( <id:y:63328720,x:63328784>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:63329616] {__exp__( <id:x:63329040>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:63330192] {__ln__( <id:x:63329552>)} >
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
    2013-11-30 18:13:21,793 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-11-30 18:13:21,794 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    nctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:63330768] {__log2__( <id:x:63330704>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:63331344] {__log10__( <id:x:63331280>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:63331920] {__abs__( <id:x:63330128>)} >
    p_lhs! params: {'base': <FunctionDefParameterInstantiation: base >, 'exp': <FunctionDefParameterInstantiation: exp >}
    <FunctionDefBuiltInInstantiation [id:63332688] {__pow__( <id:base:63332624,exp:63332432>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:63333456] {__ceil__( <id:x:63332880>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:63334032] {__fabs__( <id:x:63333392>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:63334608] {__floor__( <id:x:63333968>)} >
    p_lhs! <MulOp [id:63324368] [??] >
    p_lhs! <MulOp [id:65302864] [??] >
    p_lhs! <DivOp [id:65311632] [??] >
    p_lhs! <MulOp [id:65313232] [??] >
    p_lhs! <DivOp [id:65312784] [??] >
    p_lhs! <DivOp [id:65339984] [??] >
    p_lhs! <ConstValue [id:65388688] Value: '96485.3365e0 s  A  mol ' >
    p_lhs! <ConstValue [id:65392080] Value: '6.02214129e+23e0 mol ' >
    p_lhs! <ConstValue [id:65389008] Value: '1.380648e-23e0 m 2 kg  s  K ' >
    p_lhs! <ConstValue [id:65392464] Value: '1.602176565e0 s  A ' >
    p_lhs! <ConstValue [id:65392336] Value: '8.3144621e0 m 2 kg  s  K  mol ' >
    Parsing: ms
    Parsing: ms
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/03/034422473ed892103454ee88ab9a2079.bundle (11k) : 0.803 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-51.0) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(9.19125) * S/m**2}
    
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_01a0996bbc60b0f6ccc56fc1fe23decf.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_66865290056d853214a4339e4e4b6b9e.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_12f4e83b7e2718e973deebd1a23b15e1.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_7600478d01e0b9510e7cb196c284fe70.so
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
    Time for Extracting Data: (2 records) 0.00104308128357
    Running simulation : 0.142 seconds
    Post-processing : 0.002 seconds
    Entire load-run-save time : 0.947 seconds
    Suceeded
    /usr/bin/pdflatex
    nctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:51486032] {__log2__( <id:x:51485968>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:51486608] {__log10__( <id:x:51486544>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:54067728] {__abs__( <id:x:54067536>)} >
    p_lhs! params: {'base': <FunctionDefParameterInstantiation: base >, 'exp': <FunctionDefParameterInstantiation: exp >}
    <FunctionDefBuiltInInstantiation [id:54068432] {__pow__( <id:base:54067792,exp:54068176>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:54069200] {__ceil__( <id:x:54068624>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:54069776] {__fabs__( <id:x:54069136>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:54070352] {__floor__( <id:x:54069712>)} >
    p_lhs! <MulOp [id:50844880] [??] >
    p_lhs! <MulOp [id:53597072] [??] >
    p_lhs! <DivOp [id:53599056] [??] >
    p_lhs! <MulOp [id:53533136] [??] >
    p_lhs! <DivOp [id:53532944] [??] >
    p_lhs! <DivOp [id:53555792] [??] >
    p_lhs! <ConstValue [id:53604496] Value: '96485.3365e0 s  A  mol ' >
    p_lhs! <ConstValue [id:53607888] Value: '6.02214129e+23e0 mol ' >
    p_lhs! <ConstValue [id:53604816] Value: '1.380648e-23e0 m 2 kg  s  K ' >
    p_lhs! <ConstValue [id:53608272] Value: '1.602176565e0 s  A ' >
    p_lhs! <ConstValue [id:53608144] Value: '8.3144621e0 m 2 kg  s  K  mol ' >
    Parsing: ms
    Parsing: ms
    Parsing: ms
    Parsing: ms
    Parsing: um2
    Parsing: uF/cm2
    Parsing: ms
    Warning: node 'Cell1', graph 'graphname' size too small for label
    Warning: node 'AnonObj0001', graph 'graphname' size too small for label
    
    [(100.0, array([ 1.,  0.,  0.])), (0.0, array([ 0.,  1.,  0.])), (0.0, array([ 0.,  0.,  1.]))]
    Saving figure /home/mh735/.mredoc/build/figs/opfile0002
    Saving figure /home/mh735/.mredoc/build/figs/opfile0003
    Saving figure /home/mh735/.mredoc/build/figs/opfile0004
    Saving figure /home/mh735/.mredoc/build/figs/opfile0005
    PlotManger saving:  _output/figures/singlecell_simulation040/{png,svg}/fig000_Autosave_figure_1.{png,svg}
    PlotManger saving:  _output/figures/singlecell_simulation040/{png,svg}/fig001_Autosave_figure_2.{png,svg}
    PlotManger saving:  _output/figures/singlecell_simulation040/{png,svg}/fig002_Autosave_figure_3.{png,svg}
    PlotManger saving:  _output/figures/singlecell_simulation040/{png,svg}/fig003_Autosave_figure_4.{png,svg}
    PlotManger saving:  _output/figures/singlecell_simulation040/{png,svg}/fig004_Autosave_figure_5.{png,svg}
    Saving figure /home/mh735/.mredoc/build/figs/opfile0006
    Tex File: /home/mh735/.mredoc/build/pdflatex/eqnset.tex
    Successfully written PDF to:  /local/scratch/mh735/tmp/morphforge/tmp/mf_doc_build/singlecell_simulation040.py.pdf
    PlotManger saving:  _output/figures/singlecell_simulation040/{png,svg}/fig005_Autosave_figure_6.{png,svg}




