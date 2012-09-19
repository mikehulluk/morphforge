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

import numpy
from morphforge.traces.eventset import EventSet
from morphforge.traces.eventset import Event


# TODO: THIS IS PAINFULLY SLOW!

class NewSpike(Event):

    def __init__(self, time):
        super(NewEvent, self).__init__(time=time)
        


class SpikeFinder(object):

    @classmethod
    def find_spikes(cls, trace, crossingthresh=0, firingthres=None):
        s = SpikeFinderThreshCross(trace=trace,
                                   crossingthresh=crossingthresh,
                                   firingthres=firingthres)

        return EventSet([spike.get_peak_time() for spike in s.spikes])


class SpikeFinderThreshCross(object):

    def __init__(self, trace, crossingthresh=0, firingthres=None):
        self.trace = trace
        self.crossingthresh = crossingthresh

        # Get the crossing times:
        thresh_indices = self.find_threshold_crossings()

        # Make a spike for each one:
        self.spikes = [Spike(self.trace, threshInd,
                       firingthres=firingthres) for threshInd in
                       thresh_indices]

    def num_spikes(self):
        return len(self.spikes)

    def find_threshold_crossings(self):
        # t = self.trace.time

        d = self.trace._data.rescale('mV').magnitude

        above_zero = numpy.zeros(d.shape, dtype=int)
        above_zero[d > self.crossingthresh] = 1

        crossings = above_zero - numpy.roll(above_zero, 1)
        crossings[0] = 0
        rising_edge_ind = numpy.where(crossings == 1)[0]
        falling_edge_ind = numpy.where(crossings == -1)[0]

        # Do we strat above the threshold?
        if d[0] > self.crossingthresh:
            # Then ignore the first fall:
            falling_edge_ind = falling_edge_ind[1:]
        # Same for the final rising edge:
        if d[-1] > self.crossingthresh:
            # Then ignore the first fall:
            rising_edge_ind = rising_edge_ind[:-1]

        # print 'above-zero', above_zero
        # print 'crossings', crossings
        # print 'rising_edge_ind', rising_edge_ind
        # for i in rising_edge_ind:
        #    print i, self.trace._time[i]
        # print 'fallingEdgeInd', fallingEdgeInd
        # for i in fallingEdgeInd:
        #    print i, self.trace._time[i]

        # print 'fallingEdgeInd', falling_edge_ind

        assert len(rising_edge_ind) == len(falling_edge_ind)

        # t = range(d.shape[0])

        # pylab.figure()
        # pylab.plot(t, d)
        # pylab.plot(t, above_zero*100)
        # pylab.savefig("/home/michael/Desktop/temp.svg")

        thresh_indices = zip(rising_edge_ind, falling_edge_ind)

        # Some sanity checking:
        import itertools
        on_off = list(itertools.chain(*thresh_indices))
        assert on_off == sorted(on_off)
        # print on_off

        
        #print 'ThresIndices', thresh_indices
        thresh_indices = [ (a,b) for (a,b) in thresh_indices if (b-a)>2]

        return thresh_indices


