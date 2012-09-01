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
from morphforge.traces.traceobjpluginctrl import copy_trace_attrs

import numpy as np
from morphforge.traces.tracetypes import TraceVariableDT
from morphforge.traces.tracetypes import TracePiecewise
from morphforge.traces.tracetypes import TraceFixedDT
import copy

def _clone_fixed(tr):
    tr_new = TraceFixedDT( 
            time = np.copy( tr.time_pts_np) * tr.time_units,
            data = np.copy( tr.data_pts_np) * tr.data_units )
    copy_trace_attrs(tr,tr_new, comment='+(cloned)')
    return tr_new

def _clone_variable(tr):
    tr_new = TraceVariableDT(
            time = np.copy( tr.time_pts_np) * tr.time_units,
            data = np.copy( tr.data_pts_np) * tr.data_units )
    copy_trace_attrs(tr,tr_new, comment='+(cloned)')
    return tr_new

def _clone_piecewise(tr):
    tr_new = TracePiecewise(pieces = [copy.copy(piece) for piece in tr.pieces])
    copy_trace_attrs(tr,tr_new, comment='+(cloned)')
    return tr_new


TraceMethodCtrl.register(TraceFixedDT,    'clone', _clone_fixed)
TraceMethodCtrl.register(TraceVariableDT, 'clone', _clone_variable)
TraceMethodCtrl.register(TracePiecewise,  'clone', _clone_piecewise)

