#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
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
from morphforge.core.quantities import unit

import numpy as np

import quantities as pq


from tracePointBased import Trace_PointBased

class Trace_FixedDT(Trace_PointBased):


    @classmethod
    def is_array_fixed_dt(cls, time_array):
        d = np.diff(time_array.rescale('ms').magnitude)
        if np.ptp(d) > 0.01:
            return False
        return True


    def __init__(self, time, data, name=None, comment=None, tags=None):
        super(Trace_FixedDT, self).__init__(time=time, data=data, name=name, comment=comment, tags=tags)

        # Check we actually have an array with a fixed timestep:
        if not Trace_FixedDT.is_array_fixed_dt(time):
            raise ValueError('A trace with a fixed dt was created, but has a non-constant time step was detected')

        assert self.get_n() >= 2, 'Points Based Trace has less than 2 points: %d' % self.get_n()

    def get_dt_new(self):
        return self._time[1] - self._time[0]

    def __str__(self):
        return "Trace_FixedDT: " + self.name + " Shape:" + str(self._time.shape)





    def __getitem__(self, time):

        if isinstance(time, tuple):
            assert len(time) == 2
            start = unit(time[0])
            stop = unit(time[1])

            if start < self._time[0]:
                assert False, 'Time out of bounds'
            if stop > self._time[-1]:
                assert False, 'Time out of bounds'


            #print start
            #print stop
            mask = np.logical_and((start < self._time), (self._time < stop))
            #print  np.nonzero(mask)[0]
            if len(np.nonzero(mask)[0]) < 2:
                assert False
            return Trace_FixedDT(time=self._time[ np.nonzero(mask)[0] ],
                                  data=self._data[ np.nonzero(mask)[0] ]
                          )


        assert isinstance(time, pq.quantity.Quantity), "Times Shoudl be quanitity. Found: %s %s"%(time, type(time) )
        # Rebase the Time:
        time.rescale(self._time.units)
        interpolator = interp1d(self._time.magnitude, self._data.magnitude)
        d_mag = interpolator(time.magnitude)
        return d_mag * self._data.units






