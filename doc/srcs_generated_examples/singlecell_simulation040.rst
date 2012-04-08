
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

    	Setting Random Seed: 77149
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//20/208a511afda2f610fafdfcf7d32e6d1d.bundle
	Setting Random Seed: 69403
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_e1b89fdc34cbf062a60781404f41c1d2.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_e1b89fdc34cbf062a60781404f41c1d2.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_e1b89fdc34cbf062a60781404f41c1d2.lo tmp_e1b89fdc34cbf062a60781404f41c1d2.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_e1b89fdc34cbf062a60781404f41c1d2.la  -rpath /opt/nrn/x86_64/libs  tmp_e1b89fdc34cbf062a60781404f41c1d2.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_33e71969c0bc35012f382ed99fed61f6.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_33e71969c0bc35012f382ed99fed61f6.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_33e71969c0bc35012f382ed99fed61f6.lo tmp_33e71969c0bc35012f382ed99fed61f6.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_33e71969c0bc35012f382ed99fed61f6.la  -rpath /opt/nrn/x86_64/libs  tmp_33e71969c0bc35012f382ed99fed61f6.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_81c8996876ae362887af818d8b9ad96e.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_81c8996876ae362887af818d8b9ad96e.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_81c8996876ae362887af818d8b9ad96e.lo tmp_81c8996876ae362887af818d8b9ad96e.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_81c8996876ae362887af818d8b9ad96e.la  -rpath /opt/nrn/x86_64/libs  tmp_81c8996876ae362887af818d8b9ad96e.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_10d604d1ed1a0ee0784d0505e9b40c1e.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_10d604d1ed1a0ee0784d0505e9b40c1e.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_10d604d1ed1a0ee0784d0505e9b40c1e.lo tmp_10d604d1ed1a0ee0784d0505e9b40c1e.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_10d604d1ed1a0ee0784d0505e9b40c1e.la  -rpath /opt/nrn/x86_64/libs  tmp_10d604d1ed1a0ee0784d0505e9b40c1e.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Time for Building Mod-Files:  1.6847679615
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_e3f0c0dac17eccfb717a9b3c3298ee62.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_a9a29e058800e4260c553399bf090500.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_b2c85f10c9d93eaeed49d6a978572d64.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_973f43a7da443db4d18f3e17de5e0bc9.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0108768939972
	Time for Extracting Data: (2 records) 0.00087308883667
	Simulation Time Elapsed:  2.03070497513
	Suceeded
	Setting Random Seed: 27928
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//06/06264df7fb831496abfd38be585307c2.bundle
	Setting Random Seed: 69403
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_68c2185bf9153cef88e1242ad849f7bd.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_68c2185bf9153cef88e1242ad849f7bd.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_68c2185bf9153cef88e1242ad849f7bd.lo tmp_68c2185bf9153cef88e1242ad849f7bd.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_68c2185bf9153cef88e1242ad849f7bd.la  -rpath /opt/nrn/x86_64/libs  tmp_68c2185bf9153cef88e1242ad849f7bd.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_db225c041f861342136a2ec1ad7ebfea.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_db225c041f861342136a2ec1ad7ebfea.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_db225c041f861342136a2ec1ad7ebfea.lo tmp_db225c041f861342136a2ec1ad7ebfea.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_db225c041f861342136a2ec1ad7ebfea.la  -rpath /opt/nrn/x86_64/libs  tmp_db225c041f861342136a2ec1ad7ebfea.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_da6be8dcb2d376277b5bb75f476abbcb.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_da6be8dcb2d376277b5bb75f476abbcb.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_da6be8dcb2d376277b5bb75f476abbcb.lo tmp_da6be8dcb2d376277b5bb75f476abbcb.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_da6be8dcb2d376277b5bb75f476abbcb.la  -rpath /opt/nrn/x86_64/libs  tmp_da6be8dcb2d376277b5bb75f476abbcb.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_8b30fb365f8a707ebb1e3c1bf0c8eee3.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_8b30fb365f8a707ebb1e3c1bf0c8eee3.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_8b30fb365f8a707ebb1e3c1bf0c8eee3.lo tmp_8b30fb365f8a707ebb1e3c1bf0c8eee3.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_8b30fb365f8a707ebb1e3c1bf0c8eee3.la  -rpath /opt/nrn/x86_64/libs  tmp_8b30fb365f8a707ebb1e3c1bf0c8eee3.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Time for Building Mod-Files:  1.69953083992
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_23945a02f89d49f7e42b21f6a3d66db1.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_71f1c9a9bbe5428560965f941ff66ef0.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_6cc672b695627cf0ac12a3edc0661282.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_e3427b14d66ac5c7f848f81f5f5c2c83.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0129630565643
	Time for Extracting Data: (2 records) 0.000897884368896
	Simulation Time Elapsed:  1.99632906914
	Suceeded
	Setting Random Seed: 61153
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//1e/1e6d21cb7ce88efc99be67a633ad920f.bundle
	Setting Random Seed: 69403
	Time for Building Mod-Files:  0.000921010971069
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_343538bff8b283ecd9082ad4693221dd.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_4d6c1586068ada6716bf3b779de91eec.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_8a642c618ace83168913bc0418382542.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_21a13f17922cd569c796e2d461c80065.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0145900249481
	Time for Extracting Data: (2 records) 0.00090217590332
	Simulation Time Elapsed:  0.28321480751
	Suceeded
	Setting Random Seed: 37280
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//b2/b27681224762117a63f5b5341fc95c2a.bundle
	Setting Random Seed: 69403
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_da85ef1d57a353b1ae930990ce868afb.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_da85ef1d57a353b1ae930990ce868afb.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_da85ef1d57a353b1ae930990ce868afb.lo tmp_da85ef1d57a353b1ae930990ce868afb.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_da85ef1d57a353b1ae930990ce868afb.la  -rpath /opt/nrn/x86_64/libs  tmp_da85ef1d57a353b1ae930990ce868afb.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_51cd2e7d095d96508a519754fbbcbbb9.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_51cd2e7d095d96508a519754fbbcbbb9.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_51cd2e7d095d96508a519754fbbcbbb9.lo tmp_51cd2e7d095d96508a519754fbbcbbb9.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_51cd2e7d095d96508a519754fbbcbbb9.la  -rpath /opt/nrn/x86_64/libs  tmp_51cd2e7d095d96508a519754fbbcbbb9.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_a7a5c820cf8b1dca09a768a7c1f03018.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_a7a5c820cf8b1dca09a768a7c1f03018.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_a7a5c820cf8b1dca09a768a7c1f03018.lo tmp_a7a5c820cf8b1dca09a768a7c1f03018.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_a7a5c820cf8b1dca09a768a7c1f03018.la  -rpath /opt/nrn/x86_64/libs  tmp_a7a5c820cf8b1dca09a768a7c1f03018.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_dcc888c91abb6a2b36ae893adb4d2ff2.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_dcc888c91abb6a2b36ae893adb4d2ff2.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_dcc888c91abb6a2b36ae893adb4d2ff2.lo tmp_dcc888c91abb6a2b36ae893adb4d2ff2.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_dcc888c91abb6a2b36ae893adb4d2ff2.la  -rpath /opt/nrn/x86_64/libs  tmp_dcc888c91abb6a2b36ae893adb4d2ff2.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Time for Building Mod-Files:  1.54490685463
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_55a7ddd3a70b10067591d87fdd9086bd.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_8b39df59f6b605dea59256fe68337e94.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_bd057cd4dcf0ed09e6431af30711b0d8.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_34923606fec6ef8603a8bc75593e25ed.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0147500038147
	Time for Extracting Data: (2 records) 0.00117301940918
	Simulation Time Elapsed:  1.81891298294
	Suceeded
	Setting Random Seed: 5249
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//b3/b367cbf0e5988380fb6a3b2f8b6e5097.bundle
	Setting Random Seed: 69403
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_472d67bc3e5f459b5c721cfb5f1acf9f.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_472d67bc3e5f459b5c721cfb5f1acf9f.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_472d67bc3e5f459b5c721cfb5f1acf9f.lo tmp_472d67bc3e5f459b5c721cfb5f1acf9f.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_472d67bc3e5f459b5c721cfb5f1acf9f.la  -rpath /opt/nrn/x86_64/libs  tmp_472d67bc3e5f459b5c721cfb5f1acf9f.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_6a4474ce3d41bd7a5c4197e68cdb7e80.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_6a4474ce3d41bd7a5c4197e68cdb7e80.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_6a4474ce3d41bd7a5c4197e68cdb7e80.lo tmp_6a4474ce3d41bd7a5c4197e68cdb7e80.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_6a4474ce3d41bd7a5c4197e68cdb7e80.la  -rpath /opt/nrn/x86_64/libs  tmp_6a4474ce3d41bd7a5c4197e68cdb7e80.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_7e80b99389d1622b4a758da0170063d6.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_7e80b99389d1622b4a758da0170063d6.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_7e80b99389d1622b4a758da0170063d6.lo tmp_7e80b99389d1622b4a758da0170063d6.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_7e80b99389d1622b4a758da0170063d6.la  -rpath /opt/nrn/x86_64/libs  tmp_7e80b99389d1622b4a758da0170063d6.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_be7820666e4b83e4cc31d34442ad0ef2.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_be7820666e4b83e4cc31d34442ad0ef2.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_be7820666e4b83e4cc31d34442ad0ef2.lo tmp_be7820666e4b83e4cc31d34442ad0ef2.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_be7820666e4b83e4cc31d34442ad0ef2.la  -rpath /opt/nrn/x86_64/libs  tmp_be7820666e4b83e4cc31d34442ad0ef2.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Time for Building Mod-Files:  2.72190999985
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_0499da7b39c02a439b4dc6cd86822a48.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_89154c3005ba97ebc469519a05359381.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_c88d585624280bba45b78e4d7b66bb11.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_699de7a909d4bdf824dbb64f41ab5c62.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0147469043732
	Time for Extracting Data: (2 records) 0.00114512443542
	Simulation Time Elapsed:  3.0015039444
	Suceeded
	Setting Random Seed: 60731
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//16/16cf048ac66a47450dc2ac8bc7c3b1d4.bundle
	Setting Random Seed: 69403
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_d6af48e40877af099da5ecf1698c0149.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_d6af48e40877af099da5ecf1698c0149.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_d6af48e40877af099da5ecf1698c0149.lo tmp_d6af48e40877af099da5ecf1698c0149.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_d6af48e40877af099da5ecf1698c0149.la  -rpath /opt/nrn/x86_64/libs  tmp_d6af48e40877af099da5ecf1698c0149.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_927ce5d9cb8ec1ce6edab0bbdd305820.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_927ce5d9cb8ec1ce6edab0bbdd305820.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_927ce5d9cb8ec1ce6edab0bbdd305820.lo tmp_927ce5d9cb8ec1ce6edab0bbdd305820.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_927ce5d9cb8ec1ce6edab0bbdd305820.la  -rpath /opt/nrn/x86_64/libs  tmp_927ce5d9cb8ec1ce6edab0bbdd305820.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_ad83e07593bed581ca3bbed494ce542d.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_ad83e07593bed581ca3bbed494ce542d.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_ad83e07593bed581ca3bbed494ce542d.lo tmp_ad83e07593bed581ca3bbed494ce542d.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_ad83e07593bed581ca3bbed494ce542d.la  -rpath /opt/nrn/x86_64/libs  tmp_ad83e07593bed581ca3bbed494ce542d.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_f5f8296d4e647cc60dcef493533d189d.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_f5f8296d4e647cc60dcef493533d189d.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_f5f8296d4e647cc60dcef493533d189d.lo tmp_f5f8296d4e647cc60dcef493533d189d.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_f5f8296d4e647cc60dcef493533d189d.la  -rpath /opt/nrn/x86_64/libs  tmp_f5f8296d4e647cc60dcef493533d189d.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Time for Building Mod-Files:  2.17011284828
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_b37d8f964fcb3f7336bcc79b31ff9669.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_774d6d8f75492d03973898f34d5f08b0.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_239189712e8cebe3ba3ca1bf69303a98.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_4e9b5a708d5b7060f1ce5be2510d4c11.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0146210193634
	Time for Extracting Data: (2 records) 0.00126004219055
	Simulation Time Elapsed:  2.43852090836
	Suceeded
	Setting Random Seed: 69403
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x290e510>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x2904190>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x2904450>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x28ff810>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x2903590>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x28f9110>
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x28ba2d0>
	Setting Time Range [  95.  200.] ms
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x28ddad0>
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



