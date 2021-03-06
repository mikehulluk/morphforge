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


"""Visualising the internal states of a neuron

We look at the internal states of an HH neuron, and plot the properties on
different graphs.

"""


from morphforge.stdimports import *
from morphforgecontrib.stdimports import *



# Create the environment:
env = NEURONEnvironment()

# Create the simulation:
sim = env.Simulation()


# Create a cell:
morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
m1 = MorphologyTree.fromDictionary(morphDict1)
cell = sim.create_cell(name="Cell1", morphology=m1)


# Apply the channels uniformly over the cell
lk_chl = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Lk", env=env)
na_chl = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Na", env=env)
k_chl = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="K", env=env)

cell.apply_channel( lk_chl)
cell.apply_channel( na_chl)
cell.apply_channel( k_chl)
cell.set_passive( PassiveProperty.SpecificCapacitance, qty('1.0:uF/cm2'))

# Create the stimulus and record the injected current:
cc = sim.create_currentclamp(name="Stim1", amp=qty("250:pA"), dur=qty("100:ms"), delay=qty("100:ms"), cell_location=cell.soma)
sim.record(cc, what=StandardTags.Current)

# Define what to record:
sim.record(cell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = cell.soma)
sim.record(lk_chl, cell_location = cell.soma, what=StandardTags.ConductanceDensity)
sim.record(na_chl, cell_location = cell.soma, what=StandardTags.ConductanceDensity)
sim.record(k_chl,  cell_location = cell.soma, what=StandardTags.ConductanceDensity)

sim.record(lk_chl, cell_location = cell.soma, what=StandardTags.CurrentDensity)
sim.record(na_chl, cell_location = cell.soma, what=StandardTags.CurrentDensity)
sim.record(k_chl,  cell_location = cell.soma, what=StandardTags.CurrentDensity)

sim.record(na_chl, cell_location = cell.soma, what=StandardTags.StateVariable, state="m")
sim.record(na_chl, cell_location = cell.soma, what=StandardTags.StateVariable, state="h")
sim.record(k_chl,  cell_location = cell.soma, what=StandardTags.StateVariable, state="n")

# run the simulation
results = sim.run()


# Display the results, there is a lot of info for one graph, so lets split it up:
TagViewer([results], timerange=(50, 250)*units.ms, show=False)


TagViewer([results], timerange=(50, 250)*units.ms, show=False,
          plots = [
                       DefaultTagPlots.Voltage,
                       DefaultTagPlots.Current,
                       DefaultTagPlots.CurrentDensity,
                      ])


TagViewer([results], timerange=(100, 120)*units.ms, show=True,
          plots = [
                       DefaultTagPlots.Voltage,
                       DefaultTagPlots.ConductanceDensity,
                       DefaultTagPlots.StateVariable,
                      ])
