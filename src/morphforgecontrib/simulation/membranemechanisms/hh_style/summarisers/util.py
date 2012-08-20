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

import numpy as np

import morphforge.core.quantities as pq


class AlphaBetaCalculator(object):

    @classmethod
    def calc_alpha_beta(cls, V, ab):
        v = V.rescale('mV').magnitude
        alphabeta = (ab[0] + ab[1] * v) / (ab[2] + np.exp((ab[3] + v) / ab[4]))
        alphabeta = alphabeta * (pq.J / pq.J)
        return alphabeta

class InfTauCalculator(object):
    @classmethod
    def alpha_beta_to_inf_tau(cls, alpha, beta):
        inf = alpha / (alpha + beta)
        tau = 1.0 / (alpha + beta) * pq.milli * pq.second
        return (inf, tau)

    @classmethod
    def evaluate_inf_tau_for_v(cls, (alphaParams, betaParams), V):
        (alpha, beta) = AlphaBetaCalculator.getAlphaBeta(V, alphaParams, betaParams)
        (inf, tau) = InfTauCalculator.alpha_beta_to_inf_tau(alpha, beta)
        return (inf, tau)


class ReportLabTools(object):

    @classmethod
    def build_alpha_beta_table(cls, elements, reportlabconfig, title, params):

        from reportlab.platypus import Paragraph, Table
        elements.append(Paragraph(title,reportlabconfig.styles['Heading4']))
        print params
        print
        alpha_params = '%2.2f %2.2f %2.2f %2.2f %2.2f' % tuple(params)
        alpha_table_data = [['A', 'B', 'C', 'D', 'E'],
                            alpha_params.split()]
        elements.append(Table(alpha_table_data,
                        style=reportlabconfig.defaultTableStyle))


