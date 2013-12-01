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

import numpy as np

from morphforge.traces.tracetypes.tracepointbased import TracePointBased

import scipy
import scipy.interpolate
#import numpy as np

class TraceFixedDT(TracePointBased):

    @classmethod
    def is_array_fixed_dt(cls, time_array):
        time_steps = np.diff(time_array.rescale('ms').magnitude)
        if np.ptp(time_steps) > 0.01:
            return False
        return True

    def __init__(self, time, data, name=None, comment=None, tags=None):
        super(TraceFixedDT, self).__init__(time=time, data=data, name=name, comment=comment, tags=tags)

        # Check we actually have an array with a fixed timestep:
        if not TraceFixedDT.is_array_fixed_dt(time):
            raise ValueError('A trace with a fixed dt was created, but has a non-constant time step was detected')

        assert self.get_n() >= 2, 'Points Based Trace has less than 2 points: %d' % self.get_n()

    def get_dt_new(self):
        return self._time[1] - self._time[0]

    def __str__(self):
        return 'TraceFixedDT: ' + self.name + ' Shape:'  + str(self._time.shape)




    # TO MOVE:
    def simplify(self, npoints):

        
        def moving_average(a, n=3) :
            ret = np.cumsum(a, dtype=float)
            return (ret[n - 1:] - ret[:1 - n]) / n


        t = self.time_pts_ms
        d = self.data_pts_np

        d_interpolator =  scipy.interpolate.interp1d(t, d, kind='linear')


        # Take the absolute value of the second derivative, which tells us
        # where the curve changes the most:
        d_dd = np.fabs(np.gradient(np.gradient(d) ) )


        # Process the gradients:
        # 1. Filter it:
        filter_len = 13
        fil = np.ones( (filter_len,) ) / filter_len
        d_dd = np.convolve(d_dd, fil ,'same' ) 

        # 2. Sqrt it, to reduce the effects of the peaks:
        d_dd = np.sqrt(d_dd)

        # 3. Add 10% of its value 'all-over'. This helps ensure that we
        # get a distrubtion of points all over the curve, not just at the 
        # regions of high change:
        tot = np.trapz(d_dd) / t.shape[0]
        d_dd = d_dd + 0.1 * tot
        
        # Now, convert this 'pdf' into a cdf so we can sample points from it:
        cn = np.cumsum(d_dd)
        cn /= cn[-1]

        # Make sure ends are clamped at 0,1:
        cn[0] = 0.0
        cn[-1] = 1.0

        # Sample from the cdf:
        sample_pts = np.linspace(0.0,1.0,num=100)
        interp_pts = scipy.interpolate.interp1d(cn, t, kind='linear')
        new_times = interp_pts(sample_pts)
        new_data = d_interpolator(new_times)


        from tracevariabledt import TraceVariableDT
        import quantities as pq


        return TraceVariableDT(
                time=new_times * pq.ms, 
                data=new_data*self.data_unit,
                name=self.name, 
                comment=self.comment,
                tags=self.tags)
        #ax1.plot( new_times, new_data,'o',)
        #ax1.plot( new_times, new_times*0.-55.,'o',)


        #ax4.plot( new_times, new_data,)
        #pylab.show()


