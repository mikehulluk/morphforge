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

from morphforge.simulation.neuron.objects.neuronobject import NEURONObject
from morphforge.simulation.neuron.simulationdatacontainers import MHOCSections


class NeuronSimSetupObj(NEURONObject):

    def __init__(self, simsettings, simulation):
        super(NeuronSimSetupObj, self).__init__(
                    name='mneuronbasesetup',
                    simulation=simulation)

        self.simsettings = simsettings

    def build_hoc(self, hocfile_obj):
        hocfile_obj.add_to_section(MHOCSections.InitHeader,
                                   """load_file("noload.hoc")""")

        if self.simsettings['cvode']:
            hocfile_obj.add_to_section( MHOCSections.InitHeader, """cvode_active(1)""")
            #hocfile_obj.add_to_section( MHOCSections.InitHeader, """cvode.atol(1e-12)""")
            #hocfile_obj.add_to_section( MHOCSections.InitHeader, """cvode.rtol(1e-12)""")

        # For testing: should be done properly:
        hocfile_obj.add_to_section(MHOCSections.InitSimParams, """tstop=%s"""%(self.simsettings["tstop"].rescale("ms").magnitude))
        hocfile_obj.add_to_section(MHOCSections.InitSimParams, """dt=%s"""%(self.simsettings["dt"].rescale("ms").magnitude))
        hocfile_obj.add_to_section(MHOCSections.InitRecords, "\n".join(["objref rect", "rect = new Vector()", "rect.record(&t)"]))

    def build_mod(self, modfile_set):
        pass

    def get_recordable(self, what, **kwargs):
        raise NotImplementedError()
