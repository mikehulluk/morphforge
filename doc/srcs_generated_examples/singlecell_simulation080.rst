
16. Applying different channel densities over a cell
====================================================



Applying different channel densities over a cell.
We start with a cell with a long axon, and then apply Hodgkin-Huxley channels over the surface.
We look at the effect of changing the density of leak and sodium channels in just the axon 
of the neuron (not the soma)

This example also shows the use of tags; 300 traces are recorded in this experiment; but we don't ever need to get
involved in managing them directly. We can just specify that all traces recorded on simulation X should be tagged with "SIMY", and 
then tell the TagViewer to plot everything with a tag 'SIMY' 




Code
~~~~

.. code-block:: python

	
	
	"""Applying different channel densities over a cell.
	We start with a cell with a long axon, and then apply Hodgkin-Huxley channels over the surface.
	We look at the effect of changing the density of leak and sodium channels in just the axon 
	of the neuron (not the soma)
	
	This example also shows the use of tags; 300 traces are recorded in this experiment; but we don't ever need to get
	involved in managing them directly. We can just specify that all traces recorded on simulation X should be tagged with "SIMY", and 
	then tell the TagViewer to plot everything with a tag 'SIMY' 
	
	"""
	
	
	
	from morphforge.stdimports import *
	from morphforgecontrib.data_library.stdmodels import StandardModels
	
	
	def sim( glk_multiplier, gna_multiplier, tag):
	    # Create the environment:
	    env = NeuronSimulationEnvironment()
	    
	    # Create the simulation:
	    mySim = env.Simulation()
	    
	    # Create a cell:
	    morph = MorphologyBuilder.getSomaAxonMorph(axonLength=3000.0, axonRad=0.3, somaRad=9.0, axonSections=20)
	    myCell = mySim.createCell(name="Cell1", morphology=morph)
	    
	    
	    lkChannels = ChannelLibrary.getChannel(modelsrc=StandardModels.HH52, channeltype="Lk", env=env)
	    naChannels = ChannelLibrary.getChannel(modelsrc=StandardModels.HH52, channeltype="Na", env=env) 
	    kChannels  = ChannelLibrary.getChannel(modelsrc=StandardModels.HH52, channeltype="K", env=env) 
	     
	    # Apply the channels uniformly over the cell
	    ApplyMechanismEverywhereUniform(myCell, lkChannels )
	    ApplyMechanismEverywhereUniform(myCell, naChannels )
	    ApplyMechanismEverywhereUniform(myCell, kChannels )
	    
	    # Over-ride the parameters in the axon:
	    ApplyMechanismRegionUniform(cell=myCell, mechanism=lkChannels, region=morph.getRegion("axon"), parameter_multipliers={'gScale':glk_multiplier})
	    ApplyMechanismRegionUniform(cell=myCell, mechanism=naChannels, region=morph.getRegion("axon"), parameter_multipliers={'gScale':gna_multiplier})
	    
	    ApplyPassiveEverywhereUniform(myCell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )
	    
	    
	    for cell_location in CellLocator.getLocationsAtDistancesAwayFromDummy(cell=myCell, distances=range(9, 3000, 100) ):
	        mySim.record( myCell, what=StdRec.MembraneVoltage, location=cell_location, user_tags=[tag])
	    
	    # Create the stimulus and record the injected current:
	    cc = mySim.createCurrentClamp( name="Stim1", amp=unit("250:pA"), dur=unit("5:ms"), delay=unit("100:ms"), celllocation=myCell.getLocation("soma"))
	    mySim.record( cc, what=StdRec.Current)
	    
	    # Run the simulation
	    return mySim.Run()
	    
	
	# Display the results:
	results_a = [     
	    sim( glk_multiplier=0.1, gna_multiplier=1.0, tag="SIM1"),
	    sim( glk_multiplier=0.5, gna_multiplier=1.0, tag="SIM2"),
	    sim( glk_multiplier=1.0, gna_multiplier=1.0, tag="SIM3"),
	    sim( glk_multiplier=5.0, gna_multiplier=1.0, tag="SIM4"),
	    sim( glk_multiplier=10.0, gna_multiplier=1.0, tag="SIM5"),
	]
	
	TagViewer(results_a, timeranges=[(97.5, 140)*pq.ms], show=False,
	          plotspecs = [
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM1}", ylabel='gLeak: 0.1\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),  
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM2}", ylabel='gLeak: 0.5\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM3}", ylabel='gLeak: 1.0\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM4}", ylabel='gLeak: 5.0\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM5}", ylabel='gLeak: 10.0\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
	                        ] )
	
	results_b = [
	    sim( gna_multiplier=0.1,  glk_multiplier=1.0, tag="SIM6"),     
	    sim( gna_multiplier=0.5,  glk_multiplier=1.0, tag="SIM7"),
	    sim( gna_multiplier=0.75,  glk_multiplier=1.0, tag="SIM8"),
	    sim( gna_multiplier=1.0,  glk_multiplier=1.0, tag="SIM9"),
	]
	
	TagViewer(results_b, timeranges=[(97.5, 140)*pq.ms],show=True,
	          plotspecs = [
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM6}", ylabel='gNa: 0.10\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),  
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM7}", ylabel='gNa: 0.50\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM8}", ylabel='gNa: 0.75\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
	                    PlotSpec_DefaultNew( s="ALL{Voltage,SIM9}", ylabel='gNa: 1.00\nVoltage', yrange=(-80*mV,50*mV), legend_labeller=None ),
	                        ] )
	
	


