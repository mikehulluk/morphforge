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

""" 2 cells connected with an AMPA synapse.

Timed input into a cell causes an action potential, which causes an EPSP in
another cell via an excitatry synapse.

"""

from neurounits import NeuroUnitParser

from morphforgecontrib.simulation.synapses.core.presynaptic_mechanisms import PreSynapticMech_TimeList
from morphforgecontrib.simulation.synapses.core.presynaptic_mechanisms import PreSynapticMech_VoltageThreshold
from morphforgecontrib.simulation.synapses_neurounit import NeuroUnitEqnsetPostSynaptic


from morphforge.stdimports import *
from morphforgecontrib.simulation.membranemechanisms.simulatorbuiltin.sim_builtin_core import BuiltinChannel

def simulate_chls_on_neuron():
    # Create the environment:
    env = NEURONEnvironment()

    # Create the simulation:
    sim = env.Simulation()

    # Create a cell:
    morphDict1 = {'root': {'length': 18.8, 'diam': 18.8, 'id':'soma'} }
    m1 = MorphologyTree.fromDictionary(morphDict1)
    cell1 = sim.create_cell(name="Cell1", morphology=m1)
    apply_mechanism_everywhere_uniform(cell1, env.Channel(BuiltinChannel,  sim_chl_name="hh", mechanism_id="IDB"))
    apply_passive_everywhere_uniform(cell1, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2'))

    m2 = MorphologyTree.fromDictionary(morphDict1)
    cell2 = sim.create_cell(name="Cell2", morphology=m2)
    apply_mechanism_everywhere_uniform(cell2, env.Channel(BuiltinChannel,  sim_chl_name="hh", mechanism_id="IDA"))
    apply_passive_everywhere_uniform(cell2, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2'))

    

    eqnsetfile = "/home/michael/hw_to_come/libs/NeuroUnits/src/test_data/eqnsets/syn_simple.eqn"
    syn = sim.create_synapse(
            presynaptic_mech =  env.PreSynapticMechanism(
                                     PreSynapticMech_TimeList,
                                     time_list =   (100,105,110,112,115, 115,115) * pq.ms ,
                                     weight = unit("1:nS")),
            postsynaptic_mech = env.PostSynapticMechanism(
                                     NeuroUnitEqnsetPostSynaptic,
                                     name = "mYName1",
                                     eqnset = NeuroUnitParser.EqnSet(open(eqnsetfile).read()),
                                     cell_location = cell1.soma
                                    )
           )

    syn = sim.create_synapse(
            presynaptic_mech =  env.PreSynapticMechanism(
                                     PreSynapticMech_VoltageThreshold,
                                     cell_location=cell1.soma,
                                     voltage_threshold=unit("0:mV"),
                                     delay=unit('1:ms'),
                                     weight = unit("1:nS")),
            postsynaptic_mech = env.PostSynapticMechanism(
                                     NeuroUnitEqnsetPostSynaptic,
                                     name = "mYName1",
                                     eqnset = NeuroUnitParser.EqnSet(open(eqnsetfile).read()),
                                     cell_location = cell2.soma
                                    )
           )


    # Define what to record:
    sim.record(what=StandardTags.Voltage, name="SomaVoltage1", cell_location = cell1.soma)
    sim.record(what=StandardTags.Voltage, name="SomaVoltage2", cell_location = cell2.soma)


    # run the simulation
    results = sim.run()
    return results


results = simulate_chls_on_neuron()
TagViewer(results, timerange=(95, 200)*pq.ms, show=True)
#
