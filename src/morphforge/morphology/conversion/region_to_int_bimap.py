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


class RegionToIntMapBiMap(object):

    def __init__(self):
        self.regionname2int = {}
        self.int2regionname = {}

    def add_mapping(self, regionname, int):
        assert not regionname in self.regionname2int
        assert not int in self.int2regionname
        self.regionname2int[regionname] = int
        self.int2regionname[int] = regionname

    def int_to_region_name(self, int):
        return self.int2regionname[int]

    def region_name_to_int(self, regionname):
        return self.regionname2int[regionname]


class AutoRegionToIntMapTable(RegionToIntMapBiMap):

    def __init__(self):
        RegionToIntMapBiMap.__init__(self)

        # Add the standard SWC conversions:
        self.add_mapping(regionname=None, int=0)
        from morphforge.morphology import conventions
        for (name, number) in conventions.SWCRegionCodes.name2number.iteritems():
            self.add_mapping(name, number)

    def int_to_region_name(self, int):

        if not int in self.int2regionname:
            self.add_mapping(regionname='AutoRegion%d' % int, int=int)
        return RegionToIntMapBiMap.int_to_region_name(self, int)

    def region_name_to_int(self, regionname):
        if not regionname in self.regionname2int:
            self.add_mapping(regionname=regionname, int=len(self.int2regionname))
        return RegionToIntMapBiMap.region_name_to_int(self,regionname)
