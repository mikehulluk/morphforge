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

import quantities as pq

import operator
from morphforge.traces.tracetypes import TracePiecewise
from morphforge.traces.tracetypes.tracepiecewise import TracePieceFunctionLinear
from morphforge.traces.tracetypes.tracepiecewise import TracePieceFunctionFlat
from morphforge.traces.tracetypes.tracepiecewise import PieceWiseComponentVisitor

from morphforge.traces.traceobjpluginctrl import TraceOperatorCtrl


class PiecewiseScalarOperation(PieceWiseComponentVisitor):

    @classmethod
    def visit_linear(cls, o, operator_type, scalar):
        return TracePieceFunctionLinear(
                time_window=o.time_window,
                x0=operator_type(o.x0, scalar),
                x1=operator_type(o.x1, scalar))

    @classmethod
    def visit_flat(cls, o, operator_type, scalar):
        return TracePieceFunctionFlat(
                time_window=o.time_window,
                x=operator_type(o.x, scalar))


class TraceOperator_TracePiecewise_Quantity(object):

    @classmethod
    def do_op(cls, lhs, rhs, operator_type):
        assert (type(lhs) == TracePiecewise and type(rhs) in (pq.Quantity,)) or \
               (type(rhs) == TracePiecewise and type(lhs) in (pq.Quantity,))

        if type(lhs) == TracePiecewise:
            (trace, sc) = (lhs, rhs)
        else:
            (sc, trace) = (lhs, rhs)

        pieces = [PiecewiseScalarOperation.visit(piece, operator_type=operator_type, scalar=sc) for piece in trace.pieces]
        return TracePiecewise(pieces=pieces)

    @classmethod
    def do_add(cls, lhs, rhs):
        return cls.do_op(lhs=lhs, rhs=rhs, operator_type=operator.__add__)

    #@classmethod
    #def do_sub(cls, lhs, rhs):
    #    assert False
    #    return cls.do_op(lhs=lhs, rhs=rhs, operator_type=operator.__sub__)

    @classmethod
    def do_mul(cls, lhs, rhs):
        return cls.do_op(lhs=lhs, rhs=rhs, operator_type=operator.__mul__)

    #@classmethod
    #def do_div(cls, lhs, rhs):
    #    assert False
    #    return cls.do_op(lhs=lhs, rhs=rhs, operator_type=operator.__div__)



from morphforge.traces.tracetypes.tracepiecewise import TracePieceFunctionLinear
from morphforge.traces.tracetypes.tracepiecewise import TracePieceFunctionFlat
from morphforge.traces.tracetypes.tracepiecewise import PieceWiseComponentVisitor
from morphforge.traces.traceobjpluginctrl import TraceOperatorCtrl









# Times quantity:
TraceOperatorCtrl.add_trace_operator_symmetrical_handler(
        operator_type=operator.__add__,
        lhs_type=TracePiecewise, rhs_type=pq.Quantity,
        operator_func=TraceOperator_TracePiecewise_Quantity.do_add,
        flag='default')

#TraceOperatorCtrl.add_trace_operator(
#        operator_type=operator.__sub__,
#        lhs_type=TracePiecewise, rhs_type=pq.Quantity,
#        operator_func=TraceOperator_TracePiecewise_Quantity.do_sub,
#        flag='default')

TraceOperatorCtrl.add_trace_operator_symmetrical_handler(
        operator_type=operator.__mul__,
        lhs_type=TracePiecewise, rhs_type=pq.Quantity,
        operator_func=TraceOperator_TracePiecewise_Quantity.do_mul,
        flag='default')

#TraceOperatorCtrl.add_trace_operator(
#        operator_type=operator.__div__,
#        lhs_type=TracePiecewise, rhs_type=pq.Quantity,
#        operator_func=TraceOperator_TracePiecewise_Quantity.do_div,
#        flag='default')

def do_op_piecewise_pow_scalar(lhs, rhs):
        pieces = [PiecewiseScalarOperation.visit(piece, operator_type=operator.__pow__, scalar=rhs) for piece in lhs.pieces]
        return TracePiecewise(pieces)


TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__pow__,
        lhs_type=TracePiecewise, rhs_type=int,
        operator_func=do_op_piecewise_pow_scalar,
        flag='default')
TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__pow__,
        lhs_type=TracePiecewise, rhs_type=float,
        operator_func=do_op_piecewise_pow_scalar,
        flag='default')
