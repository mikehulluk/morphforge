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



"""Hodgkin-Huxley '52 neuron simulation.

A simulation of the HodgkinHuxley52 neuron. We create 3 channels, Lk, Na, and K channels and apply them over the neuron.
The morphforge backend takes care of building/compiling .mod-files from these,
and runs the simulation.
Note that the neurons reseting potentials have been shifted from 0mV to -65mV.
"""



from morphforge.stdimports import *
from morphforgecontrib.stdimports import StdChlLeak
from morphforgecontrib.stdimports import StdChlAlphaBeta


# Create the environment:
env = NEURONEnvironment()

# Create the simulation:
sim = env.Simulation()


# Create a cell:
morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
m1 = MorphologyTree.fromDictionary(morphDict1)
cell = sim.create_cell(name="Cell1", morphology=m1)


lk_chl = env.Channel(
                         StdChlLeak,
                         name="LkChl",
                         conductance=qty("0.3:mS/cm2"),
                         reversalpotential=qty("-54.3:mV"),
                       )

na_state_vars = { "m": {
                      "alpha":[-4.00,-0.10,-1.00,40.00,-10.00],
                      "beta": [4.00, 0.00, 0.00,65.00, 18.00]},
                    "h": {
                        "alpha":[0.07,0.00,0.00,65.00,20.00] ,
                        "beta": [1.00,0.00,1.00,35.00,-10.00]}
                  }

na_chl = env.Channel(
                        StdChlAlphaBeta,
                        name="NaChl", ion="na",
                        equation="m*m*m*h",
                        conductance=qty("120:mS/cm2"),
                        reversalpotential=qty("50:mV"),
                        statevars=na_state_vars,
                        
                       )
k_state_vars = { "n": {
                      "alpha":[-0.55,-0.01,-1.0,55.0,-10.0],
                      "beta": [0.125,0,0,65,80]},
                   }

k_chl = env.Channel(
                        StdChlAlphaBeta,
                        name="KChl", ion="k",
                        equation="n*n*n*n",
                        conductance=qty("36:mS/cm2"),
                        reversalpotential=qty("-77:mV"),
                        statevars=k_state_vars,
                        
                       )


# Apply the channels uniformly over the cell
cell.apply_channel( lk_chl)
cell.apply_channel( na_chl)
cell.apply_channel( k_chl)
cell.set_passive( PassiveProperty.SpecificCapacitance, qty('1.0:uF/cm2'))


# Create the stimulus and record the injected current:
cc = sim.create_currentclamp(name="Stim1", amp=qty("250:pA"), dur=qty("100:ms"), delay=qty("100:ms"), cell_location=cell.soma)
sim.record(cc, what=StandardTags.Current)
# Define what to record:
sim.record(cell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = cell.soma)

# run the simulation
results = sim.run()

# Create an output .pdf
SimulationMRedoc.build( sim ).to_pdf(__file__ + '.pdf')

# Display the results:
TagViewer([results], timerange=(50, 250)*units.ms, show=True)


