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




import morphforge.stdimports as mf
import morphforgecontrib.stdimports as mfc
import pylab

from morphforgecontrib.simulation.synapse_templates.neurounit import * 
from morphforgecontrib.simulation.synapse_templates.exponential_form.expsyn.core import * 
from morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core import * 
from morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core import * 
from morphforge import units


# Define the formulae used in the model:

na_eqnset_txt = """
define_component sautois_hh_na {
    i = gmax * (v-erev) * m**3*h
    minf = m_alpha_rate / (m_alpha_rate + m_beta_rate)
    mtau = 1.0 / (m_alpha_rate + m_beta_rate)
    m' = (minf-m) / mtau
    hinf = h_alpha_rate / (h_alpha_rate + h_beta_rate)
    htau = 1.0 / (h_alpha_rate + h_beta_rate)
    h' = (hinf-h) / htau
    StdFormAB(V, a1, a2, a3, a4, a5) = (a1+a2*V)/(a3+std.math.exp((V+a4)/a5))
    m_alpha_rate = StdFormAB(V=v, a1=m_a1, a2=m_a2, a3=m_a3, a4=m_a4, a5=m_a5)
    m_beta_rate =  StdFormAB(V=v, a1=m_b1, a2=m_b2, a3=m_b3, a4=m_b4, a5=m_b5)
    h_alpha_rate = StdFormAB(V=v, a1=h_a1, a2=h_a2, a3=h_a3, a4=h_a4, a5=h_a5)
    h_beta_rate =  StdFormAB(V=v, a1=h_b1, a2=h_b2, a3=h_b3, a4=h_b4, a5=h_b5)

    <=> PARAMETER m_a1:{s-1}, m_a2:{V-1 s-1}, m_a3:{}, m_a4:{V}, m_a5:{V}
    <=> PARAMETER m_b1:{s-1}, m_b2:{V-1 s-1}, m_b3:{}, m_b4:{V}, m_b5:{V}
    <=> PARAMETER h_a1:{s-1}, h_a2:{V-1 s-1}, h_a3:{}, h_a4:{V}, h_a5:{V}
    <=> PARAMETER h_b1:{s-1}, h_b2:{V-1 s-1}, h_b3:{}, h_b4:{V}, h_b5:{V}
    <=> PARAMETER gmax:(S/m2), erev:(V)

    <=> OUTPUT    i:(A/m2)   METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }
    <=> INPUT     v: V       METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
}"""

lk_eqnset_txt = """
define_component sautois_hh_lk {
    i = gmax * (v-erev)

    <=> PARAMETER gmax:(S/m2), erev:(V)

    <=> OUTPUT    i:(A/m2)   METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }
    <=> INPUT     v: V       METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
}"""

k_eqnset_txt = """
    define_component chlstd_hh_k {
    i = gmax * (v-erev) * n
    ninf = n_alpha_rate / (n_alpha_rate + n_beta_rate)
    ntau = 1.0 / (n_alpha_rate + n_beta_rate)
    n' = (ninf-n) / ntau
    StdFormAB(V, a1, a2, a3, a4, a5) = (a1 + a2*V)/(a3+std.math.exp((V+a4)/a5))
    n_alpha_rate = StdFormAB(V=v, a1=k_a1, a2=k_a2, a3=k_a3, a4=k_a4, a5=k_a5)
    n_beta_rate =  StdFormAB(V=v, a1=k_b1, a2=k_b2, a3=k_b3, a4=k_b4, a5=k_b5)

    <=> PARAMETER k_a1:{s-1}, k_a2:{V-1 s-1}, k_a3:{}, k_a4:{V}, k_a5:{V}
    <=> PARAMETER k_b1:{s-1}, k_b2:{V-1 s-1}, k_b3:{}, k_b4:{V}, k_b5:{V}
    <=> PARAMETER gmax:(S/m2), erev:(V)

    <=> OUTPUT    i:(A/m2)    METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }
    <=> INPUT     v: V        METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
}"""


