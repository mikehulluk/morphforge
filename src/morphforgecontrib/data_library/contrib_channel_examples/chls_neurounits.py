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


eqnset_txt_na = """
define_component chlstd_hh_na {
    from std.math import exp
    i = g * (v-erev) * m**3*h
    minf = m_alpha_rate / (m_alpha_rate + m_beta_rate)
    mtau = 1.0 / (m_alpha_rate + m_beta_rate)
    m' = (minf-m) / mtau
    hinf = h_alpha_rate / (h_alpha_rate + h_beta_rate)
    htau = 1.0 / (h_alpha_rate + h_beta_rate)
    h' = (hinf-h) / htau
    StdFormAB(V, a1, a2, a3, a4, a5) = (a1 + a2*V)/(a3+exp((V+a4)/a5))
    m_alpha_rate = StdFormAB(V=v, a1=m_a1, a2=m_a2, a3=m_a3, a4=m_a4, a5=m_a5)
    m_beta_rate =  StdFormAB(V=v, a1=m_b1, a2=m_b2, a3=m_b3, a4=m_b4, a5=m_b5)
    h_alpha_rate = StdFormAB(V=v, a1=h_a1, a2=h_a2, a3=h_a3, a4=h_a4, a5=h_a5)
    h_beta_rate =  StdFormAB(V=v, a1=h_b1, a2=h_b2, a3=h_b3, a4=h_b4, a5=h_b5)
    m_a1 = {-4.00 ms-1}
    m_a2 = {-0.10 mV-1 ms-1}
    m_a3 = -1.00
    m_a4 = {40.00 mV}
    m_a5 = {-10.00 mV}
    m_b1 = {4.00 ms-1}
    m_b2 = {0.00 mV-1 ms-1}
    m_b3 = {0.00}
    m_b4 = {65.00 mV}
    m_b5 = {18.00 mV}
    h_a1 = {0.07 ms-1}
    h_a2 = {0.00 mV-1 ms-1}
    h_a3 = {0.00}
    h_a4 = {65.00 mV}
    h_a5 = {20.00 mV}
    h_b1 = {1.00  ms-1}
    h_b2 = {0.00  mV-1 ms-1}
    h_b3 = {1.00}
    h_b4 = {35.00  mV}
    h_b5 = {-10.00 mV}
    sg = {120.0mS/cm2}
    erev = {50.0mV}
    <=> PARAMETER g:(S/m2)
    <=> OUTPUT    i:(A/m2)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }
    <=> INPUT     v: V           METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
}
"""

eqnset_txt_k = """
define_component chlstd_hh_k {
    from std.math import exp
    i = g * (v-erev) * n*n*n*n
    ninf = n_alpha_rate / (n_alpha_rate + n_beta_rate)
    ntau = 1.0 / (n_alpha_rate + n_beta_rate)
    n' = (ninf-n) / ntau
    StdFormAB(V, a1, a2, a3, a4, a5) = (a1 + a2*V)/(a3+exp((V+a4)/a5))
    n_alpha_rate = StdFormAB(V=v, a1=n_a1, a2=n_a2, a3=n_a3, a4=n_a4, a5=n_a5)
    n_beta_rate =  StdFormAB(V=v, a1=n_b1, a2=n_b2, a3=n_b3, a4=n_b4, a5=n_b5)

    n_a1 = {-0.55 ms-1}
    n_a2 = {-0.01 mV-1 ms-1}
    n_a3 = -1.00
    n_a4 = {55.00 mV}
    n_a5 = {-10.00 mV}
    n_b1 = {0.125 ms-1}
    n_b2 = {0.00 mV-1 ms-1}
    n_b3 = {0.00}
    n_b4 = {65.00 mV}
    n_b5 = {80.00 mV}

    g = {36.0mS/cm2}
    erev = {-77.0mV}
    <=> OUTPUT    i:(A/m2)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }
    <=> INPUT     v: V          METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
}
"""

eqnset_txt_lk = """
    define_component chlstd_hh_lk {
        i = g * (v-erev)
        g = {0.3 mS/cm2}
        erev = -54.3 mV
        <=> OUTPUT    i:(A/m2)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }
        <=> INPUT     v: V          METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
        }
"""

from morphforge.stdimports import ChannelLibrary, cached_functor

@cached_functor
def get_hh_na(env):
    return env.Channel(
        NeuroUnitEqnsetMechanism,
        name="_neurounits_hh_na",
        eqnset=eqnset_txt_na,
        default_parameters={"g":qty("120:mS/cm2")}
        )
@cached_functor
def get_hh_k(env):
    return env.Channel(
        NeuroUnitEqnsetMechanism,
        name="_neurounits_hh_k",
        eqnset=eqnset_txt_k,
        )

@cached_functor
def get_hh_lk(env):
    return env.Channel(
        NeuroUnitEqnsetMechanism,
        name="_neurounits_hh_lk",
        eqnset=eqnset_txt_lk,
        )



ChannelLibrary.register_channel(modelsrc="_test_neurounits_HH52", channeltype='Na', chl_functor=get_hh_na)
ChannelLibrary.register_channel(modelsrc="_test_neurounits_HH52", channeltype='K', chl_functor=get_hh_k)
ChannelLibrary.register_channel(modelsrc="_test_neurounits_HH52", channeltype='Lk', chl_functor=get_hh_lk)
