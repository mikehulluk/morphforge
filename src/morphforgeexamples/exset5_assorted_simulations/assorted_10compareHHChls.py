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
when we create these channels with parameters as an StdChlAlphaBeta.

In you are not familiar with python, then this is an example of the one of
the advantages of the laanguage: functions are objects!

In "test_neuron", we create a neuron morphology, but put the code to add the channels
in a different function. This makes it easy to try out different channel types and
distributions easily and quickly.

"""


from morphforgecontrib.simulation.membranemechanisms.neuroml_via_neurounits.neuroml_via_neurounits_core import NeuroML_Via_NeuroUnits_Channel
from morphforgecontrib.simulation.membranemechanisms.neurounits.neuro_units_bridge import Neuron_NeuroUnitEqnsetMechanism

from morphforge.stdimports import *
from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmleak import StdChlLeak
from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmalphabeta import StdChlAlphaBeta
from morphforgecontrib.simulation.membranemechanisms.simulatorbuiltin.sim_builtin_core import BuiltinChannel
from morphforgecontrib.simulation.membranemechanisms.neuroml_via_xsl.neuroml_via_xsl_core import NeuroML_Via_XSL_Channel

import random as R


variables = ['h', 'm', 'minf', 'mtau', 'm_alpha_rate', 'm_beta_rate']

def apply_hh_chls_neurounits_direct(env, cell, sim):

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
        StdFormAB(V, a1, a2, a3, a4, a5) = (a1 + a2*V)/(a3+exp((V+a4)/a5))
        m_alpha_rate = StdFormAB(V=v, a1=m_a1, a2=m_a2, a3=m_a3, a4=m_a4, a5=m_a5)
        m_beta_rate =  StdFormAB(V=v, a1=m_b1, a2=m_b2, a3=m_b3, a4=m_b4, a5=m_b5)
        h_alpha_rate = StdFormAB(V=v, a1=h_a1, a2=h_a2, a3=h_a3, a4=h_a4, a5=h_a5)
        h_beta_rate =  StdFormAB(V=v, a1=h_b1, a2=h_b2, a3=h_b3, a4=h_b4, a5=h_b5)
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
        StdFormAB(V, a1, a2, a3, a4, a5) = (a1 + a2*V)/(a3+exp((V+a4)/a5))
        n_alpha_rate = StdFormAB(V=v, a1=n_a1, a2=n_a2, a3=n_a3, a4=n_a4, a5=n_a5)
        n_beta_rate =  StdFormAB(V=v, a1=n_b1, a2=n_b2, a3=n_b3, a4=n_b4, a5=n_b5)

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


    na_chl = Neuron_NeuroUnitEqnsetMechanism(name="Chl1", eqnset=eqnset_txt_na, default_parameters={"g":unit("120:mS/cm2")}, )
    lk_chl = Neuron_NeuroUnitEqnsetMechanism(name="Chl2", eqnset=eqnset_txt_lk, )
    k_chl  = Neuron_NeuroUnitEqnsetMechanism(name="Chl3", eqnset=eqnset_txt_k,  )


    cell.apply_channel( na_chl)
    cell.apply_channel( lk_chl)
    cell.apply_channel( k_chl)


    sim.record(na_chl, what='m', cell_location= cell.soma, user_tags=[StandardTags.StateVariable])
    sim.record(na_chl, what='mtau', cell_location= cell.soma, user_tags=[StandardTags.StateTimeConstant])

    sim.record(na_chl, what='h', cell_location= cell.soma, user_tags=[StandardTags.StateVariable])
    sim.record(na_chl, what='htau', cell_location= cell.soma, user_tags=[StandardTags.StateTimeConstant])

    sim.record(k_chl, what='n', cell_location= cell.soma, user_tags=[StandardTags.StateVariable])
    sim.record(k_chl, what='ntau', cell_location= cell.soma, user_tags=[StandardTags.StateTimeConstant])




def apply_hh_chls_neuroml_xsl(env, cell, sim):



    lk_chl = env.Channel(
                         StdChlLeak,
                         name="LkChl",
                         conductance=unit("0.3:mS/cm2"),
                         reversalpotential=unit("-54.3:mV"),
                           )

    na_chl = env.Channel(NeuroML_Via_XSL_Channel,
                                            xml_filename = "/home/michael/srcs/neuroml/CommandLineUtils/ChannelMLConverter/NaChannel_HH.xml",
                                            xsl_filename = "/home/michael/srcs/neuroml/CommandLineUtils/ChannelMLConverter/ChannelML_v1.8.1_NEURONmod.xsl",
                                            
                                           )

    k_chl = env.Channel(NeuroML_Via_XSL_Channel,
                                            xml_filename = "/home/michael/srcs/neuroml/CommandLineUtils/ChannelMLConverter/KChannel_HH.xml",
                                            xsl_filename = "/home/michael/srcs/neuroml/CommandLineUtils/ChannelMLConverter/ChannelML_v1.8.1_NEURONmod.xsl",
                                            
                                           )

    cell.apply_channel( na_chl)
    cell.apply_channel( lk_chl)
    cell.apply_channel( k_chl)








def apply_hh_chls_neuroml_neurounits(env, cell, sim):



    lk_chl = env.Channel(
                         StdChlLeak,
                         name="LkChl",
                         conductance=unit("0.3:mS/cm2"),
                         reversalpotential=unit("-54.3:mV"),
                           )

    na_chl = env.Channel(NeuroML_Via_NeuroUnits_Channel,
                                            xml_filename = "/home/michael/srcs/neuroml/CommandLineUtils/ChannelMLConverter/NaChannel_HH.xml",
                                            #xsl_filename = "/home/michael/srcs/neuroml/CommandLineUtils/ChannelMLConverter/ChannelML_v1.8.1_NEURONmod.xsl",
                                            
                                           )

    k_chl = env.Channel(NeuroML_Via_XSL_Channel,
    #k_chl = env.Channel(NeuroML_Via_NeuroUnits_Channel,
                                            xml_filename = "/home/michael/srcs/neuroml/CommandLineUtils/ChannelMLConverter/KChannel_HH.xml",
                                            xsl_filename = "/home/michael/srcs/neuroml/CommandLineUtils/ChannelMLConverter/ChannelML_v1.8.1_NEURONmod.xsl",
                                            
                                           )

    cell.apply_channel( na_chl)
    cell.apply_channel( lk_chl)
    cell.apply_channel( k_chl)


    #for v in variables:
    #    s =NEURONChl_NeuroUnits_GenRecord(chl=na_chl, modvar=v, name=v, cell_location=cell.soma)
    #    sim.add_recordable(s)



def apply_hh_chls_morphforge_format(env, cell, sim):

    lk_chl = env.Channel(
                             StdChlLeak,
                             name="LkChl",
                             conductance=unit("0.3:mS/cm2"),
                             reversalpotential=unit("-54.3:mV"),
                           )

    na_state_vars = { "m": {
                          "alpha":[-4.00, -0.10, -1.00, 40.00, -10.00],
                          "beta": [4.00, 0.00, 0.00, 65.00, 18.00]},
                    "h": {
                            "alpha":[0.07, 0.00, 0.00, 65.00, 20.00] ,
                            "beta": [1.00, 0.00, 1.00, 35.00, -10.00]}
                      }

    na_chl = env.Channel(
                            StdChlAlphaBeta,
                            name="NaChl", ion="na",
                            equation="m*m*m*h",
                            conductance=unit("120:mS/cm2"),
                            reversalpotential=unit("50:mV"),
                            statevars=na_state_vars,
                            
                           )
    k_state_vars = { "n": {
                          "alpha":[-0.55, -0.01, -1.0, 55.0, -10.0],
                          "beta": [0.125, 0, 0, 65, 80]},
                       }

    k_chl = env.Channel(
                            StdChlAlphaBeta,
                            name="KChl", ion="k",
                            equation="n*n*n*n",
                            conductance=unit("36:mS/cm2"),
                            reversalpotential=unit("-77:mV"),
                            statevars=k_state_vars,
                            
                           )

    cell.apply_channel( lk_chl)
    cell.apply_channel( na_chl)
    cell.apply_channel( k_chl)




def apply_hh_chls_NEURON_builtin(env, cell, sim):

    hhChls = env.Channel(BuiltinChannel,  sim_chl_name="hh", )
    cell.apply_channel( hhChls)






def simulate_chls_on_neuron(chl_applicator_functor):
    # Create the environment:
    env = NEURONEnvironment()

    # Create the simulation:
    sim = env.Simulation()

    # Create a cell:
    morphDict1 = {'root': {'length': 18.8, 'diam': 18.8, 'id':'soma'} }
    m1 = MorphologyTree.fromDictionary(morphDict1)
    cell = sim.create_cell(name="Cell1", morphology=m1)

    # Setup the HH-channels on the cell:
    chl_applicator_functor(env, cell, sim)

    # Setup passive channels:
    apply_passive_everywhere_uniform(cell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2'))



    # Create the stimulus and record the injected current:
    cc = sim.create_currentclamp(name="Stim1", amp=unit("100:pA"), dur=unit("100:ms"), delay=unit("100:ms") * R.uniform(0.95, 1.0), cell_location=cell.soma)


    # Define what to record:
    sim.record(cell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = cell.soma)


    # run the simulation
    results = sim.run()
    return results





resultsA =None
resultsB =None
resultsC =None
resultsD =None
resultsE =None


resultsA = simulate_chls_on_neuron(apply_hh_chls_morphforge_format)
resultsB = simulate_chls_on_neuron(apply_hh_chls_NEURON_builtin)
resultsC = simulate_chls_on_neuron(apply_hh_chls_neuroml_neurounits)
resultsD = simulate_chls_on_neuron(apply_hh_chls_neuroml_xsl)
resultsE = simulate_chls_on_neuron(apply_hh_chls_neurounits_direct)
#
trs = [resultsA, resultsB, resultsC, resultsD, resultsE]
trs = [tr for tr in trs if tr is not None]
TagViewer(trs, timerange=(95, 200)*pq.ms, show=True)


pylab.show()
