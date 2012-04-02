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
from morphforge.traces.trace_methods_ctrl import CloneTrace



# Shifting:
#############

def ShiftPtTrace(trace, offset):
    return CloneTrace(trace, time=trace._time + offset, data=trace._data, comment="+ Shifted %2.2f" % offset)
                    

TraceMethodCtrl.register(Trace_FixedDT,    'shift', ShiftPtTrace)        
TraceMethodCtrl.register(Trace_VariableDT, 'shift', ShiftPtTrace)  


# Windowing:
###############

def WindowFixedTrace(trace, timeWindow):
    
    #Dirty Pre-processing
    if isinstance(timeWindow, Quantity):
        assert len(timeWindow) == 2
        timeWindow = (timeWindow[0], timeWindow[1])
        
    #print timeWindow, type(timeWindow)
    
    assert isinstance(timeWindow, tuple)
    assert len(timeWindow) == 2 
    timeWindow[0].rescale('ms').magnitude
    timeWindow[1].rescale('ms').magnitude
    if not isinstance(trace, Trace_PointBased): raise ValueError()
    
    #print trace
    #print "timeWindow[0]" , timeWindow[0]
    #print "trace._time[0]", trace._time[0]  
            
    
    tDiff1 = timeWindow[0] - trace._time[0] 
    if tDiff1 < 0:
        print  "timeWindow[0]", timeWindow[0].rescale("s")
        print  "trace.time[0]", trace._time[0].rescale("s")
        print
        raise ValueError("Windowing outside of trace (min) WindowMin/TraceMin: %f %f  " % (timeWindow[0], trace._time[0]))
    
    #if timeWindow[1] > trace._time[-1]:
    if timeWindow[1] - trace._time[-1] > 0:
        print  "timeWindow[1]", timeWindow[1].rescale("s")
        print  "trace.time[-1]", trace._time[-1].rescale("s")
        print
        
        raise ValueError("Windowing outside of trace (max)")
    
    timeIndices1 = numpy.nonzero(trace._time > timeWindow[0])
    timeTraceNew = trace._time[timeIndices1]
    traceNew = trace._data[timeIndices1]
    
    timeIndices2 = numpy.nonzero(timeTraceNew < timeWindow[1])
    timeTraceNew = timeTraceNew[timeIndices2]
    traceNew = traceNew[timeIndices2]
    
    
    
    
    
    # Ensure we have at least 2 points:
    if len(timeTraceNew) < 2:

        tw0 = timeWindow[0]
        tw1 = timeWindow[1]
        
        traceNew1 = trace.getValueAtTime(tw0)
        traceNew2 = trace.getValueAtTime(tw1)
        data_unts = traceNew1.units
        time_unts = timeWindow[0].units
        
        timeTraceNew = np.array([timeWindow[0].rescale(time_unts).magnitude, timeWindow[1].rescale(time_unts).magnitude, ]) * time_unts
        traceNew = np.array([traceNew1.rescale(data_unts).magnitude, traceNew2.rescale(data_unts).magnitude, ]) * data_unts 
    
        
    
    if isinstance(trace, Trace_FixedDT):
        return Trace_FixedDT(timeTraceNew, traceNew, tags= trace.tags)
    elif isinstance(trace, Trace_VariableDT):
        return Trace_VariableDT(timeTraceNew, traceNew, tags= trace.tags)
    else:
        assert False
        
        
        
        
TraceMethodCtrl.register(Trace_FixedDT, 'window', WindowFixedTrace)        
TraceMethodCtrl.register(Trace_VariableDT, 'window', WindowFixedTrace)
        
        
# WindowAndShift:
#################        
TraceMethodCtrl.register(Trace_FixedDT, 'windowshift', lambda tr,window: tr.window(window).shift(-1.0*window[0]) )        
TraceMethodCtrl.register(Trace_VariableDT, 'windowshift', lambda tr,window: tr.window(window).shift(-1.0*window[0]) )        
        
        
        
        
        
      
        
