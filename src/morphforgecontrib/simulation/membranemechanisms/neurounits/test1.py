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


from neurounits.units_wrapper import NeuroUnitParser
from morphforgecontrib.simulation.indev.neuro_units_bridge.neuro_units_bridge import NeuroUnitEqnsetMechanism,\
    RecordableData


textHH = r"""EQNSET chlstd_hh_k {
    from std.math import exp
    i = g * (v-erev) * n**4

    ninf = n_alpha_rate / (n_alpha_rate + n_beta_rate)
    ntau = 1.0 / (n_alpha_rate + n_beta_rate)
    n' = (ninf-n) / ntau
    StdFormAB(V,a1,a2,a3,a4,a5) = (a1 + a2*V)/(a3+exp((V+a4)/a5))
    n_alpha_rate = StdFormAB(V=v,a1=n_a1,a2=n_a2,a3=n_a3,a4=n_a4,a5=n_a5)
    n_beta_rate =  StdFormAB(V=v,a1=n_b1,a2=n_b2,a3=n_b3,a4=n_b4,a5=n_b5)
    <=> PARAMETER g
    <=> PARAMETER erev
    <=> PARAMETER n_a1, n_a2, n_a3, n_a4, n_a5
    <=> PARAMETER n_b1, n_b2, n_b3, n_b4, n_b5
    <=> OUTPUT    i:(mA/cm2)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }
    <=> INPUT     v: mV           METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
}"""



textHH = r"""EQNSET chlstd_hh_k {
    from std.math import exp
    mult = m**3*h
    g = gmax* mult
    i =  g * (v-erev)
    minf = m_alpha_rate / (m_alpha_rate + m_beta_rate)
    mtau = 1.0 / (m_alpha_rate + m_beta_rate)
    m' = (minf-m) / mtau
    hinf = h_alpha_rate / (h_alpha_rate + h_beta_rate)
    htau = 1.0 / (h_alpha_rate + h_beta_rate)
    h' = (hinf-h) / htau
    StdFormAB(V,a1,a2,a3,a4,a5) = (a1 + a2*V)/(a3+exp((V+a4)/a5))
    m_alpha_rate = StdFormAB(V=v,a1=m_a1,a2=m_a2,a3=m_a3,a4=m_a4,a5=m_a5)
    m_beta_rate =  StdFormAB(V=v,a1=m_b1,a2=m_b2,a3=m_b3,a4=m_b4,a5=m_b5)
    h_alpha_rate = StdFormAB(V=v,a1=h_a1,a2=h_a2,a3=h_a3,a4=h_a4,a5=h_a5)
    h_beta_rate =  StdFormAB(V=v,a1=h_b1,a2=h_b2,a3=h_b3,a4=h_b4,a5=h_b5)
    <=> PARAMETER gmax
    <=> PARAMETER erev
    <=> PARAMETER m_a1, m_a2, m_a3, m_a4, m_a5
    <=> PARAMETER m_b1, m_b2, m_b3, m_b4, m_b5
    <=> PARAMETER h_a1, h_a2, h_a3, h_a4, h_a5
    <=> PARAMETER h_b1, h_b2, h_b3, h_b4, h_b5
    <=> OUTPUT    i:(mA/cm2)      METADATA {"mf":{"role":"TRANSMEMBRANECURRENT"} }
    <=> INPUT     v: mV                 METADATA {"mf":{"role":"MEMBRANEVOLTAGE"} }
}"""









from morphforge.stdimports import *
from morphforgecontrib.stdimports import *

# NeuroUnitEqnsetMechanism

# Create the morphology for the cell:
morphDict1 = {'root': {'length': 20, 'diam': 20, 'id': 'soma'}}
m1 = MorphologyLoader.fromDictionary(morphDict1)

# Create the environment:
env = NeuronSimulationEnvironment()

# Create the simulation:

mySim = env.Simulation(name='TestSim1')

# Create a cell:
myCell = mySim.create_cell(name="Cell1", morphology=m1)


