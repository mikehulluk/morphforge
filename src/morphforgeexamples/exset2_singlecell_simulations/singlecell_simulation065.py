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




"""Using a channel library to reduce duplication.

We define functions that produce morphology and channel objects for our simulations.
We could stop here, and simply import and use the functions in our simulations, but
we go a step further, and register them with  "ChannelLibrary" and "MorphologyLibrary".
These are basically glorified dictionaries, that do the lookup for the appropriate functors
based on a key from the tuple (modelsrc, celltype, channeltype). The advantage for doing this is that
there is single repository for morphologies and channels.

There is not really anythin clever going on here, and you can run simulations completely ignorantly
of these classes, I just included it because it made life much easier for me, when I had to start managing
lots of channel definitions.

"""


from morphforge.stdimports import *
from morphforgecontrib.stdimports import StdChlLeak,StdChlAlphaBeta




# This can be put into a file that is loaded on
# you path somewhere:
# ======================================================
def getSimpleMorphology():
    mDict  = {'root': { 'length': 17.5, 'diam': 17.5, 'id':'soma', 'region':'soma',   } }
    return  MorphologyTree.fromDictionary(mDict)


def get_sample_lk(env):
    lk_chl = env.Channel(
                         StdChlLeak,
                         name="LkChl",
                         conductance=qty("0.3:mS/cm2"),
                         reversalpotential=qty("-54.3:mV"),
                       )
    return lk_chl


def get_sample_na(env):
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
    return na_chl


def get_sample_k(env):
    k_state_vars = { "n": { "alpha":[-0.55,-0.01,-1.0,55.0,-10.0],
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
    return k_chl



MorphologyLibrary.register_morphology(modelsrc="Sample", celltype="Cell1", morph_functor=getSimpleMorphology)
ChannelLibrary.register_channel(modelsrc="Sample", celltype="Cell1", channeltype="Na", chl_functor=get_sample_na)
ChannelLibrary.register_channel(modelsrc="Sample", celltype="Cell1", channeltype="K", chl_functor=get_sample_k)
ChannelLibrary.register_channel(modelsrc="Sample", celltype="Cell1", channeltype="Lk", chl_functor=get_sample_lk)

# =============================================================









# Now in our script elsewhere, we can use them as:
modelsrc = "Sample"
celltype="Cell1"

# Create the environment:
env = NEURONEnvironment()

# Create the simulation:
sim = env.Simulation()

# Create a cell:
morphology=MorphologyLibrary.get_morphology(modelsrc=modelsrc, celltype=celltype)
cell = sim.create_cell(morphology=morphology)

# Apply the channels uniformly over the cell
na_chl = ChannelLibrary.get_channel(modelsrc=modelsrc, celltype=celltype, channeltype="Na", env=env)
k_chl  = ChannelLibrary.get_channel(modelsrc=modelsrc, celltype=celltype, channeltype="K", env=env)
lk_chl = ChannelLibrary.get_channel(modelsrc=modelsrc, celltype=celltype, channeltype="Lk", env=env)

cell.apply_channel( na_chl)
cell.apply_channel( k_chl )
cell.apply_channel( lk_chl)

cell.set_passive( PassiveProperty.SpecificCapacitance, qty('1.0:uF/cm2'))

# Create the stimulus and record the injected current:
cc = sim.create_currentclamp(name="Stim1", amp=qty("150:pA"), dur=qty("5:ms"), delay=qty("100:ms"), cell_location=cell.soma)

sim.record(cc, what=StandardTags.Current)
sim.record(cell, what=StandardTags.Voltage, cell_location=cell.soma)


# run the simulation
results = sim.run()

# Display the results:
TagViewer([results], timerange=(97.5, 140)*units.ms)
