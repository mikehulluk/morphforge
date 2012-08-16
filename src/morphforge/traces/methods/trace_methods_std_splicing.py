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


from morphforge.traces import TraceFixedDT
from morphforge.traces import TraceVariableDT
from morphforge.traces import TracePointBased

import numpy
import numpy as np
from quantities.quantity import Quantity
from morphforge.traces.traceobjpluginctrl import TraceMethodCtrl
from morphforge.traces.traceobjpluginctrl import clone_trace



# Shifting:
#############

def _shift_pt_trace(trace, offset):
    return clone_trace(trace, 
                       time=trace._time + offset,
                       data=trace._data, 
                       comment='+ Shifted %2.2f' % offset)


TraceMethodCtrl.register(TraceFixedDT, 'shift', _shift_pt_trace)
TraceMethodCtrl.register(TraceVariableDT, 'shift', _shift_pt_trace)


# Windowing:
###############

def _window_fixed_trace(trace, time_window):

    # Dirty Pre-processing
    if isinstance(time_window, Quantity):
        assert len(time_window) == 2
        time_window = (time_window[0], time_window[1])

    # print time_window, type(time_window)

    assert isinstance(time_window, tuple)
    assert len(time_window) == 2

    if time_window[0] is None:
        time_window = (trace._time[0], time_window[1])
    if time_window[1] is None:
        time_window = (time_window[0], trace._time[-1])


    time_window[0].rescale('ms').magnitude
    time_window[1].rescale('ms').magnitude
    if not isinstance(trace, TracePointBased):
        raise ValueError()


    t_diff1 = time_window[0] - trace._time[0]
    if t_diff1 < 0:
        print 'time_window[0]', time_window[0].rescale('s')
        print 'trace.time[0]', trace._time[0].rescale('s')
        print
        raise ValueError("Windowing outside of trace (min) WindowMin/TraceMin: %f %f  " % (time_window[0], trace._time[0]))

    # if time_window[1] > trace._time[-1]:
    if time_window[1] - trace._time[-1] > 0:
        print 'time_window[1]', time_window[1].rescale('s')
        print 'trace.time[-1]', trace._time[-1].rescale('s')
        print

        raise ValueError('Windowing outside of trace (max)')

    time_indices1 = numpy.nonzero(trace._time > time_window[0])
    time_trace_new = trace._time[time_indices1]
    trace_new = trace._data[time_indices1]

    time_indices2 = numpy.nonzero(time_trace_new < time_window[1])
    time_trace_new = time_trace_new[time_indices2]
    trace_new = trace_new[time_indices2]





    # Ensure we have at least 2 points:
    if len(time_trace_new) < 2:

        tw0 = time_window[0]
        tw1 = time_window[1]

        # get_values( time_window )

        # trace_new1 = trace.get_value_at_time(tw0)
        # trace_new2 = trace.get_value_at_time(tw1)

        trace_new1 = trace.get_values(time_window[0])
        trace_new2 = trace.get_values(time_window[1])

        data_unts = trace_new1.units
        time_unts = time_window[0].units

        time_trace_new = np.array([time_window[0].rescale(time_unts).magnitude, time_window[1].rescale(time_unts).magnitude, ]) * time_unts
        trace_new = np.array([trace_new1.rescale(data_unts).magnitude, trace_new2.rescale(data_unts).magnitude, ]) * data_unts



    if isinstance(trace, TraceFixedDT):
        return TraceFixedDT(time_trace_new, trace_new, tags=trace.tags)
    elif isinstance(trace, TraceVariableDT):
        return TraceVariableDT(time_trace_new, 
                               trace_new,
                               tags=trace.tags)
    else:
        assert False




TraceMethodCtrl.register(TraceFixedDT, 'window', _window_fixed_trace)
TraceMethodCtrl.register(TraceVariableDT, 'window', _window_fixed_trace)


# WindowAndShift:
#################
TraceMethodCtrl.register(TraceFixedDT, 'windowshift', lambda tr,window: tr.window(window).shift(-1.0*window[0]) )
TraceMethodCtrl.register(TraceVariableDT, 'windowshift', lambda tr,window: tr.window(window).shift(-1.0*window[0]) )







