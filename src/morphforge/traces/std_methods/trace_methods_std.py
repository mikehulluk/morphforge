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
from morphforge.traces.trace_methods_ctrl import TraceMethodCtrl

import numpy as np
from morphforge.traces.tracetypes import Trace_VariableDT,Trace_Piecewise, Trace_FixedDT












def _get_piecewise_linear_points(tr):
    xUnit = tr._pieces[0].get_min_time().units
    yUnit = tr._pieces[0].get_start_value().units

    xPoints = []
    yPoints = []

    for p in tr._pieces:
        xPoints.append( float(p.get_min_time().rescale(xUnit).magnitude) )
        xPoints.append( float(p.get_max_time().rescale(xUnit).magnitude) )

        yPoints.append( float(p.get_start_value().rescale(yUnit).magnitude) )
        yPoints.append( float(p.get_end_value().rescale(yUnit).magnitude) )

    return np.array(xPoints) * xUnit, np.array(yPoints) * yUnit

# Plotting:
TraceMethodCtrl.register(Trace_FixedDT,    'plotpoints', lambda tr: (tr._time, tr._data) )
TraceMethodCtrl.register(Trace_VariableDT, 'plotpoints', lambda tr: (tr._time, tr._data) )
TraceMethodCtrl.register(Trace_Piecewise,  'plotpoints', _get_piecewise_linear_points)