# Some Utility Functions:
def extract_params(p, prefix, replace_prefix=""):
    return dict([(replace_prefix+k[len(prefix):], v) for (k, v) in p.iteritems() if k.startswith(prefix)])

def remap_keys(dct, remap_dct):
    # Avoid collisions
    for v in remap_dct.values():
        assert not v in dct
    return dict ([(remap_dct.get(k, k), v) for (k, v) in dct.iteritems()])




param_units = """
nS/um2; nS/um2; nS/um2; nS/um2;
mV; mV; mV; mV;
ms-1; mV-1 ms-1; ;mV; mV;
ms-1; mV-1 ms-1; ;mV; mV;
ms-1; mV-1 ms-1; ;mV; mV;
ms-1; mV-1 ms-1; ;mV; mV;
ms-1; mV-1 ms-1; ;mV; mV;
ms-1; mV-1 ms-1; ;mV; mV;
ms-1; mV-1 ms-1; ;mV; mV;
ms-1; mV-1 ms-1; ;mV; mV;
"""
param_names = """
lk_gmax na_gmax kf_gmax ks_gmax
lk_erev na_erev kf_erev ks_erev
na_m_a1 na_m_a2 na_m_a3 na_m_a4 na_m_a5
na_m_b1 na_m_b2 na_m_b3 na_m_b4 na_m_b5
na_h_a1 na_h_a2 na_h_a3 na_h_a4 na_h_a5
na_h_b1 na_h_b2 na_h_b3 na_h_b4 na_h_b5
kf_a1 kf_a2 kf_a3 kf_a4 kf_a5
kf_b1 kf_b2 kf_b3 kf_b4 kf_b5
ks_a1 ks_a2 ks_a3 ks_a4 ks_a5
ks_b1 ks_b2 ks_b3 ks_b4 ks_b5
"""


# Param Details:
params_aIN = """
1.35 150 15 2.5
-54 50 -80  -80
8.67  0.00  0.50  -13.01 -18.56
5.73  0.00  1.00   -2.99   9.69
0.04  0.00  0.00   15.8   26.00
4.08  0.00  0.001 -19.09 -10.21
3.10  0.00  1.00  -35.5   -9.30
1.10  0.00  1.00    0.98  16.19
0.20  0.00  1.00  -10.96  -7.74
0.05  0.00  1.00  -22.07   6.10
"""

params_MN = """
2.4691 110.0 8.0 1.0
-61 50 -80 -80
13.26  0.0  0.5   -5.01 -12.56
 5.73  0.0  1.0    5.01   9.69
 0.04  0.0  0.0   28.8   26.0
 2.04  0.0  0.001 -9.09 -10.21
 3.1   0.0  1.0   -27.5   -9.3
 0.44  0.0  1.0    8.98  16.19
 0.20  0.0  1.0   -2.96  -7.74
 0.05  0.0  1.0  -14.07   6.1
"""

params_dIN = """
3.6765 210.0 0.5 3.0
-51 50 -80 -80
13.01  0.0   4.0   -1.01   -12.56
 5.73  0.0   1.0    9.01     9.69
 0.06  0.0   0.0   30.88    26.0
 3.06  0.0   1.0   -7.09   -10.21
 3.10  0.0   1.0  -31.50    -9.3
 0.44  0.0   1.0    4.98    16.19
 0.20  0.0   1.0   -6.96    -7.74
 0.05  0.0   2.0  -18.07     6.1
"""

params_RB = """
4.3573 120 1.5 8.0
-70 50 -80 -80
13.01  0   1   -4.01   -12.56
 5.73  0   1   6.01     9.69
 0.04  0   0   29.88   26.00
 2.04  0   1   -8.09  -10.21
 3.1   0   1   -32.5   -9.30
 0.44  0   1   3.98    16.19
 0.2   0   1   -7.96   -7.74
 0.05  0   2   -19.07   6.10
"""

