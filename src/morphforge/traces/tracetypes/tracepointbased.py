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

from morphforge.traces.tracetypes.trace import Trace
import quantities as pq
import numpy as np
from morphforge.core import unit


class TracePointBased(Trace):

    def __init__(self, time, data, name=None, comment=None, tags=None):

        super(TracePointBased, self).__init__(name=name,
                comment=comment, tags=tags)

        if not isinstance(time, pq.quantity.Quantity):
            raise ValueError("Time is not a 'unit'ed quantity")

        _dummy = time.rescale('ms').magnitude

        if not isinstance(data, (pq.quantity.Quantity, pq.unitquantity.Dimensionless)):
            raise ValueError("Data is not a 'unit'ed quantity")
        if not time.shape == data.shape:
            raise ValueError('Time and Data are different shapes! %s vs %s' % (time.shape, data.shape))

        self._time = time
        self._data = data

        assert self.get_n() >= 2, 'Points Based Trace has less than 2 points: %d' % self.get_n()


    @property
    def time_pts(self):
        return self._time

    @property
    def time_pts_np(self):
        return self._time.magnitude

    @property
    def time_pts_s(self):
        return self._time.rescale('s').magnitude

    @property
    def time_pts_ms(self):
        return self._time.rescale('ms').magnitude

    #@property
    def time_pts_in(self, rebase_unit):
        return self._time.rescale(rebase_unit).magnitude


    @property
    def data_pts(self):
        return self._data

    #@property
    def data_pts_in(self, rebase_unit):
        return self._data.rescale(rebase_unit).magnitude

    @property
    def data_pts_np(self):
        return self._data.magnitude

    @property
    def data_unit(self):
        #print 'in @prop:data_unit'
        return self._data.units

    @property
    def time_unit(self):
        return self._time.units

    def get_n(self):
        return len(self._time)

    # Conform to interface:
    # ############################

    def get_min_time(self):
        return self._time[0]

    def get_max_time(self):
        return self._time[-1]

    def get_values(self, time_array):
        from scipy.interpolate.interpolate import interp1d
        time_units = self._time.units
        data_units = self._data.units
        interpolator = interp1d(self._time.magnitude,
                                self._data.magnitude)
        return interpolator(time_array.rescale(time_units).magnitude) \
            * data_units
    # ##############################


    def __getitem__(self, time):
        from scipy.interpolate import interp1d
        from morphforge.traces.tracetypes.tracefixeddt import TraceFixedDT

        if isinstance(time, tuple):
            assert len(time) == 2
            start = unit(time[0])
            stop = unit(time[1])

            if start < self._time[0]:
                assert False, 'Time out of bounds'
            if stop > self._time[-1]:
                assert False, 'Time out of bounds'

            mask = np.logical_and(start < self.time_pts, self._time < stop)

            if len(np.nonzero(mask)[0]) < 2:
                assert False
            return TraceFixedDT(time=self._time[np.nonzero(mask)[0]],
                                data=self.data_pts[np.nonzero(mask)[0]])


        assert isinstance(time, pq.quantity.Quantity), "Times should be quantity. Found: %s %s"%(time, type(time))
        # Rebase the Time:
        time.rescale(self._time.units)
        interpolator = interp1d(self.time_pts_np,
                                self.data_pts_np)
        d_mag = interpolator(time.magnitude)
        return d_mag * self.data_unit

