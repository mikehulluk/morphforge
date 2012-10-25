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


class PostSynapticMech_Exp2SynNMDA_Base(object):

    def __init__(self, tau_open, tau_close, e_rev, popening, peak_conductance, eta=None, mg2conc=None, gamma=None, vdep=True, **kwargs):

        # TODO: THESE SHOULD BE SPECIFIED, and should not default:

        if gamma is None:
            gamma = 0.08 * units.per_mV
        if eta is None:
            eta = 0.1 * units.per_mM
        if mg2conc is None:
            mg2conc= 0.5 * units.mM


        super(PostSynapticMech_Exp2SynNMDA_Base, self).__init__( **kwargs)
        self._default_parameters = { 'vdep':vdep, 'tau_open':tau_open, 'tau_close':tau_close, 
                'e_rev':e_rev, 'popening':popening, 'peak_conductance':peak_conductance, 'eta':eta, 'gamma':gamma, 'mg2conc':mg2conc}


    def get_preferred_unit(cls, varname):
        _units = {
                'tau_open': units.ms,
                'tau_close': units.ms,
                'popening': units.dimensionless,
                'e_rev': units.mV,
                'peak_conductance': units.nS,
                'gamma': (1/units.mV),
                'eta': (1/units.mM),
                'mg2conc': units.mM,
                'vdep':units.dimensionless,
                }
        return _units[varname]

    @classmethod
    def get_variables(cls):
        return [ 'tau_open', 'tau_close', 'popening', 'e_rev', 'vdep',
                 'peak_conductance', 'gamma', 'eta', 'mg2conc', ]

