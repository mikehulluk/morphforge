
29. Action potential propagation and synaptic transmission
==========================================================


Action potential propagation and synaptic transmission.
In this simulation, we create 3 neurons; Neuron 1 has an axon, and when the
soma is stimulated, we see the action potential propagate along it. Neuron 1
forms synapses onto cell2 and cell3 with different strengths and different
positions along the axon.

Code
~~~~

.. code-block:: python

	
	
	
	
	
	
	
	
	
	import matplotlib as mpl
	mpl.rcParams['font.size'] = 14
	
	
	
	from morphforge.stdimports import *
	from morphforgecontrib.stdimports import *
	
	# Create a cell:
	def build_cell(name,sim):
	
	    my_morph = MorphologyBuilder.get_soma_axon_morph(axon_length=1500.0, axon_radius=0.3, soma_radius=10.0, )
	    my_cell = sim.create_cell(name=name, morphology=my_morph)
	
	    na_chls = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Na", env=sim.environment)
	    k_chls  = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="K",  env=sim.environment)
	    lk_chls = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Lk", env=sim.environment)
	
	    apply_mechanism_everywhere_uniform(my_cell, lk_chls )
	    apply_mechanism_everywhere_uniform(my_cell, k_chls )
	    apply_mechanism_everywhere_uniform(my_cell, na_chls )
	    apply_mechanism_region_uniform( my_cell,
	                                    na_chls,
	                                    region = my_cell.get_region("axon"),
	                                    parameter_multipliers={'gScale':1.0} )
	    return my_cell
	
	
	# Create a simulation:
	env = NeuronSimulationEnvironment()
	sim = env.Simulation()
	
	# Two cells:
	cell1 = build_cell(name="cell1",sim=sim)
	cell2 = build_cell(name="cell2",sim=sim)
	cell3 = build_cell(name="cell3",sim=sim)
	
	
	# Connect with a synapse:
	simple_ampa_syn = """
	EQNSET syn_simple {
	
	    g' = - g/g_tau
	    i = gmax * (v-erev) * g
	
	    gmax = 300pS * scale
	    erev = 0mV
	
	    g_tau = 10ms
	    <=> INPUT     v: mV       METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
	    <=> OUTPUT    i:(mA)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }
	    <=> PARAMETER scale:()
	    ==>> on_event() {
	        g = g + 1.0
	    }
	}
	"""
	
	
	syn1 = sim.create_synapse(
	        presynaptic_mech =  env.PreSynapticMechanism(
	                                    PreSynapticMech_VoltageThreshold,
	                                    cell_location = CellLocator.get_location_at_distance_away_from_dummy(cell1, 300),
	                                    voltage_threshold = U("0:mV"),  delay = U("0:ms"),     weight = U("1:nS"),
	                                    ),
	        postsynaptic_mech = env.PostSynapticMechanism(
	                                    NeuroUnitEqnsetPostSynaptic,
	                                    eqnset = neurounits.NeuroUnitParser.EqnSet(simple_ampa_syn),
	                                    default_parameters= {'scale':1.0*pq.dimensionless},
	                                    cell_location = cell2.get_location("soma")
	                                    )
	        )
	
	syn1 = sim.create_synapse(
	        presynaptic_mech =  env.PreSynapticMechanism(
	                                    PreSynapticMech_VoltageThreshold,
	                                    cell_location = CellLocator.get_location_at_distance_away_from_dummy(cell1, 700),
	                                    voltage_threshold = U("0:mV"),  delay = U("0:ms"), weight = U("1:nS"),
	                                    ),
	        postsynaptic_mech = env.PostSynapticMechanism(
	                                    NeuroUnitEqnsetPostSynaptic,
	                                    eqnset = neurounits.NeuroUnitParser.EqnSet(simple_ampa_syn),
	                                    default_parameters= {'scale':2.0*pq.dimensionless},
	                                    cell_location = cell3.get_location("soma")
	                                    )
	        )
	
	# Record Voltages from axons:
	for loc in CellLocator.get_locations_at_distances_away_from_dummy( cell1, range(0,1000,50) ):
	    sim.record(  what=StandardTags.Voltage, cell_location = loc, user_tags=['cell1'] )
	sim.record( what=StandardTags.Voltage, cell_location = cell2.get_location("soma"), user_tags=['cell2'] )
	sim.record( what=StandardTags.Voltage, cell_location = cell3.get_location("soma"), user_tags=['cell3'] )
	
	# Create the stimulus and record the injected current:
	cc = sim.create_currentclamp( name="CC1", amp=U("200:pA"), dur=U("1:ms"), delay=U("100:ms"), cell_location=cell1.get_location("soma"))
	sim.record(cc, what=StandardTags.Current)
	
	results = sim.run()
	TagViewer(results, timeranges=[(98, 120)*pq.ms], 
	          fig_kwargs = {'figsize':(12,10)},
	          show=True,
	          plotspecs = [
	              PlotSpec_DefaultNew('Current', yunit=pq.picoamp),
	              PlotSpec_DefaultNew('Voltage,cell1', yrange=(-80*mV,50*mV), yunit=pq.mV ),
	              PlotSpec_DefaultNew('Voltage AND ANY{cell2,cell3}', yrange=(-70*mV,-55*mV), yunit=pq.millivolt),
	              ],
	            )
	
	
	




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/poster2_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/poster2_out1.png>`






Output
~~~~~~

.. code-block:: bash

    	2012-07-15 16:22:14,849 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 16:22:14,849 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
	2012-07-15 16:22:15,750 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 16:22:15,750 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/0f/0f65930724f185d4babf1f4227002efd.bundle
	{'sectionpos': 0.0, 'sectionindex': 0, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0003'}
	{'sectionpos': 0.20000000000000001, 'sectionindex': 1, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0004'}
	{'sectionpos': 0.53333333333333333, 'sectionindex': 1, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0005'}
	{'sectionpos': 0.8666666666666667, 'sectionindex': 1, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0006'}
	{'sectionpos': 0.20000000000000001, 'sectionindex': 2, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0007'}
	{'sectionpos': 0.53333333333333333, 'sectionindex': 2, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0008'}
	{'sectionpos': 0.8666666666666667, 'sectionindex': 2, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0009'}
	{'sectionpos': 0.20000000000000001, 'sectionindex': 3, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0010'}
	{'sectionpos': 0.53333333333333333, 'sectionindex': 3, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0011'}
	{'sectionpos': 0.8666666666666667, 'sectionindex': 3, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0012'}
	{'sectionpos': 0.20000000000000001, 'sectionindex': 4, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0013'}
	{'sectionpos': 0.53333333333333333, 'sectionindex': 4, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0014'}
	{'sectionpos': 0.8666666666666667, 'sectionindex': 4, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0015'}
	{'sectionpos': 0.20000000000000001, 'sectionindex': 5, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0016'}
	{'sectionpos': 0.53333333333333333, 'sectionindex': 5, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0017'}
	{'sectionpos': 0.8666666666666667, 'sectionindex': 5, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0018'}
	{'sectionpos': 0.20000000000000001, 'sectionindex': 6, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0019'}
	{'sectionpos': 0.53333333333333333, 'sectionindex': 6, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0020'}
	{'sectionpos': 0.8666666666666667, 'sectionindex': 6, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0021'}
	{'sectionpos': 0.20000000000000001, 'sectionindex': 7, 'cellname': 'cell_cell1', 'recVecName': 'AnonObj0022'}
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_cell2', 'recVecName': 'AnonObj0023'}
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_cell3', 'recVecName': 'AnonObj0024'}
	Executing: /opt/nrn/i686/bin/modlunit /home/michael/old_home/mftmp/tmp_3765b0f9567b344f0274f43f5291f49d.mod
	/mnt/sdb5/home/michael/mftmp/modbuild_2850
	Executing: /opt/nrn/i686/bin/nocmodl tmp_3765b0f9567b344f0274f43f5291f49d.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/i686/lib"    -g -O2 -c -o tmp_3765b0f9567b344f0274f43f5291f49d.lo tmp_3765b0f9567b344f0274f43f5291f49d.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_3765b0f9567b344f0274f43f5291f49d.la  -rpath /opt/nrn/i686/libs  tmp_3765b0f9567b344f0274f43f5291f49d.lo  -L/opt/nrn/i686/lib -L/opt/nrn/i686/lib  /opt/nrn/i686/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/opt/nrn/include/nrn -I/opt/nrn/i686/lib -g -O2 -c tmp_3765b0f9567b344f0274f43f5291f49d.c  -fPIC -DPIC -o .libs/tmp_3765b0f9567b344f0274f43f5291f49d.o
	
	OP2: libtool: link: gcc -shared  .libs/tmp_3765b0f9567b344f0274f43f5291f49d.o   -Wl,-rpath -Wl,/opt/nrn/i686/lib -Wl,-rpath -Wl,/opt/nrn/i686/lib -L/opt/nrn/i686/lib /opt/nrn/i686/lib/libnrniv.so /opt/nrn/i686/lib/libnrnoc.so /opt/nrn/i686/lib/liboc.so /opt/nrn/i686/lib/libmemacs.so /opt/nrn/i686/lib/libnrnmpi.so /opt/nrn/i686/lib/libscopmath.so /opt/nrn/i686/lib/libsparse13.so -lreadline -lncurses /opt/nrn/i686/lib/libivoc.so /opt/nrn/i686/lib/libneuron_gnu.so /opt/nrn/i686/lib/libmeschach.so /opt/nrn/i686/lib/libsundials.so -lm -ldl    -pthread -WlNEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	,-soname -Wl,tmp_3765b0f9567b344f0274f43f5291f49d.so.0 -o .libs/tmp_3765b0f9567b344f0274f43f5291f49d.so.0.0.0
	libtool: link: (cd ".libs" && rm -f "tmp_3765b0f9567b344f0274f43f5291f49d.so.0" && ln -s "tmp_3765b0f9567b344f0274f43f5291f49d.so.0.0.0" "tmp_3765b0f9567b344f0274f43f5291f49d.so.0")
	libtool: link: (cd ".libs" && rm -f "tmp_3765b0f9567b344f0274f43f5291f49d.so" && ln -s "tmp_3765b0f9567b344f0274f43f5291f49d.so.0.0.0" "tmp_3765b0f9567b344f0274f43f5291f49d.so")
	libtool: link: ( cd ".libs" && rm -f "tmp_3765b0f9567b344f0274f43f5291f49d.la" && ln -s "../tmp_3765b0f9567b344f0274f43f5291f49d.la" "tmp_3765b0f9567b344f0274f43f5291f49d.la" )
	
	Time for Building Mod-Files:  0.553593873978
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_b9561f3b8794fa66ebc2cce450f95024.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_9b5f608a37f872edf03d16c72ccd71c5.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_74c59031c780519a8019364f7c98b1b3.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_47dffa573b1bee1b1d3f6b85672e9bca.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_0aa0a8d639fdf428b84cdd20ccde5bd3.so
		1 
		1 
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
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb6779ec> t= 495.0 ms
	Time for Simulation:  1.16159677505
	Time for Extracting Data: (23 records) 0.0688679218292
	Simulation Time Elapsed:  2.19765210152
	Suceeded
	Reading JSON: {"mf":{"role":"MEMBRANEVOLTAGE"}}
	Reading JSON: {"mf":{"role":"TRANSMEMBRANECURRENT"}}
	<neurounits.ast.astobjects.Parameter object at 0xaf38a0c>
	scale
	iii 1.0 dimensionless <class 'quantities.quantity.Quantity'>
	iiii 1.0 dimensionless <class 'quantities.quantity.Quantity'>
	gmax <class 'neurounits.ast.astobjects.AssignedVariable'>
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	g <class 'neurounits.ast.astobjects.StateVariable'>
	scale <class 'neurounits.ast.astobjects.Parameter'>
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xafe7fec>])
	g <class 'neurounits.ast.astobjects.StateVariable'>
	g <class 'neurounits.ast.astobjects.StateVariable'>
	Reading JSON: {"mf":{"role":"MEMBRANEVOLTAGE"}}
	Reading JSON: {"mf":{"role":"TRANSMEMBRANECURRENT"}}
	<neurounits.ast.astobjects.Parameter object at 0xafbe14c>
	scale
	iii 1.0 dimensionless <class 'quantities.quantity.Quantity'>
	iiii 2.0 dimensionless <class 'quantities.quantity.Quantity'>
	scale <class 'neurounits.ast.astobjects.Parameter'>
	gmax <class 'neurounits.ast.astobjects.AssignedVariable'>
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	g <class 'neurounits.ast.astobjects.StateVariable'>
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xafd6c2c>])
	g <class 'neurounits.ast.astobjects.StateVariable'>
	g <class 'neurounits.ast.astobjects.StateVariable'>
	['name', 'simulation']
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xafe506c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xae7302c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa93eecc>
	Saving File _output/figures/poster2/eps/fig000_Autosave_figure_1.eps
	Saving File _output/figures/poster2/pdf/fig000_Autosave_figure_1.pdf
	Saving File _output/figures/poster2/png/fig000_Autosave_figure_1.png
	Saving File _output/figures/poster2/svg/fig000_Autosave_figure_1.svg
	




