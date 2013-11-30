
.. _example_singlecell_simulation060:

Example 12. Visualising action potential propagation along an axon
==================================================================


Visualising action potential propagation along an axon
In this simulation, we create a cell with a long axon. We put HH-channels over its surface and give it a short current injection into the soma. We look at the voltage at various points along the axon, and see it propogate.

Code
~~~~

.. code-block:: python

    
    
    
    
    
    
    
    
    from morphforge.stdimports import *
    from morphforgecontrib.simulation.channels.hh_style.core.mmleak import StdChlLeak
    from morphforgecontrib.simulation.channels.hh_style.core.mmalphabeta import StdChlAlphaBeta
    
    
    # Create the environment:
    env = NEURONEnvironment()
    
    # Create the simulation:
    sim = env.Simulation()
    
    # Create a cell:
    morph = MorphologyBuilder.get_soma_axon_morph(axon_length=3000.0, axon_radius=0.15, soma_radius=9.0, axon_sections=20)
    cell = sim.create_cell(name="Cell1", morphology=morph)
    
    
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
    
    
    # Apply the channels uniformly over the cell
    cell.apply_channel( lk_chl)
    cell.apply_channel( na_chl)
    cell.apply_channel( k_chl)
    cell.set_passive( PassiveProperty.SpecificCapacitance, qty('1.0:uF/cm2'))
    
    
    # Create the stimulus and record the injected current:
    cc = sim.create_currentclamp(name="Stim1", amp=qty("250:pA"), dur=qty("5:ms"), delay=qty("100:ms"), cell_location=cell.soma)
    sim.record(cc, what=StandardTags.Current)
    
    
    
    # To record along the axon, we create a set of 'CellLocations', at the distances
    # specified (start, stop,
    for cell_location in CellLocator.get_locations_at_distances_away_from_dummy(cell=cell, distances=range(9, 3000, 100)):
    
        print " -- ", cell_location.section
        print " -- ", cell_location.sectionpos
        print " -- ", cell_location.get_3d_position()
    
        # Create a path along the morphology from the centre of the
        # Soma
        path = MorphPath(cell.soma, cell_location)
        print "Distance to Soma Centre:", path.get_length()
    
        sim.record(cell, what=StandardTags.Voltage, cell_location=cell_location, description="Distance Recording at %0.0f (um)"% path.get_length())
    
    
    # Define what to record:
    sim.record(cell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = cell.soma)
    
    # run the simulation
    results = sim.run()
    
    # Display the results:
    TagViewer([results], timerange=(97.5, 140)*units.ms)
    




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation060_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation060_out1.png>`






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
    p_lhs! <ConstValue [id:74460880] Value: '3.141592653' >
    p_lhs! <ConstValue [id:77377616] Value: '2.718281828' >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:77378256] {__sin__( <id:x:77378000>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:77378832] {__cos__( <id:x:77378192>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:77379408] {__tan__( <id:x:77378768>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:77379984] {__sinh__( <id:x:77379344>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:77380560] {__cosh__( <id:x:77379920>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:77381136] {__tanh__( <id:x:77380496>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74449040] {__asin__( <id:x:77381072>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74449616] {__acos__( <id:x:74448976>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74450192] {__atan__( <id:x:74449552>)} >
    p_lhs! params: {'y': <FunctionDefParameterInstantiation: y >, 'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74450896] {__atan2__( <id:y:74450768,x:74450704>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74451664] {__exp__( <id:x:74451088>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74452240] {__ln__( <id:x:74451600>)} >
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
    nctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74452816] {__log2__( <id:x:74452752>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74453456] {__log10__( <id:x:74453392>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74454032] {__abs__( <id:x:74453328>)} >
    p_lhs! params: {'base': <FunctionDefParameterInstantiation: base >, 'exp': <FunctionDefParameterInstantiation: exp >}
    <FunctionDefBuiltInInstantiation [id:74454736] {__pow__( <id:base:74453520,exp:74454480>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74455504] {__ceil__( <id:x:74454928>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74456080] {__fabs__( <id:x:74455440>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:74456656] {__floor__( <id:x:74456016>)} >
    p_lhs! <MulOp [id:76567568] [??] >
    p_lhs! <MulOp [id:76567952] [??] >
    p_lhs! <DivOp [id:76569040] [??] >
    p_lhs! <MulOp [id:76537680] [??] >
    p_lhs! <DivOp [id:76530768] [??] >
    p_lhs! <DivOp [id:76530704] [??] >
    p_lhs! <ConstValue [id:76464784] Value: '96485.3365e0 s  A  mol ' >
    p_lhs! <ConstValue [id:76468176] Value: '6.02214129e+23e0 mol ' >
    p_lhs! <ConstValue [id:76466320] Value: '1.380648e-23e0 m 2 kg  s  K ' >
    p_lhs! <ConstValue [id:76466832] Value: '1.602176565e0 s  A ' >
    p_lhs! <ConstValue [id:76467152] Value: '8.3144621e0 m 2 kg  s  K  mol ' >
    Parsing: ms
    Parsing: ms
    Parsing: ms
    Parsing: ms
    Parsing: mS/cm2
    Parsing: mS/cm2
    Parsing: mS/cm2
    Parsing: uF/cm2
    Parsing: ms
    Parsing: ms
     --  <SectionObject: [0.000000, 0.000000, 0.000000, r=9.000000] -> [18.000000, 0.000000, 0.000000, r=9.000000], Length: 18.00, Region:soma, idtag:soma, >
     --  0.5
     --  [ 9.  0.  0.]
    Distance to Soma Centre: 0.0
     --  <SectionObject: [18.000000, 0.000000, 0.000000, r=9.000000] -> [168.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_1, >
     --  0.606666666667
     --  [ 109.    0.    0.]
    Distance to Soma Centre: 100.0
     --  <SectionObject: [168.000000, 0.000000, 0.000000, r=0.150000] -> [318.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_2, >
     --  0.273333333333
     --  [ 209.    0.    0.]
    Distance to Soma Centre: 200.0
     --  <SectionObject: [168.000000, 0.000000, 0.000000, r=0.150000] -> [318.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_2, >
     --  0.94
     --  [ 309.    0.    0.]
    Distance to Soma Centre: 300.0
     --  <SectionObject: [318.000000, 0.000000, 0.000000, r=0.150000] -> [468.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_3, >
     --  0.606666666667
     --  [ 409.    0.    0.]
    Distance to Soma Centre: 400.0
     --  <SectionObject: [468.000000, 0.000000, 0.000000, r=0.150000] -> [618.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_4, >
     --  0.273333333333
     --  [ 509.    0.    0.]
    Distance to Soma Centre: 500.0
     --  <SectionObject: [468.000000, 0.000000, 0.000000, r=0.150000] -> [618.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_4, >
     --  0.94
     --  [ 609.    0.    0.]
    Distance to Soma Centre: 600.0
     --  <SectionObject: [618.000000, 0.000000, 0.000000, r=0.150000] -> [768.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_5, >
     --  0.606666666667
     --  [ 709.    0.    0.]
    Distance to Soma Centre: 700.0
     --  <SectionObject: [768.000000, 0.000000, 0.000000, r=0.150000] -> [918.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_6, >
     --  0.273333333333
     --  [ 809.    0.    0.]
    Distance to Soma Centre: 800.0
     --  <SectionObject: [768.000000, 0.000000, 0.000000, r=0.150000] -> [918.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_6, >
     --  0.94
     --  [ 909.    0.    0.]
    Distance to Soma Centre: 900.0
     --  <SectionObject: [918.000000, 0.000000, 0.000000, r=0.150000] -> [1068.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_7, >
     --  0.606666666667
     --  [ 1009.     0.     0.]
    Distance to Soma Centre: 1000.0
     --  <SectionObject: [1068.000000, 0.000000, 0.000000, r=0.150000] -> [1218.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_8, >
     --  0.273333333333
     --  [ 1109.     0.     0.]
    Distance to Soma Centre: 1100.0
     --  <SectionObject: [1068.000000, 0.000000, 0.000000, r=0.150000] -> [1218.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_8, >
     --  0.94
     --  [ 1209.     0.     0.]
    Distance to Soma Centre: 1200.0
     --  <SectionObject: [1218.000000, 0.000000, 0.000000, r=0.150000] -> [1368.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_9, >
     --  0.606666666667
     --  [ 1309.     0.     0.]
    Distance to Soma Centre: 1300.0
     --  <SectionObject: [1368.000000, 0.000000, 0.000000, r=0.150000] -> [1518.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_10, >
     --  0.273333333333
     --  [ 1409.     0.     0.]
    Distance to Soma Centre: 1400.0
     --  <SectionObject: [1368.000000, 0.000000, 0.000000, r=0.150000] -> [1518.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_10, >
     --  0.94
     --  [ 1509.     0.     0.]
    Distance to Soma Centre: 1500.0
     --  <SectionObject: [1518.000000, 0.000000, 0.000000, r=0.150000] -> [1668.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_11, >
     --  0.606666666667
     --  [ 1609.     0.     0.]
    Distance to Soma Centre: 1600.0
     --  <SectionObject: [1668.000000, 0.000000, 0.000000, r=0.150000] -> [1818.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_12, >
     --  0.273333333333
     --  [ 1709.     0.     0.]
    Distance to Soma Centre: 1700.0
     --  <SectionObject: [1668.000000, 0.000000, 0.000000, r=0.150000] -> [1818.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_12, >
     --  0.94
     --  [ 1809.     0.     0.]
    Distance to Soma Centre: 1800.0
     --  <SectionObject: [1818.000000, 0.000000, 0.000000, r=0.150000] -> [1968.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_13, >
     --  0.606666666667
     --  [ 1909.     0.     0.]
    Distance to Soma Centre: 1900.0
     --  <SectionObject: [1968.000000, 0.000000, 0.000000, r=0.150000] -> [2118.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_14, >
     --  0.273333333333
     --  [ 2009.     0.     0.]
    Distance to Soma Centre: 2000.0
     --  <SectionObject: [1968.000000, 0.000000, 0.000000, r=0.150000] -> [2118.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_14, >
     --  0.94
     --  [ 2109.     0.     0.]
    Distance to Soma Centre: 2100.0
     --  <SectionObject: [2118.000000, 0.000000, 0.000000, r=0.150000] -> [2268.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_15, >
     --  0.606666666667
     --  [ 2209.     0.     0.]
    Distance to Soma Centre: 2200.0
     --  <SectionObject: [2268.000000, 0.000000, 0.000000, r=0.150000] -> [2418.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_16, >
     --  0.273333333333
     --  [ 2309.     0.     0.]
    Distance to Soma Centre: 2300.0
     --  <SectionObject: [2268.000000, 0.000000, 0.000000, r=0.150000] -> [2418.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_16, >
     --  0.94
     --  [ 2409.     0.     0.]
    Distance to Soma Centre: 2400.0
     --  <SectionObject: [2418.000000, 0.000000, 0.000000, r=0.150000] -> [2568.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_17, >
     --  0.606666666667
     --  [ 2509.     0.     0.]
    Distance to Soma Centre: 2500.0
     --  <SectionObject: [2568.000000, 0.000000, 0.000000, r=0.150000] -> [2718.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_18, >
     --  0.273333333333
     --  [ 2609.     0.     0.]
    Distance to Soma Centre: 2600.0
     --  <SectionObject: [2568.000000, 0.000000, 0.000000, r=0.150000] -> [2718.000000, 0.0000002013-11-30 17:30:58,133 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-11-30 17:30:58,133 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
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
    p_lhs! <ConstValue [id:73156944] Value: '3.141592653' >
    p_lhs! <ConstValue [id:73157264] Value: '2.718281828' >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:73157904] {__sin__( <id:x:73157648>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:73158480] {__cos__( <id:x:73157840>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:73159120] {__tan__( <id:x:73158928>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:73159696] {__sinh__( <id:x:73159056>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:73160272] {__cosh__( <id:x:73159632>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:73160848] {__tanh__( <id:x:73160208>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:73161424] {__asin__( <id:x:73160784>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:73162000] {__acos__( <id:x:73161360>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:73162576] {__atan__( <id:x:73161936>)} >
    p_lhs! params: {'y': <FunctionDefParameterInstantiation: y >, 'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:73167440] {__atan2__( <id:y:73167312,x:73167376>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:73168208] {__exp__( <id:x:73167632>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:73168784] {__ln__( <id:x:73168144>)} >
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
    2013-11-30 17:30:59,794 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-11-30 17:30:59,795 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    nctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:73169360] {__log2__( <id:x:73169296>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:73169936] {__log10__( <id:x:73169872>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:73170512] {__abs__( <id:x:73168720>)} >
    p_lhs! params: {'base': <FunctionDefParameterInstantiation: base >, 'exp': <FunctionDefParameterInstantiation: exp >}
    <FunctionDefBuiltInInstantiation [id:73179472] {__pow__( <id:base:73179408,exp:73179216>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:73180240] {__ceil__( <id:x:73179664>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:73180816] {__fabs__( <id:x:73180176>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:73181392] {__floor__( <id:x:73180752>)} >
    p_lhs! <MulOp [id:73216208] [??] >
    p_lhs! <MulOp [id:75231568] [??] >
    p_lhs! <DivOp [id:75264912] [??] >
    p_lhs! <MulOp [id:75266512] [??] >
    p_lhs! <DivOp [id:75266064] [??] >
    p_lhs! <DivOp [id:75248208] [??] >
    p_lhs! <ConstValue [id:75206800] Value: '96485.3365e0 s  A  mol ' >
    p_lhs! <ConstValue [id:75210192] Value: '6.02214129e+23e0 mol ' >
    p_lhs! <ConstValue [id:75207120] Value: '1.380648e-23e0 m 2 kg  s  K ' >
    p_lhs! <ConstValue [id:75210576] Value: '1.602176565e0 s  A ' >
    p_lhs! <ConstValue [id:75210448] Value: '8.3144621e0 m 2 kg  s  K  mol ' >
    Parsing: ms
    Parsing: ms
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/7e/7ec1f2c94d36a03e276a28894bb9ec04.bundle (24k) : 0.806 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_24625a83055d0c988ab518c15847d4cc.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_1f76b30f77c601d1a05bfed95a0e2649.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_cfb644ede262e02ffdfd209f6b117162.so
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
    	50000 
    	1 
    Running Simulation
    Time for Extracting Data: (31 records) 0.015261888504
    Running simulation : 0.848 seconds
    Post-processing : 0.027 seconds
    Entire load-run-save time : 1.681 seconds
    Suceeded
    , 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_18, >
     --  0.94
     --  [ 2709.     0.     0.]
    Distance to Soma Centre: 2700.0
     --  <SectionObject: [2718.000000, 0.000000, 0.000000, r=0.150000] -> [2868.000000, 0.000000, 0.000000, r=0.150000], Length: 150.00, Region:axon, idtag:axon_19, >
     --  0.606666666667
     --  [ 2809.     0.     0.]
    Distance to Soma Centre: 2800.0
    PlotManger saving:  _output/figures/singlecell_simulation060/{png,svg}/fig000_Autosave_figure_1.{png,svg}




