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

import mredoc

class cached_functor(object):

    """ Since we only want functors to return a single object, this 
        decorator is able to cache the output results """

    def __init__(self, func):
        self._functor = func
        self.res = {}

    def __call__(self, *args, **kwargs):
        kwargstuple = tuple(sorted(kwargs.iteritems()))
        key = (args, kwargstuple)

            # Cache if not run already:
        if not key in self.res:
            self.res[key] = self._functor(*args, **kwargs)

            # Return the cached result:
        return self.res[key]


class ChannelLibrary(object):

    _channels = dict()

    @classmethod
    def register_channel(
        cls,
        channeltype,
        chl_functor,
        modelsrc=None,
        celltype=None,
        ):
        assert modelsrc or celltype
        key = (modelsrc, celltype, channeltype)
        assert not key in cls._channels
        cls._channels[key] = chl_functor

    @classmethod
    def get_channel_functor(cls, channeltype, modelsrc=None, celltype=None):
        return cls._channels[(modelsrc, celltype, channeltype)]

    @classmethod
    def get_channel( cls, channeltype, env, modelsrc=None, celltype=None,):
        functor = cls._channels[(modelsrc, celltype, channeltype)]
        return functor(env=env)


    @classmethod
    def summary_table(cls, ):
        summary_data = []
        for ((modelsrc,celltype, channel_type), functor) in sorted(cls._channels.iteritems()):
            summary_data.append( ( modelsrc, celltype, channel_type ))# , functor.__file__)
        summary_table = mredoc.VerticalColTable( ('Model','CellType','Channel-Type'), summary_data)
        return mredoc.Section('Channel Library Summary', summary_table )


