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

from morphforge.core import PluginDict
from morphforge.simulation.base import SimulationEnvironment
from morphforge.simulation.base import CurrentClampStepChange
from morphforge.simulation.base import VoltageClampStepChange

from morphforge.simulation.neuron.core import NeuronSimulationSettings
from morphforge.simulation.neuron.networks import NeuronGapJunction
from morphforge.simulation.neuron.core import MNeuronCell
from morphforge.simulation.neuron.core import MNeuronSimulation


class NeuronSimulationEnvironment(SimulationEnvironment):

    def Simulation(self, **kwargs):
        return MNeuronSimulation(environment=self, **kwargs)

    def Cell(self, **kwargs):
        return MNeuronCell(**kwargs)

    def SimulationSettings(self, **kwargs):
        return NeuronSimulationSettings(**kwargs)

    membranemechanisms = PluginDict()
    presynapticmechanisms = PluginDict()
    postsynapticmechanisms = PluginDict()
    currentclamps = PluginDict()
    voltageclamps = PluginDict()

    @classmethod
    def MembraneMechanism(cls, mechanismtype, **kwargs):
        mech = cls.membranemechanisms.get_plugin(mechanismtype)
        return mech(**kwargs)

    @classmethod
    def PreSynapticMechanism(cls, mechanismtype, **kwargs):
        mech = cls.presynapticmechanisms.get_plugin(mechanismtype)
        return mech(**kwargs)

    @classmethod
    def PostSynapticMechanism(cls, mechanismtype, **kwargs):
        mech = cls.postsynapticmechanisms.get_plugin(mechanismtype)
        return mech(**kwargs)

    def CurrentClamp(self, form=CurrentClampStepChange, **kwargs):
        cc = self.currentclamps.get_plugin(form)
        return cc(**kwargs)

    def VoltageClamp(self, form=VoltageClampStepChange, **kwargs):
        vc = self.voltageclamps.get_plugin(form)
        return vc(**kwargs)

    def GapJunction(self, **kwargs):
        return NeuronGapJunction(**kwargs)

    def Synapse(self, **kwargs):
        from morphforge.simulation.neuron.networks import NeuronSynapse
        return NeuronSynapse(**kwargs)


