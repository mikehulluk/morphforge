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

import itertools
import numpy as np
from morphforge.constants.standardtags import StandardTags


class Event(object):

    def __init__(self, time):
        time.rescale('ms')
        self.time = time

    def get_time(self):
        return self.time


class EventSet(object):

    @classmethod
    def combine_sets(cls, eventsets, tags=None, comment=None, name=None):
        """ If 'tags' is none, then take 'communal' tags """

        # Rewritten on August 2012 
        if tags is None:
            # Find tags common to all sets:
            tags = eventsets[0].tags.intersection(*[evset.tags for evset in eventsets])
        #if not tags:
        #    communal_tags = None
        #    for ev_set in eventsets:
        #        communal_tags = set(ev_set.tags) if communal_tags is None else communal_tags & set(ev_set.tags)
        #    tags = communal_tags

        return EventSet(itertools.chain(*eventsets), tags=tags, comment=comment, name=name)



    def __init__(self, events=None, name=None, comment=None, tags=None,):
        print events, type(events)


        if events is None:
            events = []

        self.events = [(Event(event) if not isinstance(event, Event) else event) for event in events ]

        self._tags = set( ( tags if tags is not None else [StandardTags.Event] ) )
        self.name = name if name else '<Unnamed EventSet>'
        self.comment = comment if comment else "UnknownSrcEventSet"
        self._tags.add('Event')

    def __len__(self):
        return len(self.events)

    def __getitem__(self, i):
        return self.events[i]

    def __iter__(self):
        return iter(self.events)

    def add_event(self, ev):
        if ev is None:
            return
        self.events.append(ev)

    # Iterators:
    @property
    def times(self):
        for event in self.events:
            yield event.get_time()

    @property 
    def tags(self):
        return self._tags

    def summarise_timings_in_comment(self):
        times_a = np.array([float(time.rescale('ms').magnitude) for time in self.times])
        self.comment = '%d Mean: %2.2f ms (Std:%2.2f ms)' % (len(self), np.mean(times_a), np.std(times_a))


    def times_in_np_array_ms(self):
        return np.array( [ float(t.rescale('ms') ) for t in self.times] )


