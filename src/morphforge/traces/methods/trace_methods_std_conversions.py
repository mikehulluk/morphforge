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


from morphforge.traces.traceobjpluginctrl import copy_trace_attrs
from morphforge.traces.traceobjpluginctrl import TraceMethodCtrl
from morphforge.traces import TraceFixedDT, TraceVariableDT, TracePiecewise
from MMtrace_conversion import TraceConverter, TraceApproximator


# Conversion to: FixedDT:
#########################
TraceMethodCtrl.register(TraceFixedDT,     'convert_to_fixed', lambda tr,dt: copy_trace_attrs(tr_old=tr, tr_new=TraceConverter.rebase_to_fixed_dt(tr,dt)))
TraceMethodCtrl.register(TraceVariableDT,  'convert_to_fixed', lambda tr,dt: copy_trace_attrs(tr_old=tr, tr_new=TraceConverter.rebase_to_fixed_dt(tr,dt)))
TraceMethodCtrl.register(TracePiecewise,   'convert_to_fixed', lambda tr,dt: copy_trace_attrs(tr_old=tr, tr_new=TraceConverter.rebase_to_fixed_dt(tr,dt)))


# Conversion to VariableDT:
###########################
TraceMethodCtrl.register(TraceFixedDT,     'convert_to_variable', lambda tr: copy_trace_attrs(tr_old=tr, tr_new=TraceConverter.reduce_to_variable_dt_trace()))
TraceMethodCtrl.register(TraceVariableDT,  'convert_to_variable', lambda tr: copy_trace_attrs(tr_old=tr, tr_new=TraceConverter.reduce_to_variable_dt_trace()))
# MISSING: PIECEWISE


# Conversion to Piecewise:
##########################
TraceMethodCtrl.register(TraceFixedDT, 'convert_to_piecewise', TraceApproximator.fit_piecewise_linear_trace)
# MISSING: VariableDT
# MISSING: Piecewise







