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
import quantities as pq
from morphforge.simulation.base import Channel


class StdChlCalciumAlphaBetaBeta(Channel):

    class Recordables(object):

        CurrentDensity = 'CurrentDensity'
        StateVar = 'StateVar'
        StateVarSteadyState = 'StateSteaddyState'
        StateVarTimeConstant = 'StateTimeConstant'

        all = [CurrentDensity, StateVar, StateVarSteadyState,
               StateVarTimeConstant]


    def __init__(self, name, ion, equation, permeability, intracellular_concentration, extracellular_concentration, temperature, beta2threshold,  statevars, mechanism_id, **kwargs):
        super( StdChlCalciumAlphaBetaBeta, self).__init__(name=name, mechanism_id=mechanism_id, **kwargs)
        #Channel.__init__(self, mechanism_id=mechanism_id, **kwargs)

        #self.name = name
        self.ion = ion

        self.permeability = unit(permeability)
        self.intracellular_concentration = unit(intracellular_concentration)
        self.extracellular_concentration = unit(extracellular_concentration)

        self.eqn = equation
        self.statevars = dict([(s, (sDict['alpha'], sDict['beta1'], sDict['beta2'])) for s, sDict in statevars.iteritems()])
        self.beta2threshold = unit(beta2threshold)

        self.F = unit('96485.3365:C/mol')
        self.R = unit('8.314421:J/(K mol)')
        self.CaZ = unit('2:')
        self.T = unit(temperature)

    def get_variables(self):
        return ['gScale', 'pca']

    def get_defaults(self):
        return {'gScale': unit('1.0'), 'pca':self.permeability}

    def get_prefered_units(self):
        return {'gScale': pq.dimensionless, 'pca': unit('cm/sec') }

