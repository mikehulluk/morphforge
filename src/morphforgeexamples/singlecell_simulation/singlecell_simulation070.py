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
from morphforge.traces.tagviewer.tagviewer import DefaultPlotSpec
from morphforgecontrib.data_library.stdmodels import StandardModels



# Create the environment:
env = NeuronSimulationEnvironment()

# Create the simulation:
mySim = env.Simulation()


# Create a cell:
morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma'} }
m1 = MorphologyTree.fromDictionary(morphDict1)
myCell = mySim.create_cell(name="Cell1", morphology=m1)


lkChannels = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Lk", env=env)
naChannels = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Na", env=env)
kChannels = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="K", env=env)


# Apply the channels uniformly over the cell
apply_mechanism_everywhere_uniform(myCell, lkChannels )
apply_mechanism_everywhere_uniform(myCell, naChannels )
apply_mechanism_everywhere_uniform(myCell, kChannels )
apply_passive_everywhere_uniform(myCell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )

# Get a cell_location on the cell:
somaLoc = myCell.get_location("soma")

# Create the stimulus and record the injected current:
cc = mySim.create_currentclamp( name="Stim1", amp=unit("250:pA"), dur=unit("100:ms"), delay=unit("100:ms"), celllocation=somaLoc)
mySim.record( cc, what=StdRec.Current)
# Define what to record:
mySim.record( myCell, what=StdRec.MembraneVoltage, name="SomaVoltage", cell_location = somaLoc )


mySim.record( lkChannels, where = somaLoc, what=StdRec.ConductanceDensity )
mySim.record( naChannels, where = somaLoc, what=StdRec.ConductanceDensity )
mySim.record( kChannels,  where = somaLoc, what=StdRec.ConductanceDensity )

mySim.record( lkChannels, where = somaLoc,what=StdRec.CurrentDensity )
mySim.record( naChannels, where = somaLoc,what=StdRec.CurrentDensity )
mySim.record( kChannels,  where = somaLoc, what=StdRec.CurrentDensity )


mySim.record( naChannels, where = somaLoc, what=StdRec.StateVariable, state="m" )
mySim.record( naChannels, where = somaLoc, what=StdRec.StateVariable, state="h" )
mySim.record( kChannels,  where = somaLoc, what=StdRec.StateVariable, state="n" )


# Also:
#mySim.record( naChannels, where = somaLoc, what=StdRec.StateVarTimeConstant, state="m" )
#mySim.record( naChannels, where = somaLoc, what=StdRec.StateVarTimeConstant, state="h" )
#mySim.record( kChannels,  where = somaLoc, what=StdRec.StateVarTimeConstant, state="n" )

#mySim.record( naChannels, where = somaLoc, what=StdRec.StateVarSteadyState, state="m" )
#mySim.record( naChannels, where = somaLoc, what=StdRec.StateVarSteadyState, state="h" )
#mySim.record( kChannels,  where = somaLoc, what=StdRec.StateVarSteadyState, state="n" )


# run the simulation
results = mySim.run()


# Display the results, there is a lot of info for one graph, so lets split it up:
TagViewer([results], timeranges=[(50, 250)*pq.ms], show=False )


TagViewer([results], timeranges=[(50, 250)*pq.ms], show=False,
          plotspecs = [
                       DefaultPlotSpec.Voltage,
                       DefaultPlotSpec.Current,
                       DefaultPlotSpec.CurrentDensity,
                       ] )


TagViewer([results], timeranges=[(100, 120)*pq.ms], show=True,
          plotspecs = [
                       DefaultPlotSpec.Voltage,
                       DefaultPlotSpec.ConductanceDensity,
                       DefaultPlotSpec.StateVariable,
                       ] )
