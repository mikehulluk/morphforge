#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------
from morphforge.traces import Trace_FixedDT
from morphforge.traces import Trace_VariableDT
from morphforge.traces import Trace_PointBased

import numpy
import numpy as np
from quantities.quantity import Quantity
from morphforge.traces.trace_methods_ctrl import TraceMethodCtrl
from morphforge.traces.trace_methods_ctrl import clone_trace



# Shifting:
#############

def _shift_pt_trace(trace, offset):
    return clone_trace(trace, time=trace._time + offset, data=trace._data, comment="+ Shifted %2.2f" % offset)


TraceMethodCtrl.register(Trace_FixedDT,    'shift', _shift_pt_trace)
TraceMethodCtrl.register(Trace_VariableDT, 'shift', _shift_pt_trace)


# Windowing:
###############

def _window_fixed_trace(trace, time_window):

    #Dirty Pre-processing
    if isinstance(time_window, Quantity):
        assert len(time_window) == 2
        time_window = (time_window[0], time_window[1])

    #print time_window, type(time_window)

    assert isinstance(time_window, tuple)
    assert len(time_window) == 2

    if time_window[0] is None:
        time_window = ( trace._time[0], time_window[1] )
    if time_window[1] is None:
        time_window = ( time_window[0], trace._time[-1] )


    time_window[0].rescale('ms').magnitude
    time_window[1].rescale('ms').magnitude
    if not isinstance(trace, Trace_PointBased): raise ValueError()


    tDiff1 = time_window[0] - trace._time[0]
    if tDiff1 < 0:
        print  "time_window[0]", time_window[0].rescale("s")
        print  "trace.time[0]", trace._time[0].rescale("s")
        print
        raise ValueError("Windowing outside of trace (min) WindowMin/TraceMin: %f %f  " % (time_window[0], trace._time[0]))

    #if time_window[1] > trace._time[-1]:
    if time_window[1] - trace._time[-1] > 0:
        print  "time_window[1]", time_window[1].rescale("s")
        print  "trace.time[-1]", trace._time[-1].rescale("s")
        print

        raise ValueError("Windowing outside of trace (max)")

    timeIndices1 = numpy.nonzero(trace._time > time_window[0])
    timeTraceNew = trace._time[timeIndices1]
    traceNew = trace._data[timeIndices1]

    timeIndices2 = numpy.nonzero(timeTraceNew < time_window[1])
    timeTraceNew = timeTraceNew[timeIndices2]
    traceNew = traceNew[timeIndices2]





    # Ensure we have at least 2 points:
    if len(timeTraceNew) < 2:

        tw0 = time_window[0]
        tw1 = time_window[1]

        #getValues( time_window )

        #traceNew1 = trace.getValueAtTime(tw0)
        #traceNew2 = trace.getValueAtTime(tw1)

        traceNew1 = trace.getValues( time_window[0] )#[0]
        traceNew2 = trace.getValues( time_window[1] )#[0]

        data_unts = traceNew1.units
        time_unts = time_window[0].units

        timeTraceNew = np.array([time_window[0].rescale(time_unts).magnitude, time_window[1].rescale(time_unts).magnitude, ]) * time_unts
        traceNew = np.array([traceNew1.rescale(data_unts).magnitude, traceNew2.rescale(data_unts).magnitude, ]) * data_unts



    if isinstance(trace, Trace_FixedDT):
        return Trace_FixedDT(timeTraceNew, traceNew, tags= trace.tags)
    elif isinstance(trace, Trace_VariableDT):
        return Trace_VariableDT(timeTraceNew, traceNew, tags= trace.tags)
    else:
        assert False




TraceMethodCtrl.register(Trace_FixedDT, 'window', _window_fixed_trace)
TraceMethodCtrl.register(Trace_VariableDT, 'window', _window_fixed_trace)


# WindowAndShift:
#################
TraceMethodCtrl.register(Trace_FixedDT, 'windowshift', lambda tr,window: tr.window(window).shift(-1.0*window[0]) )
TraceMethodCtrl.register(Trace_VariableDT, 'windowshift', lambda tr,window: tr.window(window).shift(-1.0*window[0]) )







