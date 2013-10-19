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
from morphforge.stdimports import *
from morphforgecontrib.stdimports import *

def main():

    """ Change parameters from 3 and show a single spiking and mutltiple spiking neuron in one plot"""
    
    """In this example, we build a single section neuron, with passive channels,
     and stimulate it with a current clamp"""
    
    
    
    
    env = NEURONEnvironment()
    morphDict1 = {'root': {'length': 20, 'diam': 20, 'id': 'soma'}}
    m1 = MorphologyTree.fromDictionary(morphDict1)
    
    
    def getKSInfTau(env):
        i = InfTauInterpolation(
            V   = [-100, -80,  -40,   0,   40],
            inf = [0.0, 0.0,  0.2,   0.5, 1.0],
            tau = [0.0, 50,   12,    15,  10]
       )
    
        ks_vars = {'ks': i}
    
    
        ks_chl = env.Channel(
            MM_InfTauInterpolatedChannel,
            name='InfTau1',
            equation='ks*ks*ks*ks',
            conductance='2.:pS/um2',
            reversalpotential='-80:mV',
            statevars_new=ks_vars,
            )
        return ks_chl
    
    
    tr0 = get_voltageclamp_soma_current_trace(env=env, V='-50:mV',
            channel_functor=getKSInfTau, morphology=m1)
    tr1 = get_voltageclamp_soma_current_trace(env=env, V='-20:mV',
            channel_functor=getKSInfTau, morphology=m1)
    tr2 = get_voltageclamp_soma_current_trace(env=env, V='20:mV',
            channel_functor=getKSInfTau, morphology=m1)
    
    
    TagViewer([tr0, tr1, tr2])
    
    
    
    
    
    
    
    #def build_simulation(gbar_multiplier):
    #    # Create the morphology for the cell:
    #    morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
    #    m1 = MorphologyTree.fromDictionary(morphDict1, name="SimpleMorphology1")
    #
    #
    #    # Create the environment:
    #    env = NEURONEnvironment()
    #
    #    # Create the simulation:
    #    sim = env.Simulation(name="TestSim1")
    #    cell = sim.create_cell(name="Cell1", morphology=m1)
    #
    #
    #    parameters = {
    #        'e_rev': qty('50:mV'),
    #        'gbar': qty('120:pS/um2'),
    #
    #        'm_alpha_a': qty('13.01e3:s-1'),
    #        'm_alpha_b': qty('0e0:V-1 s'),
    #        'm_alpha_c': qty('4.0:'),
    #        'm_alpha_d': qty('6.01e-3:V'),
    #        'm_alpha_e': qty('-12.56e-3:V'),
    #
    #        'm_beta_a': qty('5.73e3:s-1'),
    #        'm_beta_b': qty('0e3:V-1 s'),
    #        'm_beta_c': qty('1.0:'),
    #        'm_beta_d': qty('16.01e-3:V'),
    #        'm_beta_e': qty('9.69e-3:V'),
    #
    #        'h_alpha_a': qty('0.04e3:s-1'),
    #        'h_alpha_b': qty('0.0e3:V-1 s'),
    #        'h_alpha_c': qty('1.0:'),
    #        'h_alpha_d': qty('29.88e-3:V'),
    #        'h_alpha_e': qty('26e-3:V'),
    #
    #        'h_beta_a': qty('2.04e3:s-1'),
    #        'h_beta_b': qty('0.0e3:V-1 s'),
    #        'h_beta_c': qty('1:'),
    #        'h_beta_d': qty('-8.09e-3:V'),
    #        'h_beta_e': qty('-10.21e-3:V'),
    #        }
    #
    #
    #    ks = getKSInfTau(env)
    #
    #
    #
    #
    #    eqnset = EquationSetLoader.load('std_leak_chl.txt',
    #                                    dir=LocMgr.getTestEqnSetsPath())
    #    lk_chl = env.Channel(EqnSetChl, eqnset=eqnset,
    #            chlname='LeakChls', 
    #            parameters={'gl': qty('5:pS/um2'), 'e_rev': qty('-70:mV')}
    #            )
    #
    #
    #
    #
    #
    #    # Apply the mechanisms to the cells
    #    cell.apply_channel( lk_chl)
    #    cell.apply_channel( ks)
    #
    #    cell.set_passive( PassiveProperty.SpecificCapacitance, qty('1.0:uF/cm2'))
    #
    #
    #    sim.record(cell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = cell.soma, description='Membrane Voltage (gbar_multiplier = %2.2f)'%gbar_multiplier)
    #
    #
    #    sim.create_currentclamp(name='Stim1', amp=qty('200:pA'),
    #                              dur=qty('100:ms'), delay=qty('100:ms'),
    #                              cell_location=cell.soma)
    #
    #
    #    result = sim.run()
    #    return result
    #
    #
    #results = [
    #           build_simulation(gbar_multiplier = 1.0),
    #          
    #          ]
    #
    #TagViewer(results, timerange=(95, 200)*units.ms)
    #pylab.show()

if __name__=='__main__':
    main()
