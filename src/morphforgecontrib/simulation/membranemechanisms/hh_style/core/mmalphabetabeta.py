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
from morphforge.simulation.base import MembraneMechanism

import numpy as np


class MM_AlphaBetaBetaChannel(MembraneMechanism):
    class Recordables(object):
        Current = 'Current'
        all = [Current]

    def __init__(self, name, ion, equation, conductance, reversalpotential, statevars, beta2threshold, mechanism_id):

        MembraneMechanism.__init__(self, mechanism_id=mechanism_id)

        self.name = name
        self.ion = ion
        self.eqn = equation
        self.conductance = unit(conductance)

        self.beta2threshold = unit(beta2threshold)

        self.statevars = dict([(s, (sDict['alpha'], sDict['beta1'],sDict['beta2'])) for s, sDict in statevars.iteritems()])
        self.reversalpotential = unit(reversalpotential)


    def get_variables(self):
        return ['gBar', 'e_rev', 'gScale']

    def get_defaults(self):
        return {'gBar': self.conductance,
                'e_rev': self.reversalpotential, 'gScale': unit('1.0')}






    def get_alpha_beta_at_voltage(self, V, statevar):


        from morphforgecontrib.simulation.membranemechanisms.hh_style.summarisers.util import AlphaBetaCalculator
        alpha = self.statevars[statevar][0]
        beta1 = self.statevars[statevar][1]
        beta2 = self.statevars[statevar][2]
        threshold = self.beta2threshold

        alpha = AlphaBetaCalculator.calc_alpha_beta(V, alpha)
        beta1 = AlphaBetaCalculator.calc_alpha_beta(V, beta1)
        beta2 = AlphaBetaCalculator.calc_alpha_beta(V, beta2)

        beta_indices1 = np.nonzero(V < threshold)
        beta_indices2 = np.nonzero(V >= threshold)

        beta = np.hstack([beta1[beta_indices1], beta2[beta_indices2]])

        return (alpha, beta)
