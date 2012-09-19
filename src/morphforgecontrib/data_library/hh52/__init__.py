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

from morphforge.componentlibraries.channellibrary import ChannelLibrary, cached_functor
from morphforge.core.quantities.fromcore import unit
#from morphforge.core.misc import cached_functor
from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmleak import StdChlLeak
from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmalphabeta import StdChlAlphaBeta
from morphforgecontrib.data_library.stdmodels import StandardModels


@cached_functor
def get_sample_lk(env):
    lk_chl = env.Channel(StdChlLeak, name='LkChl',
            conductance=unit('0.3:mS/cm2'),
            reversalpotential=unit('-54.3:mV'),
            mechanism_id='HULL12_DIN_LK_ID')
    return lk_chl


@cached_functor
def get_sample_na(env):
    na_state_vars = { 'm': {
                          'alpha': [-4.00,-0.10,-1.00,40.00,-10.00],
                          'beta':  [4.00, 0.00, 0.00,65.00, 18.00]},
                    'h': {
                            'alpha': [0.07,0.00,0.00,65.00,20.00],
                            'beta':  [1.00,0.00,1.00,35.00,-10.00]}
                      }

    na_chl = env.Channel(
        StdChlAlphaBeta,
        name='NaChl',
        ion='na',
        equation='m*m*m*h',
        conductance=unit('120:mS/cm2'),
        reversalpotential=unit('50:mV'),
        statevars=na_state_vars,
        mechanism_id='HH_NA_CURRENT',
        )
    return na_chl


@cached_functor
def get_sample_k(env):
    kStateVars = {'n': {'alpha': [-0.55, -0.01, -1.00, 55.0, -10.00],
                  'beta': [0.125, 0, 0, 65, 80]}}
    k_chl = env.Channel(
        StdChlAlphaBeta,
        name='KChl',
        ion='k',
        equation='n*n*n*n',
        conductance=unit('36:mS/cm2'),
        reversalpotential=unit('-77:mV'),
        statevars=kStateVars,
        mechanism_id='HH_K_CURRENT',
        )
    return k_chl


ChannelLibrary.register_channel(modelsrc=StandardModels.HH52,
                                channeltype='Na',
                                chl_functor=get_sample_na)
ChannelLibrary.register_channel(modelsrc=StandardModels.HH52,
                                channeltype='K',
                                chl_functor=get_sample_k)
ChannelLibrary.register_channel(modelsrc=StandardModels.HH52,
                                channeltype='Lk',
                                chl_functor=get_sample_lk)

