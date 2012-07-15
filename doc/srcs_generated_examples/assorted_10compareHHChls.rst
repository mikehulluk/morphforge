
27. Comparing simulations: the Hodgkin-Huxley '52 channels
==========================================================


Comparing simulations: the Hodgkin-Huxley '52 channels

This simulation compares the different ways of implementing the Hodgkin-Huxley channels;
we check that the Hodgkin-Huxley channels built-in to NEURON produce the same results as
when we create these channels with parameters as an MM_AlphaBetaChannel.

In you are not familiar with python, then this is an example of the one of
the advantages of the laanguage: functions are objects!

In "test_neuron", we create a neuron morphology, but put the code to add the channels
in a different function. This makes it easy to try out different channel types and
distributions easily and quickly.

Code
~~~~

.. code-block:: python

	
	
	
	
	
	
	
	from morphforgecontrib.simulation.membranemechanisms.neuroml_via_neurounits.neuroml_via_neurounits_core import NeuroML_Via_NeuroUnits_Channel
	from morphforgecontrib.simulation.membranemechanisms.neurounits.neuro_units_bridge import Neuron_NeuroUnitEqnsetMechanism
	
	from morphforge.stdimports import *
	from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmleak import MM_LeakChannel
	from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmalphabeta import MM_AlphaBetaChannel
	from morphforgecontrib.simulation.membranemechanisms.simulatorbuiltin.sim_builtin_core import BuiltinChannel
	from morphforgecontrib.simulation.membranemechanisms.neuroml_via_xsl.neuroml_via_xsl_core import NeuroML_Via_XSL_Channel
	
	import random as R
	
	
	vars = ['h','m','minf','mtau','m_alpha_rate','m_beta_rate',]
	
	def apply_hh_chls_neurounits_direct(env, myCell, mySim):
	
	    eqnset_txt_na = """
	    EQNSET chlstd_hh_na {
	        from std.math import exp
	        i = g * (v-erev) * m**3*h
	        minf = m_alpha_rate / (m_alpha_rate + m_beta_rate)
	        mtau = 1.0 / (m_alpha_rate + m_beta_rate)
	        m' = (minf-m) / mtau
	        hinf = h_alpha_rate / (h_alpha_rate + h_beta_rate)
	        htau = 1.0 / (h_alpha_rate + h_beta_rate)
	        h' = (hinf-h) / htau
	        StdFormAB(V,a1,a2,a3,a4,a5) = (a1 + a2*V)/(a3+exp( (V+a4)/a5) )
	        m_alpha_rate = StdFormAB( V=v,a1=m_a1,a2=m_a2,a3=m_a3,a4=m_a4,a5=m_a5)
	        m_beta_rate =  StdFormAB( V=v,a1=m_b1,a2=m_b2,a3=m_b3,a4=m_b4,a5=m_b5)
	        h_alpha_rate = StdFormAB( V=v,a1=h_a1,a2=h_a2,a3=h_a3,a4=h_a4,a5=h_a5)
	        h_beta_rate =  StdFormAB( V=v,a1=h_b1,a2=h_b2,a3=h_b3,a4=h_b4,a5=h_b5)
	        m_a1 = {-4.00 ms-1}
	        m_a2 = {-0.10 mV-1 ms-1}
	        m_a3 = -1.00
	        m_a4 = {40.00 mV}
	        m_a5 = {-10.00 mV}
	        m_b1 = {4.00 ms-1}
	        m_b2 = {0.00 mV-1 ms-1}
	        m_b3 = {0.00}
	        m_b4 = {65.00 mV}
	        m_b5 = {18.00 mV}
	        h_a1 = {0.07 ms-1}
	        h_a2 = {0.00 mV-1 ms-1}
	        h_a3 = {0.00}
	        h_a4 = {65.00 mV}
	        h_a5 = {20.00 mV}
	        h_b1 = {1.00  ms-1}
	        h_b2 = {0.00  mV-1 ms-1}
	        h_b3 = {1.00}
	        h_b4 = {35.00  mV}
	        h_b5 = {-10.00 mV}
	        sg = {120.0mS/cm2}
	        erev = {50.0mV}
	        <=> PARAMETER g:(S/m2)
	        <=> OUTPUT    i:(A/m2)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }
	        <=> INPUT     v: V           METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
	    }
	    """
	
	    eqnset_txt_k = """
	    EQNSET chlstd_hh_k {
	        from std.math import exp
	        i = g * (v-erev) * n*n*n*n
	        ninf = n_alpha_rate / (n_alpha_rate + n_beta_rate)
	        ntau = 1.0 / (n_alpha_rate + n_beta_rate)
	        n' = (ninf-n) / ntau
	        StdFormAB(V,a1,a2,a3,a4,a5) = (a1 + a2*V)/(a3+exp( (V+a4)/a5) )
	        n_alpha_rate = StdFormAB( V=v,a1=n_a1,a2=n_a2,a3=n_a3,a4=n_a4,a5=n_a5)
	        n_beta_rate =  StdFormAB( V=v,a1=n_b1,a2=n_b2,a3=n_b3,a4=n_b4,a5=n_b5)
	
	        n_a1 = {-0.55 ms-1}
	        n_a2 = {-0.01 mV-1 ms-1}
	        n_a3 = -1.00
	        n_a4 = {55.00 mV}
	        n_a5 = {-10.00 mV}
	        n_b1 = {0.125 ms-1}
	        n_b2 = {0.00 mV-1 ms-1}
	        n_b3 = {0.00}
	        n_b4 = {65.00 mV}
	        n_b5 = {80.00 mV}
	
	        g = {36.0mS/cm2}
	        erev = {-77.0mV}
	        <=> OUTPUT    i:(A/m2)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }
	        <=> INPUT     v: V          METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
	    }
	    """
	
	    eqnset_txt_lk = """
	        EQNSET chlstd_hh_lk {
	            i = g * (v-erev)
	            g = {0.3 mS/cm2}
	            erev = -54.3 mV
	            <=> OUTPUT    i:(A/m2)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }
	            <=> INPUT     v: V          METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
	            }
	    """
	
	
	    naChls = Neuron_NeuroUnitEqnsetMechanism(name="Chl1", eqnset=eqnset_txt_na, default_parameters={"g":unit("120:mS/cm2")}, mechanism_id="JLK")
	    lkChls = Neuron_NeuroUnitEqnsetMechanism(name="Chl2", eqnset=eqnset_txt_lk, mechanism_id="JasdasdasdLK")
	    kChls  = Neuron_NeuroUnitEqnsetMechanism(name="Chl3", eqnset=eqnset_txt_k,  mechanism_id="JLasdasdK")
	
	
	    apply_mechanism_everywhere_uniform(myCell, naChls )
	    apply_mechanism_everywhere_uniform(myCell, lkChls )
	    apply_mechanism_everywhere_uniform(myCell, kChls )
	
	
	    mySim.record(naChls, what='m', cell_location= myCell.get_location("soma"), user_tags=[StandardTags.StateVariable] )
	    mySim.record(naChls, what='mtau', cell_location= myCell.get_location("soma"), user_tags=[StandardTags.StateTimeConstant] )
	
	    mySim.record(naChls, what='h', cell_location= myCell.get_location("soma"), user_tags=[StandardTags.StateVariable] )
	    mySim.record(naChls, what='htau', cell_location= myCell.get_location("soma"), user_tags=[StandardTags.StateTimeConstant] )
	
	    mySim.record(kChls, what='n', cell_location= myCell.get_location("soma"), user_tags=[StandardTags.StateVariable] )
	    mySim.record(kChls, what='ntau', cell_location= myCell.get_location("soma"), user_tags=[StandardTags.StateTimeConstant] )
	
	
	
	
	def apply_hh_chls_neuroml_xsl(env, myCell, mySim):
	
	
	
	    leakChannels = env.MembraneMechanism(
	                         MM_LeakChannel,
	                         name="LkChl",
	                         conductance=unit("0.3:mS/cm2"),
	                         reversalpotential=unit("-54.3:mV"),
	                         mechanism_id = 'HULL12_DIN_LK_ID'
	                            )
	
	    sodiumChannels = env.MembraneMechanism( NeuroML_Via_XSL_Channel,
	                                            xml_filename = "/home/michael/srcs/neuroml/CommandLineUtils/ChannelMLConverter/NaChannel_HH.xml",
	                                            xsl_filename = "/home/michael/srcs/neuroml/CommandLineUtils/ChannelMLConverter/ChannelML_v1.8.1_NEURONmod.xsl",
	                                            mechanism_id="Na"
	                                            )
	
	    kChannels = env.MembraneMechanism( NeuroML_Via_XSL_Channel,
	                                            xml_filename = "/home/michael/srcs/neuroml/CommandLineUtils/ChannelMLConverter/KChannel_HH.xml",
	                                            xsl_filename = "/home/michael/srcs/neuroml/CommandLineUtils/ChannelMLConverter/ChannelML_v1.8.1_NEURONmod.xsl",
	                                            mechanism_id="K"
	                                            )
	
	    apply_mechanism_everywhere_uniform(myCell, sodiumChannels )
	    apply_mechanism_everywhere_uniform(myCell, leakChannels )
	    apply_mechanism_everywhere_uniform(myCell, kChannels )
	
	
	
	
	
	
	
	
	def apply_hh_chls_neuroml_neurounits(env, myCell, mySim):
	
	
	
	    leakChannels = env.MembraneMechanism(
	                         MM_LeakChannel,
	                         name="LkChl",
	                         conductance=unit("0.3:mS/cm2"),
	                         reversalpotential=unit("-54.3:mV"),
	                         mechanism_id = 'HULL12_DIN_LK_ID'
	                            )
	
	    sodiumChannels = env.MembraneMechanism( NeuroML_Via_NeuroUnits_Channel,
	                                            xml_filename = "/home/michael/srcs/neuroml/CommandLineUtils/ChannelMLConverter/NaChannel_HH.xml",
	                                            #xsl_filename = "/home/michael/srcs/neuroml/CommandLineUtils/ChannelMLConverter/ChannelML_v1.8.1_NEURONmod.xsl",
	                                            mechanism_id="Na"
	                                            )
	
	    kChannels = env.MembraneMechanism( NeuroML_Via_XSL_Channel,
	    #kChannels = env.MembraneMechanism( NeuroML_Via_NeuroUnits_Channel,
	                                            xml_filename = "/home/michael/srcs/neuroml/CommandLineUtils/ChannelMLConverter/KChannel_HH.xml",
	                                            xsl_filename = "/home/michael/srcs/neuroml/CommandLineUtils/ChannelMLConverter/ChannelML_v1.8.1_NEURONmod.xsl",
	                                            mechanism_id="K"
	                                            )
	
	    apply_mechanism_everywhere_uniform(myCell, sodiumChannels )
	    apply_mechanism_everywhere_uniform(myCell, leakChannels )
	    apply_mechanism_everywhere_uniform(myCell, kChannels )
	
	
	    #for v in vars:
	    #    s =MM_Neuron_NeuroUnits_GenRecord(chl=sodiumChannels, modvar=v, name=v, cell_location=myCell.get_location("soma"))
	    #    mySim.add_recordable(s)
	
	
	
	def apply_hh_chls_morphforge_format(env, myCell, mySim):
	
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
	
	    apply_mechanism_everywhere_uniform(myCell, leakChannels )
	    apply_mechanism_everywhere_uniform(myCell, sodiumChannels )
	    apply_mechanism_everywhere_uniform(myCell, kChannels )
	
	
	
	
	def apply_hh_chls_NEURON_builtin(env, myCell,mySim):
	
	    hhChls = env.MembraneMechanism(BuiltinChannel,  sim_chl_name="hh", mechanism_id="IDA" )
	    apply_mechanism_everywhere_uniform(myCell, hhChls )
	
	
	
	
	
	
	def simulate_chls_on_neuron(chl_applicator_functor):
	    # Create the environment:
	    env = NeuronSimulationEnvironment()
	
	    # Create the simulation:
	    mySim = env.Simulation()
	
	    # Create a cell:
	    morphDict1 = {'root': {'length': 18.8, 'diam': 18.8, 'id':'soma'} }
	    m1 = MorphologyTree.fromDictionary(morphDict1)
	    myCell = mySim.create_cell(name="Cell1", morphology=m1)
	
	    # Setup the HH-channels on the cell:
	    chl_applicator_functor(env, myCell, mySim)
	
	    # Setup passive channels:
	    apply_passive_everywhere_uniform(myCell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )
	
	
	
	
	    # Get a cell_location on the cell:
	    somaLoc = myCell.get_location("soma")
	
	    # Create the stimulus and record the injected current:
	    cc = mySim.create_currentclamp( name="Stim1", amp=unit("100:pA"), dur=unit("100:ms"), delay=unit("100:ms") * R.uniform(0.95,1.0), cell_location=somaLoc)
	
	
	    # Define what to record:
	    mySim.record( myCell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = somaLoc )
	
	
	    # run the simulation
	    results = mySim.run()
	    return results
	
	
	
	
	
	resultsA =None
	resultsB =None
	resultsC =None
	resultsD =None
	resultsE =None
	
	
	resultsA = simulate_chls_on_neuron( apply_hh_chls_morphforge_format )
	resultsB = simulate_chls_on_neuron( apply_hh_chls_NEURON_builtin )
	resultsC = simulate_chls_on_neuron( apply_hh_chls_neuroml_neurounits )
	resultsD = simulate_chls_on_neuron( apply_hh_chls_neuroml_xsl )
	resultsE = simulate_chls_on_neuron( apply_hh_chls_neurounits_direct )
	#
	trs = [resultsA,resultsB,resultsC,resultsD,resultsE]
	trs = [tr for tr in trs if tr is not None]
	TagViewer(trs, timeranges=[(95, 200)*pq.ms], show=True )
	
	
	pylab.show()
	




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/assorted_10compareHHChls_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/assorted_10compareHHChls_out1.png>`






Output
~~~~~~

.. code-block:: bash

    	2012-07-15 16:22:02,195 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 16:22:02,195 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
	2012-07-15 16:22:02,876 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 16:22:02,876 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/5a/5ac98c2e5ea924159dbd36c4c0ce3ec8.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'SomaVoltage'}
	Time for Building Mod-Files:  0.000953912734985
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_84d1bd07ca97dcd5fbbd02b9f9e24292.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_5802f621da7bdb78d8cf28aa6f52a53d.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_84aedd04410d6d41b5f3d80aec3853c1.so
		1 
		1 
		1 
		50000 
		1 
	Running Simulation
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xabb47cc> t= 495.0 ms
	Time for Simulation:  0.039715051651
	Time for Extracting Data: (1 records) 0.0158109664917
	Simulation Time Elapsed:  0.218096971512
	Suceeded
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/e6/e66cf60034b9e48fed79502a07d31dde.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'SomaVoltage'}
	Time for Building Mod-Files:  4.05311584473e-06
		1 
		1 
		1 
		50000 
		1 
	Running Simulation
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa1818ac> t= 495.0 ms
	2012-07-15 16:22:03,709 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 16:22:03,710 - DISABLEDLOGGING - INFO - Simulation Ran OK. Post Processing:
	Time for Simulation:  0.0295219421387
	Time for Extracting Data: (1 records) 0.0139319896698
	Simulation Time Elapsed:  0.161772012711
	Suceeded
	2012-07-15 16:22:04,624 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 16:22:04,624 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/37/37b112b364ffe89e5ea45a738ae68cf7.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'SomaVoltage'}
	Executing: /opt/nrn/i686/bin/modlunit /home/michael/old_home/mftmp/tmp_3e41c7b0a82b3d23e1a4b214e4b61fbc.mod
	/mnt/sdb5/home/michael/mftmp/modbuild_1870
	Executing: /opt/nrn/i686/bin/nocmodl tmp_3e41c7b0a82b3d23e1a4b214e4b61fbc.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/i686/lib"    -g -O2 -c -o tmp_3e41c7b0a82b3d23e1a4b214e4b61fbc.lo tmp_3e41c7b0a82b3d23e1a4b214e4b61fbc.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_3e41c7b0a82b3d23e1a4b214e4b61fbc.la  -rpath /opt/nrn/i686/libs  tmp_3e41c7b0a82b3d23e1a4b214e4b61fbc.lo  -L/opt/nrn/i686/lib -L/opt/nrn/i686/lib  /opt/nrn/i686/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/opt/nrn/include/nrn -I/opt/nrn/i686/lib -g -O2 -c tmp_3e41c7b0a82b3d23e1a4b214e4b61fbc.c  -fPIC -DPIC -o .libs/tmp_3e41c7b0a82b3d23e1a4b214e4b61fbc.o
	
	OP2: libtool: link: gcc -shared  .libs/tmp_3e41c7b0a82b3d23e1a4b214e4b61fbc.o   -Wl,-rpath -Wl,/opt/nrn/i686/lib -Wl,-rpath -Wl,/opt/nrn/i686/lib -L/opt/nrn/i686/lib /opt/nrn/i686/lib/libnrniv.so /opt/nrn/i686/lib/libnrnoc.so /opt/nrn/i686/lib/liboc.so /opt/nrn/i686/lib/libmemacs.so /opt/nrn/i686/lib/libnrnmpi.so /opt/nrn/i686/lib/libscopmath.so /opt/nrn/i686/lib/libsparse13.so -lreadline -lncurses /opt/nrn/i686/lib/libivoc.so /opt/nrn/i686/lib/libneuron_gnu.so /opt/nrn/i686/lib/libmeschach.so /opt/nrn/i686/lib/libsundials.so -lm -ldl    -pthread -Wl,-soname -Wl,tmp_3e41c7b0a82b3d23e1a4b214e4b61fbc.so.0 -o .libs/tmp_3e41c7b0a82b3d23e1a4b214e4b61fbc.so.0.0.0
	libtool: link: (cd ".libs" && rm -f "tmp_3e41c7b0a82b3d23e1a4b214e4b61fbc.so.0" && ln -s "tmp_3e41c7b0a82b3d23e1a4b214e4b61fbc.so.0.0.0" "tmp_3e41c7b0a82b3d23e1a4b214e4b61fbc.so.0")
	libtool: link: (cd ".libs" && rm -f "tmp_3e41c7b0a82b3d23e1a4b214e4b61fbc.so" && ln -s "tmp_3e41c7b0a82b3d23e1a4b214e4b61fbc.so.0.0.0" "tmp_3e41c7b0a82b3d23e1a4b214e4b61fbc.so")
	libtool: link: ( cd ".libs" && rm -f "tmp_3e41c7b0a82b3d23e1a4b214e4b61fbc.la" && ln -s "../tmp_3e41c7b0a82b3d23e1a4b214e4b61fbc.la" "tmp_3e41c7b0a82b3d23e1a4b214e4b61fbc.la" )
	
	Time for Building Mod-Files:  0.543470144272
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_46e7d42aa7b4c050c823bdd80e99d0d7.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_1efc531eaf0bae2e49f6a5c8a91797f1.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_6a13c7a5c1256b824ea32520f372f65e.so
		1 
		1 
		1 
		50000 
		1 
	Running Simulation
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x98d6cac> t= 495.0 ms
	Time for Simulation:  0.0422339439392
	Time for Extracting Data: (1 records) 0.0147619247437
	Simulation Time Elapsed:  0.789886951447
	Suceeded
	2012-07-15 16:22:06,072 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 16:22:06,072 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/dd/dd826ad8301a22237eb9df0bb2de3e6b.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'SomaVoltage'}
	Time for Building Mod-Files:  0.000976085662842
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_a46bf2f1691a80cf44bb3239e7721133.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_1efc531eaf0bae2e49f6a5c8a91797f1.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_5a083cfce4e72edc3d6a4e32ec25038e.so
		1 
		1 
		1 
		50000 
		1 
	Running Simulation
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa55e60c> t= 495.0 ms
	Time for Simulation:  0.0482721328735
	Time for Extracting Data: (1 records) 0.0148410797119
	Simulation Time Elapsed:  0.249479055405
	Suceeded
	['name', 'simulation']
	['name', 'simulation']
	Loading Channel Type: NaChannel
	Reading JSON: {"mf":{"role":"TRANSMEMBRANECURRENT"}}
	Reading JSON: {"mf":{"role":"MEMBRANEVOLTAGE"}}
	Reading JSON: {"mf":{"role":"TEMPERATURE"}}
	CHECKING
	<neurounits.ast.astobjects.Parameter object at 0xb18da0c>
	VREV
	iii 1.0 kg*m**2/(s**3*A) <class 'quantities.quantity.Quantity'>
	iiii 0.05 kg*m**2/(s**3*A) <class 'quantities.quantity.Quantity'>
	OK
	
	CHECKING
	<neurounits.ast.astobjects.Parameter object at 0xb1402cc>
	GMAX
	iii 1.0 s**3*A**2/(kg*m**4) <class 'quantities.quantity.Quantity'>
	iiii 1200.0 s**3*A**2/(kg*m**4) <class 'quantities.quantity.Quantity'>
	OK
	
	g <class 'neurounits.ast.astobjects.AssignedVariable'>
	V <class 'neurounits.ast.astobjects.SuppliedValue'>
	VREV <class 'neurounits.ast.astobjects.Parameter'>
	T [<class 'neurounits.ast.astobjects.DivOp'>]
	V <class 'neurounits.ast.astobjects.SuppliedValue'>
	m_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
	m_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
	m_beta <class 'neurounits.ast.astobjects.AssignedVariable'>
	h_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
	h_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
	h_beta <class 'neurounits.ast.astobjects.AssignedVariable'>
	GMAX <class 'neurounits.ast.astobjects.Parameter'>
	GATEPROP <class 'neurounits.ast.astobjects.AssignedVariable'>
	T [<class 'neurounits.ast.astobjects.DivOp'>]
	V <class 'neurounits.ast.astobjects.SuppliedValue'>
	V <class 'neurounits.ast.astobjects.SuppliedValue'>
	T [<class 'neurounits.ast.astobjects.MulOp'>]
	V <class 'neurounits.ast.astobjects.SuppliedValue'>
	h <class 'neurounits.ast.astobjects.StateVariable'>
	m <class 'neurounits.ast.astobjects.StateVariable'>
	m <class 'neurounits.ast.astobjects.StateVariable'>
	m <class 'neurounits.ast.astobjects.StateVariable'>
	h_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
	h_beta <class 'neurounits.ast.astobjects.AssignedVariable'>
	m_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
	m_beta <class 'neurounits.ast.astobjects.AssignedVariable'>
	T [<class 'neurounits.ast.astobjects.DivOp'>]
	V <class 'neurounits.ast.astobjects.SuppliedValue'>
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xb149b0c>, <neurounits.ast.astobjects.AssignedVariable object at 0xb149dec>])
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xb149b0c>, <neurounits.ast.astobjects.AssignedVariable object at 0xb149dec>])
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xb146d2c>, <neurounits.ast.astobjects.AssignedVariable object at 0xb19a0ec>])
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xb146d2c>, <neurounits.ast.astobjects.AssignedVariable object at 0xb19a0ec>])
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
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xb183d0c>, <neurounits.ast.astobjects.AssignedVariable object at 0xb183d6c>])
	h_inf <class 'neurounits.ast.astobjects.AssignedVariable'>
	h <class 'neurounits.ast.astobjects.StateVariable'>
	h_tau <class 'neurounits.ast.astobjects.AssignedVariable'>
	m_inf <class 'neurounits.ast.astobjects.AssignedVariable'>
	m <class 'neurounits.ast.astobjects.StateVariable'>
	m_tau <class 'neurounits.ast.astobjects.AssignedVariable'>
	Loading Channel Type: KConductance
	['name', 'simulation']
	Loading Channel Type: NaChannel
	Loading Channel Type: KConductance
	['name', 'simulation']
	Reading JSON: {"mf":{"role":"TRANSMEMBRANECURRENT"}}
	Reading JSON: {"mf":{"role":"MEMBRANEVOLTAGE"}}
	CHECKING
	<neurounits.ast.astobjects.Parameter object at 0xb18216c>
	g
	iii 1.0 s**3*A**2/(kg*m**4) <class 'quantities.quantity.Quantity'>
	iiii 1200.0 s**3*A**2/(kg*m**4) <class 'quantities.quantity.Quantity'>
	OK
	
	m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	m_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	h_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	h_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	h_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	g <class 'neurounits.ast.astobjects.Parameter'>
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	m <class 'neurounits.ast.astobjects.StateVariable'>
	h <class 'neurounits.ast.astobjects.StateVariable'>
	h_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	h_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	m_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xb33fe2c>, <neurounits.ast.astobjects.AssignedVariable object at 0xb33f0cc>])
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xb33fe2c>, <neurounits.ast.astobjects.AssignedVariable object at 0xb33f0cc>])
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xb33ff8c>, <neurounits.ast.astobjects.AssignedVariable object at 0xb33f4ec>])
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xb33ff8c>, <neurounits.ast.astobjects.AssignedVariable object at 0xb33f4ec>])
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
	minf <class 'neurounits.ast.astobjects.AssignedVariable'>
	m <class 'neurounits.ast.astobjects.StateVariable'>
	mtau <class 'neurounits.ast.astobjects.AssignedVariable'>
	hinf <class 'neurounits.ast.astobjects.AssignedVariable'>
	h <class 'neurounits.ast.astobjects.StateVariable'>
	htau <class 'neurounits.ast.astobjects.AssignedVariable'>
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
	Reading JSON: {"mf":{"role":"TRANSMEMBRANECURRENT"}}
	Reading JSON: {"mf":{"role":"MEMBRANEVOLTAGE"}}
	T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.as2012-07-15 16:22:07,097 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 16:22:07,097 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/57/57bc2e28f6fe6de86999781e352ad7ed.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'SomaVoltage'}
	Executing: /opt/nrn/i686/bin/modlunit /home/michael/old_home/mftmp/tmp_bbefa8032bf31fa5452bfc7f83a7d671.mod
	/mnt/sdb5/home/michael/mftmp/modbuild_2081
	Executing: /opt/nrn/i686/bin/nocmodl tmp_bbefa8032bf31fa5452bfc7f83a7d671.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/i686/lib"    -g -O2 -c -o tmp_bbefa8032bf31fa5452bfc7f83a7d671.lo tmp_bbefa8032bf31fa5452bfc7f83a7d671.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_bbefa8032bf31fa5452bfc7f83a7d671.la  -rpath /opt/nrn/i686/libs  tmp_bbefa8032bf31fa5452bfc7f83a7d671.lo  -L/opt/nrn/i686/lib -L/opt/nrn/i686/lib  /opt/nrn/i686/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/opt/nrn/include/nrn -I/opt/nrn/i686/lib -g -O2 -c tmp_bbefa8032bf31fa5452bfc7f83a7d671.c  -fPIC -DPIC -o .libs/tmp_bbefa8032bf31fa5452bfc7f83a7d671.o
	
	OP2: libtool: link: gcc -shared  .libs/tmp_bbefa8032bf31fa5452bfc7f83a7d671.o   -Wl,-rpath -Wl,/opt/nrn/i686/lib -Wl,-rpath -Wl,/opt/nrn/i686/lib -L/opt/nrn/i686/lib /opt/nrn/i686/lib/libnrniv.so /opt/nrn/i686/lib/libnrnoc.so /opt/nrn/i686/lib/liboc.so /opt/nrn/i686/lib/libmemacs.so /opt/nrn/i686/lib/libnrnmpi.so /opt/nrn/i686/lib/libscopmath.so /opt/nrn/i686/lib/libsparse13.so -lreadline -lncurses /opt/nrn/i686/lib/libivoc.so /opt/nrn/i686/lib/libneuron_gnu.so /opt/nrn/i686/lib/libmeschach.so /opt/nrn/i686/lib/libsundials.so -lm -ldl    -pthread -Wl,-soname -Wl,tmp_bbefa8032bf31fa5452bfc7f83a7d671.so.0 -o .libs/tmp_bbefa8032bf31fa5452bfc7f83a7d671.so.0.0.0
	libtool: link: (cd ".libs" && rm -f "tmp_bbefa8032bf31fa5452bfc7f83a7d671.so.0" && ln -s "tmp_bbefa8032bf31fa5452bfc7f83a7d671.so.0.0.0" "tmp_bbefa8032bf31fa5452bfc7f83a7d671.so.0")
	libtool: link: (cd ".libs" && rm -f "tmp_bbefa8032bf31fa5452bfc7f83a7d671.so" && ln -s "tmp_bbefa8032bf31fa5452bfc7f83a7d671.so.0.0.0" "tmp_bbefa8032bf31fa5452bfc7f83a7d671.so")
	libtool: link: ( cd ".libs" && rm -f "tmp_bbefa8032bf31fa5452bfc7f83a7d671.la" && ln -s "../tmp_bbefa8032bf31fa5452bfc7f83a7d671.la" "tmp_bbefa8032bf31fa5452bfc7f83a7d671.la" )
	
	Executing: /opt/nrn/i686/bin/modlunit /home/michael/old_home/mftmp/tmp_93aba50cdaa2c963a67d5c47b385a8dc.mod
	/mnt/sdb5/home/michael/mftmp/modbuild_2081
	Executing: /opt/nrn/i686/bin/nocmodl tmp_93aba50cdaa2c963a67d5c47b385a8dc.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/i686/lib"    -g -O2 -c -o tmp_93aba50cdaa2c963a67d5c47b385a8dc.lo tmp_93aba50cdaa2c963a67d5c47b385a8dc.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_93aba50cdaa2c963a67d5c47b385a8dc.la  -rpath /opt/nrn/i686/libs  tmp_93aba50cdaa2c963a67d5c47b385a8dc.lo  -L/opt/nrn/i686/lib -L/opt/nrn/i686/lib  /opt/nrn/i686/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/opt/nrn/include/nrn -I/opt/nrn/i686/lib -g -O2 -c tmp_93aba50cdaa2c963a67d5c47b385a8dc.c  -fPIC -DPIC -o .libs/tmp_93aba50cdaa2c963a67d5c47b385a8dc.o
	
	OP2: libtool: link: gcc -shared  .libs/tmp_93aba50cdaa2c963a67d5c47b385a8dc.o   -Wl,-rpath -Wl,/opt/nrn/i686/lib -Wl,-rpath -Wl,/opt/nrn/i686/lib -L/opt/nrn/i686/lib /opt/nrn/i686/lib/libnrniv.so /opt/nrn/i686/lib/libnrnoc.so /opt/nrn/i686/lib/liboc.so /opt/nrn/i686/lib/libmemacs.so /opt/nrn/i686/lib/libnrnmpi.so /opt/nrn/i686/lib/libscopmath.so /opt/nrn/i686/lib/libsparse13.so -lreadline -lncurses /opt/nrn/i686/lib/libivoc.so /opt/nrn/i686/lib/libneuron_gnu.so /opt/nrn/i686/lib/libmeschach.so /opt/nrn/i686/lib/libsundials.so -lm -ldl    -pthread -Wl,-sonNEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	ame -Wl,tmp_93aba50cdaa2c963a67d5c47b385a8dc.so.0 -o .libs/tmp_93aba50cdaa2c963a67d5c47b385a8dc.so.0.0.0
	libtool: link: (cd ".libs" && rm -f "tmp_93aba50cdaa2c963a67d5c47b385a8dc.so.0" && ln -s "tmp_93aba50cdaa2c963a67d5c47b385a8dc.so.0.0.0" "tmp_93aba50cdaa2c963a67d5c47b385a8dc.so.0")
	libtool: link: (cd ".libs" && rm -f "tmp_93aba50cdaa2c963a67d5c47b385a8dc.so" && ln -s "tmp_93aba50cdaa2c963a67d5c47b385a8dc.so.0.0.0" "tmp_93aba50cdaa2c963a67d5c47b385a8dc.so")
	libtool: link: ( cd ".libs" && rm -f "tmp_93aba50cdaa2c963a67d5c47b385a8dc.la" && ln -s "../tmp_93aba50cdaa2c963a67d5c47b385a8dc.la" "tmp_93aba50cdaa2c963a67d5c47b385a8dc.la" )
	
	Time for Building Mod-Files:  1.18869113922
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_94ba4a90fa3b0d26f840892caf229c9b.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_7e1b2d96b76f63ca29b09c7fa3dbd568.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_0101db8482f49353d63063a9b1f83197.so
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
	Running Simulation
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9fd71ec> t= 495.0 ms
	Time for Simulation:  0.0450081825256
	Time for Extracting Data: (7 records) 0.0168869495392
	Simulation Time Elapsed:  1.38690781593
	Suceeded
	tobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	n_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	n <class 'neurounits.ast.astobjects.StateVariable'>
	n <class 'neurounits.ast.astobjects.StateVariable'>
	n <class 'neurounits.ast.astobjects.StateVariable'>
	n <class 'neurounits.ast.astobjects.StateVariable'>
	T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	n_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xb24668c>, <neurounits.ast.astobjects.AssignedVariable object at 0xb18dfec>])
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xb24668c>, <neurounits.ast.astobjects.AssignedVariable object at 0xb18dfec>])
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
	a1 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	a2 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	V <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	a3 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	T [<class 'neurounits.ast.astobjects.DivOp'>]
	V <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	a4 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	a5 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	['name', 'simulation']
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xb042a8c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xb05010c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xb05038c>
	Saving File _output/figures/assorted_10compareHHChls/eps/fig000_Autosave_figure_1.eps
	Saving File _output/figures/assorted_10compareHHChls/pdf/fig000_Autosave_figure_1.pdf
	Saving File _output/figures/assorted_10compareHHChls/png/fig000_Autosave_figure_1.png
	Saving File _output/figures/assorted_10compareHHChls/svg/fig000_Autosave_figure_1.svg
	