params_dlc = """
2.3364 420 70 10
-66 50 -80 -80
13.26  0  3.00   -3.01  -12.56
 5.73  0  1.00    6.01    9.69
 0.06  0  0.00   19.88   26.0
 4.08  0  0.001  -8.09  -10.21
 3.10  0  1.00  -32.5    -9.3
 1.10  0  2.00    3.98   16.19
 4.00  0  1.00  -53.0    -7.74
 0.01  0  1.00   47.0     6.1
"""
params_dla = """
0.6964 150 70 5
-63 50 -80 -80
13.26  0.0  1.20   -9.01 -12.56
 5.73  0.0  1.00    1.01   9.69
 0.04  0.0  0.00   14.88  26.00
 2.04  0.0  0.001 -13.09 -10.21
 3.10  0.0  1.00  -37.5   -9.3
 1.10  0.0  0.60   -1.02  16.19
 4.00  0.0  1.00  -58.0   -7.74
 0.01  0.0  1.00   42.0    6.1
"""

params_cIN = """
4.8544 500 30 20
-60 50 -80 -80
13.26  0  0.1   -10.01 -12.56
 5.73  0  1       0.01   9.69
 0.06  0  0      23.8   26.0
 3.06  0  0.001 -14.09 -10.21
 3.10  0  1     -32.5   -9.3
 1.10  0  1       3.98  16.19
 0.20  0  1      -7.96  -7.74
 0.05  0  0.5   -19.07   6.1
"""
params_dINr = """
4.807 190 20 3
-59 50 -80 -80
12.3  0  0.1  -10.01  -12.56
3.73  0  1.0    0.01    9.69
0.04  0  0.0   23.8    26.0
2.04  0  0.3  -18.09  -10.21
3.10  0  1.0  -32.5    -9.3
1.10  0  1.0    3.98   16.19
0.20  0  0.5   -7.96   -7.74
0.05  0  0.7  -19.07    6.1
"""


def load_std_channels(param_str):
    nrn_params = dict([(p, mf.qty("%s:%s"%(v, u.strip()))) for (p, u, v) in zip(param_names.split(), param_units.split(';'), param_str.split())])
    nrn_params_na = extract_params(nrn_params, prefix='na_')
    nrn_params_lk = extract_params(nrn_params, prefix='lk_')
    nrn_params_ks = extract_params(nrn_params, prefix='ks_', replace_prefix='k_')
    nrn_params_kf = extract_params(nrn_params, prefix='kf_', replace_prefix='k_')
    nrn_params_ks = remap_keys(nrn_params_ks, {'k_gmax':'gmax', 'k_erev':'erev'})
    nrn_params_kf = remap_keys(nrn_params_kf, {'k_gmax':'gmax', 'k_erev':'erev'})
    eqnsetna = mf.neurounits.NeuroUnitParser.Parse9MLFile(na_eqnset_txt).get_component()
    eqnsetlk = mf.neurounits.NeuroUnitParser.Parse9MLFile(lk_eqnset_txt).get_component()
    eqnsetk = mf.neurounits.NeuroUnitParser.Parse9MLFile(k_eqnset_txt).get_component()

    na_chl = mfc.Neuron_NeuroUnitEqnsetMechanism(name="Chl1", eqnset=eqnsetna, default_parameters = nrn_params_na)
    lk_chl = mfc.Neuron_NeuroUnitEqnsetMechanism(name="Chl2", eqnset=eqnsetlk, default_parameters = nrn_params_lk)
    ksChls = mfc.Neuron_NeuroUnitEqnsetMechanism(name="Chl3", eqnset=eqnsetk,  default_parameters = nrn_params_ks)
    kfChls = mfc.Neuron_NeuroUnitEqnsetMechanism(name="Chl4", eqnset=eqnsetk,  default_parameters = nrn_params_kf)

    chls =  [na_chl, lk_chl, ksChls, kfChls]
    return chls



