
12. Investigating the rheobase of a neuron with a parameter sweep
=================================================================



Investigating the rheobase of a neuron with a parameter sweep

WARNING: The automatic naming and linkage between grpah colors is currently under a refactor;
what is done in this script is not representing the best possible solution, or even something that
will reliably work in the future! 

The aim of this script is just to show that it is possible to run multiple simulations from a single script!







Code
~~~~

.. code-block:: python

	"""Investigating the rheobase of a neuron with a parameter sweep
	
	WARNING: The automatic naming and linkage between grpah colors is currently under a refactor;
	what is done in this script is not representing the best possible solution, or even something that
	will reliably work in the future! 
	
	The aim of this script is just to show that it is possible to run multiple simulations from a single script!
	
	
	
	
	"""
	
	
	from morphforge.stdimports import *
	from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmleak import MM_LeakChannel
	from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmalphabeta import MM_AlphaBetaChannel
	
	
	
	def get_Na_Channels(env):
	    naStateVars = {"m": 
	                    {"alpha": [ 13.01,0,4,-1.01,-12.56 ], "beta": [5.73,0,1,9.01,9.69 ] }, 
	                   "h":
	                    {"alpha": [ 0.06,0,0,30.88,26 ], "beta": [3.06,0,1,-7.09,-10.21 ]}
	                   }
	        
	    return  env.MembraneMechanism( 
	                            MM_AlphaBetaChannel,
	                            name="NaChl", ion="na",
	                            equation="m*m*m*h",
	                            conductance=unit("210:nS") / unit("400:um2"),
	                            reversalpotential=unit("50.0:mV"),
	                            statevars=naStateVars,
	                            mechanism_id = 'Na_ID'
	                            )
	    
	def get_Ks_Channels(env):
	    kfStateVars = {"ks": {"alpha": [ 0.2,0,1,-6.96,-7.74  ], "beta": [0.05,0,2,-18.07,6.1  ] } } 
	
	    return  env.MembraneMechanism( 
	                            MM_AlphaBetaChannel,
	                            name="KsChl", ion="ks",
	                            equation="ks*ks*ks*ks",
	                            conductance=unit("3:nS") / unit("400:um2"),
	                            reversalpotential=unit("-80.0:mV"),
	                            statevars=kfStateVars,
	                            mechanism_id = 'IN_Ks_ID'
	                            )
	    
	def get_Kf_Channels(env):
	    kfStateVars = {"kf": {"alpha": [  3.1,0,1,-31.5,-9.3 ], "beta": [0.44,0,1,4.98,16.19  ] } } 
	                   
	    return  env.MembraneMechanism( 
	                            MM_AlphaBetaChannel,
	                            name="KfChl", ion="kf",
	                            equation="kf*kf*kf*kf",
	                            conductance=unit("0.5:nS") / unit("400:um2") ,
	                            reversalpotential=unit("-80.0:mV"),
	                            statevars=kfStateVars,
	                            mechanism_id = 'N_Kf_ID'
	                            )
	
	def get_Lk_Channels(env):
	    leakChannels = env.MembraneMechanism( 
	                         MM_LeakChannel,
	                         name="LkChl", 
	                         conductance=unit("3.6765:nS") / unit("400:um2"), 
	                         reversalpotential=unit("-51:mV"),
	                         mechanism_id = 'Lk_ID'
	                        )
	    return leakChannels
	
	
	
	
	def simulate(current_inj_level):
	    # Create the environment:
	    env = NeuronSimulationEnvironment()
	    
	    # Create the simulation:
	    mySim = env.Simulation(name="AA")
	    
	    
	    # Create a cell:
	    morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
	    morph = MorphologyTree.fromDictionary(morphDict1)
	    myCell = mySim.createCell(name="Cell1", morphology=morph)
	    
	    leakChannels = get_Lk_Channels(env)
	    sodiumChannels = get_Na_Channels(env)
	    potFastChannels = get_Kf_Channels(env)
	    potSlowChannels = get_Ks_Channels(env)
	    
	    shortcuts.ApplyMechanismEverywhereUniform(myCell, leakChannels )
	    shortcuts.ApplyMechanismEverywhereUniform(myCell, sodiumChannels )
	    shortcuts.ApplyMechanismEverywhereUniform(myCell, potFastChannels )
	    shortcuts.ApplyMechanismEverywhereUniform(myCell, potSlowChannels )
	    shortcuts.ApplyPassiveEverywhereUniform(myCell, PassiveProperty.SpecificCapacitance, unit('2.0:uF/cm2') )
	    
	    
	    # Get a location on the cell:
	    somaLoc = myCell.getLocation("soma")
	    
	    # Create the stimulus and record the injected current:
	    cc = mySim.createCurrentClamp( amp=current_inj_level, dur=unit("100:ms"), delay=unit("100:ms"), celllocation=somaLoc)
	    mySim.record(cc, what=StdRec.Current)
	    
	    # Define what to record:
	    mySim.record( myCell, what=StdRec.MembraneVoltage, location = somaLoc ) 
	    
	    # Run the simulation
	    results = mySim.Run()
	    
	    return results
	
	
	# Display the results:
	results = [ simulate(current_inj_level='%d:pA'%i) for i in [50,100,150,200, 250, 300]   ]
	TagViewer(results, timeranges=[(95, 200)*pq.ms], show=True )
	
	


