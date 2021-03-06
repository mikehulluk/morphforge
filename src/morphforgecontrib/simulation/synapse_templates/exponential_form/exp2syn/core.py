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

from morphforge.stdimports import units

class PostSynapticMech_Exp2Syn_Base(object):

    def __init__(self, tau_open, tau_close, e_rev, popening, peak_conductance, **kwargs):
        super(PostSynapticMech_Exp2Syn_Base, self).__init__( **kwargs)
        self._default_parameters = { 'tau_open':tau_open, 'tau_close':tau_close, 'e_rev':e_rev, 'popening':popening, 'peak_conductance':peak_conductance}

    @classmethod
    def get_variables(cls):
        return ['tau_open','tau_close', 'popening','e_rev', 'peak_conductance']

    @classmethod
    def get_preferred_unit(cls, varname):


        _units = {
                'tau_open': units.ms,
                'tau_close': units.ms,
                'popening': units.dimensionless,
                'e_rev': units.mV,
                'peak_conductance': units.nS,
                }
        return _units[varname]

    def get_defaults(self):
        return self._default_parameters

    def get_summary_description(self, instance):
        return "Exp2Syn (onto %s)" % instance.cell_location.get_location_description_str()

