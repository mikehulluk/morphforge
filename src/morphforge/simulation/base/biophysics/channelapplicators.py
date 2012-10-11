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


class ChannelApplicator(object):

    def __init__(self,):
        super(ChannelApplicator, self).__init__()
        self.target_channel = None

    def set_target_channel(self, target_channel):
        assert self.target_channel is None
        self.target_channel = target_channel

        # Check that everything that is over-ridden actually exists:
        for varname in self.get_variables_overriden():
            assert varname in self.target_channel.get_variables(), 'unexpected setting of %s' % varname


    def get_variable_value_for_section(self, variablename, section):
        raise NotImplementedError()

    def get_description(self):
        raise NotImplementedError()

    def get_variables_overriden(self):
        raise NotImplementedError()


class ChannelApplicatorUniform(ChannelApplicator):

    def __init__(self,  parameter_multipliers=None, parameter_overrides=None):
        super(ChannelApplicatorUniform, self).__init__()
        self._parameter_multipliers =  parameter_multipliers or {}
        self._parameter_overrides = parameter_overrides or {}

        # Check  no parameters are specified twice:
        duplicate_defs = set(self._parameter_multipliers.keys()) & set(self._parameter_overrides.keys())
        assert len(duplicate_defs) == 0, 'Ambiguity: Parameter specified twice: %s' % duplicate_defs


    def get_variables_overriden(self):
        return set(self._parameter_multipliers.keys()) | set(self._parameter_overrides.keys())


    def get_variable_value_for_section(self, variable_name, section):

        assert not ( variable_name in self._parameter_multipliers and  variable_name in self._parameter_overrides)

        if variable_name in self._parameter_multipliers:
            return self._parameter_multipliers[variable_name] * self.target_channel.get_default(variable_name)
        if variable_name in self._parameter_overrides:
            return self._parameter_overrides[variable_name]
        return self.target_channel.get_default(variable_name)


    def get_description(self):
        s1 = 'Uniform Applicator: '
        s2 = ('Overrides:{%s} ' % (','.join( [ "%s=%s" % (key,value) for (key,value) in self._parameter_overrides.iteritems()] )) ) if self._parameter_overrides else ''
        s3 = ('Multipliers:{%s} ' % (','.join( [ "%s=%s" % (key,value) for (key,value) in self._parameter_multipliers.iteritems()] )) ) if self._parameter_multipliers else ''
        return (s1 + s2 + s3).strip()



