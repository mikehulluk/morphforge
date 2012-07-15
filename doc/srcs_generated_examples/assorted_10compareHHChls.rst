
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

	#!/usr/bin/python
	# -*- coding: utf-8 -*-
	
	# ---------------------------------------------------------------------
	# Copyright (c) 2012 Michael Hull.
	# All rights reserved.
	#
	# Redistribution and use in source and binary forms, with or without
	# modification, are permitted provided that the following conditions
	# are met:
	#
	#  - Redistributions of source code must retain the above copyright 
	#    notice, this list of conditions and the following disclaimer. 
	#  - Redistributions in binary form must reproduce the above copyright 
	#    notice, this list of conditions and the following disclaimer in 
	#    the documentation and/or other materials provided with the 
	#    distribution.
	#
	# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
	# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
	# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR 
	# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT 
	# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
	# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT 
	# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
	# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY 
	# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
	# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
	#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
	# ----------------------------------------------------------------------
	
	
	
	
	
	
	from morphforgecontrib.simulation.membranemechanisms.neuroml_via_neurounits.neuroml_via_neurounits_core import NeuroML_Via_NeuroUnits_Channel
	#from morphforgecontrib.simulation.membranemechanisms.neuroml_via_neurounits.neuroml_via_neurounits_neuron import MM_Neuron_NeuroUnits_GenRecord
	#from neurounits.neurounitparser import NeuroUnitParser
	#from morphforgecontrib.simulation.membranemechanisms.exisitingmodfile.core import SimulatorSpecificChannel
	#from morphforgecontrib.simulation.membranemechanisms.exisitingmodfile.neuron import MM_Neuron_SimulatorSpecificChannel
	#from neurounits.tools.nmodl import WriteToNMODL
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
	
	
	
	
	
	
	
	
	
	#
	#resultsE = simulate_chls_on_neuron( apply_hh_chls_neurounits_direct )
	#TagViewer([resultsE], timeranges=[(95, 200)*pq.ms], show=True )
	#
	#import sys
	#sys.exit(0)
	
	
	
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
	
	import sys
	sys.exit(0)
	
	
	
	import pylab
	
	
	
	
	
	resultsC = simulate_chls_on_neuron( apply_hh_chls_neuroml_neurounits )
	resultsD = simulate_chls_on_neuron( apply_hh_chls_neuroml_xsl )
	resultsE = simulate_chls_on_neuron( apply_hh_chls_neurounits_direct )
	
	
	TagViewer([resultsC,resultsD,resultsE], timeranges=[(95, 200)*pq.ms], show=True )
	#TagViewer([resultsC], timeranges=[(95, 200)*pq.ms], show=True )
	
	
	
	for v in vars:
	    ax = pylab.figure().add_subplot(111)
	    tr = resultsC.get_trace(v)
	    ax.plot( tr._time.magnitude, tr._data.magnitude, label=v )
	    ax.legend()
	#pylab.show()
	
	
	#import sys
	#sys.exit(1)
	
	
	
	TagViewer([resultsC,resultsD], timeranges=[(95, 200)*pq.ms], show=True )
	
	
	
	
	import sys
	sys.exit(1)
	
	
	resultsA = simulate_chls_on_neuron( apply_hh_chls_morphforge_format )
	resultsB = simulate_chls_on_neuron( apply_hh_chls_NEURON_builtin )
	# Display the results:
	TagViewer([resultsA,resultsB,resultsC], timeranges=[(95, 200)*pq.ms], show=True )
	
	
	








Output
~~~~~~

