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
from morphforge import units
from morphforge.stdimports import StandardTags
from morphforge.simulation.base import Channel


class StdChlCalciumAlphaBetaBeta(Channel):

    class Recordables(object):

        CurrentDensity = StandardTags.CurrentDensity
        StateVar = StandardTags.StateVariable
        StateVarSteadyState = 'StateSteaddyState'
        StateVarTimeConstant = 'StateTimeConstant'

        all = [CurrentDensity, StateVar, StateVarSteadyState,
               StateVarTimeConstant]


    def __init__(self, name, ion, equation, permeability, intracellular_concentration, extracellular_concentration, temperature, beta2threshold,  statevars, **kwargs):
        super( StdChlCalciumAlphaBetaBeta, self).__init__(name=name, **kwargs)

        self.ion = ion

        self.permeability = qty(permeability)
        self.intracellular_concentration = qty(intracellular_concentration)
        self.extracellular_concentration = qty(extracellular_concentration)

        self.eqn = equation
        self.statevars = dict([(s, (sDict['alpha'], sDict['beta1'], sDict['beta2'])) for s, sDict in statevars.iteritems()])
        self.beta2threshold = qty(beta2threshold)

        self.F = qty('96485.3365:C/mol')
        self.R = qty('8.314421:J/(K mol)')
        self.CaZ = qty('2.0:')
        self.T = qty(temperature)

    def get_variables(self):
        return ['gScale', 'pca']

    def get_defaults(self):
        return {'gScale': qty('1.0'), 'pca':self.permeability}

    def get_prefered_units(self):
        return {'gScale': units.dimensionless, 'pca': qty('cm/sec') }

