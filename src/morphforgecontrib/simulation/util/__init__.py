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

from voltageclampchannel import get_voltageclamp_soma_current_trace
from calculate_input_resistance import CellAnalysis_StepInputResponse
from calculate_input_resistance import CellAnalysis_ReboundResponse
from calculate_input_resistance import CellAnalysis_IVCurve

import numpy as np
from morphforge.core.misc import SeqUtils


def exec_with_prob(p, func):

    def new_func(*args, **kwargs):
        if np.random.sample() < p:
            return func(*args, **kwargs)
        else:
            return None

    return new_func




def record_from_mechanism(sim, mechanism_name, cell_location, what, on_error_skip=False, user_tags = None, **kwargs):
    user_tags = user_tags or []

    assert on_error_skip == False


    channels = cell_location.cell.get_biophysics().get_all_mechanisms_applied_to_cell()


    chl = SeqUtils.filter_expect_single(seq=channels, filter_func=lambda m:m.name==mechanism_name)
    r = sim.record(chl, what=what, cell_location=cell_location, user_tags = user_tags + [chl.name], **kwargs)

    return r




def record_from_all_mechanisms(sim, cell_location, what, on_error_skip=False, user_tags=None, **kwargs):
    user_tags = user_tags or []

    assert on_error_skip == False

    cell = cell_location.cell

    channels = cell.get_biophysics().get_all_mechanisms_applied_to_cell()

    recs = []
    for chl in channels:

        r = sim.record(chl, what=what, cell_location=cell_location,
                       user_tags=user_tags + [chl.name], **kwargs)
        recs.append(r)

    return recs


