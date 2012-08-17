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


class SummariserLibrary(object):

    summarisers = {}

    @classmethod
    def register_summariser(cls, channel_baseclass, summariser_class):
        # Check it has a to_report_lab Method:
        # Todo: Replace this with 'hasattr'
        assert 'to_report_lab' in summariser_class.__dict__

        # Add it to the dictionary of summarisers:
        cls.summarisers[channel_baseclass] = summariser_class

    @classmethod
    def get_summarisier(cls, obj):
        possible_summarisers = []
        for (ChlType, summarisier) in SummariserLibrary.summarisers.iteritems():
            if issubclass(type(obj), ChlType):
                possible_summarisers.append(summarisier)

        if len(possible_summarisers) == 0:
            return None
        if len(possible_summarisers) == 1:
            return possible_summarisers[0]
        else:
            assert False, 'I have to many options for summarising: ' \
                + str(obj)