def load_ka_channel():
    ka_param_names = """
    ka_gmax ka_erev
    ka_m_a1 ka_m_a2 ka_m_a3 ka_m_a4 ka_m_a5
    ka_m_b1 ka_m_b2 ka_m_b3 ka_m_b4 ka_m_b5
    ka_h_a1 ka_h_a2 ka_h_a3 ka_h_a4 ka_h_a5
    ka_h_b1 ka_h_b2 ka_h_b3 ka_h_b4 ka_h_b5
    """

    ka_param_units = """
    nS/um2; mV;
    ms-1; mV-1 ms-1; ;mV; mV;
    ms-1; mV-1 ms-1; ;mV; mV;
    ms-1; mV-1 ms-1; ;mV; mV;
    ms-1; mV-1 ms-1; ;mV; mV;
    """
    ka_param_str = """
    30   -80
    12.025   0   0.5 -10.01  -12.56
    14.325   0   1    -8.01    9.69
    0.0001   0   1    15.88   26.0
    10.000   0   500 -22.09  -10.21
    """

    nrn_params = dict([(p, mf.qty("%s:%s"%(v, u.strip()))) for (p, u, v) in zip(ka_param_names.split(), ka_param_units.split(';'), ka_param_str.split())])
    nrn_params_ka = extract_params(nrn_params, prefix='ka_')
    print nrn_params_ka
    eqnsetka = mf.neurounits.NeuroUnitParser.EqnSet(na_eqnset_txt.replace("sautois", "saut2"))
    kaChls = mfc.Neuron_NeuroUnitEqnsetMechanism(name="Chl5", eqnset=eqnsetka,  default_parameters = nrn_params_ka)
    return kaChls


@mf.cached_functor
def get_ain_chls():
    return load_std_channels(params_aIN)
@mf.cached_functor
def get_mn_chls():
    return load_std_channels(params_MN)
@mf.cached_functor
def get_dinr_chls():
    return load_std_channels(params_dINr)
@mf.cached_functor
def get_din_chls():
    return load_std_channels(params_dIN)
@mf.cached_functor
def get_rb_chls():
    return load_std_channels(params_RB)
@mf.cached_functor
def get_dla_chls():
    return load_std_channels(params_dla)
@mf.cached_functor
def get_dlc_chls():
    return load_std_channels(params_dlc)
@mf.cached_functor
def get_cin_chls():
    return load_std_channels(params_cIN) + [load_ka_channel()]


import random
def make_cell(sim, cell_name, cell_chl_functor):
    m1 = mf.MorphologyBuilder.get_single_section_soma(area=mf.qty("1:um2"))
    cell = sim.create_cell(name=cell_name, morphology=m1)
    for chl in cell_chl_functor():
        cell.apply_channel( chl, parameter_multipliers={'gmax':random.uniform(0.9, 1.1)})
    cell.set_passive( mf.PassiveProperty.SpecificCapacitance, mf.qty('4:pF/um2'))
    return cell


def make_cell_ain(sim, name=None, cell_tags=[]):
    return make_cell(sim, cell_name=name, cell_chl_functor= get_ain_chls)
def make_cell_cin(sim, name=None, cell_tags=[]):
    return make_cell(sim, cell_name=name, cell_chl_functor= get_cin_chls)
def make_cell_din(sim, name=None, cell_tags=[]):
    return make_cell(sim, cell_name=name, cell_chl_functor= get_din_chls)
def make_cell_dinr(sim, name=None, cell_tags=[]):
    return make_cell(sim, cell_name=name, cell_chl_functor= get_dinr_chls)



celltypes = [
    ('aIN', get_ain_chls),
    ('MN',  get_mn_chls),
    ('dIN', get_din_chls),
    ('RB',  get_rb_chls),
    ('dla', get_dla_chls),
    ('dlc', get_dlc_chls),
    ('cIN', get_cin_chls),
    ('dINr', get_dinr_chls),
]






# Test the effects of step-current injections:
# ############################################

def test_cell_current(cell_name, cell_chl_functor, current):
    sim = mf.NEURONEnvironment().Simulation()

    m1 = mf.MorphologyBuilder.get_single_section_soma(area=mf.qty("1:um2"))
    cell = sim.create_cell(name=cell_name, morphology=m1)
    cc = sim.create_currentclamp(name="CC1", delay=100*mf.ms, dur=400*mf.ms, amp=current * mf.pA, cell_location=cell.soma)

    for chl in cell_chl_functor():
        mf.cell.apply_channel( chl)

    mf.cell.set_passive( mf.PassiveProperty.SpecificCapacitance, mf.qty('4:pF/um2'))

    sim.record(cell, what=mf.Cell.Recordables.MembraneVoltage)
    sim.record(cc, what=mf.CurrentClamp.Recordables.Current)

    res =sim.run()
    return res


