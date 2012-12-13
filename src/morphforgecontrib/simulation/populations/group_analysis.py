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

from morphforgecontrib.traces.tracetools import SpikeFinder
from morphforge.traces.eventset import EventSet
import itertools


class PopAnalSpiking(object):

    @classmethod
    def evset_nth_spike(cls, res, tag_selector, n, comment=None, comment_incl_nspikes=False, evset_tags=None, evset_name=None):
        comment = comment or ''

        if evset_tags is None:
            evset_tags = []
        evset_tags.extend( ['Spike', 'Event'] )

        traces = [trace for trace in res.get_traces()
                  if tag_selector(trace)]

        spike_list = [SpikeFinder.find_spikes(tr, crossingthresh=0,
                      firingthres=None) for tr in traces]
        spike_list = [spl[n] for spl in spike_list if len(spl) > n]

        comment = '%s (%dth Spike)' % (comment, n)

        if comment_incl_nspikes:
            comment += ' (NSpikes: %d'%len(spike_list)

        spikes = EventSet(spike_list, tags=evset_tags, name=evset_name, comment=comment)
        return spikes

    @classmethod
    def evset_first_spike(cls,  **kwargs):
        return cls.evset_nth_spike(n=0, **kwargs)


    @classmethod
    def evset_all_spikes(cls, res, tag_selector, comment=None, comment_incl_nspikes=False, evset_tags=None, evset_name=None):
        if evset_tags is None:
            evset_tags = []
        evset_tags.extend( ['Spike', 'Event'] )


        comment = comment or ''

        traces = [trace for trace in res.get_traces()
                  if tag_selector(trace)]

        spike_list = [SpikeFinder.find_spikes(tr, crossingthresh=0,
                      firingthres=None) for tr in traces]
        spike_list = list(itertools.chain(*spike_list) )

        comment='%s (All Spike)' if not comment else comment
        if comment_incl_nspikes:
            comment += ' (NSpikes: %d'%len(list(spike_list) )

        spikes = EventSet(spike_list, tags=evset_tags, comment=comment, name=evset_name)

        return spikes


