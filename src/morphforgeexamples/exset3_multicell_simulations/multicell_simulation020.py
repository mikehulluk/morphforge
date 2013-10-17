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



"""
The responses of two cells connected by a gap junction to a step current injection into the first
"""

import morphforge.stdimports as mf
import morphforgecontrib.stdimports as mfc
from morphforge.stdimports import units as U

# The simulation:
env = mf.NEURONEnvironment()
sim = env.Simulation(cvode=True)
cell1 = sim.create_cell(area=5000 * U.um2, initial_voltage=0*U.mV, name='Cell1')
lk_chl1 = env.Channel(mfc.StdChlLeak,
                conductance=0.66  * U.mS/U.cm2,
                reversalpotential=0*U.mV )

cell1.apply_channel(lk_chl1)
cell1.set_passive(mf.PassiveProperty.SpecificCapacitance, (1e-3) * U.uF / U.cm2)


cell2 = sim.create_cell(area=20000 * U.um2, initial_voltage=0*U.mV, name='Cell2')
lk_chl2 = env.Channel(mfc.StdChlLeak,
                conductance=0.01* U.mS/U.cm2,
                reversalpotential=0*U.mV
                )

cell2.apply_channel(lk_chl2)
cell2.set_passive(mf.PassiveProperty.SpecificCapacitance, (1e-3) * U.uF / U.cm2)

gj = sim.create_gapjunction(
    celllocation1 = cell1.soma,
    celllocation2 = cell2.soma,
    resistance = 100 * mf.units.MOhm
    )

cc = sim.create_currentclamp(cell_location=cell1.soma,
                        amp=200 * U.pA,
                        delay=100*U.ms,
                        dur=250*U.ms)



sim.record(cell1, what=mf.StandardTags.Voltage)
sim.record(cell2, what=mf.StandardTags.Voltage)
sim.record(cc, what=mf.StandardTags.Current)

res = sim.run()


mf.TagViewer(res)