.. code-block:: bash

    	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.math
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.geom
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s2012-07-15 15:57:45,076 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:45,076 - DISABLEDLOGGING - INFO - _run_spawn() [Pickling Sim]
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.math
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.geom
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <cla2012-07-15 15:57:45,749 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:45,750 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	ss 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.neuro
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.physics
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/67/6759cbddebb1ebe9c3417fbd7d9b3779.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'SomaVoltage'}
	Time for Building Mod-Files:  0.000946998596191
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_60c3176ccd39a2716e59acb4aae32c6c.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_e38908b5bc02fc80d5b0e1d97d5b1aa7.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_714554be3b0a5b42eb0b14c97a5be284.so
		1 
		1 
		1 
		50000 
		1 
	Running Simulation
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa0668cc> t= 495.0 ms
	Time for Simulation:  0.0392339229584
	Time for Extracting Data: (1 records) 0.0185830593109
	Simulation Time Elapsed:  0.218359947205
	Suceeded
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.math
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.geom
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <claNEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	ss 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.neuro
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.physics
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/ed/ed62f525466986e2eb61620af86c056e.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'SomaVoltage'}
	Time for Building Mod-Files:  5.00679016113e-06
		1 
		1 
		1 
		50000 
		1 
	Running Simulation
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa3ac8ac> t= 495.0 ms
	2012-07-15 15:57:46,690 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:46,690 - DISABLEDLOGGING - INFO - Simulation Ran OK. Post Processing:
	Time for Simulation:  0.0378789901733
	Time for Extracting Data: (1 records) 0.0142049789429
	Simulation Time Elapsed:  0.152791976929
	Suceeded
	 -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.neuro
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.physics
	['name', 'simulation']
	['name', 'simulation']
	Loading Channel Type: NaChannel
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	Reading JSON: {"mf":{"role":"TRANSMEMBRANECURRENT"}}
	Reading JSON: {"mf":{"role":"MEMBRANEVOLTAGE"}}
	Reading JSON: {"mf":{"role":"TEMPERATURE"}}
	<MMUnit: (10e0) m -4 kg -1 s 3 A 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) K 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -4 kg -1 s 3 A 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -4 kg -1 s 3 A 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	CHECKING
	<neurounits.ast.astobjects.Parameter object at 0xa69074c>
	VREV
	iii 1.0 kg*m**2/(s**3*A) <class 'quantities.quantity.Quantity'>
	iiii 0.05 kg*m**2/(s**3*A) <class 'quantities.quantity.Quantity'>
	OK
	
	CHECKING
	<neurounits.ast.astobjects.Parameter object at 0xa692c6c>
	GMAX
	iii 1.0 s**3*A**2/(kg*m**4) <class 'quantities.quantity.Quantity'>
	iiii 1200.0 s**3*A**2/(kg*m**4) <class 'quantities.quantity.Quantity'>
	OK
	
	T [<class 'neurounits.ast.astobjects.DivOp'>]
	V <class 'neurounits.ast.astobjects.SuppliedValue'>
	h_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
	h_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
	h_beta <class 'neurounits.ast.astobjects.AssignedVariable'>
	m <class 'neurounits.ast.astobjects.StateVariable'>
	m <class 'neurounits.ast.astobjects.StateVariable'>
	m <class 'neurounits.ast.astobjects.StateVariable'>
	h <class 'neurounits.ast.astobjects.StateVariable'>
	m_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
	m_beta <class 'neurounits.ast.astobjects.AssignedVariable'>
	T [<class 'neurounits.ast.astobjects.DivOp'>]
	V <class 'neurounits.ast.astobjects.SuppliedValue'>
	GMAX <class 'neurounits.ast.astobjects.Parameter'>
	GATEPROP <class 'neurounits.ast.astobjects.AssignedVariable'>
	V <class 'neurounits.ast.astobjects.SuppliedValue'>
	T [<class 'neurounits.ast.astobjects.MulOp'>]
	V <class 'neurounits.ast.astobjects.SuppliedValue'>
	h_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
	h_beta <class 'neurounits.ast.astobjects.AssignedVariable'>
	g <class 'neurounits.ast.astobjects.AssignedVariable'>
	V <class 'neurounits.ast.astobjects.SuppliedValue'>
	VREV <class 'neurounits.ast.astobjects.Parameter'>
	m_alpha <class 'neurounits.ast.astobje<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.math
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.geom
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 2012-07-15 15:57:47,591 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:47,591 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.neuro
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.physics
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/8c/8c925284a589522fc85cdef5eb16686b.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'SomaVoltage'}
	Executing: /opt/nrn/i686/bin/modlunit /home/michael/old_home/mftmp/tmp_435bbe1a7a4c8b8db2f609f46cf1b81f.mod
	/mnt/sdb5/home/michael/mftmp/modbuild_30273
	Executing: /opt/nrn/i686/bin/nocmodl tmp_435bbe1a7a4c8b8db2f609f46cf1b81f.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/i686/lib"    -g -O2 -c -o tmp_435bbe1a7a4c8b8db2f609f46cf1b81f.lo tmp_435bbe1a7a4c8b8db2f609f46cf1b81f.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_435bbe1a7a4c8b8db2f609f46cf1b81f.la  -rpath /opt/nrn/i686/libs  tmp_435bbe1a7a4c8b8db2f609f46cf1b81f.lo  -L/opt/nrn/i686/lib -L/opt/nrn/i686/lib  /opt/nrn/i686/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/opt/nrn/include/nrn -I/opt/nrn/i686/lib -g -O2 -c tmp_435bbe1a7a4c8b8db2f609f46cf1b81f.c  -fPIC -DPIC -o .libs/tmp_435bbe1a7a4c8b8db2f609f46cf1b81f.o
	
	OP2: libtool: link: gcc -shared  .libs/tmp_435bbe1a7a4c8b8db2f609f46cf1b81f.o   -Wl,-rpath -Wl,/opt/nrn/i686/lib -Wl,-rpath -Wl,/opt/nrn/i686/lib -L/opt/nrn/i686/lib /opt/nrn/i686/lib/libnrniv.so /opt/nrn/i686/lib/libnrnoc.so /opt/nrn/i686/lib/liboc.so /opt/nrn/i686/lib/libmemacs.so /opt/nrn/i686/lib/libnrnmpi.so /opt/nrn/i686/lib/libscopmath.so /opt/nrn/i686/lib/libsparse13.so -lreadline -lncurses /opt/nrn/i686/lib/libivoc.so /opt/nrn/i686/lib/libneuron_gnu.so /opt/nrn/i686/lib/libmeschach.so /opt/nrn/i686/lib/libsundials.so -lm -ldl    -pthread -Wl,-soname -Wl,tmp_435bbe1a7a4c8b8db2f609f46cf1b81f.so.0 -o .libs/tmp_435bbe1a7a4c8b8db2f609f46cf1b81f.so.0.0.0
	libtool: link: (cd ".libs" && rm -f "tmp_435bbe1a7a4c8b8db2f609f46cf1b81f.so.0" && ln -s "tmp_435bbe1a7a4c8b8db2f609f46cf1b81f.so.0.0.0" "tmp_435bbe1a7a4c8b8db2f609f46cf1b81f.so.0")
	libtool: link: (cd ".libs" && rm -f "tmp_435bbe1a7a4c8b8db2f609f46cf1b81f.so" && ln -s "tmp_435bbe1a7a4c8b8db2f609f46cf1b81f.so.0.0.0" "tmp_435bbe1a7a4c8b8db2f609f46cf1b81f.so")
	libtool: link: ( cd ".libs" && rm -f "tmp_435bbe1a7a4c8b8db2f609f46cf1b81f.la" && ln -s "../tmp_435bbe1a7a4c8b8db2f609f46cf1b81f.la" "tmp_435bbe1a7a4c8b8db2f609f46cf1b81f.la" )
	
	Time for Building Mod-Files:  0.574654817581
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_84d1bd07ca97dcd5fbbd02b9f9e24292.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_1efc531eaf0bae2e49f6a5c8a91797f1.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_47fdb5990ae9776703ab34b5a9ef2fe2.so
		1 
		1 
		1 
		50000 
		1 
	Running Simulation
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xa315c8c> t= 495.0 ms
	Time for Simulation:  0.04168176651
	Time for Extracting Data: (1 records) 0.0147309303284
	Simulation Time Elapsed:  0.823637008667
	Suceeded
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.math
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.geom
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <cla2012-07-15 15:57:49,094 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:49,095 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	ss 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.neuro
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.physics
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/2a/2adf789e31bcfedde4dcaa4ab6497efd.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'SomaVoltage'}
	Time for Building Mod-Files:  0.000787973403931
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_714554be3b0a5b42eb0b14c97a5be284.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_a46bf2f1691a80cf44bb3239e7721133.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_1efc531eaf0bae2e49f6a5c8a91797f1.so
		1 
		1 
		1 
		50000 
		1 
	Running Simulation
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0x9f3d5ec> t= 495.0 ms
	Time for Simulation:  0.0433671474457
	Time for Extracting Data: (1 records) 0.0183081626892
	Simulation Time Elapsed:  0.273189067841
	Suceeded
	cts.AssignedVariable'>
	m_alpha <class 'neurounits.ast.astobjects.AssignedVariable'>
	m_beta <class 'neurounits.ast.astobjects.AssignedVariable'>
	T [<class 'neurounits.ast.astobjects.DivOp'>]
	V <class 'neurounits.ast.astobjects.SuppliedValue'>
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xa64df2c>, <neurounits.ast.astobjects.AssignedVariable object at 0xa69612c>])
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xa64df2c>, <neurounits.ast.astobjects.AssignedVariable object at 0xa69612c>])
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xa65392c>, <neurounits.ast.astobjects.AssignedVariable object at 0xa650cac>])
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xa65392c>, <neurounits.ast.astobjects.AssignedVariable object at 0xa650cac>])
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
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xa69022c>, <neurounits.ast.astobjects.AssignedVariable object at 0xa69004c>])
	m_inf <class 'neurounits.ast.astobjects.AssignedVariable'>
	m <class 'neurounits.ast.astobjects.StateVariable'>
	m_tau <class 'neurounits.ast.astobjects.AssignedVariable'>
	h_inf <class 'neurounits.ast.astobjects.AssignedVariable'>
	h <class 'neurounits.ast.astobjects.StateVariable'>
	h_tau <class 'neurounits.ast.astobjects.AssignedVariable'>
	o1 m <MMUnit: (10e0) >
	o2 m_inf <MMUnit: (10e0) >
	o1 h <MMUnit: (10e0) >
	o2 h_inf <MMUnit: (10e0) >
	0
	Loading Channel Type: KConductance
	['name', 'simulation']
	Loading Channel Type: NaChannel
	Loading Channel Type: KConductance
	['name', 'simulation']
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -4 kg -1 s 3 A 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Reading JSON: {"mf":{"role":"TRANSMEMBRANECURRENT"}}
	Reading JSON: {"mf":{"role":"MEMBRANEVOLTAGE"}}
	<MMUnit: (10e0) m -4 kg -1 s 3 A 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -4 kg -1 s 3 A 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -4 kg -1 s 3 A 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	CHECKING
	<neurounits.ast.astobjects.Parameter object at 0xa69406c>
	g
	iii 1.0 s**3*A**2/(kg*m**4) <class 'quantities.quantity.Quantity'>
	iiii 1200.0 s**3*A**2/(kg*m**4) <class 'quantities.quantity.Quantity'>
	OK
	
	T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	m_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
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
	T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	m_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	m_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xa8495cc>, <neurounits.ast.astobjects.AssignedVariable object at 0xa84956c>])
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xa8495cc>, <neurounits.ast.astobjects.AssignedVariable object at 0xa84956c>])
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xa84906c>, <neurounits.ast.astobjects.AssignedVariable object at 0xa849eec>])
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xa84906c>, <neurounits.ast.astobjects.AssignedVariable object at 0xa849eec>])
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
	a1 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	a2 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	V <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	a3 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	T [<class 'neurounits.ast.astobjects.DivOp'>]
	V <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	a4 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	a5 <class 'neurounits.ast.astobjects.FunctionDefParameter'>
	0
	<MMUnit: (10e0) m -4 kg -1 s 3 A 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Reading JSON: {"mf":{"role":"TRANSMEMBRANECURRENT"}}
	Reading JSON: {"mf":{"role":"MEMBRANEVOLTAGE"}}
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -4 kg -1 s 3 A 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -4 kg -1 s 3 A 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	Deps; set([])
	0
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -4 kg -1 s 3 A 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Reading JSON: {"mf":{"role":"TRANSMEMBRANECURRENT"}}
	Reading JSON: {"mf":{"role":"MEMBRANEVOLTAGE"}}
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -4 kg -1 s 3 A 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -4 kg -1 s 3 A 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	n_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.Symbol<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.math
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.geom
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m -2 kg -1 s 2 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	Searching for library:  std.math
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 3 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 4 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s -1> <cla2012-07-15 15:57:50,319 - morphforge.core.logmgr - INFO - Logger Started OK
	2012-07-15 15:57:50,320 - DISABLEDLOGGING - INFO - Ensuring Modfile is built
	ss 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -3 A -2> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) > <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.neuro
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) m 2 kg 1 s -2 K -1 mol -1> <class 'neurounits.units_backends.mh.MMUnit'>
	<MMUnit: (10e0) s 1 A 1> <class 'neurounits.units_backends.mh.MMUnit'>
	Name std.physics
	Loading Bundle from  /home/michael/old_home/mftmp/simulationresults/1c/1cb87b1a43e0d160af007e39f3289f7f.bundle
	{'sectionpos': 0.5, 'sectionindex': 0, 'cellname': 'cell_Cell1', 'recVecName': 'SomaVoltage'}
	Executing: /opt/nrn/i686/bin/modlunit /home/michael/old_home/mftmp/tmp_00ed65b55e583a1928f884b3267f93ea.mod
	/mnt/sdb5/home/michael/mftmp/modbuild_30441
	Executing: /opt/nrn/i686/bin/nocmodl tmp_00ed65b55e583a1928f884b3267f93ea.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/opt/nrn/include/nrn"  -I"/opt/nrn/i686/lib"    -g -O2 -c -o tmp_00ed65b55e583a1928f884b3267f93ea.lo tmp_00ed65b55e583a1928f884b3267f93ea.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_00ed65b55e583a1928f884b3267f93ea.la  -rpath /opt/nrn/i686/libs  tmp_00ed65b55e583a1928f884b3267f93ea.lo  -L/opt/nrn/i686/lib -L/opt/nrn/i686/lib  /opt/nrn/i686/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/opt/nrn/include/nrn -I/opt/nrn/i686/lib -g -O2 -c tmp_00ed65b55e583a1928f884b3267f93ea.c  -fPIC -DPIC -o .libs/tmp_00ed65b55e583a1928f884b3267f93ea.o
	
	OP2: libtool: link: gcc -shared  .libs/tmp_00ed65b55e583a1928f884b3267f93ea.o   -Wl,-rpath -Wl,/opt/nrn/i686/lib -Wl,-rpath -Wl,/opt/nrn/i686/lib -L/opt/nrn/i686/lib /opt/nrn/i686/lib/libnrniv.so /opt/nrn/i686/lib/libnrnoc.so /opt/nrn/i686/lib/liboc.so /opt/nrn/i686/lib/libmemacs.so /opt/nrn/i686/lib/libnrnmpi.so /opt/nrn/i686/lib/libscopmath.so /opt/nrn/i686/lib/libsparse13.so -lreadline -lncurses /opt/nrn/i686/lib/libivoc.so /opt/nrn/i686/lib/libneuron_gnu.so /opt/nrn/i686/lib/libmeschach.so /opt/nrn/i686/lib/libsundials.so -lm -ldl    -pthread -Wl,-soname -Wl,tmp_00ed65b55e583a1928f884b3267f93ea.so.0 -o .libs/tmp_00ed65b55e583a1928f884b3267f93ea.so.0.0.0
	libtool: link: (cd ".libs" && rm -f "tmp_00ed65b55e583a1928f884b3267f93ea.so.0" && ln -s "tmp_00ed65b55e583a1928f884b3267f93ea.so.0.0.0" "tmp_00ed65b55e583a1928f884b3267f93ea.so.0")
	libtool: link: (cd ".libs" && rm -f "tmp_00ed65b55e583a1928f884b3267f93ea.so" && ln -s "tmp_00ed65b55e583a1928f884b3267f93ea.so.0.0.0" "tmp_00ed65b55e583a1928f884b3267f93ea.so")
	libtool: link: ( cd ".libs" && rm -f "tmp_00ed65b55e583a1928f884b3267f93ea.la" && ln -s "../tmp_00ed65b55e583a1928f884b3267f93ea.la" "tmp_00ed65b55e583a1928f884b3267f93ea.la" )
	
	Executing: /opt/nrn/i686/bin/modlunit /home/michael/old_home/mftmp/tmp_091c5e7bfc2fd34a4f0a40f475588350.mod
	/mnt/sdb5/home/michael/mftmp/modbuild_30441
	Executing: /opt/nrn/i686/bin/nocmodl tmp_091c5e7bfc2fd34a4f0a40f475588350.mod
	Executing: /opt/nrn/share/nrn/libtool --mode=compile gcc -DHAVE_CONFIG_H   -I"."  -I".."  -I"/oNEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
	Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
	See http://www.neuron.yale.edu/credits.html
	
	pt/nrn/include/nrn"  -I"/opt/nrn/i686/lib"    -g -O2 -c -o tmp_091c5e7bfc2fd34a4f0a40f475588350.lo tmp_091c5e7bfc2fd34a4f0a40f475588350.c  
	Executing: /opt/nrn/share/nrn/libtool --mode=link gcc -module  -g -O2  -shared  -o tmp_091c5e7bfc2fd34a4f0a40f475588350.la  -rpath /opt/nrn/i686/libs  tmp_091c5e7bfc2fd34a4f0a40f475588350.lo  -L/opt/nrn/i686/lib -L/opt/nrn/i686/lib  /opt/nrn/i686/lib/libnrniv.la  -lnrnoc -loc -lmemacs -lnrnmpi -lscopmath -lsparse13 -lreadline -lncurses -livoc -lneuron_gnu -lmeschach -lsundials -lm -ldl   
	OP1: libtool: compile:  gcc -DHAVE_CONFIG_H -I. -I.. -I/opt/nrn/include/nrn -I/opt/nrn/i686/lib -g -O2 -c tmp_091c5e7bfc2fd34a4f0a40f475588350.c  -fPIC -DPIC -o .libs/tmp_091c5e7bfc2fd34a4f0a40f475588350.o
	
	OP2: libtool: link: gcc -shared  .libs/tmp_091c5e7bfc2fd34a4f0a40f475588350.o   -Wl,-rpath -Wl,/opt/nrn/i686/lib -Wl,-rpath -Wl,/opt/nrn/i686/lib -L/opt/nrn/i686/lib /opt/nrn/i686/lib/libnrniv.so /opt/nrn/i686/lib/libnrnoc.so /opt/nrn/i686/lib/liboc.so /opt/nrn/i686/lib/libmemacs.so /opt/nrn/i686/lib/libnrnmpi.so /opt/nrn/i686/lib/libscopmath.so /opt/nrn/i686/lib/libsparse13.so -lreadline -lncurses /opt/nrn/i686/lib/libivoc.so /opt/nrn/i686/lib/libneuron_gnu.so /opt/nrn/i686/lib/libmeschach.so /opt/nrn/i686/lib/libsundials.so -lm -ldl    -pthread -Wl,-soname -Wl,tmp_091c5e7bfc2fd34a4f0a40f475588350.so.0 -o .libs/tmp_091c5e7bfc2fd34a4f0a40f475588350.so.0.0.0
	libtool: link: (cd ".libs" && rm -f "tmp_091c5e7bfc2fd34a4f0a40f475588350.so.0" && ln -s "tmp_091c5e7bfc2fd34a4f0a40f475588350.so.0.0.0" "tmp_091c5e7bfc2fd34a4f0a40f475588350.so.0")
	libtool: link: (cd ".libs" && rm -f "tmp_091c5e7bfc2fd34a4f0a40f475588350.so" && ln -s "tmp_091c5e7bfc2fd34a4f0a40f475588350.so.0.0.0" "tmp_091c5e7bfc2fd34a4f0a40f475588350.so")
	libtool: link: ( cd ".libs" && rm -f "tmp_091c5e7bfc2fd34a4f0a40f475588350.la" && ln -s "../tmp_091c5e7bfc2fd34a4f0a40f475588350.la" "tmp_091c5e7bfc2fd34a4f0a40f475588350.la" )
	
	Time for Building Mod-Files:  1.13530111313
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_0612813cb4a4d61a21a5f182a457546c.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_7e1b2d96b76f63ca29b09c7fa3dbd568.so
	loading membrane mechanisms from /home/michael/old_home/mftmp/modout/mod_ecb7e039ce9ae6f8d9f77ef7ef71a16c.so
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
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 0.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 5.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 10.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 15.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 20.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 25.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 30.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 35.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 40.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 45.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 50.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 55.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 60.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 65.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 70.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 75.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 80.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 85.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 90.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 95.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 100.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 105.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 110.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 115.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 120.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 125.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 130.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 135.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 140.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 145.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 150.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 155.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 160.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 165.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 170.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 175.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 180.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 185.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 190.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 195.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 200.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 205.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 210.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 215.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 220.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 225.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 230.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 235.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 240.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 245.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 250.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 255.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 260.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 265.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 270.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 275.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 280.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 285.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 290.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 295.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 300.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 305.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 310.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 315.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 320.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 325.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 330.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 335.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 340.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 345.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 350.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 355.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 360.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 365.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 370.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 375.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 380.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 385.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 390.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 395.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 400.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 405.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 410.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 415.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 420.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 425.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 430.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 435.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 440.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 445.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 450.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 455.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 460.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 465.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 470.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 475.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 480.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 485.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 490.0 ms
	<morphforge.simulation.neuron.core.neuronsimulation.Event object at 0xb5481ec> t= 495.0 ms
	Time for Simulation:  0.0451729297638
	Time for Extracting Data: (7 records) 0.017077922821
	Simulation Time Elapsed:  1.38450098038
	Suceeded
	icConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	n_alpha_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	n_beta_rate <class 'neurounits.ast.astobjects.AssignedVariable'>
	T [<class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SymbolicConstant'>, <class 'neurounits.ast.astobjects.SuppliedValue'>]
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	v <class 'neurounits.ast.astobjects.SuppliedValue'>
	n <class 'neurounits.ast.astobjects.StateVariable'>
	n <class 'neurounits.ast.astobjects.StateVariable'>
	n <class 'neurounits.ast.astobjects.StateVariable'>
	n <class 'neurounits.ast.astobjects.StateVariable'>
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xa740b8c>, <neurounits.ast.astobjects.AssignedVariable object at 0xa740f2c>])
	Deps; set([<neurounits.ast.astobjects.AssignedVariable object at 0xa740b8c>, <neurounits.ast.astobjects.AssignedVariable object at 0xa740f2c>])
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
	0
	['name', 'simulation']
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa54eb2c>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa55a1ac>
	Plotting For PlotSpec: <morphforge.simulationanalysis.tagviewer.plotspecs.PlotSpec_DefaultNew object at 0xa55a42c>
	Saving File _output/figures/assorted_10compareHHChls/eps/fig000_Autosave_figure_1.eps
	Saving File _output/figures/assorted_10compareHHChls/pdf/fig000_Autosave_figure_1.pdf
	Saving File _output/figures/assorted_10compareHHChls/png/fig000_Autosave_figure_1.png
	Saving File _output/figures/assorted_10compareHHChls/svg/fig000_Autosave_figure_1.svg
	




