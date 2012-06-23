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
from morphforge.traces.trace import Trace
import quantities as pq
import numpy as np



class Trace_PointBased(Trace):

    def __init__(self, time, data, name=None, comment=None, tags=None):

        super(Trace_PointBased, self).__init__(name=name, comment=comment, tags=tags)

        if not isinstance(time, pq.quantity.Quantity):
            raise ValueError("Time is not a 'unit'ed quantity")
        time.rescale('ms').magnitude

        if not isinstance(data, (pq.quantity.Quantity, pq.Dimensionless)):
            raise ValueError("Data is not a 'unit'ed quantity")
        if not time.shape == data.shape:
            raise ValueError('Time and Data are different shapes! %s vs %s' % (time.shape, data.shape))

        self._time = time
        self._data = data

        assert self.get_n() >= 2, 'Points Based Trace has less than 2 points: %d' % self.get_n()



    def get_min_time(self):
        return self._time[0]

    def get_max_time(self):
        return self._time[-1]

    def get_values(self, timeArray):
        from scipy.interpolate.interpolate import interp1d
        timeUnits = self._time.units
        dataUnits = self._data.units
        interpolator = interp1d(self._time.magnitude, self._data.magnitude)
        return interpolator(timeArray.rescale(timeUnits).magnitude) * dataUnits





    def get_n(self):
        return len(self._time)


    def time_within_trace(self, times):
        t = times.rescale("ms").magnitude
        t0 = self.get_min_time().rescale("ms").magnitude
        t1 = self.get_max_time().rescale("ms").magnitude
        return np.logical_and( t>=t0, t<=t1 )
        #raise NotImplementedError()