def test_cell(cell_name, cell_chl_functor):
    current_levels = [0, 40, 80, 120, 160, 200, 240]
    reses = [test_cell_current(cell_name=cell_name, cell_chl_functor=cell_chl_functor, current=c) for c in current_levels]
    mf.TagViewer(reses, show=False)

def test_step_current_injections():
    for cell_name, functor in celltypes:
        test_cell(cell_name, functor)

# End of step current injections
################################




simple_syn = """
eqnset syn_simple {

    g' = - g/g_tau
    i = gmax * (v-erev) * g

    gmax = 300pS
    erev = 0mV

    g_tau = 20ms
    <=> INPUT     v: mV       METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
    <=> OUTPUT    i:(mA)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }

    ==>> on_event() {
        g = g + 1.0
    }
}
"""


syn_inhib = """
eqnset syn_decaying_inhib {
    o' = - o/{1.5 ms}
    c' = - c/{4.0 ms}
    i = (v- {-80mV}) *g
    g = {0.435nS}  * (c-o)  * scale
    x=10.0
    f = scale
    plas' = -plas / beta

    <=> PARAMETER scale:()
    <=> INPUT     v: mV       METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
    <=> OUTPUT    i:(mA)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }

    alpha = 0.75
    beta = 60ms
    update = x - (x * (1-alpha) * plas)
    ==>> on_event() {
        update = x - (x * (1-alpha) * plas)
        o = o + [update]if[update>0]else[0]
        c = c + [update]if[update>0]else[0]

        plas = plas + 1.0
    }
}
"""



syn_onto_driver= """
eqnset syn_simple {

    o' = - o/{1.5 ms}
    c' = - c/{10.0 s}
    i = {0.835nS} * (v- {0mV})  * (c-o) * scale

    <=> PARAMETER scale:()
    <=> INPUT     v: mV       METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
    <=> OUTPUT    i:(mA)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }

    ==>> on_event() {
        o = o +  10
        c = c +  10
    }
}
"""

syn_std_excite_AMPA= """
eqnset syn_simple {

    o' = - o/{1.5 ms}
    c' = - c/{4.0 ms}
    i = {0.435nS} * (v- {0mV})  * (c-o)  * scale

    <=> PARAMETER scale:()
    <=> INPUT     v: mV       METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
    <=> OUTPUT    i:(mA)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }

    ==>> on_event() {
        o = o + 10
        c = c + 10
    }
}
"""

syn_std_excite_NMDA= """
eqnset syn_simple {

    o' = - o/{1.5 ms}
    c' = - c/{80 ms}
    i = {0.435nS} * (v- {0mV})  * (c-o)  * scale  * vdep
    vdep = 1/(1+ 0.1*0.5*std.math.exp(-0.08*v/{1mV}))

    <=> PARAMETER scale:()
    <=> INPUT     v: mV       METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
    <=> OUTPUT    i:(mA)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }

    ==>> on_event() {
        o = [o + 10]if[o<15]else[25]
        c = [c + 10]if[c<15]else[25]
    }
}
"""


env = mf.NEURONEnvironment()


# Create the synaptic templates:
driver_syn_tmpl = env.PostSynapticMechTemplate(
        NeuroUnitEqnsetPostSynaptic,
        eqnset = mf.neurounits.NeuroUnitParser.EqnSet(syn_onto_driver), 
        template_name='driver_syn_templ',
        default_parameters={'scale':1.0} 
        )

excite_ampa_syn_tmpl = env.PostSynapticMechTemplate(
        NeuroUnitEqnsetPostSynaptic,
        template_name='excite_ampa_syn_tmpl',
        eqnset = mf.neurounits.NeuroUnitParser.EqnSet(syn_std_excite_AMPA), 
        default_parameters={'scale':1.0} 
        )

