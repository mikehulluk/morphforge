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
from morphforge.traces import TraceFixedDT

from morphforge import units
import numpy as np

        
def _butterworthfilter(tr, filterorder, cutoff_frequency):
    cutoff_frequency.rescale('Hz')
    import scipy.signal
    frequency_hz = 1 / float(tr.get_dt_new().rescale('s'))
    n_frq_hz = frequency_hz / 2.0

    cuttoff_norm = cutoff_frequency / n_frq_hz
    (coeff_num, coeff_denom) = scipy.signal.filter_design.butter(filterorder, cuttoff_norm)
    filteredsignal = scipy.signal.lfilter(coeff_num, coeff_denom, tr.data_pts_np)

    tr_new = TraceFixedDT(time=tr.time_pts, data=filteredsignal * tr.data_unit,)
    copy_trace_attrs(tr, tr_new, comment="+(Butterworth Filtered)" )
    return tr_new


TraceMethodCtrl.register(TraceFixedDT, 'filterbutterworth', _butterworthfilter, can_fallback_to_fixed_trace=True)




def _besselfilter(tr, filterorder, cutoff_frequency):
    cutoff_frequency.rescale('Hz')
    import scipy.signal
    frequency_hz = 1 / float(tr.get_dt_new().rescale('s'))
    n_frq_hz = frequency_hz / 2.0

    cuttoff_norm = cutoff_frequency / n_frq_hz
    (coeff_num, coeff_denom) = scipy.signal.filter_design.bessel(filterorder, cuttoff_norm)
    filteredsignal = scipy.signal.lfilter(coeff_num, coeff_denom, tr.data_pts_np)

    time_shift = tr.get_dt_new() * max(len(coeff_denom), len(coeff_num))

    tr_new = TraceFixedDT(time=tr.time_pts - time_shift,
                          data=filteredsignal * tr.data_unit,
                         )
    copy_trace_attrs(tr, tr_new, comment="+(Bessel Filtered)" )
    return tr_new


TraceMethodCtrl.register(TraceFixedDT, 'filterbessel', _besselfilter, can_fallback_to_fixed_trace=True)


def _filterlowpassrc(tr, tau):
    import scipy.signal
    assert isinstance(tr, TraceFixedDT)
    dt = tr.get_dt_new()
    k = 1. / tau * dt
    k = float(k.rescale(units.dimensionless))

    coeff_denom = np.array([1, k - 1])
    coeff_num = np.array([0, k])

    xp = scipy.signal.lfilter(coeff_num, coeff_denom, tr.data_pts_np)
    tr_new = TraceFixedDT(time=tr.time_pts,
                          data=xp * tr.data_unit,
                         )
    copy_trace_attrs(tr, tr_new, comment="+(LP RC Filtered)" )
    return tr_new


TraceMethodCtrl.register(TraceFixedDT, 'filterlowpassrc', _filterlowpassrc, can_fallback_to_fixed_trace=True)

