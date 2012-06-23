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


from morphforge.core.quantities.fromcore import unit
import copy
from morphforgecontrib.simulation.synapses.core.presynaptic_mechanisms import PreSynapticMech_VoltageThreshold,\
    PreSynapticMech_TimeList

class SynapseParameter(object):
    def __init__(self, synapse_type, **kwargs):
        self.synapse_type = synapse_type
        self.kwargs = kwargs

    def __getitem__(self,k):
        return self.kwargs[k]
    def __setitem__(self,k,v):
        self.kwargs[k] = v











def create_synapse_cell_to_cell( sim, presynaptic, postsynaptic, synapse_parameters, **kwargs ):

    synapse_parameters = copy.copy(synapse_parameters)

    for k,v in kwargs.iteritems():

        print 'Over-Riding Parameter:', k, v
        assert k in synapse_parameters.kwargs
        #assert k in synapse_parameters.kwargs
        synapse_parameters[k] = v


    # Presynaptic properties:
    delay = synapse_parameters['delay']
    threshold = synapse_parameters['vthreshold']
    conductance = synapse_parameters["conductance"]
    multiplier = synapse_parameters["multiplier"]

    #Post synaptic properties:
    t_opening = synapse_parameters["t_opening"]
    t_closing = synapse_parameters["t_closing"]
    erev = synapse_parameters["erev"]
    popening = synapse_parameters['popening']
    vdep = synapse_parameters['vdep']


    env = sim.environment
    syn = sim.create_synapse(
                presynaptic_mech =  env.PreSynapticMechanism(
                                                PreSynapticMech_VoltageThreshold,
                                                celllocation =  presynaptic.get_location('soma'),
                                                voltage_threshold = threshold,
                                                delay=delay,
                                                weight=conductance * multiplier),

                postsynaptic_mech = env.PostSynapticMechanism(
                                                synapse_parameters.synapse_type,
                                                simulation=sim,
                                                celllocation = postsynaptic.get_location('soma'),
                                                tau_open = t_opening,
                                                tau_close=t_closing,
                                                e_rev=erev,
                                                popening=popening,
                                                vdep=vdep),
                            )

    return syn

def create_synapse_times_to_cell( sim, times, postsynaptic, synapse_parameters, **kwargs ):

    # Copy the updates parameters:
    synapse_parameters = copy.copy(synapse_parameters)
    for k,v in kwargs.iteritems():
        print 'Over-Riding Parameter:', k, v
        assert k in synapse_parameters.kwargs
        synapse_parameters[k] = v


    # Presynaptic properties:
    conductance = synapse_parameters["conductance"]
    multiplier = synapse_parameters["multiplier"]

    #Post synaptic properties:
    t_opening = synapse_parameters["t_opening"]
    t_closing = synapse_parameters["t_closing"]
    erev = synapse_parameters["erev"]
    popening = synapse_parameters['popening']
    vdep = synapse_parameters['vdep']

    env = sim.environment
    syn = sim.create_synapse(
                presynaptic_mech =  env.PreSynapticMechanism(
                                                PreSynapticMech_TimeList,
                                                time_list = times,
                                                weight=conductance * multiplier),

                postsynaptic_mech = env.PostSynapticMechanism(
                                                synapse_parameters.synapse_type,
                                                simulation=sim,
                                                celllocation = postsynaptic.get_location('soma'),
                                                tau_open = t_opening,
                                                tau_close=t_closing,
                                                e_rev=erev,
                                                vdep=vdep,
                                                popening=popening  ),
                            )

    return syn

