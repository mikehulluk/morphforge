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
from morphforgecontrib.traces.tracetools import SpikeFinder
from morphforge.traces.eventset import EventSet
import itertools



class PopAnalSpiking(object):


    @classmethod
    def EvSetNthSpike(cls, res, tag_selector, n, comment=None ):
        comment = comment or ""

        traces = [ trace for trace in res.get_traces() if tag_selector( trace ) ]

        spikeList = [SpikeFinder.find_spikes(tr, crossingthresh=0,  firingthres=None) for tr in traces]
        spikeList = [ spl[n] for spl in spikeList if len(spl) > n ]
        spikes = EventSet(spikeList, tags=['Spike','Event'], comment="%s (%d Spike)"%(comment,n) )
        return spikes


    @classmethod
    def EvSetFirstSpike(cls, res, tag_selector, comment=None ):
        return cls.EvSetNthSpike( res=res, tag_selector=tag_selector, n=0, comment=comment, )



    @classmethod
    def EvSetAllSpikes(cls, res, tag_selector, comment=None):
        comment = comment or ""

        traces = [ trace for trace in res.get_traces() if tag_selector( trace ) ]

        spikeList = [SpikeFinder.find_spikes(tr, crossingthresh=0,  firingthres=None) for tr in traces]
        spikeList = itertools.chain(*spikeList)
        spikes = EventSet(spikeList, tags=['Spike','Event'], comment="%s (All Spike)"%(comment) )
        return spikes
