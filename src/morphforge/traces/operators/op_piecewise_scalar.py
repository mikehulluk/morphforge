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


import operator
from morphforge import units
from morphforge.traces.tracetypes import TracePiecewise
from morphforge.traces.tracetypes.tracepiecewise import TracePieceFunctionLinear
from morphforge.traces.tracetypes.tracepiecewise import TracePieceFunctionFlat
from morphforge.traces.tracetypes.tracepiecewise import PieceWiseComponentVisitor
from morphforge.traces.traceobjpluginctrl import TraceOperatorCtrl



class PiecewiseOperationLHS(PieceWiseComponentVisitor):
    @classmethod
    def visit(cls, lhs_piece, operator_type, rhs_scalar, **_kwargs):
        return PieceWiseComponentVisitor.visit(o=lhs_piece, operator_type=operator_type, rhs_scalar=rhs_scalar)

    @classmethod
    def visit_linear(cls, lhs_piece, operator_type, rhs_scalar, **_kwargs):
        return TracePieceFunctionLinear(
                time_window=lhs_piece.time_window,
                x0=operator_type(lhs_piece.x0, rhs_scalar),
                x1=operator_type(lhs_piece.x1, rhs_scalar)
                )

    @classmethod
    def visit_flat(cls, lhs_piece, operator_type, rhs_scalar, **_kwargs):
        return TracePieceFunctionFlat(
                time_window=lhs_piece.time_window,
                x=operator_type(lhs_piece.x, rhs_scalar)
                )

class TraceOperator_TracePiecewise_Quantity(object):

    @classmethod
    def do_add(cls, lhs, rhs):        
        return TracePiecewise( [PiecewiseOperationLHS.visit(lhs_piece=piece, operator_type=operator.__add__, rhs_scalar=rhs) for piece in lhs.pieces] )
    @classmethod
    def do_sub(cls, lhs, rhs):        
        return TracePiecewise( [PiecewiseOperationLHS.visit(lhs_piece=piece, operator_type=operator.__sub__, rhs_scalar=rhs) for piece in lhs.pieces] )
    @classmethod
    def do_mul(cls, lhs, rhs):        
        return TracePiecewise( [PiecewiseOperationLHS.visit(lhs_piece=piece, operator_type=operator.__mul__, rhs_scalar=rhs) for piece in lhs.pieces] )
    @classmethod
    def do_div(cls, lhs, rhs):        
        return TracePiecewise( [PiecewiseOperationLHS.visit(lhs_piece=piece, operator_type=operator.__div__, rhs_scalar=rhs) for piece in lhs.pieces] )        


TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__add__,
        lhs_type=TracePiecewise, rhs_type=units.Quantity,
        operator_func=TraceOperator_TracePiecewise_Quantity.do_add,
        flag='default')
TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__sub__,
        lhs_type=TracePiecewise, rhs_type=units.Quantity,
        operator_func=TraceOperator_TracePiecewise_Quantity.do_sub,
        flag='default')
TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__mul__,
        lhs_type=TracePiecewise, rhs_type=units.Quantity,
        operator_func=TraceOperator_TracePiecewise_Quantity.do_mul,
        flag='default')
TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__div__,
        lhs_type=TracePiecewise, rhs_type=units.Quantity,
        operator_func=TraceOperator_TracePiecewise_Quantity.do_div,
        flag='default')









class PiecewiseOperationRHS(PieceWiseComponentVisitor):

    @classmethod
    def visit(cls, rhs_piece, operator_type, lhs_scalar):
        return PieceWiseComponentVisitor.visit(o=rhs_piece, operator_type=operator_type, lhs_scalar=lhs_scalar)

    @classmethod
    def visit_linear(cls, rhs_piece, operator_type, lhs_scalar):
        return TracePieceFunctionLinear(
                time_window=rhs_piece.time_window,
                x0=operator_type(lhs_scalar, rhs_piece.x0 ),
                x1=operator_type(lhs_scalar, rhs_piece.x1)
                )

    @classmethod
    def visit_flat(cls, rhs_piece, operator_type, lhs_scalar):
        return TracePieceFunctionFlat(
                time_window=rhs_piece.time_window,
                x=operator_type(lhs_scalar, rhs_piece.x)
                )

class TraceOperator_Quantity_TracePiecewise(object):

    @classmethod
    def do_add(cls, lhs, rhs):        
        return TracePiecewise( [PiecewiseOperationRHS.visit(rhs_piece=piece, operator_type=operator.__add__, lhs_scalar=lhs) for piece in rhs.pieces] )
    @classmethod
    def do_sub(cls, lhs, rhs):        
        return TracePiecewise( [PiecewiseOperationRHS.visit(rhs_piece=piece, operator_type=operator.__sub__, lhs_scalar=lhs) for piece in rhs.pieces] )
    @classmethod
    def do_mul(cls, lhs, rhs):        
        return TracePiecewise( [PiecewiseOperationRHS.visit(rhs_piece=piece, operator_type=operator.__mul__, lhs_scalar=lhs) for piece in rhs.pieces] )
    @classmethod
    def do_div(cls, lhs, rhs):        
        return TracePiecewise( [PiecewiseOperationRHS.visit(rhs_piece=piece, operator_type=operator.__div__, lhs_scalar=lhs) for piece in rhs.pieces] )        


TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__add__,
        lhs_type=units.Quantity, rhs_type=TracePiecewise,
        operator_func=TraceOperator_Quantity_TracePiecewise.do_add,
        flag='default')
TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__sub__,
        lhs_type=units.Quantity, rhs_type=TracePiecewise,
        operator_func=TraceOperator_Quantity_TracePiecewise.do_sub,
        flag='default')
TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__mul__,
        lhs_type=units.Quantity, rhs_type=TracePiecewise,
        operator_func=TraceOperator_Quantity_TracePiecewise.do_mul,
        flag='default')
TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__div__,
        lhs_type=units.Quantity, rhs_type=TracePiecewise,
        operator_func=TraceOperator_Quantity_TracePiecewise.do_div,
        flag='default')











def do_op_piecewise_pow_scalar(lhs, rhs):
    pieces = [PiecewiseOperationLHS.visit(lhs_piece=piece, operator_type=operator.__pow__, rhs_scalar=rhs) for piece in lhs.pieces]
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
