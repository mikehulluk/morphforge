
.. _example_multicell_simulation050:

Example 20. Defining populations of neurons
===========================================


Defining populations of neurons.

Code
~~~~

.. code-block:: python

    
    PostSynapticTemplateLibrary.register_template_specialisation( modelsrc='HULL10', synapsetype='MHR-dIN-Inhib',
            template_type = PostSynapticMech_Exp2Syn_Base,
            tau_open=1.5*ms, tau_close=30*ms, e_rev=-70*mV, popening=1.0, peak_conductance=0.5*nS,)
    
    
    # tIN -> dIN
    # ==============
    
    def create_synapse_tIN_to_dIN_AMPANMDA_spike_times_new(sim, times, postsynaptic, parameter_overrides=None ):
        parameter_overrides = parameter_overrides or {}
    
        psm_tmpl = PostSynapticTemplateLibrary.get_template( modelsrc='HULL10', synapsetype='tIN-dIN-AMPA', sim=sim)
        s1 = sim.create_synapse(
                    trigger=sim.environment.SynapticTrigger(SynapticTriggerAtTimes, time_list=times),
                    postsynaptic_mech=psm_tmpl.instantiate(cell_location=postsynaptic.soma, parameter_overrides=parameter_overrides))
    
        psm_tmpl = PostSynapticTemplateLibrary.get_template( modelsrc='HULL10', synapsetype='tIN-dIN-NMDA', sim=sim)
        s2 = sim.create_synapse(
                    trigger=sim.environment.SynapticTrigger(SynapticTriggerAtTimes, time_list=times),
                    postsynaptic_mech=psm_tmpl.instantiate(cell_location=postsynaptic.soma, parameter_overrides=parameter_overrides)) 
        return [s1,s2]
    
    def create_synapse_tIN_to_dIN_AMPANMDA_new(sim, times, postsynaptic, parameter_overrides=None):
        parameter_overrides = parameter_overrides or {}
        psm_tmpl = PostSynapticTemplateLibrary.get_template( modelsrc='HULL10', synapsetype='tIN-dIN-AMPA', sim=sim)
        s1 =  sim.create_synapse(
                    trigger=sim.environment.SynapticTrigger( SynapticTriggerByVoltageThreshold,
                                        cell_location = presynaptic.soma,
                                        voltage_threshold = 0*mV, delay=1.0*ms,),
                    postsynaptic_mech=psm_tmpl.instantiate(cell_location=postsynaptic.soma,parameter_overrides=parameter_overrides ))
    
        psm_tmpl = PostSynapticTemplateLibrary.get_template( modelsrc='HULL10', synapsetype='tIN-dIN-NMDA', sim=sim)
        s2 = sim.create_synapse(
                    trigger=sim.environment.SynapticTrigger( SynapticTriggerByVoltageThreshold,
                                        cell_location = presynaptic.soma,
                                        voltage_threshold = 0*mV, delay=1.0*ms),
                    postsynaptic_mech=psm_tmpl.instantiate(cell_location=postsynaptic.soma,parameter_overrides=parameter_overrides  ))
        return [s1,s2]
    
    
    
    
    
    
    def create_synapse_dIN_to_dIN_AMPA_spike_times_new( sim, times, postsynaptic, **kwargs ):
        psm_tmpl = PostSynapticTemplateLibrary.get_template( modelsrc='HULL10', synapsetype='dIN-dIN-AMPA', sim=sim)
        return sim.create_synapse(
                    trigger=sim.environment.SynapticTrigger(SynapticTriggerAtTimes, time_list=times),
                    postsynaptic_mech=psm_tmpl.instantiate(cell_location=postsynaptic.soma, **kwargs))
    
    def create_synapse_dIN_to_dIN_NMDA_spike_times_new( sim, times, postsynaptic, **kwargs ):
        psm_tmpl = PostSynapticTemplateLibrary.get_template( modelsrc='HULL10', synapsetype='dIN-dIN-NMDA', sim=sim)
        return sim.create_synapse(
                    trigger=sim.environment.SynapticTrigger(SynapticTriggerAtTimes, time_list=times),
                    postsynaptic_mech=psm_tmpl.instantiate(cell_location=postsynaptic.soma, **kwargs))
    
    def create_synapse_background_NMDA_spike_times_new( sim, times, postsynaptic, **kwargs):
        psm_tmpl = PostSynapticTemplateLibrary.get_template( modelsrc='HULL10', synapsetype='dIN-dIN-Background-NMDA', sim=sim)
        return sim.create_synapse(
                    trigger=sim.environment.SynapticTrigger(SynapticTriggerAtTimes, time_list=times),
                    postsynaptic_mech=psm_tmpl.instantiate(cell_location=postsynaptic.soma, **kwargs))
    
    def create_synapse_mhr_to_dIN_inhib_spike_times_new( sim, times, postsynaptic, **kwargs ):
        psm_tmpl = PostSynapticTemplateLibrary.get_template( modelsrc='HULL10', synapsetype='MHR-dIN-Inhib', sim=sim)
        return sim.create_synapse(
                    trigger=sim.environment.SynapticTrigger(SynapticTriggerAtTimes, time_list=times),
                    postsynaptic_mech=psm_tmpl.instantiate(cell_location=postsynaptic.soma, **kwargs))
    
    def create_synapse_dIN_to_dIN_AMPA_new( sim, presynaptic, postsynaptic, **kwargs ):
        psm_tmpl = PostSynapticTemplateLibrary.get_template( modelsrc='HULL10', synapsetype='dIN-dIN-AMPA', sim=sim)
        return sim.create_synapse(
                    trigger=sim.environment.SynapticTrigger( SynapticTriggerByVoltageThreshold, cell_location = presynaptic.soma,
                                        voltage_threshold = 0*mV, delay=1.0*ms,),
                    postsynaptic_mech=psm_tmpl.instantiate(cell_location=postsynaptic.soma, **kwargs))
    
    def create_synapse_dIN_to_dIN_NMDA_new( sim, presynaptic, postsynaptic, **kwargs ):
        psm_tmpl = PostSynapticTemplateLibrary.get_template( modelsrc='HULL10', synapsetype='dIN-dIN-NMDA', sim=sim)
        return sim.create_synapse(
                    trigger=sim.environment.SynapticTrigger( SynapticTriggerByVoltageThreshold, cell_location = presynaptic.soma,
                                        voltage_threshold = 0*mV, delay=1.0*ms,),
                    postsynaptic_mech=psm_tmpl.instantiate(cell_location=postsynaptic.soma, **kwargs))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    @cached_functor
    def get_leak_chls(env):
        return env.Channel( StdChlLeak,
                conductance=qty('0.3:mS/cm2'), reversalpotential=-54.3*mV,)
    
    @cached_functor
    def get_na_chls(env):
        na_state_vars = { "m": {
                              "alpha":[-4.00,-0.10,-1.00,40.00,-10.00],
                              "beta": [ 4.00, 0.00, 0.00,65.00, 18.00]},
                        "h": {
                                "alpha":[0.07,0.00,0.00,65.00,20.00] ,
                                "beta": [1.00,0.00,1.00,35.00,-10.00]}
                          } 
        return env.Channel( StdChlAlphaBeta,
            equation='m*m*m*h', conductance=qty('120:mS/cm2'), reversalpotential=50*mV,
            statevars=na_state_vars,
            )
    
    
    @cached_functor
    def get_k_chls(env):
        k_state_vars = { "n": {
                              "alpha":[-0.55,-0.01,-1.0,55.0,-10.0],
                              "beta": [0.125,0,0,65,80]},
                           }
        return env.Channel( StdChlAlphaBeta,
            equation='n*n*n*n', conductance=qty('36:mS/cm2'), reversalpotential=-77*mV,
            statevars=k_state_vars,
            )
    
    
    def makehh(sim, name=None, cell_tags=None):
        m = MorphologyBuilder.get_single_section_soma(area=1000.*um2)
        cell = sim.create_cell(name=name, morphology=m)
        cell.apply_channel(get_leak_chls(sim.environment))
        cell.apply_channel(get_na_chls(sim.environment))
        cell.apply_channel(get_k_chls(sim.environment))
        return cell
    
    
    
    
    
    def _run_sim():
    
        env = NEURONEnvironment()
        sim = env.Simulation(cvode=True, tstop=1600 * ms)
        
    
        R_dINs = NeuronPopulation(sim=sim, n=30, neuron_functor=makehh, pop_name="RHS_dIN" )
    
        R_dINs.record_from_all( description="dIN RHS" )
    
        sim.record(R_dINs[5], what=Cell.Recordables.MembraneVoltage,  user_tags=['RHS_dIN_5'] )
        sim.record(R_dINs[10], what=Cell.Recordables.MembraneVoltage, user_tags=['RHS_dIN_10'] )
        sim.record(R_dINs[15], what=Cell.Recordables.MembraneVoltage, user_tags=['RHS_dIN_15'] )
        sim.record(R_dINs[20], what=Cell.Recordables.MembraneVoltage, user_tags=['RHS_dIN_20'] )
        sim.record(R_dINs[25], what=Cell.Recordables.MembraneVoltage, user_tags=['RHS_dIN_25'] )
    
    
        # Connect tIN -> dIN:
        tINSpikeTimesRHS = EventSet( np.random.normal(100,1,40) * ms )
        synapses_tIN_to_dIN1 = Connectors.times_to_all( sim=sim,
                                                     syncronous_times=tINSpikeTimesRHS,
                                                     postsynaptic_population=R_dINs,
                                                     connect_functor = partial( create_synapse_tIN_to_dIN_AMPANMDA_spike_times_new, parameter_overrides={'popening':1.0} ),
                                                     synapse_pop_name = "dIN_NMDA_background",)
    
        tINSpikeTimesRHS = EventSet( np.random.normal(750,1,40) * ms )
        synapses_tIN_to_dIN2 = Connectors.times_to_all( sim=sim,
                                                     syncronous_times=tINSpikeTimesRHS,
                                                     postsynaptic_population=R_dINs,
                                                     connect_functor = partial( create_synapse_tIN_to_dIN_AMPANMDA_spike_times_new, parameter_overrides={'popening':1.0} ),
                                                     synapse_pop_name = "dIN_NMDA_background2",)
        # Connect MHR -> dIN:
        MHRSpikeTimesRHS = EventSet( np.random.normal(400,15,20) * ms )
        synapses_MHR_to_dIN1 = Connectors.times_to_all( sim=sim,
                                                     syncronous_times=MHRSpikeTimesRHS,
                                                     postsynaptic_population=R_dINs,
                                                     connect_functor = partial( create_synapse_mhr_to_dIN_inhib_spike_times_new, parameter_multipliers={'peak_conductance':1.5},   ),
                                                     synapse_pop_name = "mhr_inhib",
                                                   )
        # Connect MHR -> dIN:
        MHRSpikeTimesRHS = EventSet( np.random.normal(1400,15,20) * ms )
        synapses_MHR_to_dIN2 = Connectors.times_to_all( sim=sim,
                                                     syncronous_times=MHRSpikeTimesRHS,
                                                     postsynaptic_population=R_dINs,
                                                     connect_functor = partial( create_synapse_mhr_to_dIN_inhib_spike_times_new, parameter_multipliers={'peak_conductance':1.5},   ),
                                                     synapse_pop_name = "mhr_inhib2",
                                                   )
    
        # dIN -> dIN
        synapses_dIN_to_dIN_AMPA = Connectors.all_to_all(sim,
                                presynaptic_population=R_dINs,
                                postsynaptic_population=R_dINs,
                                connect_functor = exec_with_prob(0.15, partial(create_synapse_dIN_to_dIN_AMPA_new, parameter_multipliers={'peak_conductance':0.1}))  )
        synapses_dIN_to_dIN = Connectors.all_to_all(sim,
                                presynaptic_population=R_dINs,
                                postsynaptic_population=R_dINs,
                                connect_functor = exec_with_prob(0.15, partial(create_synapse_dIN_to_dIN_NMDA_new, parameter_multipliers={'peak_conductance':1.5})))
    
    
        # Record from the tIN -> dIN population:
        synapses_tIN_to_dIN1.record_from_all(what=Synapse.Recordables.SynapticConductance, user_tags=['PREPOP:RHS_tINs'] )
        synapses_tIN_to_dIN2.record_from_all(what=Synapse.Recordables.SynapticConductance, user_tags=['PREPOP:RHS_tINs'] )
    
        synapses_MHR_to_dIN1.record_from_all(what=Synapse.Recordables.SynapticConductance, user_tags=['PREPOP:RHS_mhrs'] )
        synapses_MHR_to_dIN2.record_from_all(what=Synapse.Recordables.SynapticConductance, user_tags=['PREPOP:RHS_mhrs'] )
    
        return sim.run(), tINSpikeTimesRHS
    
    
    
    def testSingleSynapseAMPANMDA():
        res, tINSpikeTimesRHS = _run_sim()
    
        all_spikes = PopAnalSpiking.evset_all_spikes( res=res, tag_selector=TagSelector.from_string("ALL{dINs,Voltage}"), comment="dIN All Spikes" )
    
    
        rasters = []
        #for i in range(0, 30, 4):
        for i in range(0, 30):
            nrn_all_spikes = PopAnalSpiking.evset_all_spikes( res=res, tag_selector=TagSelector.from_string("ALL{Voltage, RHS_dIN_%d}"%i ), evset_tags=["SpikesFor%d"%i, 'Raster'] )
            rasters.append( nrn_all_spikes)
    
        ps = [
              TagPlot( "ALL{Conductance,POSTCELL:RHS_dIN_0} AND ANY{PREPOP:RHS_mhrs,PREPOP:RHS_tINs}",
                        yunit=nS,
                        ylabel='Conductance',
                        yticks=(0,15)*nS,
                        yrange=(0,20)*nS,
                        legend_labeller=None,
                        show_yticklabels_with_units=True,
                        yticklabel_quantisation=Decimal('1'),
              ),
              TagPlot( "ALL{Voltage, RHS_dIN_10}",
                        yunit=mV,
                        colors=['blue'],
                        ylabel='Voltage (dIN #10)',
                        legend_labeller=None,
                        yticks=(-80,-40,0,40)*mV,
                        show_yticklabels_with_units=True,
                        yticklabel_quantisation=Decimal('1')
              ),
              TagPlot( "ALL{Raster}", ylabel='Spike\nraster',legend_labeller=None, show_yticklabels=True),
              ]
    
        TagViewer([res, tINSpikeTimesRHS, all_spikes] + rasters,
                        plots=ps,
                        timerange=(50,1600)*ms,
                        xticks=(200,600,1000,1400)*ms,
                        show_xlabel = False,
                        show_xticklabels = 'only-once',
                        show_xaxis_position = 'top',
                        show_xticklabels_with_units = True,
                        xticklabel_quantisation=Decimal('1'),
                        linkage= StandardLinkages(linkage_rules=[
                                        LinkageRuleTag('ALL{PREPOP:RHS_mhrs,Conductance}', preferred_color='red'),
                                        LinkageRuleTag('ALL{PREPOP:RHS_tINs,Conductance}', preferred_color='green'),
                                        LinkageRuleTag('ALL{Voltage, RHS_dIN_10}', preferred_color='blue'),
                                                    ])
                        )
    
    
    
    MFRandom.seed(1000)
    testSingleSynapseAMPANMDA()
    
    
    
    
    
    
    




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/multicell_simulation050_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/multicell_simulation050_out1.png>`






Output
~~~~~~

.. code-block:: bash

        No handlers could be found for logger "neurounits"
    2013-12-01 17:14:25,368 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:14:25,369 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
    No handlers could be found for logger "neurounits"
    2013-12-01 17:14:33,168 - morphforge.core.logmgr - INFO - Logger Started OK
    2013-12-01 17:14:33,168 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Loading Bundle from: /mnt/scratch/tmp/morphforge/tmp/simulationresults/af/af18b55f1f75f042d3f88deeeb4d88df.bundle (467k) : 1.004 seconds
    set(['conductance', 'reversalpotential'])
    __dict__ {'mm_neuronNumber': None, 'cachedNeuronSuffix': None, 'reversalpotential': array(-54.3) * mV, '_name': 'AnonObj0001', '_simulation': None, 'conductance': array(3.0) * s**3*A**2/(kg*m**4)}
    
    Executing: /home/michael/opt//x86_64/bin/modlunit /mnt/scratch/tmp/morphforge/tmp/tmp_449ee3b9549e47025d868977ba93dda4.mod
    /mnt/scratch/tmp/morphforge/tmp/modbuild_22922
    Executing: /home/michael/opt//x86_64/bin/nocmodl tmp_449ee3b9549e47025d868977ba93dda4.mod
    Executing: /home/michael/opt//share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/home/michael/opt//include/nrn"  -I"/home/michael/opt//x86_64/lib"    -g -O2 -c -o tmp_449ee3b9549e47025d868977ba93dda4.lo tmp_449ee3b9549e47025d868977ba93dda4.c  
    Executing: /home/michael/opt//share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_449ee3b9549e47025d868977ba93dda4.la  -rpath /home/michael/opt//x86_64/libs  tmp_449ee3b9549e47025d868977ba93dda4.lo  -L/home/michael/opt//x86_64/lib -L/home/michael/opt//x86_64/lib  /home/michael/opt//x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
    OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/home/michael/opt//include/nrn -I/home/michael/opt//x86_64/lib -g -O2 -c tmp_449ee3b9549e47025d868977ba93dda4.c  -fPIC -DPIC -o .libs/tmp_449ee3b9549e47025d868977ba93dda4.o
    
    OP2: libtool: link: gcc -shared  -fPIC -DPIC  .libs/tmp_449ee3b9549e47025d868977ba93dda4.o   -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -L/home/michael/opt//x86_64/lib /home/michael/opt/x86_64/lib/libnrniv.so /home/michael/opt/x86_64/lib/libnrnoc.so /home/michael/opt/x86_64/lib/liboc.so /home/michael/opt/x86_64/lib/libmemacs.so /home/michael/opt/x86_64/lib/libnrnmpi.so /home/michael/opt/x86_64/lib/libscopmath.so /home/michael/opt/x86_64/lib/libsparse13.so -lreadline -lncurses /home/michael/opt/x86_64/lib/libivoc.so /home/michael/opt/x86_64/lib/libneuron_gnu.so /home/michael/opt/x86_64/lib/libmeschach.so /home/michael/opt/x86_64/lib/libsundials.so -lm -ldl  -O2   -pthread -Wl,-soname -Wl,tmp_449ee3b9549e47025d868977ba93dda4.so.0 -o .libs/tmp_449ee3b9549e47025d868977ba93dda4.so.0.0.0
    libtool: link: (cd ".libs" && rm -f "tmp_449ee3b9549e47025d868977ba93dda4.so.0" && ln -s "tmp_449ee3b9549e47025d868977ba93dda4.so.0.0.0" "tmp_449ee3b9549e47025d868977ba93dda4.so.0")
    libtool: link: (cd ".libs" && rm -f "tmp_449ee3b9549e47025d868977ba93dda4.so" && ln -s "tmp_449ee3b9549e47025d868977ba93dda4.so.0.0.0" "tmp_449ee3b9549e47025d868977ba93dda4.so")
    libtool: link: ( cd ".libs" && rm -f "tmp_449ee3b9549e47025d868977ba93dda4.la" && ln -s "../tmp_449ee3b9549e47025d868977ba93dda4.la" "tmp_449ee3b9549e47025d868977ba93dda4.la" )
    
    Executing: /home/michael/opt//x86_64/bin/modlunit /mnt/scratch/tmp/morphforge/tmp/tmp_c645d0d1b217c6d417ecc3556d0600bb.mod
    /mnt/scratch/tmp/morphforge/tmp/modbuild_22922
    Executing: /home/michael/opt//x86_64/bin/nocmodl tmp_c645d0d1b217c6d417ecc3556d0600bb.mod
    Executing: /home/michael/opt//share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -NEURON -- Release 7.3 (869:0141cf0aff14) 2013-05-10
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2013
    See http://www.neuron.yale.edu/neuron/credits
    
    I"/home/michael/opt//include/nrn"  -I"/home/michael/opt//x86_64/lib"    -g -O2 -c -o tmp_c645d0d1b217c6d417ecc3556d0600bb.lo tmp_c645d0d1b217c6d417ecc3556d0600bb.c  
    Executing: /home/michael/opt//share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_c645d0d1b217c6d417ecc3556d0600bb.la  -rpath /home/michael/opt//x86_64/libs  tmp_c645d0d1b217c6d417ecc3556d0600bb.lo  -L/home/michael/opt//x86_64/lib -L/home/michael/opt//x86_64/lib  /home/michael/opt//x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
    OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/home/michael/opt//include/nrn -I/home/michael/opt//x86_64/lib -g -O2 -c tmp_c645d0d1b217c6d417ecc3556d0600bb.c  -fPIC -DPIC -o .libs/tmp_c645d0d1b217c6d417ecc3556d0600bb.o
    
    OP2: libtool: link: gcc -shared  -fPIC -DPIC  .libs/tmp_c645d0d1b217c6d417ecc3556d0600bb.o   -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -Wl,-rpath -Wl,/home/michael/opt/x86_64/lib -L/home/michael/opt//x86_64/lib /home/michael/opt/x86_64/lib/libnrniv.so /home/michael/opt/x86_64/lib/libnrnoc.so /home/michael/opt/x86_64/lib/liboc.so /home/michael/opt/x86_64/lib/libmemacs.so /home/michael/opt/x86_64/lib/libnrnmpi.so /home/michael/opt/x86_64/lib/libscopmath.so /home/michael/opt/x86_64/lib/libsparse13.so -lreadline -lncurses /home/michael/opt/x86_64/lib/libivoc.so /home/michael/opt/x86_64/lib/libneuron_gnu.so /home/michael/opt/x86_64/lib/libmeschach.so /home/michael/opt/x86_64/lib/libsundials.so -lm -ldl  -O2   -pthread -Wl,-soname -Wl,tmp_c645d0d1b217c6d417ecc3556d0600bb.so.0 -o .libs/tmp_c645d0d1b217c6d417ecc3556d0600bb.so.0.0.0
    libtool: link: (cd ".libs" && rm -f "tmp_c645d0d1b217c6d417ecc3556d0600bb.so.0" && ln -s "tmp_c645d0d1b217c6d417ecc3556d0600bb.so.0.0.0" "tmp_c645d0d1b217c6d417ecc3556d0600bb.so.0")
    libtool: link: (cd ".libs" && rm -f "tmp_c645d0d1b217c6d417ecc3556d0600bb.so" && ln -s "tmp_c645d0d1b217c6d417ecc3556d0600bb.so.0.0.0" "tmp_c645d0d1b217c6d417ecc3556d0600bb.so")
    libtool: link: ( cd ".libs" && rm -f "tmp_c645d0d1b217c6d417ecc3556d0600bb.la" && ln -s "../tmp_c645d0d1b217c6d417ecc3556d0600bb.la" "tmp_c645d0d1b217c6d417ecc3556d0600bb.la" )
    
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_5c68193e39038c48d55b2b964c7f2cc8.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_4f04099fdf3d7f394ae2f9380ee19d2a.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_d6feb6f6ba733237c404c850caa9ef5e.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_1b4cbb91ff4fbb73a54a2a3d929adce5.so
    loading membrane mechanisms from /mnt/scratch/tmp/morphforge/tmp/modout/mod_e1d9b15c15cf730d6ad5de223a1b3007.so
    Running Hoc File: /mnt/scratch/tmp/morphforge/tmp/tmp_a108bc73b58581add7b4db3708bc0635.hoc
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
    Time for Extracting Data: (215 records) 1.47911500931
    Running simulation : 44.817 seconds
    Size of results file: 220.7 (MB)
    Post-processing : 15.334 seconds
    Entire load-run-save time : 61.156 seconds
    Suceeded
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    _run_spawn() [Loading results from /mnt/scratch/tmp/morphforge/tmp/simulationresults/af//af18b55f1f75f042d3f88deeeb4d88df.neuronsim.results.pickle ]
    PlotManger saving:  _output/figures/multicell_simulation050/{png,svg}/fig000_Autosave_figure_1.{png,svg}




