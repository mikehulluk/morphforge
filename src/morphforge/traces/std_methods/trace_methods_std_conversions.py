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
from morphforge.traces.trace_methods_ctrl import CloneTrace, CopyTraceAttrs
from morphforge.traces.trace_methods_ctrl import TraceMethodCtrl
from morphforge.traces import Trace_FixedDT, Trace_VariableDT, Trace_Piecewise
from MMtrace_conversion import TraceConverter, TraceApproximator


# Conversion to: FixedDT:
#########################
TraceMethodCtrl.register(Trace_FixedDT,     'convert_to_fixed', lambda tr,dt: CopyTraceAttrs(trOld=tr, trNew=TraceConverter.RebaseToFixedDT(tr,dt) ) )
TraceMethodCtrl.register(Trace_VariableDT,  'convert_to_fixed', lambda tr,dt: CopyTraceAttrs(trOld=tr, trNew=TraceConverter.RebaseToFixedDT(tr,dt) ) )
TraceMethodCtrl.register(Trace_Piecewise,   'convert_to_fixed', lambda tr,dt: CopyTraceAttrs(trOld=tr, trNew=TraceConverter.RebaseToFixedDT(tr,dt) ) )


# Conversion to VariableDT:
###########################
TraceMethodCtrl.register(Trace_FixedDT,     'convert_to_variable', lambda tr: CopyTraceAttrs(trOld=tr, trNew=TraceConverter.reduce_to_variable_dt_trace() ) )
TraceMethodCtrl.register(Trace_VariableDT,  'convert_to_variable', lambda tr: CopyTraceAttrs(trOld=tr, trNew=TraceConverter.reduce_to_variable_dt_trace() ) )
# MISSING: PIECEWISE


# Conversion to Piecewise:
##########################
TraceMethodCtrl.register(Trace_FixedDT, 'convert_to_piecewise', TraceApproximator.FitPiecewiseLinearTrace )
# MISSING: VariableDT
# MISSING: Piecewise