# Apply the mechanisms to the cells
leakChannels = env.MembraneMechanism(EqnSetChl,
                                      mechanism_id='ID1',
                                      eqnset=EquationSetLoader.load('std_leak_chl.txt', dir= LocMgr.getTestEqnSetsPath()) ,
                                      parameters= {'gl':unit("5:pS/um2"), 'e_rev': unit("-70:mV")})
apply_mechanism_everywhere_uniform(myCell, leakChannels)
apply_passive_everywhere_uniform(myCell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2'))




hhChannel_params = {
        'm_a1': unit('13.01e3:s-1'),
        'm_a2': unit('0e0:/V s'),
        'm_a3': unit('4.0:'),
        'm_a4': unit('6.01e-3:V'),
        'm_a5': unit('-12.56e-3:V'),

        'm_b1': unit('5.73e3:s-1'),
        'm_b2': unit('0e3:/V s'),
        'm_b3': unit('1.0:'),
        'm_b4': unit('16.01e-3:V'),
        'm_b5': unit('9.69e-3:V'),

        'h_a1': unit('0.04e3:s-1'),
        'h_a2': unit('0.0e3:/V s'),
        'h_a3': unit('1.0:'),
        'h_a4': unit('29.88e-3:V'),
        'h_a5': unit('26e-3:V'),

        'h_b1': unit('2.04e3:s-1'),
        'h_b2': unit('0.0e3:/V s'),
        'h_b3': unit('1:'),
        'h_b4': unit('-8.09e-3:V'),
        'h_b5': unit('-10.21e-3:V'),
        'gmax':    unit("120:pS/um2"),
        'erev': unit("50:mV"),}





hhChannels = env.MembraneMechanism(NeuroUnitEqnsetMechanism,
                                      name = "bklk",
                                      mechanism_id='ID2',
                                      eqnset=NeuroUnitParser.File(text=textHH).get_eqnset('chlstd_hh_k'),
                                      default_parameters= hhChannel_params,
                                      recordables_map= {},
                                      recordables_data = {
                                                          "i": RecordableData(standard_tags=[StandardTags.CurrentDensity])
                                                          }

                                     )
apply_mechanism_everywhere_uniform(myCell, hhChannels)








# Get a cell_location on the cell:
somaLoc = myCell.get_location('soma')

# Create the simulous:
mySim.create_currentclamp(name="Stim1", amp=unit("250:pA"), dur=unit("100:ms"), delay=unit("100:ms"), cell_location=somaLoc)


# Define what to record:
mySim.record(myCell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = somaLoc, description='Membrane Voltage')
#mySim.recordall(leakChannels, cell_location=somaLoc)

mySim.record(hhChannels, what="i", cell_location=somaLoc)
mySim.record(hhChannels, what="g", cell_location=somaLoc, user_tags=[StandardTags.ConductanceDensity])
mySim.record(hhChannels, what="m", cell_location=somaLoc, user_tags=[StandardTags.StateVariable])
mySim.record(hhChannels, what="mult", cell_location=somaLoc, user_tags=[StandardTags.StateVariable])
mySim.record(hhChannels, what="h", cell_location=somaLoc, user_tags=[StandardTags.StateVariable])

# run the simulation
results = mySim.run()





ps = (
                PlotSpec_DefaultNew(s="Voltage", ylabel='Voltage', yrange=(-60*mV,40*mV) ),
                PlotSpec_DefaultNew(s="CurrentDensity", ylabel='CurrentDensity', yunit=unit("pA/um2") ),
                PlotSpec_DefaultNew(s="Current", ylabel='Current',yunit=pq.picoamp),
                PlotSpec_DefaultNew(s="Conductance", ylabel="Conductance"),
                PlotSpec_DefaultNew(s="ConductanceDensity", ylabel="ConductanceDensity", yunit=unit("pS/um2") ),
                PlotSpec_DefaultNew(s="StateVariable", ylabel="StateVariable"),
                PlotSpec_DefaultNew(s="StateTimeConstant",yunit=pq.millisecond, ylabel="Time Constant" ),
                PlotSpec_DefaultNew(s="StateSteadyState", ylabel="Steady State"),
                PlotSpec_DefaultNew(s="Event", ylabel="Events"),

               )

# Display the results:
TagViewer([results], timeranges=[(95, 200)*pq.ms], plotspecs = ps)
pylab.show()


