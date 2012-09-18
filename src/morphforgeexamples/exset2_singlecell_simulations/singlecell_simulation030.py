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



"""Hodgkin-Huxley '52 neuron simulation with automatic summary pdf generation.

The same simulation of the HodgkinHuxley52 neuron as before, but by adding
a single line, we can generate a pdf output of the simulation! (You can do this
on any simulation.)

.. code-block:: python

    SimulationSummariser(simulationresult=results, filename="SimulationOutput.pdf", make_graphs=True)


TODO: THIS IS NOT WORKING  - DISABLED TO ALLOW runnnign during pdf gen refactor
"""




from morphforge.stdimports import *
from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmleak import MM_LeakChannel
from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmalphabeta import MM_AlphaBetaChannel


# Create the environment:
env = NEURONEnvironment()

# Create the simulation:
sim = env.Simulation()


# Create a cell:
morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
m1 = MorphologyTree.fromDictionary(morphDict1)
cell = sim.create_cell(name="Cell1", morphology=m1)


lk_chl = env.Channel(
                         MM_LeakChannel,
                         name="LkChl",
                         conductance=unit("0.3:mS/cm2"),
                         reversalpotential=unit("-54.3:mV"),
                         mechanism_id = 'HULL12_DIN_LK_ID'
                       )

na_state_vars = { "m": {
                      "alpha":[-4.00,-0.10,-1.00,40.00,-10.00],
                      "beta": [4.00, 0.00, 0.00,65.00, 18.00]},
                    "h": {
                        "alpha":[0.07,0.00,0.00,65.00,20.00] ,
                        "beta": [1.00,0.00,1.00,35.00,-10.00]}
                  }

na_chl = env.Channel(
                        MM_AlphaBetaChannel,
                        name="NaChl", ion="na",
                        equation="m*m*m*h",
                        conductance=unit("120:mS/cm2"),
                        reversalpotential=unit("50:mV"),
                        statevars=na_state_vars,
                        mechanism_id="HH_NA_CURRENT"
                       )
kStateVars = { "n": {
                      "alpha":[-0.55,-0.01,-1.0,55.0,-10.0],
                      "beta": [0.125,0,0,65,80]},
                   }

k_chl = env.Channel(
                        MM_AlphaBetaChannel,
                        name="KChl", ion="k",
                        equation="n*n*n*n",
                        conductance=unit("36:mS/cm2"),
                        reversalpotential=unit("-77:mV"),
                        statevars=kStateVars,
                        mechanism_id="HH_K_CURRENT"
                       )


# Apply the channels uniformly over the cell
apply_mechanism_everywhere_uniform(cell, lk_chl)
apply_mechanism_everywhere_uniform(cell, na_chl)
apply_mechanism_everywhere_uniform(cell, k_chl)
apply_passive_everywhere_uniform(cell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2'))

# Get a cell_location on the cell:
somaLoc = cell.get_location("soma")

# Create the stimulus and record the injected current:
cc = sim.create_currentclamp(name="Stim1", amp=unit("250:pA"), dur=unit("100:ms"), delay=unit("100:ms"), cell_location=somaLoc)
sim.record(cc, what=StandardTags.Current)
# Define what to record:
sim.record(cell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = somaLoc)

# run the simulation
results = sim.run()

#SimulationSummariser(simulationresult=results, filename="SimulationOutput.pdf", make_graphs=True)

# Display the results:
TagViewer([results], timerange=(50, 250)*pq.ms, show=True)


#summary = SimulationMRedoc.build(sim)
#summary.to_pdf('~/Desktop/pdfs/%s.pdf'%__file__.split('/')[-1])
