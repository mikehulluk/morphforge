#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------
from morphforge.traces.trace_methods_ctrl import TraceMethodCtrl, CloneTrace
from morphforge.traces import Trace_FixedDT, Trace_VariableDT, Trace_Piecewise
import numpy as np

import scipy.integrate
from morphforge.core.quantities.fromcore import unit




# Mean, rms, stddev, variance functions:
##############################

# For FixedDT traces, these are simple:
TraceMethodCtrl.register(Trace_FixedDT, 'mean',   lambda tr: np.mean(tr._data) )
TraceMethodCtrl.register(Trace_FixedDT, 'stddev', lambda tr: np.std(tr._data) )
TraceMethodCtrl.register(Trace_FixedDT, 'var',    lambda tr: np.var(tr._data) )
TraceMethodCtrl.register(Trace_FixedDT, 'rms',    lambda tr: np.sqrt(np.mean(tr._data**2)) )

# For VariableDT traces
def variableDTMean(tr):
    # Calculate the mean with simpsons rule:
    integral = scipy.integrate.simps(y = tr._data.magnitude,x= tr._time.rescale('s').magnitude ) 
    mean = integral / tr.getDuration().rescale('s').magnitude * tr._data.units
    #mean_safe = tr.convert_to_fixed(unit("0.1:ms")).mean()
    #print mean_safe, mean
    #if np.fabs(mean-mean_safe) 
    #assert False, 'Check this'
    return mean

TraceMethodCtrl.register(Trace_VariableDT, 'mean', variableDTMean)
# MISSING: VariableDT - stddev
# MISSING: VariableDT - var
# MISSING: VariableDT - rms

# For Piecewise functions:
# MISSING: Piecewise - stddev
# MISSING: Piecewise - var
# MISSING: Piecewise - rms




# PTP Functions:
################
TraceMethodCtrl.register(Trace_FixedDT,    'ptp',  lambda tr: np.ptp(tr._data) )
TraceMethodCtrl.register(Trace_VariableDT, 'ptp',  lambda tr: np.ptp(tr._data) )
TraceMethodCtrl.register(Trace_Piecewise,  'ptp',  lambda tr: tr.max[1] - tr.min[1] )




# Min & Max functions: 
######################
#These also return the times of min/max:
def getMax(tr):
    indMax = np.argmax(tr._data)
    return tr._time[indMax], tr._data[indMax] 

def getMin(tr):
    indMin = np.argmin(tr._data)
    return tr._time[indMin], tr._data[indMin]

TraceMethodCtrl.register(Trace_FixedDT, 'max', getMax)
TraceMethodCtrl.register(Trace_FixedDT, 'min', getMin)
TraceMethodCtrl.register(Trace_VariableDT, 'max', getMax)
TraceMethodCtrl.register(Trace_VariableDT, 'min', getMin)
# MISSING: Piecewise - min
# MISSING: Piecewise - max







# Gradients:
############
def gradientFixed(self, *args):
    assert False, 'ToCheck'
    return CloneTrace(tr=self, data=np.gradient(self._data.magnitude, *args) * self._data.units / self.getDTNew(), comment='+ (Filtered)')

TraceMethodCtrl.register(Trace_FixedDT, 'gradient', gradientFixed)
# MISSING: VariableDT - gradient
# MISSING: Piecewise - gradient








# Some aliases:
###############
TraceMethodCtrl.register(Trace_FixedDT, 'Mean', lambda tr: tr.mean() )
TraceMethodCtrl.register(Trace_VariableDT, 'Mean', lambda tr: tr.mean() )
TraceMethodCtrl.register(Trace_Piecewise, 'Mean', lambda tr: tr.mean() )
