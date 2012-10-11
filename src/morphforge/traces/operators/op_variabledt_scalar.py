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

from morphforge import units

import operator
from morphforge.traces.tracetypes import TraceVariableDT

from morphforge.traces.traceobjpluginctrl import TraceOperatorCtrl


class TraceOperator_TraceVariableDT_Quantity(object):

    @classmethod
    def do_add(cls, lhs, rhs):
        assert (type(lhs) == TraceVariableDT and type(rhs) == units.Quantity)
        return TraceVariableDT(lhs.time_pts, lhs.data_pts + rhs)

    @classmethod
    def do_sub(cls, lhs, rhs):
        assert (type(lhs) == TraceVariableDT and type(rhs) == units.Quantity)
        return TraceVariableDT(lhs.time_pts, lhs.data_pts - rhs)

    @classmethod
    def do_mul(cls, lhs, rhs):
        assert (type(lhs) == TraceVariableDT and type(rhs) == units.Quantity)
        return TraceVariableDT(lhs.time_pts, lhs.data_pts * rhs)

    @classmethod
    def do_div(cls, lhs, rhs):
        assert (type(lhs) == TraceVariableDT and type(rhs) == units.Quantity)
        return TraceVariableDT(lhs.time_pts, lhs.data_pts / rhs)



class TraceOperator_Quantity_TraceVariableDT(object):

    @classmethod
    def do_add(cls, lhs, rhs):
        assert type(rhs) == TraceVariableDT and type(lhs) == units.Quantity
        return TraceVariableDT(rhs.time_pts, lhs + rhs.data_pts)

    @classmethod
    def do_sub(cls, lhs, rhs):
        assert type(rhs) == TraceVariableDT and type(lhs) == units.Quantity
        return TraceVariableDT(rhs.time_pts, lhs - rhs.data_pts)

    @classmethod
    def do_mul(cls, lhs, rhs):
        assert type(rhs) == TraceVariableDT and type(lhs) == units.Quantity
        return TraceVariableDT(rhs.time_pts, lhs * rhs.data_pts)

    @classmethod
    def do_div(cls, lhs, rhs):
        assert type(rhs) == TraceVariableDT and type(lhs) == units.Quantity
        return TraceVariableDT(rhs.time_pts, lhs / rhs.data_pts)


TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__add__,
        lhs_type=TraceVariableDT, rhs_type=units.Quantity,
        operator_func=TraceOperator_TraceVariableDT_Quantity.do_add,
        flag='default')
TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__sub__,
        lhs_type=TraceVariableDT, rhs_type=units.Quantity,
        operator_func=TraceOperator_TraceVariableDT_Quantity.do_sub,
        flag='default')
TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__mul__,
        lhs_type=TraceVariableDT, rhs_type=units.Quantity,
        operator_func=TraceOperator_TraceVariableDT_Quantity.do_mul,
        flag='default')
TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__div__,
        lhs_type=TraceVariableDT, rhs_type=units.Quantity,
        operator_func=TraceOperator_TraceVariableDT_Quantity.do_div,
        flag='default')

TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__add__,
        lhs_type=units.Quantity, rhs_type=TraceVariableDT,
        operator_func=TraceOperator_Quantity_TraceVariableDT.do_add,
        flag='default')
TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__sub__,

        lhs_type=units.Quantity, rhs_type=TraceVariableDT,
        operator_func=TraceOperator_Quantity_TraceVariableDT.do_sub,
        flag='default')
TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__mul__,
        lhs_type=units.Quantity, rhs_type=TraceVariableDT,
        operator_func=TraceOperator_Quantity_TraceVariableDT.do_mul,
        flag='default')
TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__div__,
        lhs_type=units.Quantity, rhs_type=TraceVariableDT,
        operator_func=TraceOperator_Quantity_TraceVariableDT.do_div,
        flag='default')