Output
~~~~~~

.. code-block:: bash

    	Setting Random Seed: 78480
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//d0/d006f76062b51c929c131f79e2d79593.bundle
	Setting Random Seed: 86938
	Time for Building Mod-Files:  0.00115585327148
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_fdc4ba95dc89091b81dc90c2ba3ba022.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_0919e1fe75db0337ee796d940e1177c4.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_6ee6f46dc50d08c0551cd862973f6285.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_9ce35968d17de56ec8939b8f6347a0df.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0299959182739
	Time for Extracting Data: (2 records) 0.000874042510986
	Simulation Time Elapsed:  0.43520283699
	Suceeded
	Setting Random Seed: 14148
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//d1/d121a0e5695b38df265520f60bd1ce37.bundle
	Setting Random Seed: 86938
	Time for Building Mod-Files:  0.00105094909668
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_fdc4ba95dc89091b81dc90c2ba3ba022.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_0919e1fe75db0337ee796d940e1177c4.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_6ee6f46dc50d08c0551cd862973f6285.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_9ce35968d17de56ec8939b8f6347a0df.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0289380550385
	Time for Extracting Data: (2 records) 0.000905990600586
	Simulation Time Elapsed:  0.430787086487
	Suceeded
	Setting Random Seed: 88536
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//73/73c23924b8c37d9e7e5c5033c5aa7677.bundle
	Setting Random Seed: 86938
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_983fcce43bea49a8d559582f961eea66.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_983fcce43bea49a8d559582f961eea66.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_983fcce43bea49a8d559582f961eea66.lo tmp_983fcce43bea49a8d559582f961eea66.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_983fcce43bea49a8d559582f961eea66.la  -rpath /opt/nrn/x86_64/libs  tmp_983fcce43bea49a8d559582f961eea66.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_22b9cc77b1a2250abea12eb9f16271f6.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_22b9cc77b1a2250abea12eb9f16271f6.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_22b9cc77b1a2250abea12eb9f16271f6.lo tmp_22b9cc77b1a2250abea12eb9f16271f6.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_22b9cc77b1a2250abea12eb9f16271f6.la  -rpath /opt/nrn/x86_64/libs  tmp_22b9cc77b1a2250abea12eb9f16271f6.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_a45c9dbc93d8747b425100d034fe052b.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_a45c9dbc93d8747b425100d034fe052b.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_a45c9dbc93d8747b425100d034fe052b.lo tmp_a45c9dbc93d8747b425100d034fe052b.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_a45c9dbc93d8747b425100d034fe052b.la  -rpath /opt/nrn/x86_64/libs  tmp_a45c9dbc93d8747b425100d034fe052b.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_d4ed8d370905d2953d22dab8dd62b5d2.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_d4ed8d370905d2953d22dab8dd62b5d2.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_d4ed8d370905d2953d22dab8dd62b5d2.lo tmp_d4ed8d370905d2953d22dab8dd62b5d2.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_d4ed8d370905d2953d22dab8dd62b5d2.la  -rpath /opt/nrn/x86_64/libs  tmp_d4ed8d370905d2953d22dab8dd62b5d2.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Time for Building Mod-Files:  3.09823322296
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_cf23dc6c4f01eb78afa6bb5dd06e6212.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_bed6dca2f55d3d5fe49ede8bd89119d1.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_246cdf0c0eed636fc64337986835d33b.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_27a1b034383793475c8956a861916ec3.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0383179187775
	Time for Extracting Data: (2 records) 0.00129795074463
	Simulation Time Elapsed:  3.55089688301
	Suceeded
	Setting Random Seed: 44366
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//d2/d254578953a303784a8b7e4f49d1470f.bundle
	Setting Random Seed: 86938
	Time for Building Mod-Files:  0.00128602981567
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_393746b359f54aff05ab3e0408ba1884.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_9e4b8d7484635a4df0ee77398c6aa7ae.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_6219b16f7c219a561b5ead6f0baf8317.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_a8a8776faa2259e8f56dc9507bfa9568.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0227348804474
	Time for Extracting Data: (2 records) 0.000886917114258
	Simulation Time Elapsed:  0.434092998505
	Suceeded
	Setting Random Seed: 14597
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//58/58b8e426b511920a065f8529e5a1790b.bundle
	Setting Random Seed: 86938
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_076de3e979c199d163c9bffe50b01c39.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_076de3e979c199d163c9bffe50b01c39.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_076de3e979c199d163c9bffe50b01c39.lo tmp_076de3e979c199d163c9bffe50b01c39.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_076de3e979c199d163c9bffe50b01c39.la  -rpath /opt/nrn/x86_64/libs  tmp_076de3e979c199d163c9bffe50b01c39.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_df89837772217d402b82fd57684f629d.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_df89837772217d402b82fd57684f629d.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_df89837772217d402b82fd57684f629d.lo tmp_df89837772217d402b82fd57684f629d.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_df89837772217d402b82fd57684f629d.la  -rpath /opt/nrn/x86_64/libs  tmp_df89837772217d402b82fd57684f629d.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_4ba1ca35bf83c94896256a247e5771dc.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_4ba1ca35bf83c94896256a247e5771dc.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_4ba1ca35bf83c94896256a247e5771dc.lo tmp_4ba1ca35bf83c94896256a247e5771dc.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_4ba1ca35bf83c94896256a247e5771dc.la  -rpath /opt/nrn/x86_64/libs  tmp_4ba1ca35bf83c94896256a247e5771dc.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_a187e9b1614de6b383a642c00fdbb55a.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_a187e9b1614de6b383a642c00fdbb55a.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_a187e9b1614de6b383a642c00fdbb55a.lo tmp_a187e9b1614de6b383a642c00fdbb55a.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_a187e9b1614de6b383a642c00fdbb55a.la  -rpath /opt/nrn/x86_64/libs  tmp_a187e9b1614de6b383a642c00fdbb55a.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Time for Building Mod-Files:  2.66265106201
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_2d9d78987762c0d7b4bda18207cacfcb.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_08ebe2d55da70bb9b4c11decaba918b4.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_a5be137beddc414f0124d6b6e96cf42e.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_4a9b2a63acab2d542d363bc15ead5aca.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0268681049347
	Time for Extracting Data: (2 records) 0.00133490562439
	Simulation Time Elapsed:  3.09980487823
	Suceeded
	Setting Random Seed: 22092
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//3a/3a4b2dbe59a9641bd8058876913b0789.bundle
	Setting Random Seed: 86938
	Time for Building Mod-Files:  0.00105381011963
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_fdc4ba95dc89091b81dc90c2ba3ba022.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_0919e1fe75db0337ee796d940e1177c4.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_6ee6f46dc50d08c0551cd862973f6285.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_9ce35968d17de56ec8939b8f6347a0df.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0417790412903
	Time for Extracting Data: (2 records) 0.000936031341553
	Simulation Time Elapsed:  0.452094078064
	Suceeded
	Setting Random Seed: 86938
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x3210890>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x320ad90>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x320aa50>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x31fd450>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x3200510>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x3204110>
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x31b9350>
	Setting Time Range [  95.  200.] ms
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x31dc6d0>
	Setting Time Range [  95.  200.] ms
	Setting Yunit 1 pA (picoampere)
	Saving File _output/figures/singlecell_simulation040/eps/fig000_None.eps
	Saving File _output/figures/singlecell_simulation040/pdf/fig000_None.pdf
	Saving File _output/figures/singlecell_simulation040/png/fig000_None.png
	Saving File _output/figures/singlecell_simulation040/svg/fig000_None.svg
	



Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation040_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation040_out1.png>`