excite_nmda_syn_tmpl = env.PostSynapticMechTemplate(
        NeuroUnitEqnsetPostSynaptic,
        template_name='excite_nmda_syn_tmpl',
        eqnset = mf.neurounits.NeuroUnitParser.EqnSet(syn_std_excite_NMDA), 
        default_parameters={'scale':1.0} 
        )

inhib_syn_tmpl = env.PostSynapticMechTemplate(
        NeuroUnitEqnsetPostSynaptic,
        template_name='inhib_syn_tmpl',
        eqnset = mf.neurounits.NeuroUnitParser.EqnSet(syn_inhib), 
        default_parameters={'scale':1.0} 
        )

exptemplate = env.PostSynapticMechTemplate(
        PostSynapticMech_ExpSyn_Base,
        template_name='expsyn1tmpl',
        tau = 5 * units.ms, e_rev = 0 * units.mV,
        )


exp2template = env.PostSynapticMechTemplate(
        PostSynapticMech_Exp2Syn_Base,
        template_name='expsyn2tmpl',
        tau_open = 5 * units.ms, tau_close=20*units.ms, e_rev = 0 * units.mV, popening=1.0,
        )

def build_trigger( env, cell):
    return env.SynapticTrigger(
                mfc.SynapticTriggerByVoltageThreshold,
                cell_location = cell.soma,
                voltage_threshold = mf.qty("0:mV"),
                delay = mf.qty("1:ms"),
                #,
               )

def onto_driver(sim, postsynaptic, times):
    return sim.create_synapse(
            trigger =  env.SynapticTrigger(
                                        mfc.SynapticTriggerAtTimes,
                                        time_list =   times,
                                        ),
            postsynaptic_mech = driver_syn_tmpl.instantiate(
                                        cell_location = postsynaptic.soma,
                                        parameter_multipliers = {'scale':1.0 },
                                        peak_conductance = mf.qty("1:nS")
                                       )
           )

def dual_driver(sim, presynaptic, postsynaptic, ampa_scale, nmda_scale):
    ampa = sim.create_synapse(
            trigger = build_trigger( env, presynaptic),
            postsynaptic_mech = excite_ampa_syn_tmpl.instantiate(
                                        cell_location = postsynaptic.soma,
                                        parameter_multipliers = {'scale':ampa_scale * units.dimensionless },
                                        peak_conductance = mf.qty("1:nS")
                                       )
           )
    nmda = sim.create_synapse(
            trigger = build_trigger( env, presynaptic),
            postsynaptic_mech = excite_nmda_syn_tmpl.instantiate(
                                        cell_location = postsynaptic.soma,
                                        parameter_multipliers = {'scale':nmda_scale * units.dimensionless },
                                        peak_conductance = mf.qty("1:nS")
                                       )
           )
    return [ampa, nmda]

def inhib(sim, presynaptic, postsynaptic, scale):
    inhib_syn = sim.create_synapse(
            trigger = build_trigger( env, presynaptic),
            postsynaptic_mech = inhib_syn_tmpl.instantiate(
                                        cell_location = postsynaptic.soma,
                                        parameter_multipliers = {'scale':scale * units.dimensionless },
                                       )
           )
    return [inhib_syn]

def expbuiltin_syn(sim, presynaptic, postsynaptic, scale):
    inhib_syn = sim.create_synapse(
            trigger = build_trigger( env, presynaptic),
            postsynaptic_mech = exptemplate.instantiate( cell_location = postsynaptic.soma,)
           )
    return [inhib_syn]


def exp2builtin_syn(sim, presynaptic, postsynaptic, scale):
    inhib_syn = sim.create_synapse(
            trigger = build_trigger( env, presynaptic),
            postsynaptic_mech = exp2template.instantiate( cell_location = postsynaptic.soma,)
           )
    return [inhib_syn]

def driver_onto_dinr(sim, presynaptic, postsynaptic):
    return dual_driver(sim=sim, presynaptic=presynaptic, postsynaptic=postsynaptic, ampa_scale=0.1, nmda_scale=1.0)
