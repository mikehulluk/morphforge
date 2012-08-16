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


"""The response of a single compartment neuron with leak channels to step current injection.
In this example, we build a single section neuron, with passive channels,
and stimulate it with a step current clamp of 200pA for 100ms starting at t=100ms.
We also create a summary pdf of the simulation.
"""



from morphforge.stdimports import *
from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmleak import MM_LeakChannel


# Create the morphology for the cell:
morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
m1 = MorphologyTree.fromDictionary(morphDict1)

# Create the environment:
env = NeuronSimulationEnvironment()

# Create the simulation:
mySim = env.Simulation()


# Create a cell:
myCell = mySim.create_cell(name="Cell1", morphology=m1)


# Apply the mechanisms to the cells
leakChannels = env.MembraneMechanism(MM_LeakChannel,
                         name="LkChl",
                         conductance=unit("0.25:mS/cm2"),
                         reversalpotential=unit("-51:mV"),
                         mechanism_id = 'HULL12_DIN_LK_ID'
                       )

apply_mechanism_everywhere_uniform(myCell, leakChannels)
apply_passive_everywhere_uniform(myCell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2'))


# Get a cell_location on the cell:
somaLoc = myCell.get_location("soma")

# Create the stimulus and record the injected current:
cc = mySim.create_currentclamp(name="Stim1", amp=unit("200:pA"), dur=unit("100:ms"), delay=unit("100:ms"), cell_location=somaLoc)


# Define what to record:
mySim.record(myCell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = somaLoc)
mySim.recordall(leakChannels, cell_location=somaLoc)


# run the simulation
results = mySim.run()

# Create an output .pdf
SimulationSummariser(simulationresult=results, filename="Simulation010Output.pdf", make_graphs=True)

# Display the results:
TagViewer([results], figtitle="The response of a neuron to step current injection", timeranges=[(95, 200)*pq.ms], show=True)



