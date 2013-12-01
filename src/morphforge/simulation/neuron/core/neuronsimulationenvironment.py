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

from morphforge.simulation.neuron.core import NEURONSimulationSettings
from morphforge.simulation.neuron.networks import NEURONGapJunction
from morphforge.simulation.neuron.core import NEURONCell
from morphforge.simulation.neuron.core import NEURONSimulation


class NEURONEnvironment(SimulationEnvironment):

    _env_name = "NEURON"

    def Simulation(self, **kwargs):
        return NEURONSimulation(environment=self, **kwargs)

    def Cell(self, **kwargs):
        return NEURONCell(**kwargs)

    def SimulationSettings(self, **kwargs):
        return NEURONSimulationSettings(**kwargs)

    channels = PluginDict()
    presynapticmechanisms = PluginDict()
    synapse_psm_template_type = PluginDict()
    currentclamps = PluginDict()
    voltageclamps = PluginDict()



    @classmethod
    def Channel(cls, chltype, **kwargs):
        chl = cls.channels.get_plugin(chltype)
        return chl(**kwargs)

    @classmethod
    def SynapticTrigger(cls, triggertype, **kwargs):
        trigger_functor = cls.presynapticmechanisms.get_plugin(triggertype)
        return trigger_functor(**kwargs)

    def PostSynapticMechTemplate(self, psm_type, **kwargs):
        tmpl_functor = self.synapse_psm_template_type.get_plugin(psm_type)
        return tmpl_functor(**kwargs)


    def CurrentClamp(self, protocol=CurrentClampStepChange, **kwargs):
        current_clamp = self.currentclamps.get_plugin(protocol)
        return current_clamp(**kwargs)

    def VoltageClamp(self, protocol=VoltageClampStepChange, **kwargs):
        voltage_clamp = self.voltageclamps.get_plugin(protocol)
        return voltage_clamp(**kwargs)

    def GapJunction(self, **kwargs):
        return NEURONGapJunction(**kwargs)

    def Synapse(self, **kwargs):
        from morphforge.simulation.neuron.networks import NEURONSynapse
        return NEURONSynapse(**kwargs)



