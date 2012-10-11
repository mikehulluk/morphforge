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



"""Demonstrate using NEURON mod files directly in a simulation
We run two simulations, using 2 slightly different mod files, and plot the membrane voltage seen.

"""


from morphforge.stdimports import *
from morphforgecontrib.simulation.channels.exisitingmodfile.core import SimulatorSpecificChannel


def build_simulation(modfilename):
    # Create the morphology for the cell:
    morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
    m1 = MorphologyTree.fromDictionary(morphDict1)


    # Create the environment:
    env = NEURONEnvironment()

    # Create the simulation:
    sim = env.Simulation()
    cell = sim.create_cell(morphology=m1)


    modChls = env.Channel(SimulatorSpecificChannel, modfilename=modfilename)

    # Apply the mechanisms to the cells
    cell.apply_channel( modChls)

    sim.record(cell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = cell.soma, description='Membrane Voltage')
    sim.create_currentclamp(name="Stim1", amp=unit("200:pA"), dur=unit("100:ms"), delay=unit("100:ms"), cell_location=cell.soma)

    results = sim.run()
    return results



mod3aFilename = Join(LocMgr.get_test_mods_path(), "exampleChannels3a.mod")
results3a = build_simulation(mod3aFilename)

mod3bFilename = Join(LocMgr.get_test_mods_path(), "exampleChannels3b.mod")
results3b = build_simulation(mod3bFilename)

TagViewer([results3a, results3b], timerange=(95, 200)*units.ms)

try:
    import os
    print 'Differences between the two mod files:'
    os.system("diff %s %s"%(mod3aFilename, mod3bFilename))
except:
    print "<Can't run 'diff', so can't show differences!>"





















