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

from morphforge.traces.traceobjpluginctrl import TraceMethodCtrl
from morphforge.traces import TraceFixedDT
import numpy as np
import quantities as pq
import operator
from morphforge.traces.tracetypes import TracePiecewise
from morphforge.traces.tracetypes.tracepiecewise import TracePieceFunctionLinear
from morphforge.traces.tracetypes.tracepiecewise import TracePieceFunctionFlat
from morphforge.traces.tracetypes.tracepiecewise import PieceWiseComponentVisitor
from morphforge.traces.traceobjpluginctrl import TraceOperatorCtrl


def _integrate_pointbased(tr, ):
    import scipy.integrate
    return scipy.integrate.simps(y=tr.data_pts_np, x=tr.time_pts_np) * tr.data_unit * tr.time_unit

TraceMethodCtrl.register(TraceFixedDT, 'integrate', _integrate_pointbased)





class PiecewiseIntegrator(PieceWiseComponentVisitor):

    @classmethod
    def visit_linear(cls, o):
        return 0.5 * (o.time_window[1]-o.time_window[0]) * (o.x1-o.x0)

    @classmethod
    def visit_flat(cls, o ):
        return (o.time_window[1]-o.time_window[0]) * o.x


def _integrate_piecewise(tr, ):
        pieces =  [PiecewiseIntegrator.visit(p) for p in tr.pieces]
        tot = None
        for p in pieces:
            if tot is None:
                tot = p
            else:
                tot = tot+p
        return tot

TraceMethodCtrl.register(TracePiecewise, 'integrate', _integrate_piecewise )









