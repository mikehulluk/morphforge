
.. _example_poster1:

Example 22. Simulation of a HodgkinHuxley-type neuron specified through NeuroUnits
==================================================================================


Simulation of a HodgkinHuxley-type neuron specified through NeuroUnits.

Code
~~~~

.. code-block:: python

    
    
    
    
    
    
    
    
    
    
    
    import matplotlib as mpl
    mpl.rcParams['font.size'] = 14
    
    from morphforge.stdimports import *
    from morphforgecontrib.stdimports import *
    
    eqnset_txt_na = """
    define_component hh_na {
        i = g * (v-erev) * m**3*h
    
        m_inf = m_alpha_rate / (m_alpha_rate + m_beta_rate)
        m_tau = 1.0 / (m_alpha_rate + m_beta_rate)
        m' = (m_inf-m) / m_tau
    
        h_inf = h_alpha_rate / (h_alpha_rate + h_beta_rate)
        h_tau = 1.0 / (h_alpha_rate + h_beta_rate)
        h' = (h_inf-h) / h_tau
        StdFormAB(V, a1, a2, a3, a4, a5) = (a1+a2*V)/(a3+std.math.exp((V+a4)/a5))
        m_alpha_rate = StdFormAB(V=v, a1=m_a1, a2=m_a2, a3=m_a3, a4=m_a4, a5=m_a5)
        m_beta_rate =  StdFormAB(V=v, a1=m_b1, a2=m_b2, a3=m_b3, a4=m_b4, a5=m_b5)
        h_alpha_rate = StdFormAB(V=v, a1=h_a1, a2=h_a2, a3=h_a3, a4=h_a4, a5=h_a5)
        h_beta_rate =  StdFormAB(V=v, a1=h_b1, a2=h_b2, a3=h_b3, a4=h_b4, a5=h_b5)
        m_a1={-4.00 ms-1};  m_a2={-0.10 mV-1 ms-1}; m_a3={-1.00}; m_a4={40.00 mV}; m_a5={-10.00 mV};
        m_b1={ 4.00 ms-1};  m_b2={ 0.00 mV-1 ms-1}; m_b3={ 0.00}; m_b4={65.00 mV}; m_b5={ 18.00 mV};
        h_a1={ 0.07 ms-1};  h_a2={ 0.00 mV-1 ms-1}; h_a3={ 0.00}; h_a4={65.00 mV}; h_a5={ 20.00 mV};
        h_b1={ 1.00 ms-1};  h_b2={ 0.00 mV-1 ms-1}; h_b3={ 1.00}; h_b4={35.00 mV}; h_b5={-10.00 mV};
    
        erev = 50.0mV;
        <=> PARAMETER g:(S/m2)
    
        <=> OUTPUT    i:(A/m2)  METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }
        <=> INPUT     v: V      METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
    } """
    
    eqnset_txt_k = """
    define_component hh_k {
        i = g * (v-erev) * n*n*n*n
        n_inf = n_alpha_rate / (n_alpha_rate + n_beta_rate)
        n_tau = 1.0 / (n_alpha_rate + n_beta_rate)
        n' = (n_inf-n) / n_tau
        StdFormAB(V, a1, a2, a3, a4, a5) = (a1 + a2*V)/(a3+std.math.exp((V+a4)/a5))
        n_alpha_rate = StdFormAB(V=v, a1=n_a1, a2=n_a2, a3=n_a3, a4=n_a4, a5=n_a5)
        n_beta_rate =  StdFormAB(V=v, a1=n_b1, a2=n_b2, a3=n_b3, a4=n_b4, a5=n_b5)
    
        n_a1={-0.55 ms-1}; n_a2={-0.01 mV-1 ms-1}; n_a3={-1.00}; n_a4={55.00 mV}; n_a5={-10.00 mV}
        n_b1={0.125 ms-1}; n_b2={ 0.00 mV-1 ms-1}; n_b3={ 0.00}; n_b4={65.00 mV}; n_b5={ 80.00 mV}
    
        g = {36.0mS/cm2}
        erev = {-77.0mV}
        <=> OUTPUT    i:(A/m2)  METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }
        <=> INPUT     v: V      METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
    } """
    
    eqnset_txt_lk = """
    define_component hh_lk {
        i = {0.3mS/cm2} * (v- {-54.3mV})
        <=> OUTPUT    i:(A/m2)  METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }
        <=> INPUT     v: V      METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
    } """
    
    env = NEURONEnvironment()
    sim = env.Simulation()
    
    # Create a cell:
    morph_dict = {'root': {'length': 18.8, 'diam': 18.8, 'id':'soma'} }
    my_morph = MorphologyTree.fromDictionary(morph_dict)
    cell = sim.create_cell(name="Cell1", morphology=my_morph)
    #soma = cell.get_location("soma")
    
    # Setup passive channels:
    cell.set_passive( PassiveProperty.SpecificCapacitance, qty('1.0:uF/cm2'))
    
    # Setup active channels:
    na_chl = env.Channel(NeuroUnitEqnsetMechanism, name="NaChl", eqnset=eqnset_txt_na,
            default_parameters={"g":qty("120:mS/cm2")}, )
    k_chl = env.Channel(NeuroUnitEqnsetMechanism, name="KChl", eqnset=eqnset_txt_k, )
    lk_chl = env.Channel(NeuroUnitEqnsetMechanism, name="LKChl", eqnset=eqnset_txt_lk, )
    
    cell.apply_channel( na_chl)
    cell.apply_channel( lk_chl)
    cell.apply_channel( k_chl)
    
    # Define what to record:
    sim.record(cell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = cell.soma)
    sim.record(na_chl, what='m', cell_location=cell.soma, user_tags=[StandardTags.StateVariable])
    sim.record(na_chl, what='h', cell_location=cell.soma, user_tags=[StandardTags.StateVariable])
    sim.record(k_chl,  what='n', cell_location=cell.soma, user_tags=[StandardTags.StateVariable])
    
    # Create the stimulus and record the injected current:
    cc = sim.create_currentclamp(name="CC1", amp=qty("100:pA"), dur=qty("100:ms"), delay=qty("100:ms"), cell_location=cell.soma)
    sim.record(cc, what=StandardTags.Current)
    
    
    # run the simulation
    results = sim.run()
    TagViewer(results, timerange=(50, 250)*units.ms, show=True)
    
    
    




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/poster1_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/poster1_out1.png>`






Output
~~~~~~

.. code-block:: bash

        No handlers could be found for logger "neurounits"
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    CHECKING
    <Parameter [id:66423952] Symbol: 'g' >
    g
    iii 1.0 s**3*A**2/(kg*m**4) <class 'quantities.quantity.Quantity'>
    iiii 1200.0 s**3*A**2/(kg*m**4) <class 'quantities.quantity.Quantity'>
    OK
    
    Output <StateVariable [id:66414928] Symbol: 'h' >
    None
    Output <StateVariable [id:66413904] Symbol: 'm' >
    None
    Output <AssignedVariable [id:66416144] Symbol: 'h_alpha_rate' >
    None
    Output <AssignedVariable [id:66415952] Symbol: 'h_beta_rate' >
    None
    Output <AssignedVariable [id:66423184] Symbol: 'h_inf' >
    None
    Output <AssignedVariable [id:66413200] Symbol: 'h_tau' >
    None
    Output <AssignedVariable [id:66423568] Symbol: 'i' >
    {u'mf': {u'role': u'TRANSMEMBRANECURRENT'}}
    Output <AssignedVariable [id:66421456] Symbol: 'm_alpha_rate' >
    None
    Output <AssignedVariable [id:66423760] Symbol: 'm_beta_rate' >
    None
    Output <AssignedVariable [id:66413392] Symbol: 'm_inf' >
    None
    Output <AssignedVariable [id:66415760] Symbol: 'm_tau' >
    None
    input <SuppliedValue [id:66424720] Symbol: 'v' >
    {u'mf': {u'role': u'MEMBRANEVOLTAGE'}}
    h_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    g <class 'neurounits.ast.astobjects.Parameter'>
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    m <class 'neurounits.ast.astobjects.StateVariable'>
    h <class 'neurounits.ast.astobjects.StateVariable'>
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    h_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:66416272] Symbol: h_alpha_rate >
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:66416080] Symbol: h_beta_rate >
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:66414288] Symbol: h_tau >
    h_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:66421584] Symbol: m_alpha_rate >
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:66423696] Symbol: i >
    g <class 'neurounits.ast.astobjects.Parameter'>
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    m <class 'neurounits.ast.astobjects.StateVariable'>
    h <class 'neurounits.ast.astobjects.StateVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:66423888] Symbol: m_beta_rate >
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:66415888] Symbol: m_tau >
    m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:66423312] Symbol: h_inf >
    h_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:66413520] Symbol: m_inf >
    m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    h_inf <class 'neurounits.ast.astobjects.AssignedVariable'>
    h <class 'neurounits.ast.astobjects.StateVariable'>
    h_tau <class 'neurounits.ast.astobjects.AssignedVariable'>
    m_inf <class 'neurounits.ast.astobjects.AssignedVariable'>
    m <class 'neurounits.ast.astobjects.StateVariable'>
    m_tau <class 'neurounits.ast.astobjects.AssignedVariable'>
    __exp__
    x <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    a1 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    a2 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    V <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    a3 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    T [<class 'neurounits.ast.astobjects.DivOp'>]
    V <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    a4 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    a5 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    Output <StateVariable [id:66486224] Symbol: 'n' >
    None
    Output <AssignedVariable [id:66491024] Symbol: 'i' >
    {u'mf': {u'role': u'TRANSMEMBRANECURRENT'}}
    Output <AssignedVariable [id:66483216] Symbol: 'n_alpha_rate' >
    None
    Output <AssignedVariable [id:66492752] Symbol: 'n_beta_rate' >
    None
    Output <AssignedVariable [id:66490448] Symbol: 'n_inf' >
    None
    Output <AssignedVariable [id:66492368] Symbol: 'n_tau' >
    None
    input <SuppliedValue [id:66492944] Symbol: 'v' >
    {u'mf': {u'role': u'MEMBRANEVOLTAGE'}}
    n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    n_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    n <class 'neurounits.ast.astobjects.StateVariable'>
    n <class 'neurounits.ast.astobjects.StateVariable'>
    n <class 'neurounits.ast.astobjects.StateVariable'>
    n <class 'neurounits.ast.astobjects.StateVariable'>
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    n_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:66491152] Symbol: i >
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    n <class 'neurounits.ast.astobjects.StateVariable'>
    n <class 'neurounits.ast.astobjects.StateVariable'>
    n <class 'neurounits.ast.astobjects.StateVariable'>
    n <class 'neurounits.ast.astobjects.StateVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:66492880] Symbol: n_beta_rate >
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:66485072] Symbol: n_alpha_rate >
    T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:66490960] Symbol: n_inf >
    n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    n_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    Writing assignment for:  <EqnAssignmentByRegime [id:66492496] Symbol: n_tau >
    n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    n_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
    n_inf <class 'neurounits.ast.astobjects.AssignedVariable'>
    n <class 'neurounits.ast.astobjects.StateVariable'>
    n_tau <class 'neurounits.ast.astobjects.AssignedVariable'>
    __exp__
    x <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    a1 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    a2 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    V <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    a3 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    T [<class 'neurounits.ast.astobjects.DivOp'>]
    V <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    a4 <class 'neurounits.ast.astobjects.F2013-12-01 17:16:07,592 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:16:07,592 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
    No handlers could be found for logger "neurounits"
    2013-12-01 17:16:09,887 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:16:09,887 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/e9/e90a9c98b7e5fda14e011f9dd4cecf45.bundle (134k) : 0.991 seconds
    Executing: /home/michael/opt//x86_64/bin/modlunit /mnt/scratch/tmp/morphforge/tmp/tmp_72b8e1c8c62ecd7f3649149dd83ae07a.mod
    /mnt/scratch/tmp/morphforge/tmp/modbuild_23815
    Executing: /home/michael/opt//x86_64/bin/nocmodl tmp_72b8e1c8c62ecd7f3649149dd83ae07a.mod
    Executing: /home/michael/opt//share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/home/michael/opt//include/nrn"  -I"/home/michael/opt//x86_64/lib"    -g -O2 -c -o tmp_72b8e1c8c62ecd7f3649149dd83ae07a.lo tmp_72b8e1c8c62ecd7f3649149dd83ae07a.c  
    Executing: /home/michael/opt//share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_72b8e1c8c62ecd7f3649149dd83ae07a.la  -rpath /home/michael/opt//x86_64/libs  tmp_72b8e1c8c62ecd7f3649149dd83ae07a.lo  -L/home/michael/opt//x86_64/lib -L/home/michael/opt//x86_64/lib  /home/michael/opt//x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
    OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/home/michael/opt//include/nrn -I/home/michael/opt//x86_64/lib -g -O2 -c tmp_72b8e1c8c62ecd7f3649149dd83ae07a.c  -fPIC -DPIC -o .libs/tmp_72b8e1c8c62ecd7f3649149dd83ae07a.o
    
    OP2: libtool: link: gcc -shared  -fPIC -DPIC  .libs/tmp_72b8e1c8c62ecd7f3649149dd83ae07a.o   -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -L/home/michael/opt//x86_64/lib /home/michael/opt/x86_64/lib/libnrniv.so /home/michael/opt/x86_64/lib/libnrnoc.so /home/michael/opt/x86_64/lib/liboc.so /home/michael/opt/x86_64/lib/libmemacs.so /home/michael/opt/x86_64/lib/libnrnmpi.so /home/michael/opt/x86_64/lib/libscopmath.so /home/michael/opt/x86_64/lib/libsparse13.so -lreadline -lncurses /home/michael/opt/x86_64/lib/libivoc.so /home/michael/opt/x86_64/lib/libneuron_gnu.so /home/michael/opt/x86_64/lib/libmeschach.so /home/michael/opt/x86_64/lib/libsundials.so -lm -ldl  -O2   -pthread -Wl,-soname -Wl,tmp_72b8e1c8c62ecd7f3649149dd83ae07a.so.0 -o .libs/tmp_72b8e1c8c62ecd7f3649149dd83ae07a.so.0.0.0
    libtool: link: (cd ".libs" && rm -f "tmp_72b8e1c8c62ecd7f3649149dd83ae07a.so.0" && ln -s "tmp_72b8e1c8c62ecd7f3649149dd83ae07a.so.0.0.0" "tmp_72b8e1c8c62ecd7f3649149dd83ae07a.so.0")
    libtool: link: (cd ".libs" && rm -f "tmp_72b8e1c8c62ecd7f3649149dd83ae07a.so" && ln -s "tmp_72b8e1c8c62ecd7f3649149dd83ae07a.so.0.0.0" "tmp_72b8e1c8c62ecd7f3649149dd83ae07a.so")
    libtool: link: ( cd ".libs" && rm -f "tmp_72b8e1c8c62ecd7f3649149dd83ae07a.la" && ln -s "../tmp_72b8e1c8c62ecd7f3649149dd83ae07a.la" "tmp_72b8e1c8c62ecd7f3649149dd83ae07a.la" )
    
    Executing: /home/michael/opt//x86_64/bin/modlunit /mnt/scratch/tmp/morphforge/tmp/tmp_4b8bd5611b44aa2154237a91099a4e7c.mod
    /mnt/scratch/tmp/morphforge/tmp/modbuild_23815
    Executing: /home/michael/opt//x86_64/bin/nocmodl tmp_4b8bd5611b44aa2154237a91099a4e7c.mod
    Executing: /home/michael/opt//share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/home/michael/opt//include/nrn"  -I"/home/michael/opt//x86_64/lib"    -g -O2 -c -o tmp_4b8bd5611b44aa2154237a91099a4e7c.lo tmp_4b8bd5611b44aa2154237a91099a4e7c.c  
    Executing: /home/michael/opt//share/nrn/libtool --mode=link gcc -module  -NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    g -O2  -shared  -o tmp_4b8bd5611b44aa2154237a91099a4e7c.la  -rpath /home/michael/opt//x86_64/libs  tmp_4b8bd5611b44aa2154237a91099a4e7c.lo  -L/home/michael/opt//x86_64/lib -L/home/michael/opt//x86_64/lib  /home/michael/opt//x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
    OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/home/michael/opt//include/nrn -I/home/michael/opt//x86_64/lib -g -O2 -c tmp_4b8bd5611b44aa2154237a91099a4e7c.c  -fPIC -DPIC -o .libs/tmp_4b8bd5611b44aa2154237a91099a4e7c.o
    
    OP2: libtool: link: gcc -shared  -fPIC -DPIC  .libs/tmp_4b8bd5611b44aa2154237a91099a4e7c.o   -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -L/home/michael/opt//x86_64/lib /home/michael/opt/x86_64/lib/libnrniv.so /home/michael/opt/x86_64/lib/libnrnoc.so /home/michael/opt/x86_64/lib/liboc.so /home/michael/opt/x86_64/lib/libmemacs.so /home/michael/opt/x86_64/lib/libnrnmpi.so /home/michael/opt/x86_64/lib/libscopmath.so /home/michael/opt/x86_64/lib/libsparse13.so -lreadline -lncurses /home/michael/opt/x86_64/lib/libivoc.so /home/michael/opt/x86_64/lib/libneuron_gnu.so /home/michael/opt/x86_64/lib/libmeschach.so /home/michael/opt/x86_64/lib/libsundials.so -lm -ldl  -O2   -pthread -Wl,-soname -Wl,tmp_4b8bd5611b44aa2154237a91099a4e7c.so.0 -o .libs/tmp_4b8bd5611b44aa2154237a91099a4e7c.so.0.0.0
    libtool: link: (cd ".libs" && rm -f "tmp_4b8bd5611b44aa2154237a91099a4e7c.so.0" && ln -s "tmp_4b8bd5611b44aa2154237a91099a4e7c.so.0.0.0" "tmp_4b8bd5611b44aa2154237a91099a4e7c.so.0")
    libtool: link: (cd ".libs" && rm -f "tmp_4b8bd5611b44aa2154237a91099a4e7c.so" && ln -s "tmp_4b8bd5611b44aa2154237a91099a4e7c.so.0.0.0" "tmp_4b8bd5611b44aa2154237a91099a4e7c.so")
    libtool: link: ( cd ".libs" && rm -f "tmp_4b8bd5611b44aa2154237a91099a4e7c.la" && ln -s "../tmp_4b8bd5611b44aa2154237a91099a4e7c.la" "tmp_4b8bd5611b44aa2154237a91099a4e7c.la" )
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_b710d7b3064eaabef925f2922f85b448.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_5b144839abc1f71c64edc719bdbc0a69.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_799583e317ef835f0a856c504569a8d4.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_232733c472377264461006269833bbf4.hoc
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
    Running Simulation
    Time for Extracting Data: (5 records) 0.00896692276001
    Running simulation : 2.657 seconds
    Size of results file: 0.3 (MB)
    Post-processing : 0.048 seconds
    Entire load-run-save time : 3.696 seconds
    Suceeded
    unctionDefParameter'>
    a5 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
    Output <AssignedVariable [id:66519376] Symbol: 'i' >
    {u'mf': {u'role': u'TRANSMEMBRANECURRENT'}}
    input <SuppliedValue [id:66521616] Symbol: 'v' >
    {u'mf': {u'role': u'MEMBRANEVOLTAGE'}}
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    Writing assignment for:  <EqnAssignmentByRegime [id:66521680] Symbol: i >
    v <class 'neurounits.ast.astobjects.SuppliedValue'>
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/e9//e90a9c98b7e5fda14e011f9dd4cecf45.neuronsim.results.pickle ]
    PlotManger saving:  _output/figures/poster1/{png,svg}/fig000_Autosave_figure_1.{png,svg}




