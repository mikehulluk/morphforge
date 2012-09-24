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

from morphforge.simulation.base.networks import PreSynapticTypes


class StdTagFunctors(object):

    @classmethod
    def get_record_functors_synapse(cls):
        return [SynapseInPopulationRecordTags.get_tags]

    @classmethod
    def get_record_functors_neuron(cls):
        return [NeuronInPopulationRecordTags.get_tags]


class UserTagFunctorCellLocation(object):

    pass


class NeuronInPopulationRecordTags(object):

    @classmethod
    def get_tags(cls, neuron, neuron_population, cell_location):
        tags = []

        if cell_location.section.idtag:
            tags.append('SECTION:%s' % cell_location.section.idtag)

        tags.append(neuron.name)
        tags.append(neuron_population.pop_name)
        return tags


class SynapseInPopulationRecordTags(object):

    @classmethod
    def get_tags(cls, synapse, synapse_population):

        tags = []

        # Presynaptic Cell Tagging:
        if synapse.get_presynaptic_mechanism().get_type() == PreSynapticTypes.Cell:
            tags.append('PRECELL:%s' % synapse.get_presynaptic_cell().name)
            if synapse.get_presynaptic_cell().population is not None:
                tags.append('PREPOP:%s'
                            % synapse.get_presynaptic_cell().population.pop_name)
        else:
            tags.append('FIXEDTIMETRIGGER')

        # Post Synaptic Cell Tagging:
        tags.append('POSTCELL:%s'
                    % synapse.get_postsynaptic_cell().name)

        if synapse.get_postsynaptic_cell().population:
            tags.append('POSTPOP:%s'
                        % synapse.get_postsynaptic_cell().population.pop_name)

        tags.append(synapse.name)
        tags.append(synapse_population.synapse_pop_name)

        return tags
