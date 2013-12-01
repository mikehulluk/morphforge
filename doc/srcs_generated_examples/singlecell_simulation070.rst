
.. _example_singlecell_simulation070:

Example 14. Visualising the internal states of a neuron
=======================================================


Visualising the internal states of a neuron

We look at the internal states of an HH neuron, and plot the properties on
different graphs.

Code
~~~~

.. code-block:: python

    
    
    
    
    
    
    from morphforge.stdimports import *
    from morphforgecontrib.stdimports import *
    
    
    
    # Create the environment:
    env = NEURONEnvironment()
    
    # Create the simulation:
    sim = env.Simulation()
    
    
    # Create a cell:
    morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
    m1 = MorphologyTree.fromDictionary(morphDict1)
    cell = sim.create_cell(name="Cell1", morphology=m1)
    
    
    lk_chl = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Lk", env=env)
    na_chl = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Na", env=env)
    k_chl = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="K", env=env)
    
    
    # Apply the channels uniformly over the cell
    cell.apply_channel( lk_chl)
    cell.apply_channel( na_chl)
    cell.apply_channel( k_chl)
    cell.set_passive( PassiveProperty.SpecificCapacitance, qty('1.0:uF/cm2'))
    
    # Get a cell_location on the cell:
    
    
    # Create the stimulus and record the injected current:
    cc = sim.create_currentclamp(name="Stim1", amp=qty("250:pA"), dur=qty("100:ms"), delay=qty("100:ms"), cell_location=cell.soma)
    sim.record(cc, what=StandardTags.Current)
    # Define what to record:
    sim.record(cell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = cell.soma)
    
    
    sim.record(lk_chl, cell_location = cell.soma, what=StandardTags.ConductanceDensity)
    sim.record(na_chl, cell_location = cell.soma, what=StandardTags.ConductanceDensity)
    sim.record(k_chl,  cell_location = cell.soma, what=StandardTags.ConductanceDensity)
    
    sim.record(lk_chl, cell_location = cell.soma, what=StandardTags.CurrentDensity)
    sim.record(na_chl, cell_location = cell.soma, what=StandardTags.CurrentDensity)
    sim.record(k_chl,  cell_location = cell.soma, what=StandardTags.CurrentDensity)
    
    
    sim.record(na_chl, cell_location = cell.soma, what=StandardTags.StateVariable, state="m")
    sim.record(na_chl, cell_location = cell.soma, what=StandardTags.StateVariable, state="h")
    sim.record(k_chl,  cell_location = cell.soma, what=StandardTags.StateVariable, state="n")
    
    
    # Also:
    
    
    # run the simulation
    results = sim.run()
    
    
    # Display the results, there is a lot of info for one graph, so lets split it up:
    TagViewer([results], timerange=(50, 250)*units.ms, show=False)
    
    
    TagViewer([results], timerange=(50, 250)*units.ms, show=False,
              plots = [
                           DefaultTagPlots.Voltage,
                           DefaultTagPlots.Current,
                           DefaultTagPlots.CurrentDensity,
                          ])
    
    
    TagViewer([results], timerange=(100, 120)*units.ms, show=True,
              plots = [
                           DefaultTagPlots.Voltage,
                           DefaultTagPlots.ConductanceDensity,
                           DefaultTagPlots.StateVariable,
                          ])
    




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation070_out2.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation070_out2.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation070_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation070_out1.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation070_out3.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation070_out3.png>`






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
    p_lhs! <ConstValue [id:50219856] Value: '3.141592653' >
    p_lhs! <ConstValue [id:50220176] Value: '2.718281828' >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:50220816] {__sin__( <id:x:50220560>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:53150096] {__cos__( <id:x:53149904>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:53150672] {__tan__( <id:x:53150032>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:53151248] {__sinh__( <id:x:53150608>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:53151824] {__cosh__( <id:x:53151184>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:53152400] {__tanh__( <id:x:53151760>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:53152976] {__asin__( <id:x:53152336>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:53153552] {__acos__( <id:x:53152912>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:50225552] {__atan__( <id:x:50225360>)} >
    p_lhs! params: {'y': <FunctionDefParameterInstantiation: y >, 'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:50226256] {__atan2__( <id:y:50226128,x:50226064>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:50227024] {__exp__( <id:x:50226448>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:50227600] {__ln__( <id:x:50226960>)} >
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
    2013-11-30 18:13:44,174 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-11-30 18:13:44,174 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
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
    p_lhs! <ConstValue [id:53422416] Value: '3.141592653' >
    p_lhs! <ConstValue [id:53422736] Value: '2.718281828' >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:53423376] {__sin__( <id:x:53423120>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:53423952] {__cos__( <id:x:53423312>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:53432784] {__tan__( <id:x:53432592>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:53433360] {__sinh__( <id:x:53432720>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:53433936] {__cosh__( <id:x:53433296>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:53434512] {__tanh__( <id:x:53433872>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:53435088] {__asin__( <id:x:53434448>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:53435664] {__acos__( <id:x:53435024>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:53436240] {__atan__( <id:x:53435600>)} >
    p_lhs! params: {'y': <FunctionDefParameterInstantiation: y >, 'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:53445200] {__atan2__( <id:y:53445072,x:53445136>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:53445968] {__exp__( <id:x:53445392>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:53446544] {__ln__( <id:x:53445904>)} >
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
    2013-11-30 18:13:45,800 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-11-30 18:13:45,800 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    nctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:53447120] {__log2__( <id:x:53447056>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:53447696] {__log10__( <id:x:53447632>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:53448272] {__abs__( <id:x:53446480>)} >
    p_lhs! params: {'base': <FunctionDefParameterInstantiation: base >, 'exp': <FunctionDefParameterInstantiation: exp >}
    <FunctionDefBuiltInInstantiation [id:53469520] {__pow__( <id:base:53469456,exp:53469264>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:53470288] {__ceil__( <id:x:53469712>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:53470864] {__fabs__( <id:x:53470224>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:53471440] {__floor__( <id:x:53470800>)} >
    p_lhs! <MulOp [id:53481680] [??] >
    p_lhs! <MulOp [id:55451984] [??] >
    p_lhs! <DivOp [id:55440272] [??] >
    p_lhs! <MulOp [id:55441872] [??] >
    p_lhs! <DivOp [id:55441424] [??] >
    p_lhs! <DivOp [id:55444048] [??] >
    p_lhs! <ConstValue [id:55611536] Value: '96485.3365e0 s  A  mol ' >
    p_lhs! <ConstValue [id:55614928] Value: '6.02214129e+23e0 mol ' >
    p_lhs! <ConstValue [id:55611856] Value: '1.380648e-23e0 m 2 kg  s  K ' >
    p_lhs! <ConstValue [id:55615312] Value: '1.602176565e0 s  A ' >
    p_lhs! <ConstValue [id:55615184] Value: '8.3144621e0 m 2 kg  s  K  mol ' >
    Parsing: ms
    Parsing: ms
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/ff/ff063f7c39f1951c9981090b0d13a191.bundle (13k) : 0.792 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_fd41464846adf37259cda2d7b8094d70.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_480e6f43fe3509862af7a0151bee591a.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_97e548415789729de2dc2824541ca53f.so
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
    Running Simulation
    Parsing: mA/cm2
    Parsing: mA/cm2
    Parsing: S/cm2
    Parsing: S/cm2
    Parsing: mA/cm2
    Parsing: S/cm2
    Time for Extracting Data: (11 records) 0.0155050754547
    Running simulation : 0.152 seconds
    Post-processing : 0.014 seconds
    Entire load-run-save time : 0.958 seconds
    Suceeded
    nctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:50228176] {__log2__( <id:x:50228112>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:50228752] {__log10__( <id:x:50228688>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:52768912] {__abs__( <id:x:50227536>)} >
    p_lhs! params: {'base': <FunctionDefParameterInstantiation: base >, 'exp': <FunctionDefParameterInstantiation: exp >}
    <FunctionDefBuiltInInstantiation [id:52769616] {__pow__( <id:base:52768976,exp:52769360>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:52770384] {__ceil__( <id:x:52769808>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:52770960] {__fabs__( <id:x:52770320>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:52771536] {__floor__( <id:x:52770896>)} >
    p_lhs! <MulOp [id:52317648] [??] >
    p_lhs! <MulOp [id:52335440] [??] >
    p_lhs! <DivOp [id:52338192] [??] >
    p_lhs! <MulOp [id:52320976] [??] >
    p_lhs! <DivOp [id:52319696] [??] >
    p_lhs! <DivOp [id:52208976] [??] >
    p_lhs! <ConstValue [id:52211472] Value: '96485.3365e0 s  A  mol ' >
    p_lhs! <ConstValue [id:52249232] Value: '6.02214129e+23e0 mol ' >
    p_lhs! <ConstValue [id:52249488] Value: '1.380648e-23e0 m 2 kg  s  K ' >
    p_lhs! <ConstValue [id:52251536] Value: '1.602176565e0 s  A ' >
    p_lhs! <ConstValue [id:52250576] Value: '8.3144621e0 m 2 kg  s  K  mol ' >
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
    
    ConductanceDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x39b7050>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x39af450>}
    
    ConductanceDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x39b7b90>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x39af450>}
    
    CurrentDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x39b7150>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x39af450>}
    
    CurrentDensity
    {'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x39b76d0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x39af450>}
    
    StateVariable
    {'state': 'm', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x39b72d0>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x39af450>}
    
    StateVariable
    {'state': 'h', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x39b7750>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x39af450>}
    
    StateVariable
    {'state': 'n', 'cell_location': <morphforge.simulation.base.core.celllocation.CellLocation object at 0x39b7850>, 'simulation': <morphforge.simulation.neuron.core.neuronsimulation.NEURONSimulation object at 0x39af450>}
    PlotManger saving:  _output/figures/singlecell_simulation070/{png,svg}/fig000_Autosave_figure_1.{png,svg}
    PlotManger saving:  _output/figures/singlecell_simulation070/{png,svg}/fig001_Autosave_figure_2.{png,svg}
    PlotManger saving:  _output/figures/singlecell_simulation070/{png,svg}/fig002_Autosave_figure_3.{png,svg}




