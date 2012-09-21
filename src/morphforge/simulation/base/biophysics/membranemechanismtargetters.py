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

from morphforge.morphology.core import Region

class Targeter(object):

    def get_priority(self):
        raise NotImplementedError()

    def does_target_section(self, section):
        raise NotImplementedError()

    def get_description(self):
        raise NotImplementedError()


class PassiveTargeter_EverywhereDefault(Targeter):

    def get_priority(self):
        return 0

    def does_target_section(self, section):
        return True

    def get_description(self):
        return 'Default'


class PassiveTargeter_Everywhere(Targeter):

    def get_priority(self):
        return 5

    def does_target_section(self, section):
        return True

    def get_description(self):
        return 'Everywhere'


class PassiveTargeter_Region(Targeter):

    def __init__(self, region):
        super(PassiveTargeter_Region, self).__init__()
        self.region = region

    def get_priority(self):
        return 10

    def does_target_section(self, section):
        return section.region == self.region

    def get_description(self):
        return 'Passive-Region:%s' % self.region.name


class ChannelTargeterEverywhere(Targeter):

    def get_priority(self):
        return 10

    def does_target_section(self, section):
        return True

    def get_description(self):
        return 'Everywhere'


class ChannelTargeterRegion(Targeter):

    def __init__(self, region):
        super(ChannelTargeterRegion, self).__init__()
        self.region = region

    def get_priority(self):
        return 20

    def does_target_section(self, section):
        if isinstance(self.region, Region):
            return section.region == self.region
        elif isinstance(self.region, basestring):
            return section.region.name == self.region
        else:
            assert False

    def get_description(self):
        if isinstance(self.region, Region):
            region_name = self.region.name
        elif isinstance(self.region, basestring):
            region_name = self.region
        else:
            assert False
        return 'Region: %s' % region_name


class ChannelTargeterSectionPath(Targeter):

    def get_priority(self):
        return 30

    def does_target_section(self, section):
        assert False

    def get_description(self):
        return 'MM-SectionPath: ??'


class ChannelTargeterSection(Targeter):

    def __init__(self, section):
        super(ChannelTargeterSection, self).__init__()
        self.section = section

    def get_priority(self):
        return 40

    def does_target_section(self, section):
        return self.section == section

    def get_description(self):
        if self.section.idtag:
            section_desc = self.section.idtag
        else:
            section_desc = '[No idtag]'
        return 'Section: %s' % section_desc


