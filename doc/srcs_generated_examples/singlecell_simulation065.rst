
21. Using a channel library to reduce duplication
=================================================



Using a channel library to reduce duplication.

We define functions that produce morphology and channel objects for our simulations.
We could stop here, and simply import and use the functions in our simulations, but
we go a step further, and register them with  "ChannelLibrary" and "MorphologyLibrary".
These are basically glorified dictionaries, that do the lookup for the appropriate functors
based on a key from the tuple~(modelsrc, celltype, channeltype). The advantage for doing this is that
there is single repository for morphologies and channels. 
  
There is not really anythin clever going on here, and you can run simulations completely ignorantly
of these classes, I just included it because it made life much easier for me, when I had to start managing
lots of channel definitions.  




Code
~~~~

.. code-block:: python

	
	
	
	
	"""Using a channel library to reduce duplication.
	
	We define functions that produce morphology and channel objects for our simulations.
	We could stop here, and simply import and use the functions in our simulations, but
	we go a step further, and register them with  "ChannelLibrary" and "MorphologyLibrary".
	These are basically glorified dictionaries, that do the lookup for the appropriate functors
	based on a key from the tuple~(modelsrc, celltype, channeltype). The advantage for doing this is that
	there is single repository for morphologies and channels. 
	  
	There is not really anythin clever going on here, and you can run simulations completely ignorantly
	of these classes, I just included it because it made life much easier for me, when I had to start managing
	lots of channel definitions.  
	
	"""
	
	
	from morphforge.stdimports import *
	from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmleak import MM_LeakChannel
	from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmalphabeta import MM_AlphaBetaChannel
	
	
	
	# This can be put into a file that is loaded on
	# you path somewhere:
	
	# ======================================================
	def getSimpleMorphology():
	        
	    mDict  = {'root': { 'length': 17.5, 'diam': 17.5, 'id':'soma', 'region':'soma',   } }
	    return  MorphologyTree.fromDictionary(mDict)
	
	
	def get_sample_lk(env):
	    lkChannels = env.MembraneMechanism( 
	                         MM_LeakChannel, 
	                         name="LkChl", 
	                         conductance=unit("0.3:mS/cm2"), 
	                         reversalpotential=unit("-54.3:mV"),
	                         mechanism_id = 'HULL12_DIN_LK_ID'
	                        )
	    return lkChannels
	
	
	def get_sample_na(env):
	    naStateVars = { "m": { 
	                          "alpha":[-4.00,-0.10,-1.00,40.00,-10.00],
	                          "beta": [ 4.00, 0.00, 0.00,65.00, 18.00]},
	                        "h": { 
	                            "alpha":[0.07,0.00,0.00,65.00,20.00] ,
	                            "beta": [1.00,0.00,1.00,35.00,-10.00]} 
	                      }
	    
	    naChannels = env.MembraneMechanism( 
	                            MM_AlphaBetaChannel,
	                            name="NaChl", ion="na",
	                            equation="m*m*m*h",
	                            conductance=unit("120:mS/cm2"),
	                            reversalpotential=unit("50:mV"),
	                            statevars=naStateVars,
	                            mechanism_id="HH_NA_CURRENT"
	                            )
	    return naChannels
	
	
	def get_sample_k(env):
	    kStateVars = { "n": { "alpha":[-0.55,-0.01,-1.0,55.0,-10.0],
	                          "beta": [0.125,0,0,65,80]},
	                       }
	    kChannels = env.MembraneMechanism( 
	                            MM_AlphaBetaChannel,
	                            name="KChl", ion="k",
	                            equation="n*n*n*n",
	                            conductance=unit("36:mS/cm2"),
	                            reversalpotential=unit("-77:mV"),
	                            statevars=kStateVars,
	                            mechanism_id="HH_K_CURRENT"
	                            )
	    return kChannels
	
	
	
	MorphologyLibrary.registerMorphology(modelsrc="Sample", celltype="Cell1", morphFunctor=getSimpleMorphology)
	ChannelLibrary.registerChannel(modelsrc="Sample", celltype="Cell1", channeltype="Na", chlFunctor=get_sample_na)
	ChannelLibrary.registerChannel(modelsrc="Sample", celltype="Cell1", channeltype="K", chlFunctor=get_sample_k)
	ChannelLibrary.registerChannel(modelsrc="Sample", celltype="Cell1", channeltype="Lk", chlFunctor=get_sample_lk)
	
	# =============================================================
	
	
	
	
	
	
	
	
	
	# Now in our script elsewhere, we can use them as:
	modelsrc = "Sample"
	celltype="Cell1" 
	
	# Create the environment:
	env = NeuronSimulationEnvironment()
	
	# Create the simulation:
	mySim = env.Simulation()
	
	# Create a cell:
	morphology=MorphologyLibrary.getMorphology(modelsrc=modelsrc, celltype=celltype)
	myCell = mySim.createCell(morphology=morphology )
	
	# Apply the channels uniformly over the cell
	naChls = ChannelLibrary.getChannel(modelsrc=modelsrc, celltype=celltype, channeltype="Na", env=env)
	kChls  = ChannelLibrary.getChannel(modelsrc=modelsrc, celltype=celltype, channeltype="K", env=env)
	lkChls = ChannelLibrary.getChannel(modelsrc=modelsrc, celltype=celltype, channeltype="Lk", env=env) 
	
	ApplyMechanismEverywhereUniform(myCell, naChls )
	ApplyMechanismEverywhereUniform(myCell, kChls  )
	ApplyMechanismEverywhereUniform(myCell, lkChls )
	
	ApplyPassiveEverywhereUniform(myCell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )
	
	# Get a location on the cell:
	somaLoc = myCell.getLocation("soma")
	
	# Create the stimulus and record the injected current:
	cc = mySim.createCurrentClamp( name="Stim1", amp=unit("150:pA"), dur=unit("5:ms"), delay=unit("100:ms"), celllocation=somaLoc)
	
	mySim.record( cc, what=StdRec.Current)
	mySim.record( myCell, what=StdRec.MembraneVoltage, location=somaLoc )
	    
	
	# Run the simulation
	results = mySim.Run()
	
	# Display the results:
	TagViewer([results], timeranges=[(97.5, 140)*pq.ms] )
	


Output
~~~~~~

.. code-block:: bash

    	Setting Random Seed: 85942
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//cc/ccbd1d5f98ba35902ad6395fde049784.bundle
	Setting Random Seed: 34390
	Time for Building Mod-Files:  0.000814914703369
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_50705c564a22bd64e1215d1823fc687a.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_e1d092c3391fa96414c59100b100aa1c.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_917736dee8b38abc9f74d55ff4a52f38.so
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.0180530548096
	Time for Extracting Data: (2 records) 0.000817060470581
	Simulation Time Elapsed:  0.264628887177
	Suceeded
	Setting Random Seed: 34390
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x2b77dd0>
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x2b21310>
	Setting Time Range [  97.5  140. ] ms
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x2b44d90>
	Setting Time Range [  97.5  140. ] ms
	Setting Yunit 1 pA (picoampere)
	Saving File _output/figures/singlecell_simulation065/eps/fig000_None.eps
	Saving File _output/figures/singlecell_simulation065/pdf/fig000_None.pdf
	Saving File _output/figures/singlecell_simulation065/png/fig000_None.png
	Saving File _output/figures/singlecell_simulation065/svg/fig000_None.svg
	



Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation065_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation065_out1.png>`