def driver_onto_cin(sim, presynaptic, postsynaptic):
    return dual_driver(sim=sim, presynaptic=presynaptic, postsynaptic=postsynaptic, ampa_scale=0.1, nmda_scale=0.1)
def dinr_onto_cin(sim, presynaptic, postsynaptic):
    return dual_driver(sim=sim, presynaptic=presynaptic, postsynaptic=postsynaptic, ampa_scale=0.0, nmda_scale=1.0)
def cin_onto_cin(sim, presynaptic, postsynaptic):
    return inhib(sim=sim, presynaptic=presynaptic, postsynaptic=postsynaptic, scale=4.0)
def cin_onto_dinr(sim, presynaptic, postsynaptic):
    return inhib(sim=sim, presynaptic=presynaptic, postsynaptic=postsynaptic, scale=4.0)
def expbuiltin(sim, presynaptic, postsynaptic):
    return expbuiltin_syn(sim=sim, presynaptic=presynaptic, postsynaptic=postsynaptic, scale=4.0)
def exp2builtin(sim, presynaptic, postsynaptic):
    return exp2builtin_syn(sim=sim, presynaptic=presynaptic, postsynaptic=postsynaptic, scale=4.0)



sim = env.Simulation()

nNeurons = 1
dINr_LHS =mfc.NeuronPopulation(sim=sim, neuron_functor=make_cell_dinr, n=5, pop_name="dINR_LHS")
dINr_RHS =mfc.NeuronPopulation(sim=sim, neuron_functor=make_cell_dinr, n=5, pop_name="dINR_RHS")

cIN_LHS =mfc.NeuronPopulation(sim=sim, neuron_functor=make_cell_dinr, n=5, pop_name="cIN_LHS")
cIN_RHS =mfc.NeuronPopulation(sim=sim, neuron_functor=make_cell_dinr, n=5, pop_name="cIN_RHS")
#
#aIN_LHS =mfc.NeuronPopulation(sim=sim, neuron_functor=make_cell_ain, n=nNeurons, pop_name="aIN_LHS")
#aIN_RHS =mfc.NeuronPopulation(sim=sim, neuron_functor=make_cell_ain, n=nNeurons, pop_name="aIN_RHS")


driver_LHS =mfc.NeuronPopulation(sim=sim, neuron_functor=make_cell_dinr, n=nNeurons, pop_name="driver_LHS")
driver_RHS =mfc.NeuronPopulation(sim=sim, neuron_functor=make_cell_dinr, n=nNeurons, pop_name="driver_RHS")


# Connect the drivers:
mfc.Connectors.times_to_all(sim, syncronous_times=(100,)*mf.units.ms, postsynaptic_population= driver_LHS, connect_functor = onto_driver)
mfc.Connectors.times_to_all(sim, syncronous_times=(105,)*mf.units.ms, postsynaptic_population= driver_RHS, connect_functor = onto_driver)
#
# LHS
#######
# Connect the drivers to eveything:
mfc.Connectors.all_to_all(sim, presynaptic_population=driver_LHS, postsynaptic_population= cIN_LHS, connect_functor = driver_onto_cin)
mfc.Connectors.all_to_all(sim, presynaptic_population=driver_LHS, postsynaptic_population= dINr_LHS, connect_functor = driver_onto_dinr)
# Connect the dINrs to eveything:
mfc.Connectors.all_to_all(sim, presynaptic_population=dINr_LHS, postsynaptic_population= cIN_LHS, connect_functor = dinr_onto_cin)

# Connect the cINs to eveything contra-laterally:
mfc.Connectors.all_to_all(sim, presynaptic_population=cIN_LHS, postsynaptic_population= cIN_RHS, connect_functor = cin_onto_cin)
syn_cin_dinr_lr = mfc.Connectors.all_to_all(sim, presynaptic_population=cIN_LHS, postsynaptic_population= dINr_RHS, connect_functor = cin_onto_dinr, synapse_pop_name='syn_cin_dinr_lr')


