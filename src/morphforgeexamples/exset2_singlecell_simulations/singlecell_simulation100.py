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


"""Spcifiying the different types of current clamps
TODO!
"""



from morphforge.stdimports import *
from morphforgecontrib.stdimports import *




# Create the environment:
env = NEURONEnvironment()
sim = env.Simulation()


# Create a cell:
m1 = MorphologyTree.fromDictionary({'root': {'length': 20, 'diam': 40, 'id':'soma'} })
cell = sim.create_cell(name="Cell1", morphology=m1)

# Apply the channels uniformly over the cell
lk_chl = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Lk", env=env)
cell.apply_channel( lk_chl)

# Create a selection of current clamps
cc0 = sim.create_currentclamp(name='CC0', amp=750*units.pA, dur=40*units.ms, delay=40*units.ms, cell_location=cell.soma)
cc1 = sim.create_currentclamp(name='CC1', amp=200*units.pA, dur=40*units.ms, delay=100*units.ms, cell_location=cell.soma)

cc2 = sim.create_currentclamp(protocol=CurrentClampSinwave, name='CC2', 
            amp=150*units.pA, freq=100*units.Hz, 
            delay=150*units.ms, bias = 0*units.pA, duration=40*units.ms, cell_location=cell.soma)
cc3 = sim.create_currentclamp(protocol=CurrentClampSinwave, name='CC3', 
            amp=250*units.pA, freq=250*units.Hz,
            delay=200*units.ms, bias = 200*units.pA, duration=40*units.ms, cell_location=cell.soma)

cc4 = sim.create_currentclamp(protocol=CurrentClampRamp, name='CC4', 
            amp0=0*units.pA, amp1=100*units.pA, 
            time0=250*units.ms, time1=280*units.ms, time2=290*units.ms, cell_location=cell.soma)
cc5 = sim.create_currentclamp(protocol=CurrentClampRamp, name='CC5',
            amp0=-50*units.pA, amp1=-100*units.pA, 
            time0=300*units.ms, time1=330*units.ms, time2=340*units.ms, cell_location=cell.soma)




for cc in [cc0,cc1,cc2,cc3, cc4, cc5]:
    sim.record(cc, what=StandardTags.Current)
sim.record(cell, what=StandardTags.Voltage, cell_location = cell.soma)



results = sim.run()



TagViewer([results], timerange=(30, 500)*units.ms )

