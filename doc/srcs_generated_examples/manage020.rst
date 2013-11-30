
.. _example_manage020:

Example 22. Summarise the cells and channels that are registered to an environment
==================================================================================


Summarise the cells and channels that are registered to an environment

Code
~~~~

.. code-block:: python

    
    
    
    
    
    
    import mredoc
    from morphforge.stdimports import PluginMgr, CellLibrary, ChannelLibrary, MorphologyLibrary, PostSynapticTemplateLibrary
    import morphforgecontrib.stdimports as mfc
    from  modelling import *
    from modelling.sensory_pathway import *
    fname = '~/Desktop/morphforge_registered_templates.pdf'
    
    mredoc.Section('Summary',
        CellLibrary.summary_table(),
        ChannelLibrary.summary_table(),
        MorphologyLibrary.summary_table(),
        PostSynapticTemplateLibrary.summary_table(),
    
        ).to_pdf(fname)
    
    print 'Cell & Channel summary stored at: %s'%fname
    
    
    








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
    p_lhs! <ConstValue [id:54045200] Value: '3.141592653' >
    p_lhs! <ConstValue [id:54045520] Value: '2.718281828' >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:54046160] {__sin__( <id:x:54045904>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:54157392] {__cos__( <id:x:54046096>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:54157968] {__tan__( <id:x:54157456>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:54158544] {__sinh__( <id:x:54157904>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:54159120] {__cosh__( <id:x:54158480>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:54159696] {__tanh__( <id:x:54159056>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:54160272] {__asin__( <id:x:54159632>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:54160848] {__acos__( <id:x:54160208>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:54108240] {__atan__( <id:x:54160784>)} >
    p_lhs! params: {'y': <FunctionDefParameterInstantiation: y >, 'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:54108944] {__atan2__( <id:y:54108816,x:54108880>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:54109712] {__exp__( <id:x:54109136>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:54110288] {__ln__( <id:x:54109648>)} >
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
    /home/mh735/.local/lib/python2.7/site-packages/setuptools-1.1.5-py2.7.egg/pkg_resources.py:979: UserWarning: /home/mh735/.python-eggs is writable by group/others and vulnerable to attack when used with get_resource_filename. Consider a more secure location (set with .set_extraction_path or the PYTHON_EGG_CACHE environment variable).
    nctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:54110864] {__log2__( <id:x:54110800>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:54111440] {__log10__( <id:x:54111376>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:54112016] {__abs__( <id:x:54110224>)} >
    p_lhs! params: {'base': <FunctionDefParameterInstantiation: base >, 'exp': <FunctionDefParameterInstantiation: exp >}
    <FunctionDefBuiltInInstantiation [id:54055440] {__pow__( <id:base:54055376,exp:54055184>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:54056208] {__ceil__( <id:x:54055632>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:54056784] {__fabs__( <id:x:54056144>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:54057360] {__floor__( <id:x:54056720>)} >
    p_lhs! <MulOp [id:55045136] [??] >
    p_lhs! <MulOp [id:54137168] [??] >
    p_lhs! <DivOp [id:55040336] [??] >
    p_lhs! <MulOp [id:55048336] [??] >
    p_lhs! <DivOp [id:55049552] [??] >
    p_lhs! <DivOp [id:55055952] [??] >
    p_lhs! <ConstValue [id:55058064] Value: '96485.3365e0 s  A  mol ' >
    p_lhs! <ConstValue [id:55058192] Value: '6.02214129e+23e0 mol ' >
    p_lhs! <ConstValue [id:55059792] Value: '1.380648e-23e0 m 2 kg  s  K ' >
    p_lhs! <ConstValue [id:55059984] Value: '1.602176565e0 s  A ' >
    p_lhs! <ConstValue [id:55062288] Value: '8.3144621e0 m 2 kg  s  K  mol ' >
    Parsing: ms
    Parsing: ms
    Parsing: mA/cm2
    Parsing: nA
    Parsing: mV
    Parsing: ms
    Parsing: K
    Parsing: pF
    Parsing: uF/cm2
    sqlite:////local/scratch/mh735/tmp/signalanalysis.sqlite
    Parsing: ms
    Parsing: ms
    Parsing: ms
    Parsing: um2
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> MHR-dIN-Inhib
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> MHR-dIN-Inhib
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> MHR-dIN-Inhib
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> MHR-dIN-Inhib
    Parsing: um2
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> cIN-dIN-Inhib
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> cIN-dIN-Inhib
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> cIN-dIN-Inhib
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> cIN-dIN-Inhib
    Parsing: um2
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> dIN-cIN-AMPA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> dIN-cIN-AMPA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> dIN-cIN-AMPA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> dIN-cIN-AMPA
    Parsing: um2
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> dIN-dIN-AMPA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> dIN-dIN-AMPA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> dIN-dIN-AMPA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> dIN-dIN-AMPA
    Parsing: um2
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> tIN-dIN-AMPA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> tIN-dIN-AMPA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> tIN-dIN-AMPA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> tIN-dIN-AMPA
    Parsing: um2
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA
    Parsing: um2
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-MgBlock
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-MgBlock
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-MgBlock
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-MgBlock
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-MgBlock
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-MgBlock
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-MgBlock
    Parsing: um2
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-SlowOpen
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-SlowOpen
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-SlowOpen
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-SlowOpen
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-SlowOpen
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-SlowOpen
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-SlowOpen
    Parsing: um2
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-NMDA
    <class 'morph/usr/bin/pdflatex
    forgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-NMDA
    Parsing: um2
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> tIN-dIN-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> tIN-dIN-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> tIN-dIN-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> tIN-dIN-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> tIN-dIN-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> tIN-dIN-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> tIN-dIN-NMDA
    Tex File: /home/mh735/.mredoc/build/pdflatex/eqnset.tex
    Successfully written PDF to:  /home/mh735/Desktop/morphforge_registered_templates.pdf
    Cell & Channel summary stored at: ~/Desktop/morphforge_registered_templates.pdf




