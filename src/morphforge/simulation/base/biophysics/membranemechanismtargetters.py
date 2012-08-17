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
        return 'PassiveDefault'


class PassiveTargeter_Everywhere(Targeter):

    def get_priority(self):
        return 5

    def does_target_section(self, section):
        return True

    def get_description(self):
        return 'PassiveDefault'


class PassiveTargeter_Region(Targeter):

    def __init__(self, region):
        self.region = region

    def get_priority(self):
        return 10

    def does_target_section(self, section):
        return section.region == self.region

    def get_description(self):
        return 'Passive-Region:%s' % self.region.name


class MembraneMechanismTargeter_Everywhere(Targeter):

    def get_priority(self):
        return 10

    def does_target_section(self, section):
        return True

    def get_description(self):
        return 'MM-Everywhere'


class MembraneMechanismTargeter_Region(Targeter):

    def __init__(self, region):
        self.region = region

    def get_priority(self):
        return 20

    def does_target_section(self, section):
        return section.region == self.region

    def get_description(self):
        return 'MM-Region: %s' % self.region.name


class MembraneMechanismTargeter_SectionPath(Targeter):

    def get_priority(self):
        return 30

    def does_target_section(self, section):
        assert False

    def get_description(self):
        return 'MM-SectionPath: ??'


class MembraneMechanismTargeter_Section(Targeter):

    def __init__(self, section):
        self.section = section

    def get_priority(self):
        return 40

    def does_target_section(self, section):
        return self.section == section

    def get_description(self):
        section_desc = (self.section.idtag if self.section.idtag else '[No idtag]')
        return 'MM-Section: %s' % section_desc