## RHS
########
mfc.Connectors.all_to_all(sim, presynaptic_population=driver_RHS, postsynaptic_population= cIN_RHS, connect_functor = driver_onto_cin)
mfc.Connectors.all_to_all(sim, presynaptic_population=driver_RHS, postsynaptic_population= dINr_RHS, connect_functor = driver_onto_dinr)
# Connect the dINrs to eveything:
mfc.Connectors.all_to_all(sim, presynaptic_population=dINr_RHS, postsynaptic_population= cIN_RHS, connect_functor = driver_onto_cin)
#mfc.Connectors.all_to_all(sim, presynaptic_population=dINr_RHS, postsynaptic_population= dINr_RHS, connect_functor = driver_onto_dinr)

# Connect the cINs to eveything contra-laterally:
mfc.Connectors.all_to_all(sim, presynaptic_population=cIN_RHS, postsynaptic_population= cIN_LHS, connect_functor = cin_onto_cin)
#syn_cin_dinr_rl = mfc.Connectors.all_to_all(sim, presynaptic_population=cIN_RHS, postsynaptic_population= dINr_LHS, connect_functor = cin_onto_dinr, synapse_pop_name='syn_cin_dinr_lr')




driver_LHS.record_from_all(what=mf.Cell.Recordables.MembraneVoltage)
driver_RHS.record_from_all(what=mf.Cell.Recordables.MembraneVoltage)
dINr_LHS.record_from_all(what=mf.Cell.Recordables.MembraneVoltage)
dINr_RHS.record_from_all(what=mf.Cell.Recordables.MembraneVoltage)
cIN_LHS.record_from_all(what=mf.Cell.Recordables.MembraneVoltage)
cIN_RHS.record_from_all(what=mf.Cell.Recordables.MembraneVoltage)
#aIN_LHS.record_from_all(what=mf.Cell.Recordables.MembraneVoltage)
#aIN_RHS.record_from_all(what=mf.Cell.Recordables.MembraneVoltage)


#syn_cin_dinr_lr.record_from_all(what='g')



mfc.Connectors.all_to_all(sim, presynaptic_population=cIN_RHS, postsynaptic_population= cIN_LHS, connect_functor = expbuiltin)
mfc.Connectors.all_to_all(sim, presynaptic_population=cIN_RHS, postsynaptic_population= cIN_LHS, connect_functor = exp2builtin)




#mf.SimulationMRedoc.build(sim).to_pdf('~/Desktop/BartSim.pdf')
res =sim.run()

for tr in res.get_traces():
    print tr.tags


mf.TagViewer(res,
        plots=[
    mf.TagPlot("ALL{Voltage}", yrange=(-80*mf.mV, 50*mf.mV) ),
    mf.TagPlot("ALL{Voltage,driver_LHS}", yrange=(-80*mf.mV, 50*mf.mV) ),
    mf.TagPlot("ALL{Voltage,dINR_LHS}", yrange=(-80*mf.mV, 50*mf.mV) ),
    mf.TagPlot("ALL{Voltage,cIN_LHS}", yrange=(-80*mf.mV, 50*mf.mV) ),
    mf.TagPlot("ALL{Voltage,aIN_LHS}", yrange=(-80*mf.mV, 50*mf.mV) ),
    mf.TagPlot("ALL{Voltage,driver_RHS}", yrange=(-80*mf.mV, 50*mf.mV) ),
    mf.TagPlot("ALL{Voltage,dINR_RHS}", yrange=(-80*mf.mV, 50*mf.mV) ),
    mf.TagPlot("ALL{Voltage,cIN_RHS}", yrange=(-80*mf.mV, 50*mf.mV) ),
    mf.TagPlot("ALL{Voltage,aIN_RHS}", yrange=(-80*mf.mV, 50*mf.mV) ),
    mf.TagPlot('ALL{PREPOP:cIN_LHS,POSTPOP:dINR_RHS}'),
    mf.TagPlot('ALL{PREPOP:cIN_RHS,POSTPOP:dINR_LHS}'),

           ])






















# What to run:
#test_step_current_injections()

pylab.show()

