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
from morphforge.traces.trace_methods_ctrl import TraceMethodCtrl
from morphforge.traces import Trace_FixedDT

import numpy as np
def fft(tr, normalise=True):
    ft = np.fft.fft( tr._data )
    if normalise:
        ft /= ft.max()
    ftfreq = np.fft.fftfreq( tr._data.size, tr.getDTNew().rescale("s").magnitude )
    return ftfreq, ft
    

def psd(tr, normalise=True):
    ft = np.fft.fft( tr._data )
    ft = ft.real()**2 + ft.imag()**2
    if normalise:
        ft /= ft.max()
        
    ftfreq = np.fft.fftfreq( tr._data.size, tr.getDTNew().rescale("s").magnitude )
    return ftfreq, ft   
    
            
TraceMethodCtrl.register(Trace_FixedDT, 'fft', fft, can_fallback_to_fixed_trace=True )

TraceMethodCtrl.register(Trace_FixedDT, 'psd', fft, can_fallback_to_fixed_trace=True )
