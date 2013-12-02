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
from morphforge.simulation.base import Channel

from morphforge.constants import StandardTags
import morphforge.stdimports as mf
from morphforge import units


class StdChlAlphaBeta(Channel):

    class Recordables(object):

        ConductanceDensity = StandardTags.ConductanceDensity
        CurrentDensity = StandardTags.CurrentDensity
        StateVar = StandardTags.StateVariable
        StateVarSteadyState = StandardTags.StateSteadyState
        StateVarTimeConstant = StandardTags.StateTimeConstant
        all = [ConductanceDensity, CurrentDensity, StateVar,
               StateVarSteadyState, StateVarTimeConstant]


    def __init__(self, equation, conductance, reversalpotential, statevars=None, name=None, ion=None, **kwargs):
        super(StdChlAlphaBeta, self).__init__(name=name, **kwargs)
        # TODO: FIXED DEFAULT PARAMETER 'statevars'
        if statevars is None:
            statevars = {}
        
        self.ion = ion
        self.eqn = equation
        self.conductance = qty(conductance)
        self.statevars = dict([(s, (sDict['alpha'], sDict['beta'])) for s, sDict in statevars.iteritems()])
        self.reversalpotential = qty(reversalpotential)

        self.conductance = self.conductance.rescale('S/cm2')
        self.reversalpotential = self.reversalpotential.rescale('mV')

    def get_variables(self):
        return ['gBar', 'e_rev', 'gScale']

    def get_defaults(self):
        return {'gBar': self.conductance,
                'e_rev': self.reversalpotential, 
                'gScale': qty('1.0')}

    def get_prefered_units(self):
        return {'gBar': mf.mS/mf.cm2,
                'e_rev': units.mV, 
                'gScale': units.dimensionless
                }

    def record_all(self, sim, cell_location):
        sim.record(self, what=StdChlAlphaBeta.Recordables.ConductanceDensity,cell_location=cell_location)
        sim.record(self, what=StdChlAlphaBeta.Recordables.CurrentDensity,cell_location=cell_location)
        for sv in self.statevars.keys():
            sim.record(self, what=StdChlAlphaBeta.Recordables.StateVar, state=sv,cell_location=cell_location)
            sim.record(self, what=StdChlAlphaBeta.Recordables.StateVarSteadyState, state=sv,cell_location=cell_location)
            sim.record(self, what=StdChlAlphaBeta.Recordables.StateVarTimeConstant, state=sv,cell_location=cell_location)




    def get_state_variables(self):
        return self.statevars.keys()

    def get_alpha_beta_at_voltage(self, V, statevar):

        from morphforgecontrib.simulation.channels.hh_style.summarisers.util import AlphaBetaCalculator
        AlphaBetaCalculator
        alpha = self.statevars[statevar][0]
        beta = self.statevars[statevar][1]
        alpha = AlphaBetaCalculator.calc_alpha_beta(V, alpha)
        beta = AlphaBetaCalculator.calc_alpha_beta(V, beta)
        return (alpha, beta)