class Spike(object):

    def get_peak_time(self):
        return self.trace._time[self.peakIndex]

    def get_peak_size(self):
        return self.trace._data[self.peakIndex]

    def __init__(self, trace, time_indices, firingthres=None):
        self.trace = trace
        self.thresIndices = time_indices
        self.firingthres = (firingthres if firingthres is not None else 0.0)

        self._peakIndex = None
        self._duration = None
        self._durInd = None

        #self.init_get_peak()
        #self.init_get_duration()

    @property
    def peakIndex(self):
        if self._peakIndex is None:
            self.init_get_peak()
        return self._peakIndex

    @property
    def duration(self):
        if self._duration is None:
            self.init_get_duration()
        return self._duration

    def init_get_peak(self):

        ## Old Version (v. slow):
        #d = numpy.copy(self.trace._data.rescale('mV').magnitude)
        #d[0:self.thresIndices[0]] = 0
        #d[self.thresIndices[1]:-1] = 0
        #self._peakIndex_old = numpy.argmax(d)


        # New Version:
        #self._peakIndex = numpy.argmax(self.trace._data.rescale('mV').magnitude[self.thresIndices[0]:self.thresIndices[1]] ) + self.thresIndices[0]
        self._peakIndex = numpy.argmax(self.trace._data[self.thresIndices[0]:self.thresIndices[1]] ) + self.thresIndices[0]

        ## Check for same result:
        #print 'thresh-indices',self.thresIndices 
        #print 'old/new peak index', self._peakIndex, self._peakIndex_old
        #assert self._peakIndex == self._peakIndex_old, 'Peak indices are not the same: (%s) vs (%s)' % (self._peakIndex,self._peakIndex_old)


    def init_get_duration(self):
        ''' Calculates the duration of the spike at the 50% line (halfway between spike-max and 'firingthres' '''
        assert False, 'depreacted Auguest 2012'


        # OLD: V. slow:
        self.fiftyPCLine = (self.trace._data.rescale('mV').magnitude[self.peakIndex] + self.firingthres) / 2.0

        d = numpy.copy(self.trace._data.rescale('mV').magnitude)

        d[0:self.thresIndices[0]] = 0
        d[self.thresIndices[1]:-1] = 0

        above50_pc = numpy.zeros(d.shape, dtype=int)
        above50_pc[d > self.fiftyPCLine] = 1

        crossings = above50_pc - numpy.roll(above50_pc, 1)
        rising_edge_ind = numpy.where(crossings == 1)
        falling_edge_ind = numpy.where(crossings == -1)

        assert len(rising_edge_ind) == len(falling_edge_ind) == 1

        self._durInd = rising_edge_ind, falling_edge_ind
        self._duration = (self.trace._time[falling_edge_ind] - self.trace._time[rising_edge_ind]).rescale('ms').magnitude
        #self.duration = self.duration.rescale('ms').magnitude


        ## New:
        #self.fiftyPCLine = (self.trace._data.rescale('mV').magnitude[self.peakIndex] + self.firingthres.rescale('mV')) / 2.0
        ##t_short = self.trace._time[ self.thresIndices[0]:self.thresIndices[1] ]
        #d_short = self.trace._data.rescale('mV').magnitude[ self.thresIndices[0]:self.thresIndices[1] ]

        #d_sub = d_short > self.fiftyPCLine
        #crossings = d_sub - numpy.roll(d_sub, 1)

        ##crossings = above50_pc - numpy.roll(above50_pc, 1)
        #new_rising_edge_ind = numpy.where(crossings == 1) + self.thresIndices[0]
        #new_falling_edge_ind = numpy.where(crossings == -1) + self.thresIndices[0]

        #assert len(new_rising_edge_ind) == len(new_falling_edge_ind) == 1

        ## Check they are the same:
        #print 'old', rising_edge_ind, falling_edge_ind
        #print 'new', new_rising_edge_ind, new_falling_edge_ind
        #assert (rising_edge_ind == new_rising_edge_ind).all()
        #assert (falling_edge_ind == new_falling_edge_ind).all()

        ##self.durInd = rising_edge_ind, falling_edge_ind
        ##self.duration = self.trace._time[falling_edge_ind] - self.trace._time[rising_edge_ind]
        ##self.duration = self.duration.rescale('ms').magnitude



    def add_to_axes(self, ax):
        assert False, 'depreacted Auguest 2012'
        t = self.trace._time
        d = self.trace._data.rescale('mV').magnitude

        # 50% Line:
        ax.plot((t[self.durInd[0]], t[self.durInd[1]]), (self.fiftyPCLine, self.fiftyPCLine), 'k--')

        # Peak Line:
        ax.plot((t[self.peakIndex], t[self.peakIndex]), (self.fiftyPCLine, d[self.peakIndex]), 'k:')


        # Annotate Plot
        print (t[self.peakIndex], d[self.peakIndex], self.duration, self.firingthres)
        print
        annot_str = """Time:%2.2fms \nPeak: %2.2f mV \nDur: %2.2f ms\n(ThresVoltage: %2.2f)""" % (t[self.peakIndex], d[self.peakIndex], self.duration, self.firingthres)
        ax.annotate(annot_str, xy=(t[self.peakIndex] + 2, d[self.peakIndex] - 10), xytext=None, xycoords='data', textcoords='data', arrowprops=None)

