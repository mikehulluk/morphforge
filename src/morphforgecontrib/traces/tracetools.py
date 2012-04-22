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
import numpy
from morphforge.traces.eventset import EventSet
from morphforge.traces.eventset import Event


class NewSpike( Event):
    def __init__(self, time):
        NewSpike.__init__(self, time)
        
        
class SpikeFinder(object):
    
    @classmethod
    def find_spikes(cls, trace, crossingthresh=0,  firingthres=None ):
        s = SpikeFinderThreshCross(trace=trace, crossingthresh=crossingthresh,  firingthres=firingthres )
        
        return EventSet( [spike.getPeakTime() for spike in s.spikes] )
    
    








class SpikeFinderThreshCross(object):
    
    
    def __init__(self, trace, crossingthresh=0, firingthres=None):
        self.trace = trace
        self.crossingthresh = crossingthresh
        
        #Get the crossing times:
        threshIndices = self.findThresCrossings()
    
        # Make a spike for each one:
        self.spikes = [ Spike(self.trace, threshInd, firingthres=firingthres) for threshInd in threshIndices]
        
    def NumSpikes(self):
        return len(self.spikes)   
        
        
    def findThresCrossings(self):
        #t = self.trace.time
        d = self.trace._data.rescale("mV").magnitude
        
        aboveZero = numpy.zeros(d.shape, dtype=int)
        aboveZero[d > self.crossingthresh] = 1
        
        crossings = aboveZero - numpy.roll(aboveZero, 1)
        risingEdgeInd = numpy.where(crossings == 1)[0]  
        fallingEdgeInd = numpy.where(crossings == -1)[0]
        
        assert len(risingEdgeInd) == len(fallingEdgeInd)
        
        # Do we strat above the threshold?
        if d[0] < self.crossingthresh:
            # Then ignore the first fall:
            fallingEdgeInd = fallingEdgeInd[1:] 
            
        
        threshIndices = zip(risingEdgeInd, fallingEdgeInd) 


        return threshIndices
        
        


class Spike(object):
    
    def getPeakTime(self):
        return self.trace._time[self.peakIndex]
    
    def getPeakSize(self):
        return self.trace._data[self.peakIndex]
    
    def __init__(self, trace, timeIndices, firingthres=None):
        self.trace = trace
        self.thresIndices = timeIndices
        self.firingthres = firingthres if firingthres is not None else 0.0
        
        self.init_getPeak()
        self.init_getDuration()
        
    def init_getPeak(self):
        d = numpy.copy(self.trace._data)
        d[ 0:self.thresIndices[0] ] = 0
        d[ self.thresIndices[1]:-1] = 0
        self.peakIndex = numpy.argmax(d) 
        
    
    
    def init_getDuration(self):
        
        self.fiftyPCLine = (self.trace._data.rescale("mV").magnitude[ self.peakIndex] + self.firingthres) / 2.0  
        
        d = numpy.copy(self.trace._data.rescale("mV").magnitude)
        
        d[ 0:self.thresIndices[0] ] = 0
        d[ self.thresIndices[1]:-1] = 0
        
        above50PC = numpy.zeros(d.shape, dtype=int)
        above50PC[d > self.fiftyPCLine] = 1
        
        crossings = above50PC - numpy.roll(above50PC, 1)
        risingEdgeInd = numpy.where(crossings == 1)  
        fallingEdgeInd = numpy.where(crossings == -1)  
        
        assert len(risingEdgeInd) == len(fallingEdgeInd) == 1
        
        self.durInd = risingEdgeInd, fallingEdgeInd
        self.duration = self.trace._time[fallingEdgeInd] - self.trace._time[risingEdgeInd]
        self.duration = self.duration.rescale("ms").magnitude
        
    def addToAxes(self, ax):
        t = self.trace._time
        d = self.trace._data.rescale("mV").magnitude
        
        # 50% Line:
        ax.plot((t[self.durInd[0]], t[self.durInd[1]]), (self.fiftyPCLine, self.fiftyPCLine), 'k--')

        # Peak Line:
        ax.plot((t[self.peakIndex], t[self.peakIndex]), (self.fiftyPCLine, d[self.peakIndex]), 'k:')

        
        # Annotate Plot
        print (t[self.peakIndex], d[self.peakIndex], self.duration, self.firingthres)
        print
        annotStr = """Time:%2.2fms \nPeak: %2.2f mV \nDur: %2.2f ms\n(ThresVoltage: %2.2f)""" % (t[self.peakIndex], d[self.peakIndex], self.duration, self.firingthres)
        ax.annotate(annotStr, xy=(t[self.peakIndex] + 2, d[self.peakIndex] - 10), xytext=None, xycoords='data', textcoords='data', arrowprops=None)

