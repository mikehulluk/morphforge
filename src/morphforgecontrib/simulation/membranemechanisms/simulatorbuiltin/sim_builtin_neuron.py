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

import re

from morphforge.simulation.neuron.biophysics.mm_neuron import NEURONChl_Base
from morphforge.simulation.neuron.biophysics.modfile import ModFile
from morphforge.simulation.neuron.core.neuronsimulationenvironment import NEURONEnvironment
from morphforgecontrib.simulation.membranemechanisms.common.neuron import build_hoc_default 
from morphforgecontrib.simulation.membranemechanisms.exisitingmodfile.core import SimulatorSpecificChannel
from morphforgecontrib.simulation.membranemechanisms.simulatorbuiltin.sim_builtin_core import BuiltinChannel





class BuiltinChannelNEURON(NEURONChl_Base, BuiltinChannel):

    def __init__(self, **kwargs):
        # TODO: Make this sub:
        # super(BuiltinChannelNEURON, self).__init__(self, **kwargs)
        #NEURONChl_Base.__init__(self)
        #BuiltinChannel.__init__(self, **kwargs)
        super(BuiltinChannelNEURON, self).__init__(**kwargs)


    def build_hoc_section(self, cell, section, hocfile_obj, mta):
        build_hoc_default(cell=cell, section=section, hocfile_obj=hocfile_obj, mta=mta , units={}, nrnsuffix=self.sim_chl_name)

    def create_modfile(self, modfile_set):
        pass

    # No Internal recording or adjusting of parameters for now:
    class Recordables:

        all = []

    def get_variables(self):
        return []

    def get_defaults(self):
        return {}

    def get_recordable(self, what, **kwargs):
        raise ValueError("Can't find Recordable: %s" % what)


NEURONEnvironment.membranemechanisms.register_plugin(BuiltinChannel, BuiltinChannelNEURON)

