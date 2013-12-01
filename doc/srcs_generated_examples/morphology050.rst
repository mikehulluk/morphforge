
.. _example_morphology050:

Example 5. Load morphologies from MorphML, and plot using MayaVI
================================================================


Load morphologies from MorphML, and plot using MayaVI

Code
~~~~

.. code-block:: python

    
    
    
    import morphforge.stdimports as mf
    import morphforgecontrib.morphology.importers.import_tree_morphml
    import pylab
    
    testSrcsPath = mf.LocMgr().get_test_srcs_path()
    srcMorphMLFile = mf.Join(testSrcsPath, "neuroml/morphml/CablesIncluded.xml")
    m = mf.MorphologyTree.fromMorphML(src=open(srcMorphMLFile) )
    #mf.MayaViRenderer(m).show_as_points_interpolated()
    
    
    
    ## TODO - SPEAK TO PADRAIG:
    #raise NotImplementedError()
    #srcMorphMLFile = mf.Join(testSrcsPath, "neuroml/morphml/L23PyrFRB.morph.xml",)
    #m = mf.MorphologyTree.fromMorphML(
    #        src=open(srcMorphMLFile),
    #        regions={
    #            'all':'Rgn1',
    #            'ModelViewParmSubset_1':'Rgn2',
    #            'ModelViewParmSubset_3':'Rgn2',
    #            'ModelViewParmSubset_8':'Rgn2',
    #            'OneSecGrp_SectionRef_1':'Rgn1',
    #        }
    #)
    #mf.MayaViRenderer(m).show_as_points_interpolated()
    
    
    
    
    








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
    p_lhs! <ConstValue [id:78329936] Value: '3.141592653' >
    p_lhs! <ConstValue [id:78330256] Value: '2.718281828' >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:78330896] {__sin__( <id:x:78330640>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:78331472] {__cos__( <id:x:78330832>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:78663888] {__tan__( <id:x:78331408>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:78664464] {__sinh__( <id:x:78663824>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:78665040] {__cosh__( <id:x:78664400>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:78665616] {__tanh__( <id:x:78664976>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:78666192] {__asin__( <id:x:78665552>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:78666768] {__acos__( <id:x:78666128>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:78667344] {__atan__( <id:x:78666704>)} >
    p_lhs! params: {'y': <FunctionDefParameterInstantiation: y >, 'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:75764048] {__atan2__( <id:y:75763920,x:75763984>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:75764816] {__exp__( <id:x:75764240>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:75765392] {__ln__( <id:x:75764752>)} >
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
    /local/scratch/mh735/hw/morphforge/src/morphforgecontrib/morphology/importers/import_tree_morphml.py:34: UserWarning: MorphML code in development
      warnings.warn('MorphML code in development')
    nctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:75765968] {__log2__( <id:x:75765904>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:75766544] {__log10__( <id:x:75766480>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:75767120] {__abs__( <id:x:75765328>)} >
    p_lhs! params: {'base': <FunctionDefParameterInstantiation: base >, 'exp': <FunctionDefParameterInstantiation: exp >}
    <FunctionDefBuiltInInstantiation [id:75784272] {__pow__( <id:base:75766032,exp:75767696>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:75785040] {__ceil__( <id:x:75784464>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:75785616] {__fabs__( <id:x:75784976>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:75786192] {__floor__( <id:x:75785552>)} >
    p_lhs! <MulOp [id:77794640] [??] >
    p_lhs! <MulOp [id:77793872] [??] >
    p_lhs! <DivOp [id:77764496] [??] >
    p_lhs! <MulOp [id:77800976] [??] >
    p_lhs! <DivOp [id:77801360] [??] >
    p_lhs! <DivOp [id:77802512] [??] >
    p_lhs! <ConstValue [id:77754576] Value: '96485.3365e0 s  A  mol ' >
    p_lhs! <ConstValue [id:77758352] Value: '6.02214129e+23e0 mol ' >
    p_lhs! <ConstValue [id:77757968] Value: '1.380648e-23e0 m 2 kg  s  K ' >
    p_lhs! <ConstValue [id:77822416] Value: '1.602176565e0 s  A ' >
    p_lhs! <ConstValue [id:77823312] Value: '8.3144621e0 m 2 kg  s  K  mol ' >
    Parsing: ms
    Parsing: ms
    CellName: CellWithCables
    Loaded Cable:  0 SomaSec
    Loaded Cable:  1 DendSec1
    Loaded Cable:  2 DendSec2
    Segment
    0 SomaSeg 0  (u'0', u'0', u'0', u'10') (u'10', u'0', u'0', u'10')
    Segment
    1 DendSeg1 1 0 (u'5', u'0', u'0', u'5') (u'5', u'10', u'0', u'5')
    Segment
    2 DendSeg2 1 1 (5.0, 10.0, 0.0, 5.0) (u'5', u'20', u'0', u'5')
    Segment
    3 DendSeg3 1 2 (5.0, 20.0, 0.0, 5.0) (u'5', u'30', u'0', u'5')
    Segment
    4 DendSeg4 2 0 (u'10', u'0', u'0', u'3') (u'10', u'0', u'10', u'3')
    Segment
    5 DendSeg5 2 4 (10.0, 0.0, 10.0, 3.0) (u'10', u'0', u'20', u'3')
    RegionNames: [u'soma_group', u'dendrite_group']




