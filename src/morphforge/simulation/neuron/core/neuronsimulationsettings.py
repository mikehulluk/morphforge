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

from morphforge.core.quantities import unit


class NEURONSimulationSettings(object):

    dt = 'dt'
    tstop = 'tstop'
    cvode = 'cvode'
    allparams = (dt, tstop, cvode)

    @classmethod
    def get_defaults(cls):
        defs = {NEURONSimulationSettings.dt: unit('0.01:ms'),
                NEURONSimulationSettings.tstop: unit('500:ms'),
                NEURONSimulationSettings.cvode: True}

        # Check we have defaults for all parameters:
        for parameter in NEURONSimulationSettings.allparams:
            assert parameter in defs

        return defs

    def __init__(self, **kwargs):
        self.params = NEURONSimulationSettings.get_defaults()

        for key in kwargs:
            assert key in self.params
            self.params[key] = kwargs[key]
            print 'Over-riding parameter: %s to %s' % (str(key),
                    str(self.params[key]))

    def __getitem__(self, key):
        return self.params[key]


