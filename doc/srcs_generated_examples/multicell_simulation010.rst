
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


.. figure:: /srcs_generated_examples/images/multicell_simulation010_out6.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/multicell_simulation010_out6.png>`


.. figure:: /srcs_generated_examples/images/multicell_simulation010_out2.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/multicell_simulation010_out2.png>`


.. figure:: /srcs_generated_examples/images/multicell_simulation010_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/multicell_simulation010_out1.png>`


.. figure:: /srcs_generated_examples/images/multicell_simulation010_out4.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/multicell_simulation010_out4.png>`


.. figure:: /srcs_generated_examples/images/multicell_simulation010_out5.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/multicell_simulation010_out5.png>`


.. figure:: /srcs_generated_examples/images/multicell_simulation010_out3.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/multicell_simulation010_out3.png>`






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
    p_lhs! <ConstValue [id:64347024] Value: '3.141592653' >
    p_lhs! <ConstValue [id:64347344] Value: '2.718281828' >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:64347984] {__sin__( <id:x:64347728>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:64455120] {__cos__( <id:x:64454928>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:64455696] {__tan__( <id:x:64455056>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:64456272] {__sinh__( <id:x:64455632>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:64456848] {__cosh__( <id:x:64456208>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:64457424] {__tanh__( <id:x:64456784>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:64458000] {__asin__( <id:x:64457360>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:64458576] {__acos__( <id:x:64457936>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:64442832] {__atan__( <id:x:64442640>)} >
    p_lhs! params: {'y': <FunctionDefParameterInstantiation: y >, 'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:64443536] {__atan2__( <id:y:64443408,x:64443344>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:64444304] {__exp__( <id:x:64443728>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:64444880] {__ln__( <id:x:64444240>)} >
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
    2013-11-30 18:14:20,905 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-11-30 18:14:20,906 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
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
    p_lhs! <ConstValue [id:70609232] Value: '3.141592653' >
    p_lhs! <ConstValue [id:70609552] Value: '2.718281828' >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:70610192] {__sin__( <id:x:70609936>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:70610768] {__cos__( <id:x:70610128>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:70623696] {__tan__( <id:x:70623504>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:70624272] {__sinh__( <id:x:70623632>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:70624848] {__cosh__( <id:x:70624208>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:70625424] {__tanh__( <id:x:70624784>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:70626000] {__asin__( <id:x:70625360>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:70626576] {__acos__( <id:x:70625936>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:70627152] {__atan__( <id:x:70626512>)} >
    p_lhs! params: {'y': <FunctionDefParameterInstantiation: y >, 'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:70632016] {__atan2__( <id:y:70631888,x:70631952>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:70632784] {__exp__( <id:x:70632208>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:70633360] {__ln__( <id:x:70632720>)} >
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
    2013-11-30 18:14:22,590 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-11-30 18:14:22,590 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    nctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:70633936] {__log2__( <id:x:70633872>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:70634512] {__log10__( <id:x:70634448>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:70635088] {__abs__( <id:x:70633296>)} >
    p_lhs! params: {'base': <FunctionDefParameterInstantiation: base >, 'exp': <FunctionDefParameterInstantiation: exp >}
    <FunctionDefBuiltInInstantiation [id:70656336] {__pow__( <id:base:70656272,exp:70656080>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:70657104] {__ceil__( <id:x:70656528>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:70657680] {__fabs__( <id:x:70657040>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:70658256] {__floor__( <id:x:70657616>)} >
    p_lhs! <MulOp [id:70611152] [??] >
    p_lhs! <MulOp [id:72630608] [??] >
    p_lhs! <DivOp [id:72618896] [??] >
    p_lhs! <MulOp [id:72620496] [??] >
    p_lhs! <DivOp [id:72620048] [??] >
    p_lhs! <DivOp [id:72606288] [??] >
    p_lhs! <ConstValue [id:72716432] Value: '96485.3365e0 s  A  mol ' >
    p_lhs! <ConstValue [id:72719824] Value: '6.02214129e+23e0 mol ' >
    p_lhs! <ConstValue [id:72716752] Value: '1.380648e-23e0 m 2 kg  s  K ' >
    p_lhs! <ConstValue [id:72720208] Value: '1.602176565e0 s  A ' >
    p_lhs! <ConstValue [id:72720080] Value: '8.3144621e0 m 2 kg  s  K  mol ' >
    Parsing: ms
    Parsing: ms
    Loading Bundle from: /local/scratch/mh735/tmp/morphforge/tmp/simulationresults/78/789e520afb014671b32e469ba8b417fb.bundle (17k) : 0.833 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'LkChl', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    Executing: /opt/nrn//x86_64/bin/modlunit /local/scratch/mh735/tmp/morphforge/tmp/tmp_fefde0c8b954a82e90868ec2fecb49a6.mod
    /local/scratch/mh735/tmp/morphforge/tmp/modbuild_3682
    Executing: /opt/nrn//x86_64/bin/nocmodl tmp_fefde0c8b954a82e90868ec2fecb49a6.mod
    Executing: /opt/nrn//share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn//include/nrn"  -I"/opt/nrn//x86_64/lib"    -g -O2 -c -o tmp_fefde0c8b954a82e90868ec2fecb49a6.lo tmp_fefde0c8b954a82e90868ec2fecb49a6.c  
    Executing: /opt/nrn//share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_fefde0c8b954a82e90868ec2fecb49a6.la  -rpath /opt/nrn//x86_64/libs  tmp_fefde0c8b954a82e90868ec2fecb49a6.lo  -L/opt/nrn//x86_64/lib -L/opt/nrn//x86_64/lib  /opt/nrn//x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
    OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/opt/nrn//include/nrn -I/opt/nrn//x86_64/lib -g -O2 -c tmp_fefde0c8b954a82e90868ec2fecb49a6.c  -fPIC -DPIC -o .libs/tmp_fefde0c8b954a82e90868ec2fecb49a6.o
    
    OP2: libtool: link: gcc -shared  .libs/tmp_fefde0c8b954a82e90868ec2fecb49a6.o   -Wl,-rpath -Wl,/opt/nrn/x86_64/lib -Wl,-rpath -Wl,/opt/nrn/x86_64/lib -L/opt/nrn//x86_64/lib /opt/nrn/x86_64/lib/libnrniv.so /opt/nrn/x86_64/lib/libnrnoc.so /opt/nrn/x86_64/lib/liboc.so /opt/nrn/x86_64/lib/libmemacs.so /opt/nrn/x86_64/lib/libnrnmpi.so /opt/nrn/x86_64/lib/libscopmath.so /opt/nrn/x86_64/lib/libsparse13.so -lreadline -lncurses /opt/nrn/x86_64/lib/libivoc.so /opt/nrn/x86_64/lib/libneuron_gnu.so /opt/nrn/x86_64/lib/libmeschach.so /opt/nrn/x86_64/lib/libsundials.so -lm -ldl    -pthread -Wl,-soname -Wl,tmp_fefde0c8b954a82e90868ec2fecb49a6.so.0 -o .libs/tmp_fefde0c8b954a82e90868ec2fecb49a6.so.0.0.0
    libtool: link: (cd ".libs" && rm -f "tmp_fefde0c8b954a82e90868ec2fecb49a6.so.0" && ln -s "tmp_fefde0c8b954a82e90868ec2fecb49a6.so.0.0.0" "tmp_fefde0c8b954a82e90868ec2fecb49a6.so.0")
    libtool: link: (cd ".libs" && rm -f "tmp_fefde0c8b954a82e90868ec2fecb49a6.so" && ln -s "tmp_fefde0c8b954a82e90868ec2fecbNEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    
    49a6.so.0.0.0" "tmp_fefde0c8b954a82e90868ec2fecb49a6.so")
    libtool: link: ( cd ".libs" && rm -f "tmp_fefde0c8b954a82e90868ec2fecb49a6.la" && ln -s "../tmp_fefde0c8b954a82e90868ec2fecb49a6.la" "tmp_fefde0c8b954a82e90868ec2fecb49a6.la" )
    
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_0b8ada40b5b77a1866b94c6838c2aa76.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_8938c57f84f7fddd7cb3b892ad6b96bf.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_088080f2d75a6096267bc0a4cfddcdba.so
    loading membrane mechanisms from /local/scratch/mh735/tmp/morphforge/tmp/modout/mod_964524dc8fdb5ac6e636538f99e50a0b.so
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
    Time for Extracting Data: (2 records) 0.00111699104309
    Running simulation : 0.674 seconds
    Post-processing : 0.004 seconds
    Entire load-run-save time : 1.511 seconds
    Suceeded
    /usr/bin/pdflatex
    nctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:64445456] {__log2__( <id:x:64445392>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:64446032] {__log10__( <id:x:64445968>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:64471248] {__abs__( <id:x:64444816>)} >
    p_lhs! params: {'base': <FunctionDefParameterInstantiation: base >, 'exp': <FunctionDefParameterInstantiation: exp >}
    <FunctionDefBuiltInInstantiation [id:64471952] {__pow__( <id:base:64471312,exp:64471696>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:64472720] {__ceil__( <id:x:64472144>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:64473296] {__fabs__( <id:x:64472656>)} >
    p_lhs! params: {'x': <FunctionDefParameterInstantiation: x >}
    <FunctionDefBuiltInInstantiation [id:64473872] {__floor__( <id:x:64473232>)} >
    p_lhs! <MulOp [id:64480016] [??] >
    p_lhs! <MulOp [id:65401872] [??] >
    p_lhs! <DivOp [id:65414096] [??] >
    p_lhs! <MulOp [id:65416592] [??] >
    p_lhs! <DivOp [id:65421648] [??] >
    p_lhs! <DivOp [id:65422352] [??] >
    p_lhs! <ConstValue [id:62554832] Value: '96485.3365e0 s  A  mol ' >
    p_lhs! <ConstValue [id:62556560] Value: '6.02214129e+23e0 mol ' >
    p_lhs! <ConstValue [id:62556368] Value: '1.380648e-23e0 m 2 kg  s  K ' >
    p_lhs! <ConstValue [id:62558096] Value: '1.602176565e0 s  A ' >
    p_lhs! <ConstValue [id:62557264] Value: '8.3144621e0 m 2 kg  s  K  mol ' >
    Parsing: ms
    Parsing: ms
    Parsing: mA/cm2
    Parsing: nA
    Parsing: mV
    Parsing: ms
    Parsing: K
    Parsing: ms
    Parsing: ms
    Parsing: um2
    Parsing: mS/cm2
    Parsing: mS/cm2
    Parsing: mS/cm2
    Warning: node 'AnonObj0001', graph 'graphname' size too small for label
    Warning: node 'AnonObj0002', graph 'graphname' size too small for label
    
    [(397.88735772973837, array([ 1.,  0.,  0.])), (0.0, array([ 0.,  1.,  0.])), (0.0, array([ 0.,  0.,  1.]))]
    Saving figure /home/mh735/.mredoc/build/figs/opfile0002
    [(397.88735772973837, array([ 1.,  0.,  0.])), (0.0, array([ 0.,  1.,  0.])), (0.0, array([ 0.,  0.,  1.]))]
    Saving figure /home/mh735/.mredoc/build/figs/opfile0003
    Saving figure /home/mh735/.mredoc/build/figs/opfile0004
    Saving figure /home/mh735/.mredoc/build/figs/opfile0005
    True
    True
    PlotManger saving:  _output/figures/multicell_simulation010/{png,svg}/fig000_Autosave_figure_1.{png,svg}
    PlotManger saving:  _output/figures/multicell_simulation010/{png,svg}/fig001_Autosave_figure_2.{png,svg}
    PlotManger saving:  _output/figures/multicell_simulation010/{png,svg}/fig002_Autosave_figure_3.{png,svg}
    PlotManger saving:  _output/figures/multicell_simulation010/{png,svg}/fig003_Autosave_figure_4.{png,svg}
    PlotManger saving:  _output/figures/multicell_simulation010/{png,svg}/fig004_Autosave_figure_5.{png,svg}
    Saving figure /home/mh735/.mredoc/build/figs/opfile0006
    Remove paragraph? (no)
    Tex File: /home/mh735/.mredoc/build/pdflatex/eqnset.tex
    Successfully written PDF to:  /local/scratch/mh735/tmp/morphforge/tmp/mf_doc_build/multicell_simulation010.py.pdf
    PlotManger saving:  _output/figures/multicell_simulation010/{png,svg}/fig005_Autosave_figure_6.{png,svg}




