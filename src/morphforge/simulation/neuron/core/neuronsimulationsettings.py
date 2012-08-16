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


class NeuronSimulationSettings(object):

    dt = 'dt'
    tstop = 'tstop'
    cvode = 'cvode'
    allparams = (dt, tstop, cvode)

    @classmethod
    def get_defaults(cls):
        defs = {NeuronSimulationSettings.dt: unit('0.01:ms'),
                NeuronSimulationSettings.tstop: unit('500:ms'),
                NeuronSimulationSettings.cvode: True}

        # Check we have defaults for all parameters:
        for p in NeuronSimulationSettings.allparams:
            assert p in defs

        return defs



    def __init__(self, **kwargs):
        self.params = NeuronSimulationSettings.get_defaults()

        for kw in kwargs:
            assert kw in self.params
            self.params[kw] = kwargs[kw]
            print 'Over-riding parameter: %s to %s' % 
                    (str(kw), str(self.params[kw]))

    def __getitem__(self, key):
        return self.params[key]