Output
~~~~~~

.. code-block:: bash

    	Setting Random Seed: 12602
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//1e/1eed454e23a4be17c3a46ed24f77892d.bundle
	Setting Random Seed: 1142
	Time for Building Mod-Files:  0.00079607963562
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_2f9e2a9e11812732bc7e3ddd24d8a4b8.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_6c136979192dac6a0dc705dd0c699de9.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_90246d234361e93fd612c4505155a3ae.so
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
	Time for Simulation:  0.843128204346
	Time for Extracting Data: (30 records) 0.00704908370972
	Simulation Time Elapsed:  1.21152186394
	Suceeded
	Setting Random Seed: 76401
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//b3/b3e156a8847b831f3c54452fe9e48ccf.bundle
	Setting Random Seed: 1142
	Time for Building Mod-Files:  0.000826120376587
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
	Time for Simulation:  0.617403030396
	Time for Extracting Data: (30 records) 0.00695013999939
	Simulation Time Elapsed:  0.98230099678
	Suceeded
	Setting Random Seed: 51621
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//78/78f1aed99041b67b8720e05d81f4f112.bundle
	Setting Random Seed: 1142
	Time for Building Mod-Files:  0.000874042510986
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_6c42d1d5406818833734e36dbffbb594.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_414449b2de3f3b4c1b72a3a5a965dbf2.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_796872297f486d939c8120cce8f5cb18.so
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
	Time for Simulation:  0.663022994995
	Time for Extracting Data: (30 records) 0.00744986534119
	Simulation Time Elapsed:  1.03162288666
	Suceeded
	Setting Random Seed: 61304
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//59/593411a9af3c6a8a7a01cc8bb117ffb3.bundle
	Setting Random Seed: 1142
	Time for Building Mod-Files:  0.000794172286987
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
	Time for Simulation:  0.666424036026
	Time for Extracting Data: (30 records) 0.00716114044189
	Simulation Time Elapsed:  1.05704903603
	Suceeded
	Setting Random Seed: 71582
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//8f/8f4535f200230f7bee3ba55dec416c8f.bundle
	Setting Random Seed: 1142
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_f4926d544a84303f2b92aea4de0288c6.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_f4926d544a84303f2b92aea4de0288c6.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_f4926d544a84303f2b92aea4de0288c6.lo tmp_f4926d544a84303f2b92aea4de0288c6.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_f4926d544a84303f2b92aea4de0288c6.la  -rpath /opt/nrn/x86_64/libs  tmp_f4926d544a84303f2b92aea4de0288c6.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_8700754a23aef526079720a315e88169.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_8700754a23aef526079720a315e88169.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_8700754a23aef526079720a315e88169.lo tmp_8700754a23aef526079720a315e88169.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_8700754a23aef526079720a315e88169.la  -rpath /opt/nrn/x86_64/libs  tmp_8700754a23aef526079720a315e88169.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_f3474ec05fd9c255584c6a997919050a.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_f3474ec05fd9c255584c6a997919050a.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_f3474ec05fd9c255584c6a997919050a.lo tmp_f3474ec05fd9c255584c6a997919050a.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_f3474ec05fd9c255584c6a997919050a.la  -rpath /opt/nrn/x86_64/libs  tmp_f3474ec05fd9c255584c6a997919050a.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Time for Building Mod-Files:  1.43545198441
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_535b0b5b7e1a9e3a023f5a18354de13a.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_fe8a88a6bf07eb9deee436af601fce4b.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_94c1e788a7b29065034a80f39b59a2c9.so
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
	Time for Simulation:  0.564306020737
	Time for Extracting Data: (30 records) 0.00720691680908
	Simulation Time Elapsed:  2.39569306374
	Suceeded
	Setting Random Seed: 84900
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//97/974bf40ed437b86b40350c2a259ea676.bundle
	Setting Random Seed: 1142
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_4dc312d0a3526ec1e8ae78a9509a2e0e.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_4dc312d0a3526ec1e8ae78a9509a2e0e.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_4dc312d0a3526ec1e8ae78a9509a2e0e.lo tmp_4dc312d0a3526ec1e8ae78a9509a2e0e.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_4dc312d0a3526ec1e8ae78a9509a2e0e.la  -rpath /opt/nrn/x86_64/libs  tmp_4dc312d0a3526ec1e8ae78a9509a2e0e.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_f35f61ae77d3c10701355ce4d681d3b8.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_f35f61ae77d3c10701355ce4d681d3b8.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_f35f61ae77d3c10701355ce4d681d3b8.lo tmp_f35f61ae77d3c10701355ce4d681d3b8.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_f35f61ae77d3c10701355ce4d681d3b8.la  -rpath /opt/nrn/x86_64/libs  tmp_f35f61ae77d3c10701355ce4d681d3b8.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_218e4eff41b36a41e7c10e62d2263d6c.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_218e4eff41b36a41e7c10e62d2263d6c.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_218e4eff41b36a41e7c10e62d2263d6c.lo tmp_218e4eff41b36a41e7c10e62d2263d6c.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_218e4eff41b36a41e7c10e62d2263d6c.la  -rpath /opt/nrn/x86_64/libs  tmp_218e4eff41b36a41e7c10e62d2263d6c.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Time for Building Mod-Files:  1.17991995811
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_2eefa8705b50acc432938f765b81ef13.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_b4d955d0ddf7c4bb8f4f0b75c938c929.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_f67574bed2ae8fa2dab6dd0008c16cee.so
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
	Time for Simulation:  0.470138072968
	Time for Extracting Data: (30 records) 0.00762009620667
	Simulation Time Elapsed:  2.03018903732
	Suceeded
	Setting Random Seed: 89917
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//1e/1e0821bd071709b3b40e519878abc74d.bundle
	Setting Random Seed: 1142
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_59194025329d879f3704a79c8c618e39.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_59194025329d879f3704a79c8c618e39.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_59194025329d879f3704a79c8c618e39.lo tmp_59194025329d879f3704a79c8c618e39.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_59194025329d879f3704a79c8c618e39.la  -rpath /opt/nrn/x86_64/libs  tmp_59194025329d879f3704a79c8c618e39.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_67c1dce2a4845c806b53ed0c4adc3ec4.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_67c1dce2a4845c806b53ed0c4adc3ec4.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_67c1dce2a4845c806b53ed0c4adc3ec4.lo tmp_67c1dce2a4845c806b53ed0c4adc3ec4.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_67c1dce2a4845c806b53ed0c4adc3ec4.la  -rpath /opt/nrn/x86_64/libs  tmp_67c1dce2a4845c806b53ed0c4adc3ec4.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_3f4fbba9399aa3157567dc3f2814c287.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_3f4fbba9399aa3157567dc3f2814c287.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_3f4fbba9399aa3157567dc3f2814c287.lo tmp_3f4fbba9399aa3157567dc3f2814c287.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_3f4fbba9399aa3157567dc3f2814c287.la  -rpath /opt/nrn/x86_64/libs  tmp_3f4fbba9399aa3157567dc3f2814c287.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Time for Building Mod-Files:  1.68236899376
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_7fa6e49cbb3cfac6d7d8404a757a9e29.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_16b49de1260f66b83f28d55dbdd63ca9.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_3ce0f39100883b984cf3848d9a049aed.so
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
	Time for Simulation:  0.701484918594
	Time for Extracting Data: (30 records) 0.00739097595215
	Simulation Time Elapsed:  2.81974315643
	Suceeded
	Setting Random Seed: 3736
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//f9/f950984db370a0b0f7c3af223153fcdc.bundle
	Setting Random Seed: 1142
	Time for Building Mod-Files:  0.000872850418091
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_46a5d309f0e01be61b012dce612fde22.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_b63e843a43fba6d3f3fb1e2f6869047b.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_01854025ba521a2c475a9e88d6772589.so
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
	Time for Simulation:  0.838907957077
	Time for Extracting Data: (30 records) 0.00721096992493
	Simulation Time Elapsed:  1.21274209023
	Suceeded
	Setting Random Seed: 40318
	Loading Bundle from  /home/michael/mftmp//sim/simpickles//be/beda98bd42d839ff2b203a254a16a1aa.bundle
	Setting Random Seed: 1142
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_a286d76a45b70fdb5fafcb73e5fc7d99.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_a286d76a45b70fdb5fafcb73e5fc7d99.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_a286d76a45b70fdb5fafcb73e5fc7d99.lo tmp_a286d76a45b70fdb5fafcb73e5fc7d99.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_a286d76a45b70fdb5fafcb73e5fc7d99.la  -rpath /opt/nrn/x86_64/libs  tmp_a286d76a45b70fdb5fafcb73e5fc7d99.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_ab64fd573f181004577fce58df169f48.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_ab64fd573f181004577fce58df169f48.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_ab64fd573f181004577fce58df169f48.lo tmp_ab64fd573f181004577fce58df169f48.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_ab64fd573f181004577fce58df169f48.la  -rpath /opt/nrn/x86_64/libs  tmp_ab64fd573f181004577fce58df169f48.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Executing: /opt/nrn/x86_64/bin/modlunit /home/michael/mftmp/tmp_b2fc4f44fd0a08d99e833924f58f023c.mod
	/home/michael/mftmp/simulation/nrn/build
	Executing: /opt/nrn/x86_64/bin/nocmodl tmp_b2fc4f44fd0a08d99e833924f58f023c.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/x86_64/lib"    -g -O2 -c -o tmp_b2fc4f44fd0a08d99e833924f58f023c.lo tmp_b2fc4f44fd0a08d99e833924f58f023c.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_b2fc4f44fd0a08d99e833924f58f023c.la  -rpath /opt/nrn/x86_64/libs  tmp_b2fc4f44fd0a08d99e833924f58f023c.lo  -L/opt/nrn/x86_64/lib -L/opt/nrn/x86_64/lib  /opt/nrn/x86_64/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	Time for Building Mod-Files:  1.66331911087
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_f1b3fcc73f56626f97b88a209ff60beb.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_36570ae9996eea3c2963d9bc457669ad.so
	loading membrane mechanisms from /home/michael/mftmp/modout/mod_48a14832930d15e2d54f6315b8a83252.so
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
	Time for Simulation:  0.661684989929
	Time for Extracting Data: (30 records) 0.00704312324524
	Simulation Time Elapsed:  2.70318102837
	Suceeded
	Setting Random Seed: 1142
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x2f534d0>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x2f54ad0>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x2ff57d0>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x2fd8650>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x31b6fd0>
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x31b55d0>
	Setting Time Range [  97.5  140. ] ms
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x2e75d90>
	Setting Time Range [  97.5  140. ] ms
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x31a4e50>
	Setting Time Range [  97.5  140. ] ms
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x2d740d0>
	Setting Time Range [  97.5  140. ] ms
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x31c4e90>
	Setting Time Range [  97.5  140. ] ms
	Saving File _output/figures/singlecell_simulation080/eps/fig000_None.eps
	Saving File _output/figures/singlecell_simulation080/pdf/fig000_None.pdf
	Saving File _output/figures/singlecell_simulation080/png/fig000_None.png
	Saving File _output/figures/singlecell_simulation080/svg/fig000_None.svg
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x4612690>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x472ac90>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x485ac50>
	<morphforge.simulation.core.result.simulationresult.SimulationResult object at 0x486dd10>
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x486de50>
	Setting Time Range [  97.5  140. ] ms
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x2fce990>
	Setting Time Range [  97.5  140. ] ms
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x49f5b10>
	Setting Time Range [  97.5  140. ] ms
	Plotting For PlotSpec: <morphforge.traces.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0x4872f10>
	Setting Time Range [  97.5  140. ] ms
	Saving File _output/figures/singlecell_simulation080/eps/fig001_None.eps
	Saving File _output/figures/singlecell_simulation080/pdf/fig001_None.pdf
	Saving File _output/figures/singlecell_simulation080/png/fig001_None.png
	Saving File _output/figures/singlecell_simulation080/svg/fig001_None.svg
	



Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/singlecell_simulation080_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation080_out1.png>`


.. figure:: /srcs_generated_examples/images/singlecell_simulation080_out2.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/singlecell_simulation080_out2.png>`



