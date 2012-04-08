
14. Visualising action potential propagation along an axon
==========================================================



Visualising action potential propagation along an axon
In this simulation, we create a cell with a long axon. We put HH-channels over its surface
and give it a short current injection into the soma. We look at the voltage at various points
along the axon, and see it propogate. 




Code
~~~~

.. code-block:: python

	
	
	
	
	"""Visualising action potential propagation along an axon
	In this simulation, we create a cell with a long axon. We put HH-channels over its surface
	and give it a short current injection into the soma. We look at the voltage at various points
	along the axon, and see it propogate. 
	
	"""
	
	
	from morphforge.stdimports import *
	from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmleak import MM_LeakChannel
	from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmalphabeta import MM_AlphaBetaChannel
	
	
	# Create the environment:
	env = NeuronSimulationEnvironment()
	
	# Create the simulation:
	mySim = env.Simulation()
	
	# Create a cell:
	morph = MorphologyBuilder.getSomaAxonMorph(axonLength=3000.0, axonRad=0.15, somaRad=9.0, axonSections=20)
	myCell = mySim.createCell(name="Cell1", morphology=morph)
	
	
	leakChannels = env.MembraneMechanism( 
	                         MM_LeakChannel, 
	                         name="LkChl", 
	                         conductance=unit("0.3:mS/cm2"), 
	                         reversalpotential=unit("-54.3:mV"),
	                         mechanism_id = 'HULL12_DIN_LK_ID'
	                        )
	
	sodiumStateVars = { "m": { 
	                      "alpha":[-4.00,-0.10,-1.00,40.00,-10.00],
	                      "beta": [ 4.00, 0.00, 0.00,65.00, 18.00]},
	                    "h": { 
	                        "alpha":[0.07,0.00,0.00,65.00,20.00] ,
	                        "beta": [1.00,0.00,1.00,35.00,-10.00]} 
	                  }
	
	sodiumChannels = env.MembraneMechanism( 
	                        MM_AlphaBetaChannel,
	                        name="NaChl", ion="na",
	                        equation="m*m*m*h",
	                        conductance=unit("120:mS/cm2"),
	                        reversalpotential=unit("50:mV"),
	                        statevars=sodiumStateVars,
	                        mechanism_id="HH_NA_CURRENT"
	                        )
	kStateVars = { "n": { 
	                      "alpha":[-0.55,-0.01,-1.0,55.0,-10.0],
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
	
	
	# Apply the channels uniformly over the cell
	ApplyMechanismEverywhereUniform(myCell, leakChannels )
	ApplyMechanismEverywhereUniform(myCell, sodiumChannels )
	ApplyMechanismEverywhereUniform(myCell, kChannels )
	ApplyPassiveEverywhereUniform(myCell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )
	
	# Get a location on the cell:
	somaLoc = myCell.getLocation("soma")
	
	# Create the stimulus and record the injected current:
	cc = mySim.createCurrentClamp( name="Stim1", amp=unit("250:pA"), dur=unit("5:ms"), delay=unit("100:ms"), celllocation=somaLoc)
	mySim.record( cc, what=StdRec.Current)
	
	
	
	# To record along the axon, we create a set of 'CellLocations', at the distances 
	# specified (start,stop,  
	for cell_location in CellLocator.getLocationsAtDistancesAwayFromDummy(cell=myCell, distances=range(9, 3000, 100) ):
	
	    print " -- ",cell_location.section
	    print " -- ",cell_location.sectionpos
	    print " -- ",cell_location.get_3d_position()
	    
	    # Create a path along the morphology from the centre of the 
	    # Soma
	    path = MorphPath( somaLoc, cell_location)
	    print "Distance to Soma Centre:", path.get_length()
	    
	    mySim.record( myCell, what=StdRec.MembraneVoltage, location=cell_location, description="Distance Recording at %0.0f (um)"% path.get_length() )
	    
	
	# Define what to record:
	mySim.record( myCell, what=StdRec.MembraneVoltage, name="SomaVoltage", location = somaLoc ) 
	
	# Run the simulation
	results = mySim.Run()
	
	# Display the results:
	TagViewer([results], timeranges=[(97.5, 140)*pq.ms] )
	


Output
~~~~~~

.. code-block:: bash

    	Setting Random Seed: 53964
	 --  <SectionObject: [0.000000,0.000000,0.000000, r=9.000000] -> [18.000000,0.000000,0.000000, r=9.000000], Length: 18.00, Region:soma, idTag:soma, >
	 --  0.5
	 --  [ 9.  0.  0.]
	Distance to Soma Centre: 0.0
	 --  <SectionObject: [18.000000,0.000000,0.000000, r=9.000000] -> [168.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_1, >
	 --  0.606666666667
	 --  [ 109.    0.    0.]
	Distance to Soma Centre: 100.0
	 --  <SectionObject: [168.000000,0.000000,0.000000, r=0.150000] -> [318.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_2, >
	 --  0.273333333333
	 --  [ 209.    0.    0.]
	Distance to Soma Centre: 200.0
	 --  <SectionObject: [168.000000,0.000000,0.000000, r=0.150000] -> [318.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_2, >
	 --  0.94
	 --  [ 309.    0.    0.]
	Distance to Soma Centre: 300.0
	 --  <SectionObject: [318.000000,0.000000,0.000000, r=0.150000] -> [468.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_3, >
	 --  0.606666666667
	 --  [ 409.    0.    0.]
	Distance to Soma Centre: 400.0
	 --  <SectionObject: [468.000000,0.000000,0.000000, r=0.150000] -> [618.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_4, >
	 --  0.273333333333
	 --  [ 509.    0.    0.]
	Distance to Soma Centre: 500.0
	 --  <SectionObject: [468.000000,0.000000,0.000000, r=0.150000] -> [618.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_4, >
	 --  0.94
	 --  [ 609.    0.    0.]
	Distance to Soma Centre: 600.0
	 --  <SectionObject: [618.000000,0.000000,0.000000, r=0.150000] -> [768.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_5, >
	 --  0.606666666667
	 --  [ 709.    0.    0.]
	Distance to Soma Centre: 700.0
	 --  <SectionObject: [768.000000,0.000000,0.000000, r=0.150000] -> [918.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_6, >
	 --  0.273333333333
	 --  [ 809.    0.    0.]
	Distance to Soma Centre: 800.0
	 --  <SectionObject: [768.000000,0.000000,0.000000, r=0.150000] -> [918.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_6, >
	 --  0.94
	 --  [ 909.    0.    0.]
	Distance to Soma Centre: 900.0
	 --  <SectionObject: [918.000000,0.000000,0.000000, r=0.150000] -> [1068.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_7, >
	 --  0.606666666667
	 --  [ 1009.     0.     0.]
	Distance to Soma Centre: 1000.0
	 --  <SectionObject: [1068.000000,0.000000,0.000000, r=0.150000] -> [1218.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_8, >
	 --  0.273333333333
	 --  [ 1109.     0.     0.]
	Distance to Soma Centre: 1100.0
	 --  <SectionObject: [1068.000000,0.000000,0.000000, r=0.150000] -> [1218.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_8, >
	 --  0.94
	 --  [ 1209.     0.     0.]
	Distance to Soma Centre: 1200.0
	 --  <SectionObject: [1218.000000,0.000000,0.000000, r=0.150000] -> [1368.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_9, >
	 --  0.606666666667
	 --  [ 1309.     0.     0.]
	Distance to Soma Centre: 1300.0
	 --  <SectionObject: [1368.000000,0.000000,0.000000, r=0.150000] -> [1518.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_10, >
	 --  0.273333333333
	 --  [ 1409.     0.     0.]
	Distance to Soma Centre: 1400.0
	 --  <SectionObject: [1368.000000,0.000000,0.000000, r=0.150000] -> [1518.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_10, >
	 --  0.94
	 --  [ 1509.     0.     0.]
	Distance to Soma Centre: 1500.0
	 --  <SectionObject: [1518.000000,0.000000,0.000000, r=0.150000] -> [1668.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_11, >
	 --  0.606666666667
	 --  [ 1609.     0.     0.]
	Distance to Soma Centre: 1600.0
	 --  <SectionObject: [1668.000000,0.000000,0.000000, r=0.150000] -> [1818.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_12, Setting Random Seed: 49096
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//53/5398f1bb8c7d6201dcbf1862f05014f7.bundle
	Setting Random Seed: 53964
	Time for Building Mod-Files:  0.000888109207153
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_50705c564a22bd64e1215d1823fc687a.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_e1d092c3391fa96414c59100b100aa1c.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_917736dee8b38abc9f74d55ff4a52f38.so
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
		1 
	Time for Simulation:  0.833641052246
	Time for Extracting Data: (31 records) 0.00721597671509
	Simulation Time Elapsed:  1.20682501793
	Suceeded
	>
	 --  0.273333333333
	 --  [ 1709.     0.     0.]
	Distance to Soma Centre: 1700.0
	 --  <SectionObject: [1668.000000,0.000000,0.000000, r=0.150000] -> [1818.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_12, >
	 --  0.94
	 --  [ 1809.     0.     0.]
	Distance to Soma Centre: 1800.0
	 --  <SectionObject: [1818.000000,0.000000,0.000000, r=0.150000] -> [1968.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_13, >
	 --  0.606666666667
	 --  [ 1909.     0.     0.]
	Distance to Soma Centre: 1900.0
	 --  <SectionObject: [1968.000000,0.000000,0.000000, r=0.150000] -> [2118.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_14, >
	 --  0.273333333333
	 --  [ 2009.     0.     0.]
	Distance to Soma Centre: 2000.0
	 --  <SectionObject: [1968.000000,0.000000,0.000000, r=0.150000] -> [2118.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_14, >
	 --  0.94
	 --  [ 2109.     0.     0.]
	Distance to Soma Centre: 2100.0
	 --  <SectionObject: [2118.000000,0.000000,0.000000, r=0.150000] -> [2268.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_15, >
	 --  0.606666666667
	 --  [ 2209.     0.     0.]
	Distance to Soma Centre: 2200.0
	 --  <SectionObject: [2268.000000,0.000000,0.000000, r=0.150000] -> [2418.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_16, >
	 --  0.273333333333
	 --  [ 2309.     0.     0.]
	Distance to Soma Centre: 2300.0
	 --  <SectionObject: [2268.000000,0.000000,0.000000, r=0.150000] -> [2418.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_16, >
	 --  0.94
	 --  [ 2409.     0.     0.]
	Distance to Soma Centre: 2400.0
	 --  <SectionObject: [2418.000000,0.000000,0.000000, r=0.150000] -> [2568.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_17, >
	 --  0.606666666667
	 --  [ 2509.     0.     0.]
	Distance to Soma Centre: 2500.0
	 --  <SectionObject: [2568.000000,0.000000,0.000000, r=0.150000] -> [2718.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_18, >
	 --  0.273333333333
	 --  [ 2609.     0.     0.]
	Distance to Soma Centre: 2600.0
	 --  <SectionObject: [2568.000000,0.000000,0.000000, r=0.150000] -> [2718.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_18, >
	 --  0.94
	 --  [ 2709.     0.     0.]
	Distance to Soma Centre: 2700.0
	 --  <SectionObject: [2718.000000,0.000000,0.000000, r=0.150000] -> [2868.000000,0.000000,0.000000, r=0.150000], Length: 150.00, Region:axon, idTag:axon_19, >
	 --  0.606666666667
	 --  [ 2809.     0.     0.]
	Distance to Soma Centre: 2800.0
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x3a74390>
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x3886310>
	Setting Time Range [  97.5  140. ] ms
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x38a7d90>
	Setting Time Range [  97.5  140. ] ms
	Setting Yunit 1 pA (picoampere)
	Saving File _output/figures/singlecell_simulation060/eps/fig000_None.eps
	Saving File _output/figures/singlecell_simulation060/pdf/fig000_None.pdf
	Saving File _output/figures/singlecell_simulation060/png/fig000_None.png
	Saving File _output/figures/singlecell_simulation060/svg/fig000_None.svg
	



Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation060_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation060_out1.png>`



