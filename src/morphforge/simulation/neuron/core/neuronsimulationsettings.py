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

from morphforge.units import qty


class NEURONSimulationSettings(object):

    dt = 'dt'
    tstop = 'tstop'
    cvode = 'cvode'
    reltol = 'reltol'
    abstol = 'abstol'
    strict_modlunit='strict_modlunit'
    allparams = (dt, tstop, cvode, reltol, abstol, strict_modlunit)

    @classmethod
    def get_defaults(cls):
        defs = {NEURONSimulationSettings.dt: qty('0.01:ms'),
                NEURONSimulationSettings.tstop: qty('500:ms'),
                NEURONSimulationSettings.reltol: 0.0,
                NEURONSimulationSettings.abstol: 1e-2,
                #NEURONSimulationSettings.reltol: 1e-12,
                #NEURONSimulationSettings.abstol: 1e-12,
                NEURONSimulationSettings.cvode: True,
                NEURONSimulationSettings.strict_modlunit: True
                }

        # Check we have defaults for all parameters:
        for parameter in NEURONSimulationSettings.allparams:
            assert parameter in defs

        return defs

    def __init__(self, **kwargs):
        self.params = NEURONSimulationSettings.get_defaults()

        for key in kwargs:
            assert key in self.params
            self.params[key] = kwargs[key]

    def __getitem__(self, key):
        return self.params[key]


