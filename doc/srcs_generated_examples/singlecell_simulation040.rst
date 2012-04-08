
11. Investigating the rheobase of a neuron with a parameter sweep
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
	    
	    ApplyMechanismEverywhereUniform(myCell, leakChannels )
	    ApplyMechanismEverywhereUniform(myCell, sodiumChannels )
	    ApplyMechanismEverywhereUniform(myCell, potFastChannels )
	    ApplyMechanismEverywhereUniform(myCell, potSlowChannels )
	    ApplyPassiveEverywhereUniform(myCell, PassiveProperty.SpecificCapacitance, unit('2.0:uF/cm2') )
	    
	    
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

    	Setting Random Seed: 70572
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//20/208a511afda2f610fafdfcf7d32e6d1d.bundle
	Setting Random Seed: 84582
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_8a5052bb0948c4071523c883ab271a58.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_8a5052bb0948c4071523c883ab271a58.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_8a5052bb0948c4071523c883ab271a58.lo tmp_8a5052bb0948c4071523c883ab271a58.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_8a5052bb0948c4071523c883ab271a58.la  -rpath /opt/nrn/x86_64/libs  tmp_8a5052bb0948c4071523c883ab271a58.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_e5d8e6d43ea610b4174c6fea4508880e.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_e5d8e6d43ea610b4174c6fea4508880e.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_e5d8e6d43ea610b4174c6fea4508880e.lo tmp_e5d8e6d43ea610b4174c6fea4508880e.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_e5d8e6d43ea610b4174c6fea4508880e.la  -rpath /opt/nrn/x86_64/libs  tmp_e5d8e6d43ea610b4174c6fea4508880e.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_46e759c0cc38a7b15143679384e5e34a.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_46e759c0cc38a7b15143679384e5e34a.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_46e759c0cc38a7b15143679384e5e34a.lo tmp_46e759c0cc38a7b15143679384e5e34a.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_46e759c0cc38a7b15143679384e5e34a.la  -rpath /opt/nrn/x86_64/libs  tmp_46e759c0cc38a7b15143679384e5e34a.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_7dea6d7a67753b3f01dbada35329f51e.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_7dea6d7a67753b3f01dbada35329f51e.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_7dea6d7a67753b3f01dbada35329f51e.lo tmp_7dea6d7a67753b3f01dbada35329f51e.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_7dea6d7a67753b3f01dbada35329f51e.la  -rpath /opt/nrn/x86_64/libs  tmp_7dea6d7a67753b3f01dbada35329f51e.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Time for Building Mod-Files:  2.0056040287
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_393746b359f54aff05ab3e0408ba1884.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_9e4b8d7484635a4df0ee77398c6aa7ae.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_6219b16f7c219a561b5ead6f0baf8317.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_a8a8776faa2259e8f56dc9507bfa9568.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.010085105896
	Time for Extracting Data: (2 records) 0.00104904174805
	Simulation Time Elapsed:  2.27730202675
	Suceeded
	Setting Random Seed: 34245
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//06/06264df7fb831496abfd38be585307c2.bundle
	Setting Random Seed: 84582
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_4f6fe0120f9e61e1a3468fe11a57efbf.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_4f6fe0120f9e61e1a3468fe11a57efbf.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_4f6fe0120f9e61e1a3468fe11a57efbf.lo tmp_4f6fe0120f9e61e1a3468fe11a57efbf.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_4f6fe0120f9e61e1a3468fe11a57efbf.la  -rpath /opt/nrn/x86_64/libs  tmp_4f6fe0120f9e61e1a3468fe11a57efbf.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_a41413b875f3390b837f982b58669ec9.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_a41413b875f3390b837f982b58669ec9.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_a41413b875f3390b837f982b58669ec9.lo tmp_a41413b875f3390b837f982b58669ec9.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_a41413b875f3390b837f982b58669ec9.la  -rpath /opt/nrn/x86_64/libs  tmp_a41413b875f3390b837f982b58669ec9.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_177c0b67aa73f5b755294b186c984ea2.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_177c0b67aa73f5b755294b186c984ea2.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_177c0b67aa73f5b755294b186c984ea2.lo tmp_177c0b67aa73f5b755294b186c984ea2.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_177c0b67aa73f5b755294b186c984ea2.la  -rpath /opt/nrn/x86_64/libs  tmp_177c0b67aa73f5b755294b186c984ea2.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_4cdeb79ebe462071890b8e64403246df.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_4cdeb79ebe462071890b8e64403246df.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_4cdeb79ebe462071890b8e64403246df.lo tmp_4cdeb79ebe462071890b8e64403246df.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_4cdeb79ebe462071890b8e64403246df.la  -rpath /opt/nrn/x86_64/libs  tmp_4cdeb79ebe462071890b8e64403246df.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Time for Building Mod-Files:  2.04093122482
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_fdc4ba95dc89091b81dc90c2ba3ba022.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_0919e1fe75db0337ee796d940e1177c4.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_6ee6f46dc50d08c0551cd862973f6285.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_9ce35968d17de56ec8939b8f6347a0df.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0104310512543
	Time for Extracting Data: (2 records) 0.000874042510986
	Simulation Time Elapsed:  2.30545806885
	Suceeded
	Setting Random Seed: 19233
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//1e/1e6d21cb7ce88efc99be67a633ad920f.bundle
	Setting Random Seed: 84582
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_748df108386ac777eb81130ee03c4916.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_748df108386ac777eb81130ee03c4916.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_748df108386ac777eb81130ee03c4916.lo tmp_748df108386ac777eb81130ee03c4916.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_748df108386ac777eb81130ee03c4916.la  -rpath /opt/nrn/x86_64/libs  tmp_748df108386ac777eb81130ee03c4916.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_2ab949fc78e07201eb410ddfa2ecefb7.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_2ab949fc78e07201eb410ddfa2ecefb7.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_2ab949fc78e07201eb410ddfa2ecefb7.lo tmp_2ab949fc78e07201eb410ddfa2ecefb7.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_2ab949fc78e07201eb410ddfa2ecefb7.la  -rpath /opt/nrn/x86_64/libs  tmp_2ab949fc78e07201eb410ddfa2ecefb7.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_4ce796a44d1498a870b3f55e9947ee1d.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_4ce796a44d1498a870b3f55e9947ee1d.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_4ce796a44d1498a870b3f55e9947ee1d.lo tmp_4ce796a44d1498a870b3f55e9947ee1d.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_4ce796a44d1498a870b3f55e9947ee1d.la  -rpath /opt/nrn/x86_64/libs  tmp_4ce796a44d1498a870b3f55e9947ee1d.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_1da8243ad24371220e34b644f0452479.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_1da8243ad24371220e34b644f0452479.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_1da8243ad24371220e34b644f0452479.lo tmp_1da8243ad24371220e34b644f0452479.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_1da8243ad24371220e34b644f0452479.la  -rpath /opt/nrn/x86_64/libs  tmp_1da8243ad24371220e34b644f0452479.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Time for Building Mod-Files:  2.11959886551
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_412e286992de17d5b0002b924fec5db8.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_38bcfdecaf2f70f8f53a31878615c9dc.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_fcd6c4a8a5712bde3584e642ea391fbb.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_5c7a63adbd0f95dc1cee4901d68f221a.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0153949260712
	Time for Extracting Data: (2 records) 0.000941038131714
	Simulation Time Elapsed:  2.38706493378
	Suceeded
	Setting Random Seed: 63249
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//b2/b27681224762117a63f5b5341fc95c2a.bundle
	Setting Random Seed: 84582
	Time for Building Mod-Files:  0.000849008560181
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_fdc4ba95dc89091b81dc90c2ba3ba022.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_0919e1fe75db0337ee796d940e1177c4.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_6ee6f46dc50d08c0551cd862973f6285.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_9ce35968d17de56ec8939b8f6347a0df.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0151770114899
	Time for Extracting Data: (2 records) 0.000777959823608
	Simulation Time Elapsed:  0.262201786041
	Suceeded
	Setting Random Seed: 10940
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//b3/b367cbf0e5988380fb6a3b2f8b6e5097.bundle
	Setting Random Seed: 84582
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_a153e4cdc7cd470c652ffd2a5435b530.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_a153e4cdc7cd470c652ffd2a5435b530.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_a153e4cdc7cd470c652ffd2a5435b530.lo tmp_a153e4cdc7cd470c652ffd2a5435b530.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_a153e4cdc7cd470c652ffd2a5435b530.la  -rpath /opt/nrn/x86_64/libs  tmp_a153e4cdc7cd470c652ffd2a5435b530.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_24ecbe6e1478a563ead5546413b1bc40.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_24ecbe6e1478a563ead5546413b1bc40.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_24ecbe6e1478a563ead5546413b1bc40.lo tmp_24ecbe6e1478a563ead5546413b1bc40.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_24ecbe6e1478a563ead5546413b1bc40.la  -rpath /opt/nrn/x86_64/libs  tmp_24ecbe6e1478a563ead5546413b1bc40.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_0ea49cbe64d88d0216837871aed5580b.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_0ea49cbe64d88d0216837871aed5580b.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_0ea49cbe64d88d0216837871aed5580b.lo tmp_0ea49cbe64d88d0216837871aed5580b.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_0ea49cbe64d88d0216837871aed5580b.la  -rpath /opt/nrn/x86_64/libs  tmp_0ea49cbe64d88d0216837871aed5580b.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_203fcb3e1f0f58fe469ec321a57b0a26.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_203fcb3e1f0f58fe469ec321a57b0a26.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_203fcb3e1f0f58fe469ec321a57b0a26.lo tmp_203fcb3e1f0f58fe469ec321a57b0a26.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_203fcb3e1f0f58fe469ec321a57b0a26.la  -rpath /opt/nrn/x86_64/libs  tmp_203fcb3e1f0f58fe469ec321a57b0a26.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Time for Building Mod-Files:  2.09443187714
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_decfebebc30dbe70a288187722b50c03.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_8a12703ee976afeed0fd6812981515c2.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_9603c34f339b5684aa756f5d11d336d6.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_52f7c720dd22a799fb19e3a71573e885.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0160281658173
	Time for Extracting Data: (2 records) 0.00114703178406
	Simulation Time Elapsed:  2.36702513695
	Suceeded
	Setting Random Seed: 99169
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//16/16cf048ac66a47450dc2ac8bc7c3b1d4.bundle
	Setting Random Seed: 84582
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_9253dd1065b513482b53ae6cf9e09593.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_9253dd1065b513482b53ae6cf9e09593.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_9253dd1065b513482b53ae6cf9e09593.lo tmp_9253dd1065b513482b53ae6cf9e09593.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_9253dd1065b513482b53ae6cf9e09593.la  -rpath /opt/nrn/x86_64/libs  tmp_9253dd1065b513482b53ae6cf9e09593.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_60bd2ff05f494358dd22f4276817b946.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_60bd2ff05f494358dd22f4276817b946.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_60bd2ff05f494358dd22f4276817b946.lo tmp_60bd2ff05f494358dd22f4276817b946.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_60bd2ff05f494358dd22f4276817b946.la  -rpath /opt/nrn/x86_64/libs  tmp_60bd2ff05f494358dd22f4276817b946.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_f5d6ae90cf020d7b655baab9ef4f97cb.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_f5d6ae90cf020d7b655baab9ef4f97cb.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_f5d6ae90cf020d7b655baab9ef4f97cb.lo tmp_f5d6ae90cf020d7b655baab9ef4f97cb.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_f5d6ae90cf020d7b655baab9ef4f97cb.la  -rpath /opt/nrn/x86_64/libs  tmp_f5d6ae90cf020d7b655baab9ef4f97cb.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_c5386ca8e9479647617773e07428f294.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_c5386ca8e9479647617773e07428f294.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_c5386ca8e9479647617773e07428f294.lo tmp_c5386ca8e9479647617773e07428f294.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_c5386ca8e9479647617773e07428f294.la  -rpath /opt/nrn/x86_64/libs  tmp_c5386ca8e9479647617773e07428f294.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Time for Building Mod-Files:  2.060516119
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_cf23dc6c4f01eb78afa6bb5dd06e6212.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_bed6dca2f55d3d5fe49ede8bd89119d1.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_246cdf0c0eed636fc64337986835d33b.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_27a1b034383793475c8956a861916ec3.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0138709545135
	Time for Extracting Data: (2 records) 0.000982999801636
	Simulation Time Elapsed:  2.31628108025
	Suceeded
	Setting Random Seed: 84582
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x3981210>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x39767d0>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x39764d0>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x3971d10>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x3971d50>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x3975f50>
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x392a910>
	Setting Time Range [  95.  200.] ms
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x394ad90>
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



