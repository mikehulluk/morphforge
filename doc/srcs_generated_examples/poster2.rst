
.. _example_poster2:

Example 22. Action potential propagation and synaptic transmission
==================================================================


Action potential propagation and synaptic transmission.
In this simulation, we create 3 neurons; Neuron 1 has an axon, and when the
soma is stimulated, we see the action potential propagate along it. Neuron 1
forms synapses onto cell2 and cell3 with different strengths and different
positions along the axon.

Code
~~~~

.. code-block:: python

    
    
    
    
    
    
    
    
    
    import matplotlib as mpl
    mpl.rcParams['font.size'] = 14
    
    
    from morphforge.stdimports import *
    from morphforgecontrib.stdimports import *
    
    # Create a cell:
    def build_cell(name, sim):
    
        my_morph = MorphologyBuilder.get_soma_axon_morph(axon_length=1500.0, axon_radius=0.3, soma_radius=10.0)
        my_cell = sim.create_cell(name=name, morphology=my_morph)
    
        na_chls = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Na", env=sim.environment)
        k_chls  = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="K",  env=sim.environment)
        lk_chls = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Lk", env=sim.environment)
    
        my_cell.apply_channel(lk_chls)
        my_cell.apply_channel(k_chls)
        my_cell.apply_channel(na_chls)
        my_cell.apply_channel(na_chls, where="axon", parameter_multipliers={'gScale':1.0})
        return my_cell
    
    
    # Create a simulation:
    env = NEURONEnvironment()
    sim = env.Simulation()
    
    # Two cells:
    cell1 = build_cell(name="cell1", sim=sim)
    cell2 = build_cell(name="cell2", sim=sim)
    cell3 = build_cell(name="cell3", sim=sim)
    
    
    # Connect with a synapse:
    simple_ampa_syn = """
    define_component syn_simple {
    
        g' = - g/g_tau
        i = gmax * (v-erev) * g
    
        gmax = 300pS * scale
        erev = 0mV
    
        g_tau = 10ms
        <=> INPUT     v: mV       METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
        <=> OUTPUT    i:(mA)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }
        <=> PARAMETER scale:()
        on on_event(){
            g = g + 1.0
        }
    }
    """
    
    
    post_syn_tmpl = env.PostSynapticMechTemplate(
            NeuroUnitEqnsetPostSynaptic,
            eqnset = simple_ampa_syn,
            default_parameters = { 'scale':1.0}
            )
    
    syn1 = sim.create_synapse(
            trigger =  env.SynapticTrigger(
                                        SynapticTriggerByVoltageThreshold,
                                            cell_location = CellLocator.get_location_at_distance_away_from_dummy(cell1, 300),
                                            voltage_threshold = qty("0:mV"),  delay=qty("0:ms"), 
                                       ),
            postsynaptic_mech = post_syn_tmpl.instantiate(cell_location = cell2.soma,), 
           )
    
    syn1 = sim.create_synapse(
            trigger =  env.SynapticTrigger(
                                        SynapticTriggerByVoltageThreshold,
                                        cell_location = CellLocator.get_location_at_distance_away_from_dummy(cell1, 700),
                                        voltage_threshold = qty("0:mV"),  delay = qty("0:ms"),
                                       ),
            postsynaptic_mech = post_syn_tmpl.instantiate(cell_location = cell3.soma, parameter_overrides={'scale':2.0} )  
           )
    
    # Record Voltages from axons:
    for loc in CellLocator.get_locations_at_distances_away_from_dummy(cell1, range(0, 1000, 50)):
        sim.record( what=StandardTags.Voltage, cell_location = loc, user_tags=['cell1'])
    sim.record(what=StandardTags.Voltage, cell_location = cell2.get_location("soma"), user_tags=['cell2'])
    sim.record(what=StandardTags.Voltage, cell_location = cell3.get_location("soma"), user_tags=['cell3'])
    
    # Create the stimulus and record the injected current:
    cc = sim.create_currentclamp(name="CC1", amp=qty("200:pA"), dur=qty("1:ms"), delay=qty("100:ms"), cell_location=cell1.get_location("soma"))
    sim.record(cc, what=StandardTags.Current)
    
    results = sim.run()
    TagViewer(results, timerange=(98, 120)*units.ms,
              fig_kwargs = {'figsize':(12, 10)},
              show=True,
              plots = [
                  TagPlot('Current', yunit=units.picoamp),
                  TagPlot('Voltage,cell1', yrange=(-80*units.mV, 50*units.mV), yunit=units.mV),
                  TagPlot('Voltage AND ANY{cell2,cell3}', yrange=(-70*units.mV, -55*units.mV), yunit=units.millivolt),
                 ],
               )
    
    
    




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/poster2_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/poster2_out1.png>`






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
    p_lhs! <ConstValue [id:65334736] Value: '3.141592653' >
    p_lhs! <ConstValue [id:65335056] Value: '2.718281828' >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:64786896] {__sin__( <id:x:64786640>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:64787472] {__cos__( <id:x:64786832>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:64788048] {__tan__( <id:x:64787408>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:64788624] {__sinh__( <id:x:64787984>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:64789200] {__cosh__( <id:x:64788560>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:64789776] {__tanh__( <id:x:64789136>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:64790352] {__asin__( <id:x:64789712>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:67883472] {__acos__( <id:x:67883280>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:67884048] {__atan__( <id:x:67883408>)} >
    p_lhs! params: {'y': <FunctionDefParameterInstantiation: y >, 'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:67884752] {__atan2__( <id:y:67884624,x:67884560>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:67885520] {__exp__( <id:x:67884944>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:67886096] {__ln__( <id:x:67885456>)} >
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
    2013-11-30 18:14:55,373 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-11-30 18:14:55,373 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
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
    p_lhs! <ConstValue [id:58779984] Value: '3.141592653' >
    p_lhs! <ConstValue [id:58780304] Value: '2.718281828' >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:58780944] {__sin__( <id:x:58780688>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:58781520] {__cos__( <id:x:58780880>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:58782160] {__tan__( <id:x:58781968>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:58782736] {__sinh__( <id:x:58782096>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:58783312] {__cosh__( <id:x:58782672>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:58783888] {__tanh__( <id:x:58783248>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:58784464] {__asin__( <id:x:58783824>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:58785040] {__acos__( <id:x:58784400>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:58785616] {__atan__( <id:x:58784976>)} >
    p_lhs! params: {'y': <FunctionDefParameterInstantiation: y >, 'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:58790480] {__atan2__( <id:y:58790352,x:58790416>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:58791248] {__exp__( <id:x:58790672>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:58791824] {__ln__( <id:x:58791184>)} >
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
    2013-11-30 18:14:57,128 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-11-30 18:14:57,128 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    nctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:58792400] {__log2__( <id:x:58792336>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:58792976] {__log10__( <id:x:58792912>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:58793552] {__abs__( <id:x:58791760>)} >
    p_lhs! params: {'base': <FunctionDefParameterInstantiation: base >, 'exp': <FunctionDefParameterInstantiation: exp >}
    <FunctionDefBuiltInInstantiation [id:58786128] {__pow__( <id:base:58786064,exp:58785872>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:58786896] {__ceil__( <id:x:58786320>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:58787472] {__fabs__( <id:x:58786832>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:58788048] {__floor__( <id:x:58787408>)} >
    p_lhs! <MulOp [id:58802384] [??] >
    p_lhs! <MulOp [id:60834128] [??] >
    p_lhs! <DivOp [id:60822416] [??] >
    p_lhs! <MulOp [id:60824016] [??] >
    p_lhs! <DivOp [id:60823568] [??] >
    p_lhs! <DivOp [id:60875344] [??] >
    p_lhs! <ConstValue [id:60825744] Value: '96485.3365e0 s  A  mol ' >
    p_lhs! <ConstValue [id:60829136] Value: '6.02214129e+23e0 mol ' >
    p_lhs! <ConstValue [id:60826064] Value: '1.380648e-23e0 m 2 kg  s  K ' >
    p_lhs! <ConstValue [id:60829520] Value: '1.602176565e0 s  A ' >
    p_lhs! <ConstValue [id:60829392] Value: '8.3144621e0 m 2 kg  s  K  mol ' >
    Parsing: ms
    Parsing: ms
    Parsing: mA/cm2
    Parsing: nA
    Parsing: mV
    Parsing: ms
    Parsing: K
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/d4/d47598b57084c4e809d7b1762a2f21a9.bundle (48k) : 0.826 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    Executing: /opt/nrn//x86_64/bin/modlunit /local/scratch/mh735/tmp/morphforge/tmp/tmp_996ea0955edffdc76efc867b859c24dd.mod
    /local/scratch/mh735/tmp/morphforge/tmp/modbuild_7654
    Executing: /opt/nrn//x86_64/bin/nocmodl tmp_996ea0955edffdc76efc867b859c24dd.mod
    Executing: /opt/nrn//share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn//include/nrn"  -I"/opt/nrn//x86_64/lib"    -g -O2 -c -o tmp_996ea0955edffdc76efc867b859c24dd.lo tmp_996ea0955edffdc76efc867b859c24dd.c  
    Executing: /opt/nrn//share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_996ea0955edffdc76efc867b859c24dd.la  -rpath /opt/nrn//x86_64/libs  tmp_996ea0955edffdc76efc867b859c24dd.lo  -L/opt/nrn//x86_64/lib -L/opt/nrn//x86_64/lib  /opt/nrn//x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
    OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/opt/nrn//include/nrn -I/opt/nrn//x86_64/lib -g -O2 -c tmp_996ea0955edffdc76efc867b859c24dd.c  -fPIC -DPIC -o .libs/tmp_996ea0955edffdc76efc867b859c24dd.o
    
    OP2: libtool: link: gcc -shared  .libs/tmp_996ea0955edffdc76efc867b859c24dd.o   -Wl,-rpath -Wl,/opt/nrn/x86_64/lib -Wl,-rpath -Wl,/opt/nrn/x86_64/lib -L/opt/nrn//x86_64/lib /opt/nrn/x86_64/lib/libnrniv.so /opt/nrn/x86_64/lib/libnrnoc.so /opt/nrn/x86_64/lib/liboc.so /opt/nrn/x86_64/lib/libmemacs.so /opt/nrn/x86_64/lib/libnrnmpi.so /opt/nrn/x86_64/lib/libscopmath.so /opt/nrn/x86_64/lib/libsparse13.so -lreadline -lncurses /opt/nrn/x86_64/lib/libivoc.so /opt/nrn/x86_64/lib/libneuron_gnu.so /opt/nrn/x86_64/lib/libmeschach.so /opt/nrn/x86_64/lib/libsundials.so -lm -ldl    -pthread -Wl,-soname -Wl,tmp_996ea0955edffdc76efc867b859c24dd.so.0 -o .libs/tmp_996ea0955edffdc76efc867b859c24dd.so.0.0.0
    libtool: link: (cd ".libs" && rm -f "tmp_996ea0955edffdc76efc867b859c24dd.so.0" && ln -s "tmp_996ea0955edffdc76efc867b859c24dd.so.0.0.0" "tmp_996ea0955edffdc76efc867b859c24dd.so.0")
    libtool: link: (cd ".libs" && rm -f "tmp_996ea0955edffdc7NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    6efc867b859c24dd.so" && ln -s "tmp_996ea0955edffdc76efc867b859c24dd.so.0.0.0" "tmp_996ea0955edffdc76efc867b859c24dd.so")
    libtool: link: ( cd ".libs" && rm -f "tmp_996ea0955edffdc76efc867b859c24dd.la" && ln -s "../tmp_996ea0955edffdc76efc867b859c24dd.la" "tmp_996ea0955edffdc76efc867b859c24dd.la" )
    
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_a6b7aa122cde4c77e4124024483c5e06.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_5f455b93d4139b3fb1c50075db474aa2.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_c455a0fdd64f6fb07344dfad99fd0d57.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_8884d1cb054ce45272b0cbf7bfe39fa4.so
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
    Running Simulation
    Time for Extracting Data: (23 records) 0.0109589099884
    Running simulation : 1.776 seconds
    Post-processing : 0.026 seconds
    Entire load-run-save time : 2.628 seconds
    Suceeded
    nctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:67886672] {__log2__( <id:x:67886608>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:67875024] {__log10__( <id:x:67874960>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:67875600] {__abs__( <id:x:67874896>)} >
    p_lhs! params: {'base': <FunctionDefParameterInstantiation: base >, 'exp': <FunctionDefParameterInstantiation: exp >}
    <FunctionDefBuiltInInstantiation [id:67876304] {__pow__( <id:base:67875088,exp:67876048>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:67877072] {__ceil__( <id:x:67876496>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:67877648] {__fabs__( <id:x:67877008>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:67878224] {__floor__( <id:x:67877584>)} >
    p_lhs! <MulOp [id:64735056] [??] >
    p_lhs! <MulOp [id:68813968] [??] >
    p_lhs! <DivOp [id:68815824] [??] >
    p_lhs! <MulOp [id:68809680] [??] >
    p_lhs! <DivOp [id:68815952] [??] >
    p_lhs! <DivOp [id:68826832] [??] >
    p_lhs! <ConstValue [id:68833680] Value: '96485.3365e0 s  A  mol ' >
    p_lhs! <ConstValue [id:68837072] Value: '6.02214129e+23e0 mol ' >
    p_lhs! <ConstValue [id:68834512] Value: '1.380648e-23e0 m 2 kg  s  K ' >
    p_lhs! <ConstValue [id:68836752] Value: '1.602176565e0 s  A ' >
    p_lhs! <ConstValue [id:68837328] Value: '8.3144621e0 m 2 kg  s  K  mol ' >
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
    Parsing: define_component syn_simple {
    g' = - g/g_tau;
    i = gmax * (v-erev) * g;
    gmax = 300pS * scale;
    erev = 0mV;
    g_tau = 10ms;
    <=> INPUT     v: mV       METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} };
    <=> OUTPUT    i:(mA)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} };
    <=> PARAMETER scale:();
    on on_event(){
    g = g + 1.0;
    };
    };
    p_lhs! <MulOp [id:75713168] [??] >
    p_lhs! <MulOp [id:75714320] [??] >
    p_lhs! <MulOp [id:75698832] [??] >
    p_lhs! <ConstValue [id:75698448] Value: '0.0e-3 m 2 kg  s  A ' >
    p_lhs! <ConstValue [id:75698512] Value: '10.0e-3 s ' >
    Parsing: mV
    Parsing: (mA)
    Parsing: ()
    <Parameter [id:75700432] Symbol: 'scale' >
    scale
    iii 1.0 dimensionless <class 'quantities.quantity.Quantity'>
    iiii 1.0 <type 'float'>
    Output <StateVariable [id:75659920] Symbol: 'g' >
    None
    Output <AssignedVariable [id:75700048] Symbol: 'gmax' >
    None
    Output <AssignedVariable [id:75692432] Symbol: 'i' >
    {u'mf': {u'role': u'TRANSMEMBRANECURRENT'}}
    input <SuppliedValue [id:75698704] Symbol: 'v' >
    {u'mf': {u'role': u'MEMBRANEVOLTAGE'}}
    gmax <class 'neurounits.ast.astobjects.AssignedVariable'>
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    g <class 'neurounits.ast.astobjects.StateVariable'>
    scale <class 'neurounits.ast.astobjects.Parameter'>
    Writing assignment for:  <EqnAssignmentByRegime [id:75699408] Symbol: gmax >
    scale <class 'neurounits.ast.astobjects.Parameter'>
    Writing assignment for:  <EqnAssignmentByRegime [id:75691728] Symbol: i >
    gmax <class 'neurounits.ast.astobjects.AssignedVariable'>
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    g <class 'neurounits.ast.astobjects.StateVariable'>
    g <class 'neurounits.ast.astobjects.StateVariable'>
    <neurounits.codegen.nmodl.MODLBuildParameters object at 0x4834090>
    g <class 'neurounits.ast.astobjects.StateVariable'>
    Parsing: ms
    Parsing: ms
    PlotManger saving:  _output/figures/poster2/{png,svg}/fig000_Autosave_figure_1.{png,svg}




