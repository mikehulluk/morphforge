
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

    	Setting Random Seed: 40822
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//05/051a9bf722ab7d14e7d0835bfb6ef170.bundle
	Setting Random Seed: 59929
	Time for Building Mod-Files:  0.000871181488037
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_fdc4ba95dc89091b81dc90c2ba3ba022.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_0919e1fe75db0337ee796d940e1177c4.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_6ee6f46dc50d08c0551cd862973f6285.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_9ce35968d17de56ec8939b8f6347a0df.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0111880302429
	Time for Extracting Data: (2 records) 0.00065803527832
	Simulation Time Elapsed:  0.25253200531
	Suceeded
	Setting Random Seed: 46302
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//94/947de9b9ad344ff45859f32452e85573.bundle
	Setting Random Seed: 59929
	Time for Building Mod-Files:  0.0103888511658
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_05b1f64c76d243a3eda29c1ec0cc24df.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_397ca329e4aa94e3e97428a6e3776b09.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_060f20cafd1dde78cb4d3dd4ae9b2273.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_7d2dbe52212dab25eb6f4308c83f9e3d.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0147869586945
	Time for Extracting Data: (2 records) 0.000805854797363
	Simulation Time Elapsed:  0.299121856689
	Suceeded
	Setting Random Seed: 48411
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//8d/8d6f55390041676cd7f180931f484e1f.bundle
	Setting Random Seed: 59929
	Time for Building Mod-Files:  0.000919818878174
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_05b1f64c76d243a3eda29c1ec0cc24df.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_397ca329e4aa94e3e97428a6e3776b09.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_060f20cafd1dde78cb4d3dd4ae9b2273.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_7d2dbe52212dab25eb6f4308c83f9e3d.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0137829780579
	Time for Extracting Data: (2 records) 0.000650882720947
	Simulation Time Elapsed:  0.282911062241
	Suceeded
	Setting Random Seed: 73163
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//09/09325c10dcb79185c2d2968473603eff.bundle
	Setting Random Seed: 59929
	Time for Building Mod-Files:  0.00092601776123
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_393746b359f54aff05ab3e0408ba1884.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_9e4b8d7484635a4df0ee77398c6aa7ae.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_6219b16f7c219a561b5ead6f0baf8317.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_a8a8776faa2259e8f56dc9507bfa9568.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0134210586548
	Time for Extracting Data: (2 records) 0.000910043716431
	Simulation Time Elapsed:  0.272053003311
	Suceeded
	Setting Random Seed: 75943
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//66/66353ed61ca3ed75698a9ee7a204d4d3.bundle
	Setting Random Seed: 59929
	Time for Building Mod-Files:  0.000902891159058
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_decfebebc30dbe70a288187722b50c03.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_8a12703ee976afeed0fd6812981515c2.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_9603c34f339b5684aa756f5d11d336d6.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_52f7c720dd22a799fb19e3a71573e885.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0207209587097
	Time for Extracting Data: (2 records) 0.000671148300171
	Simulation Time Elapsed:  0.267033815384
	Suceeded
	Setting Random Seed: 88713
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//f7/f7d2a52dbbe82b3d1f070ed5eea7c3f7.bundle
	Setting Random Seed: 59929
	Time for Building Mod-Files:  0.0137820243835
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_80210b4fdca37683f41e7723111635d8.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_5ac54391adaf63faba9bad67293a6558.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_45628929208a99958cff7109db79709d.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_736714d5c2e6395750154819b6070c87.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0141699314117
	Time for Extracting Data: (2 records) 0.000611066818237
	Simulation Time Elapsed:  0.296205997467
	Suceeded
	Setting Random Seed: 59929
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x2655a90>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x26505d0>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x2650ed0>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x2646090>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x2645050>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x264b5d0>
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x2600550>
	Setting Time Range [  95.  200.] ms
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x2623cd0>
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