class TraceOperator_TraceVariableDT_Scalar(object):

    @classmethod
    def do_add(cls, lhs, rhs):
        assert (type(lhs) == TraceVariableDT and type(rhs) == float)
        assert isinstance(lhs.data_pts, units.unitquantity.Dimensionless)
        return TraceVariableDT(lhs.time_pts, lhs.data_pts + rhs)

    @classmethod
    def do_sub(cls, lhs, rhs):
        assert (type(lhs) == TraceVariableDT and type(rhs) == float)
        assert isinstance(lhs.data_pts, units.unitquantity.Dimensionless)
        return TraceVariableDT(lhs.time_pts, lhs.data_pts - rhs)

    @classmethod
    def do_mul(cls, lhs, rhs):
        assert (type(lhs) == TraceVariableDT and type(rhs) == float)
        return TraceVariableDT(lhs.time_pts, lhs.data_pts * rhs)

    @classmethod
    def do_div(cls, lhs, rhs):
        assert (type(lhs) == TraceVariableDT and type(rhs) == float)
        return TraceVariableDT(lhs.time_pts, lhs.data_pts / rhs)

    @classmethod
    def do_pow(cls, lhs, rhs):
        assert (type(lhs) == TraceVariableDT and (type(rhs) == float or type(rhs) == int))
        return TraceVariableDT(lhs.time_pts, lhs.data_pts ** rhs)


class TraceOperator_Scalar_TraceVariableDT(object):

    @classmethod
    def do_add(cls, lhs, rhs):
        assert type(rhs) == TraceVariableDT and type(lhs) == float
        assert isinstance(rhs.data_pts, units.Dimensionless)
        return TraceVariableDT(rhs.time_pts, lhs + rhs.data_pts)

    @classmethod
    def do_sub(cls, lhs, rhs):
        assert type(rhs) == TraceVariableDT and type(lhs) == float
        assert isinstance(rhs.data_pts, units.Dimensionless)
        return TraceVariableDT(rhs.time_pts, lhs - rhs.data_pts)

    @classmethod
    def do_mul(cls, lhs, rhs):
        assert type(rhs) == TraceVariableDT and type(lhs) == float
        return TraceVariableDT(rhs.time_pts, lhs * rhs.data_pts)

    @classmethod
    def do_div(cls, lhs, rhs):
        assert type(rhs) == TraceVariableDT and type(lhs) == float
        return TraceVariableDT(rhs.time_pts, lhs / rhs.data_pts)




TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__add__,
        lhs_type=TraceVariableDT, rhs_type=float,
        operator_func=TraceOperator_TraceVariableDT_Scalar.do_add,
        flag='default')
TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__sub__,
        lhs_type=TraceVariableDT, rhs_type=float,
        operator_func=TraceOperator_TraceVariableDT_Scalar.do_sub,
        flag='default')
TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__mul__,
        lhs_type=TraceVariableDT, rhs_type=float,
        operator_func=TraceOperator_TraceVariableDT_Scalar.do_mul,
        flag='default')
TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__div__,
        lhs_type=TraceVariableDT, rhs_type=float,
        operator_func=TraceOperator_TraceVariableDT_Scalar.do_div,
        flag='default')
TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__pow__,
        lhs_type=TraceVariableDT, rhs_type=float,
        operator_func=TraceOperator_TraceVariableDT_Scalar.do_pow,
        flag='default')
TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__pow__,
        lhs_type=TraceVariableDT, rhs_type=int,
        operator_func=TraceOperator_TraceVariableDT_Scalar.do_pow,
        flag='default')



TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__add__,
        lhs_type=float, rhs_type=TraceVariableDT,
        operator_func=TraceOperator_Scalar_TraceVariableDT.do_add,
        flag='default')
TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__sub__,
        lhs_type=float, rhs_type=TraceVariableDT,
        operator_func=TraceOperator_Scalar_TraceVariableDT.do_sub,
        flag='default')
TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__mul__,
        lhs_type=float, rhs_type=TraceVariableDT,
        operator_func=TraceOperator_Scalar_TraceVariableDT.do_mul,
        flag='default')
TraceOperatorCtrl.add_trace_operator(
        operator_type=operator.__div__,
        lhs_type=float, rhs_type=TraceVariableDT,
        operator_func=TraceOperator_Scalar_TraceVariableDT.do_div,
        flag='default')




