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
from morphforge.traces.tracetypes  import TracePiecewise
from morphforge.traces.tracetypes.tracepiecewise  import TracePieceFunctionLinear, TracePieceFunctionFlat
from morphforge.traces.tracetypes.tracepiecewise  import PieceWiseComponentVisitor

from morphforge.traces.traceobjpluginctrl import TraceOperatorCtrl


class PiecewiseScalarOperation(PieceWiseComponentVisitor):

    @classmethod
    def visit_linear(cls, o, operator, scalar):
        return TracePieceFunctionLinear(time_window=o.time_window,
                                        x0=operator(o.x0,scalar ),
                                        x1=operator(o.x1,scalar ) )

    @classmethod
    def visit_flat(cls, o, operator, scalar):
        return TracePieceFunctionFlat(time_window=o.time_window,
                                      x=operator(o.x,scalar ) )



class TraceOperator_TracePiecewise_Quantity(object):
    @classmethod
    def do_op(self, lhs, rhs, operator):
        assert ( type(lhs) == TracePiecewise and type(rhs) in (pq.Quantity,) ) or \
               ( type(rhs) == TracePiecewise and type(lhs) in (pq.Quantity,) )

        if type(lhs) == TracePiecewise:
            tr,sc = lhs,rhs
        else:
            sc,tr = lhs,rhs

        pieces = [ PiecewiseScalarOperation.visit(p,operator=operator,scalar=sc) for p in tr._pieces ]
        return TracePiecewise( pieces = pieces )

    @classmethod
    def do_add(cls, lhs, rhs):
        return cls.do_op(lhs=lhs,rhs=rhs,operator=operator.__add__)
    @classmethod
    def do_sub(cls, lhs, rhs):
        return cls.do_op(lhs=lhs,rhs=rhs,operator=operator.__sub__)
    @classmethod
    def do_mul(cls, lhs, rhs):
        return cls.do_op(lhs=lhs,rhs=rhs,operator=operator.__mul__)
    @classmethod
    def do_div(cls, lhs, rhs):
        return cls.do_op(lhs=lhs,rhs=rhs,operator=operator.__div__)

# Times quantity:
TraceOperatorCtrl.add_trace_operator( operator_type = operator.__add__,
                                      lhs_type = TracePiecewise,
                                      rhs_type = pq.Quantity,
                                      operator_func = TraceOperator_TracePiecewise_Quantity.do_add,
                                      flag='default' )

TraceOperatorCtrl.add_trace_operator( operator_type = operator.__sub__,
                                      lhs_type = TracePiecewise,
                                      rhs_type = pq.Quantity,
                                      operator_func = TraceOperator_TracePiecewise_Quantity.do_sub,
                                      flag='default' )

TraceOperatorCtrl.add_trace_operator( operator_type = operator.__mul__,
                                      lhs_type = TracePiecewise,
                                      rhs_type = pq.Quantity,
                                      operator_func = TraceOperator_TracePiecewise_Quantity.do_mul,
                                      flag='default' )

TraceOperatorCtrl.add_trace_operator( operator_type = operator.__div__,
                                      lhs_type = TracePiecewise,
                                      rhs_type = pq.Quantity,
                                      operator_func = TraceOperator_TracePiecewise_Quantity.do_div,
                                      flag='default' )

