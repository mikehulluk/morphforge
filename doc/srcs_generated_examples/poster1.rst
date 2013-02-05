
28. Simulation of a HodgkinHuxley-type neuron specified through NeuroUnits
==========================================================================


Simulation of a HodgkinHuxley-type neuron specified through NeuroUnits.

Code
~~~~

.. code-block:: python

	
	
	
	
	
	
	
	
	
	
	
	import matplotlib as mpl
	mpl.rcParams['font.size'] = 14
	
	from morphforge.stdimports import *
	from morphforgecontrib.stdimports import *
	
	eqnset_txt_na = """
	eqnset hh_na {
	    i = g * (v-erev) * m**3*h
	
	    minf = m_alpha_rate / (m_alpha_rate + m_beta_rate)
	    mtau = 1.0 / (m_alpha_rate + m_beta_rate)
	    m' = (minf-m) / mtau
	
	    hinf = h_alpha_rate / (h_alpha_rate + h_beta_rate)
	    htau = 1.0 / (h_alpha_rate + h_beta_rate)
	    h' = (hinf-h) / htau
	    StdFormAB(V,a1,a2,a3,a4,a5) = (a1+a2*V)/(a3+std.math.exp((V+a4)/a5))
	    m_alpha_rate = StdFormAB(V=v,a1=m_a1,a2=m_a2,a3=m_a3,a4=m_a4,a5=m_a5)
	    m_beta_rate =  StdFormAB(V=v,a1=m_b1,a2=m_b2,a3=m_b3,a4=m_b4,a5=m_b5)
	    h_alpha_rate = StdFormAB(V=v,a1=h_a1,a2=h_a2,a3=h_a3,a4=h_a4,a5=h_a5)
	    h_beta_rate =  StdFormAB(V=v,a1=h_b1,a2=h_b2,a3=h_b3,a4=h_b4,a5=h_b5)
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
	eqnset hh_k {
	    i = g * (v-erev) * n*n*n*n
	    ninf = n_alpha_rate / (n_alpha_rate + n_beta_rate)
	    ntau = 1.0 / (n_alpha_rate + n_beta_rate)
	    n' = (ninf-n) / ntau
	    StdFormAB(V,a1,a2,a3,a4,a5) = (a1 + a2*V)/(a3+std.math.exp( (V+a4)/a5) )
	    n_alpha_rate = StdFormAB(V=v,a1=n_a1,a2=n_a2,a3=n_a3,a4=n_a4,a5=n_a5)
	    n_beta_rate =  StdFormAB(V=v,a1=n_b1,a2=n_b2,a3=n_b3,a4=n_b4,a5=n_b5)
	
	    n_a1={-0.55 ms-1}; n_a2={-0.01 mV-1 ms-1}; n_a3={-1.00}; n_a4={55.00 mV}; n_a5={-10.00 mV}
	    n_b1={0.125 ms-1}; n_b2={ 0.00 mV-1 ms-1}; n_b3={ 0.00}; n_b4={65.00 mV}; n_b5={ 80.00 mV}
	
	    g = {36.0mS/cm2}
	    erev = {-77.0mV}
	    <=> OUTPUT    i:(A/m2)  METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }
	    <=> INPUT     v: V      METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
	} """
	
	eqnset_txt_lk = """
	eqnset hh_lk {
	    i = {0.3mS/cm2} * ( v- {-54.3mV} )
	    <=> OUTPUT    i:(A/m2)  METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }
	    <=> INPUT     v: V      METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
	} """
	
	env = NeuronSimulationEnvironment()
	sim = env.Simulation()
	
	# Create a cell:
	morph_dict = {'root': {'length': 18.8, 'diam': 18.8, 'id':'soma'} }
	my_morph = MorphologyTree.fromDictionary(morph_dict)
	cell = sim.create_cell(name="Cell1", morphology=my_morph)
	soma = cell.get_location("soma")
	
	# Setup passive channels:
	apply_passive_everywhere_uniform(cell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )
	
	# Setup active channels:
	na_chl = env.MembraneMechanism(NeuroUnitEqnsetMechanism, name="NaChl", eqnset=eqnset_txt_na,
	        default_parameters={"g":U("120:mS/cm2")}, mechanism_id="NaChl")
	k_chl = env.MembraneMechanism(NeuroUnitEqnsetMechanism, name="KChl", eqnset=eqnset_txt_k, mechanism_id="kChl")
	lk_chl = env.MembraneMechanism(NeuroUnitEqnsetMechanism, name="LKChl",eqnset=eqnset_txt_lk, mechanism_id="lkChl")
	
	apply_mechanism_everywhere_uniform(cell, na_chl )
	apply_mechanism_everywhere_uniform(cell, lk_chl )
	apply_mechanism_everywhere_uniform(cell, k_chl )
	
	# Define what to record:
	sim.record( cell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = soma )
	sim.record(na_chl, what='m', cell_location=soma, user_tags=[StandardTags.StateVariable])
	sim.record(na_chl, what='h', cell_location=soma, user_tags=[StandardTags.StateVariable])
	sim.record(k_chl,  what='n', cell_location=soma, user_tags=[StandardTags.StateVariable])
	
	# Create the stimulus and record the injected current:
	cc = sim.create_currentclamp( name="CC1", amp=U("100:pA"), dur=U("100:ms"), delay=U("100:ms"), cell_location=soma)
	sim.record(cc, what=StandardTags.Current)
	
	
	# run the simulation
	results = sim.run()
	TagViewer(results, timeranges=[(50, 250)*pq.ms], show=True )
	
	
	




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/poster1_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/poster1_out1.png>`






Output
~~~~~~

.. code-block:: bash

    	Reading JSON: {"mf":{"role":"TRANSMEMBRANECURRENT"}}
	Reading JSON: {"mf":{"role":"MEMBRANEVOLTAGE"}}
	CHECKING
	<neurounits.ast.astobjects.Parameter object at 0xb6f91ec>
	g
	iii 1.0 s**3*A**2/(kg*m**4) <class 'quantities.quantity.Quantity'>
	iiii 1200.0 s**3*A**2/(kg*m**4) <class 'quantities.quantity.Quantity'>
	OK
	
	m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	m_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	m_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	g <class 'neurounits.ast.astobjects.Parameter'>
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	m <class 'neurounits.ast.astobjects.StateVariable'>
	h <class 'neurounits.ast.astobjects.StateVariable'>
	h_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	h_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	h_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	h_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	h_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xb6f732c>, <neurounits.ast.astobjects.AssignedVariable object at 0xb6fbc6c>])
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xb6f732c>, <neurounits.ast.astobjects.AssignedVariable object at 0xb6fbc6c>])
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xb6fb78c>, <neurounits.ast.astobjects.AssignedVariable object at 0xb6fba0c>])
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xb6fb78c>, <neurounits.ast.astobjects.AssignedVariable object at 0xb6fba0c>])
	[]
	Unexpected: []
	[]
	Unexpected: []
	[]
	Unexpected: []
	[]
	Unexpected: []
	[]
	Unexpected: []
	[]
	Unexpected: []
	[]
	Unexpected: []
	[]
	Unexpected: []
	Deps; set([])
	hinf <class 'neurounits.ast.astobjects.AssignedVariable'>
	h <class 'neurounits.ast.astobjects.StateVariable'>
	htau <class 'neurounits.ast.astobjects.AssignedVariable'>
	minf <class 'neurounits.ast.astobjects.AssignedVariable'>
	m <class 'neurounits.ast.astobjects.StateVariable'>
	mtau <class 'neurounits.ast.astobjects.AssignedVariable'>
	x <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	a1 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	a2 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	V <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	a3 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	T [<class 'neurounits.ast.astobjects.DivOp'>]
	V <cla2012-07-15 16:22:10,883 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 16:22:10,883 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
	2012-07-15 16:22:11,521 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 16:22:11,521 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/3d/3dcbee9ee7eee982296a112d1f5a7da8.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'SomaVoltage'}
	Executing: /opt/nrn/i686/bin/modlunit /home/michael/old_home/mftmp/tmp_b73dbf8072bb44c47b2b707332462bbb.mod
	/mnt/sdb5/home/michael/mftmp/modbuild_2509
	Executing: /opt/nrn/i686/bin/nocmodl tmp_b73dbf8072bb44c47b2b707332462bbb.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/i686/lib"    -g -O2 -c -o tmp_b73dbf8072bb44c47b2b707332462bbb.lo tmp_b73dbf8072bb44c47b2b707332462bbb.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_b73dbf8072bb44c47b2b707332462bbb.la  -rpath /opt/nrn/i686/libs  tmp_b73dbf8072bb44c47b2b707332462bbb.lo  -L/opt/nrn/i686/lib -L/opt/nrn/i686/lib  /opt/nrn/i686/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/opt/nrn/include/nrn -I/opt/nrn/i686/lib -g -O2 -c tmp_b73dbf8072bb44c47b2b707332462bbb.c  -fPIC -DPIC -o .libs/tmp_b73dbf8072bb44c47b2b707332462bbb.o
	
	OP2: libtool: link: gcc -shared  .libs/tmp_b73dbf8072bb44c47b2b707332462bbb.o   -Wl,-rpath -Wl,/opt/nrn/i686/lib -Wl,-rpath -Wl,/opt/nrn/i686/lib -L/opt/nrn/i686/lib /opt/nrn/i686/lib/libnrniv.so /opt/nrn/i686/lib/libnrnoc.so /opt/nrn/i686/lib/liboc.so /opt/nrn/i686/lib/libmemacs.so /opt/nrn/i686/lib/libnrnmpi.so /opt/nrn/i686/lib/libscopmath.so /opt/nrn/i686/lib/libsparse13.so -lreadline -lncurses /opt/nrn/i686/lib/libivoc.so /opt/nrn/i686/lib/libneuron_gnu.so /opt/nrn/i686/lib/libmeschach.so /opt/nrn/i686/lib/libsundials.so -lm -ldl    -pthread -Wl,-soname -Wl,tmp_b73dbf8072bb44c47b2b707332462bbb.so.0 -o .libs/tmp_b73dbf8072bb44c47b2b707332462bbb.so.0.0.0
	libtool: link: (cd ".libs" && rm -f "tmp_b73dbf8072bb44c47b2b707332462bbb.so.0" && ln -s "tmp_b73dbf8072bb44c47b2b707332462bbb.so.0.0.0" "tmp_b73dbf8072bb44c47b2b707332462bbb.so.0")
	libtool: link: (cd ".libs" && rm -f "tmp_b73dbf8072bb44c47b2b707332462bbb.so" && ln -s "tmp_b73dbf8072bb44c47b2b707332462bbb.so.0.0.0" "tmp_b73dbf8072bb44c47b2b707332462bbb.so")
	libtool: link: ( cd ".libs" && rm -f "tmp_b73dbf8072bb44c47b2b707332462bbb.la" && ln -s "../tmp_b73dbf8072bb44c47b2b707332462bbb.la" "tmp_b73dbf8072bb44c47b2b707332462bbb.la" )
	
	Executing: /opt/nrn/i686/bin/modlunit /home/michael/old_home/mftmp/tmp_c8202f6bb00f1baf5fdd950cf0d9a4f9.mod
	/mnt/sdb5/home/michael/mftmp/modbuild_2509
	Executing: /opt/nrn/i686/bin/nocmodl tmp_c8202f6bb00f1baf5fdd950cf0d9a4f9.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/i686/lib"    -g -O2 -c -o tmp_c8202f6bb00f1baf5fdd950cf0d9a4f9.lo tmp_c8202f6bb00f1baf5fdd950cf0d9a4f9.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_c8202f6bb00f1baf5fdd950cf0d9a4f9.la  -rpath /opt/nrn/i686/libs  tmp_c8202f6bb00f1baf5fdd950cf0d9a4f9.lo  -L/opt/nrn/i686/lib -L/opt/nrn/i686/lib  /opt/nrn/i686/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/opt/nrn/include/nrn -I/opt/nrn/i686/lib -g -O2 -c tmp_c8202f6bb00f1baf5fdd950cf0d9a4f9.c  -fPIC -DPIC -o .libs/tmp_c8202f6bb00f1baf5fdd950cf0d9a4f9.o
	
	OP2: libtool: link: gcc -shared  .libs/tmp_c8202f6bb00f1baf5fdd950cf0d9a4f9.o   -Wl,-rpath -Wl,/opt/nrn/i686/lib -Wl,-rpath -Wl,/opt/nrn/i686/lib -L/opt/nrn/i686/lib /opt/nrn/i686/lib/libnrniv.so /opt/nrn/i686/lib/libnrnoc.so /opt/nrn/i686/lib/liboc.so /opt/nrn/i686/lib/libmemacs.so /opt/nrn/i686/lib/libnrnmpi.so /opt/nrn/i686/lib/libscopmath.so /opt/nrn/i686/lib/libsparse13.so -lreadline -lncurses /opt/nrn/i686/lib/libivoc.so /opt/nrn/i686/lib/libneuron_gnu.so /opt/nrn/i686/lib/libmeschach.so /opt/nrn/i686/lib/libsundials.so -lm -ldl    -pthread -Wl,-sonNEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	ame -Wl,tmp_c8202f6bb00f1baf5fdd950cf0d9a4f9.so.0 -o .libs/tmp_c8202f6bb00f1baf5fdd950cf0d9a4f9.so.0.0.0
	libtool: link: (cd ".libs" && rm -f "tmp_c8202f6bb00f1baf5fdd950cf0d9a4f9.so.0" && ln -s "tmp_c8202f6bb00f1baf5fdd950cf0d9a4f9.so.0.0.0" "tmp_c8202f6bb00f1baf5fdd950cf0d9a4f9.so.0")
	libtool: link: (cd ".libs" && rm -f "tmp_c8202f6bb00f1baf5fdd950cf0d9a4f9.so" && ln -s "tmp_c8202f6bb00f1baf5fdd950cf0d9a4f9.so.0.0.0" "tmp_c8202f6bb00f1baf5fdd950cf0d9a4f9.so")
	libtool: link: ( cd ".libs" && rm -f "tmp_c8202f6bb00f1baf5fdd950cf0d9a4f9.la" && ln -s "../tmp_c8202f6bb00f1baf5fdd950cf0d9a4f9.la" "tmp_c8202f6bb00f1baf5fdd950cf0d9a4f9.la" )
	
	Time for Building Mod-Files:  1.08625602722
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_fbb85852e0a830e4c784a20ccbdf50e7.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_7e1b2d96b76f63ca29b09c7fa3dbd568.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_659f164e57ab1ae7e3ebb9de0f9abe7b.so
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
	Running Simulation
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb30942c> t= 495.0 ms
	Time for Simulation:  0.0483350753784
	Time for Extracting Data: (5 records) 0.0176010131836
	Simulation Time Elapsed:  1.28268694878
	Suceeded
	ss 'neurounits.ast.astobjects.FunctionDefParameter'>
	a4 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	a5 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	Reading JSON: {"mf":{"role":"TRANSMEMBRANECURRENT"}}
	Reading JSON: {"mf":{"role":"MEMBRANEVOLTAGE"}}
	n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	n_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	n <class 'neurounits.ast.astobjects.StateVariable'>
	n <class 'neurounits.ast.astobjects.StateVariable'>
	n <class 'neurounits.ast.astobjects.StateVariable'>
	n <class 'neurounits.ast.astobjects.StateVariable'>
	T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	n_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xb6f114c>, <neurounits.ast.astobjects.AssignedVariable object at 0xb6ef86c>])
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xb6f114c>, <neurounits.ast.astobjects.AssignedVariable object at 0xb6ef86c>])
	[]
	Unexpected: []
	[]
	Unexpected: []
	[]
	Unexpected: []
	[]
	Unexpected: []
	Deps; set([])
	ninf <class 'neurounits.ast.astobjects.AssignedVariable'>
	n <class 'neurounits.ast.astobjects.StateVariable'>
	ntau <class 'neurounits.ast.astobjects.AssignedVariable'>
	x <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	a1 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	a2 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	V <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	a3 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	T [<class 'neurounits.ast.astobjects.DivOp'>]
	V <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	a4 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	a5 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	Reading JSON: {"mf":{"role":"TRANSMEMBRANECURRENT"}}
	Reading JSON: {"mf":{"role":"MEMBRANEVOLTAGE"}}
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	Deps; set([])
	['name', 'simulation']
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xb05cc8c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xb06b5ac>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xb06ba2c>
	Saving File _output/figures/poster1/eps/fig000_Autosave_figure_1.eps
	Saving File _output/figures/poster1/pdf/fig000_Autosave_figure_1.pdf
	Saving File _output/figures/poster1/png/fig000_Autosave_figure_1.png
	Saving File _output/figures/poster1/svg/fig000_Autosave_figure_1.svg
	




