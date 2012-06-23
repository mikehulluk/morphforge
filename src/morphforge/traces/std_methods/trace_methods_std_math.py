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
from morphforge.traces.trace_methods_ctrl import TraceMethodCtrl, clone_trace
from morphforge.traces import Trace_FixedDT, Trace_VariableDT, Trace_Piecewise
import numpy as np





# Mean, rms, stddev, variance functions:
##############################

# For FixedDT traces, these are simple:
TraceMethodCtrl.register(Trace_FixedDT, 'mean',   lambda tr: np.mean(tr._data) )
TraceMethodCtrl.register(Trace_FixedDT, 'stddev', lambda tr: np.std(tr._data) )
TraceMethodCtrl.register(Trace_FixedDT, 'var',    lambda tr: np.var(tr._data) )
TraceMethodCtrl.register(Trace_FixedDT, 'rms',    lambda tr: np.sqrt(np.mean(tr._data**2)) )

# For VariableDT traces
def _variabledt_mean(tr):
    import scipy.integrate
    # Calculate the mean with simpsons rule:
    integral = scipy.integrate.simps(y = tr._data.magnitude,x= tr._time.rescale('s').magnitude )
    mean = integral / tr.get_duration().rescale('s').magnitude * tr._data.units
    #mean_safe = tr.convert_to_fixed(unit("0.1:ms")).mean()
    #print mean_safe, mean
    #if np.fabs(mean-mean_safe)
    #assert False, 'Check this'
    return mean

TraceMethodCtrl.register(Trace_VariableDT, 'mean', _variabledt_mean)
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
def _get_max(tr):
    ind_max = np.argmax(tr._data)
    return tr._time[ind_max], tr._data[ind_max]

def _get_min(tr):
    ind_min = np.argmin(tr._data)
    return tr._time[ind_min], tr._data[ind_min]

TraceMethodCtrl.register(Trace_FixedDT, 'max', _get_max)
TraceMethodCtrl.register(Trace_FixedDT, 'min', _get_min)
TraceMethodCtrl.register(Trace_VariableDT, 'max', _get_max)
TraceMethodCtrl.register(Trace_VariableDT, 'min', _get_min)
# MISSING: Piecewise - min
# MISSING: Piecewise - max







# Gradients:
############
def _fixeddt_gradient(self, *args):
    #assert False, 'ToCheck'
    return clone_trace(tr=self, data=np.gradient(self._data.magnitude, *args) * self._data.units / self.get_dt_new(), comment='+ (Filtered)')

TraceMethodCtrl.register(Trace_FixedDT, 'gradient', _fixeddt_gradient)
# MISSING: VariableDT - gradient
# MISSING: Piecewise - gradient








# Some aliases:
###############
TraceMethodCtrl.register(Trace_FixedDT, 'Mean', lambda tr: tr.mean() )
TraceMethodCtrl.register(Trace_VariableDT, 'Mean', lambda tr: tr.mean() )
TraceMethodCtrl.register(Trace_Piecewise, 'Mean', lambda tr: tr.mean() )
