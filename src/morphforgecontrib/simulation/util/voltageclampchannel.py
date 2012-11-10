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

from morphforge.units import qty



def get_voltageclamp_soma_current_trace(env, V, channel_functor, morphology):
    sim = build_voltageclamp_soma_simulation(env, V, channel_functor, morphology)
    res = sim.run()
    return res.get_trace('VCCurrent')


def build_voltageclamp_soma_simulation(env, V, channel_functor, morphology):
    sim = env.Simulation(name='SimXX', cvode=False, dt= qty('0.01:ms'))
    cell = sim.create_cell(name='Cell1', morphology=morphology)

    cell.apply_channel( channel=channel_functor(env=sim.environment))


    sim.record( cell, what=cell.Recordables.MembraneVoltage, name='SomaVoltage' , cell_location=cell.soma)

    vc = sim.create_voltageclamp(
        name='Stim1',
        amp1=qty('-81.5:mV'),
        amp2=qty(V),
        amp3=qty('-81.5:mV'),
        dur1=qty('100:ms'),
        dur2=qty('100:ms'),
        dur3=qty('100:ms'),
        cell_location=cell.soma,
        )
    sim.record(vc, what=vc.Recordables.Current, name='VCCurrent')
    return sim


