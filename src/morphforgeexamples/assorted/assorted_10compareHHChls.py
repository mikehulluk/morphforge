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



"""Comparing simulations: the Hodgkin-Huxley '52 channels

This simulation compares the different ways of implementing the Hodgkin-Huxley channels;
we check that the Hodgkin-Huxley channels built-in to NEURON produce the same results as
when we create these channels with parameters as an MM_AlphaBetaChannel.

In you are not familiar with python, then this is an example of the one of
the advantages of the laanguage: functions are objects!

In "test_neuron", we create a neuron morphology, but put the code to add the channels
in a different function. This makes it easy to try out different channel types and
distributions easily and quickly.

"""


from morphforgecontrib.simulation.membranemechanisms.neuroml_via_neurounits.neuroml_via_neurounits_core import NeuroML_Via_NeuroUnits_Channel
#from morphforgecontrib.simulation.membranemechanisms.neuroml_via_neurounits.neuroml_via_neurounits_neuron import MM_Neuron_NeuroUnits_GenRecord
#from neurounits.neurounitparser import NeuroUnitParser
#from morphforgecontrib.simulation.membranemechanisms.exisitingmodfile.core import SimulatorSpecificChannel
#from morphforgecontrib.simulation.membranemechanisms.exisitingmodfile.neuron import MM_Neuron_SimulatorSpecificChannel
#from neurounits.tools.nmodl import WriteToNMODL
from morphforgecontrib.simulation.membranemechanisms.neurounits.neuro_units_bridge import Neuron_NeuroUnitEqnsetMechanism
from morphforge.constants.stdrecordables import StdRec

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


    mySim.record(naChls, what='m', cell_location= myCell.get_location("soma"), user_tags=[StdRec.StateVariable] )
    mySim.record(naChls, what='mtau', cell_location= myCell.get_location("soma"), user_tags=[StdRec.StateVarTimeConstant] )

    mySim.record(naChls, what='h', cell_location= myCell.get_location("soma"), user_tags=[StdRec.StateVariable] )
    mySim.record(naChls, what='htau', cell_location= myCell.get_location("soma"), user_tags=[StdRec.StateVarTimeConstant] )

    mySim.record(kChls, what='n', cell_location= myCell.get_location("soma"), user_tags=[StdRec.StateVariable] )
    mySim.record(kChls, what='ntau', cell_location= myCell.get_location("soma"), user_tags=[StdRec.StateVarTimeConstant] )




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
    #    s =MM_Neuron_NeuroUnits_GenRecord(chl=sodiumChannels, modvar=v, name=v, where=myCell.get_location("soma"))
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
    mySim.record( myCell, what=StdRec.MembraneVoltage, name="SomaVoltage", cell_location = somaLoc )


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


