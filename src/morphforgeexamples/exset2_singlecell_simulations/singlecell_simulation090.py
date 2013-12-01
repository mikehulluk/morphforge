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


"""Compartmentalisation of neuron


   soma              axon

  |--20--|-----------4000----------|
  --------
  |      |
  |      | =========================
  |      |
  --------

        ^
        |
        x0
        
In this set of simulations, we create a cell consisting of a soma and 
long axon. We use a current-clamp at the soma to start an action potential 
that propagates along the axon and record the voltages at 10um intervals (~400 recordings)
along the axon. In each simulation, we change the number of compartments of the axon.

"CellSegmenter_MaxLengthByID" allows us to specify the maximum length of 
a compartment based on the Section ID. We see that as the length of the 
compartments goes up, the number of distinct recordings goes down.


Custom cell-segmentation algorithms can be written by subclassing 
from: 'CellSegmenterStd' and overridding the method: '_get_n_segments(self, section)', 
which should query the section and return the number of compartments in the cell.
"""


from morphforge.stdimports import *
from morphforgecontrib.stdimports import *



def run_sim(axon_compartment_length):
    
    env = NEURONEnvironment()
    sim = env.Simulation()

    # Create a cell, consisting of a soma and long axon:
    morphDict1 = {'root': {'length': 20, 'diam': 20, 'id':'soma', 'sections': [ {'length':4000,'diam':0.3, 'id':'axon'} ] } }
    m1 = MorphologyTree.fromDictionary(morphDict1)
    cell = sim.create_cell(
                name="Cell1", 
                morphology=m1, 
                segmenter=CellSegmenter_MaxLengthByID(section_id_segment_maxsizes={'soma':20,'axon':axon_compartment_length} ) 
                )

    lk_chl = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Lk", env=env)
    na_chl = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="Na", env=env)
    k_chl = ChannelLibrary.get_channel(modelsrc=StandardModels.HH52, channeltype="K", env=env)

    # Apply the channels uniformly over the cell
    cell.apply_channel( lk_chl)
    cell.apply_channel( na_chl)
    cell.apply_channel( k_chl)
    cell.set_passive( PassiveProperty.SpecificCapacitance, qty('1.0:uF/cm2'))

    # Create the stimulus and record the injected current:
    cc = sim.create_currentclamp(name="Stim1", amp=qty("250:pA"), dur=qty("5:ms"), delay=qty("100:ms"), cell_location=cell.soma)
    sim.record(cc, what=StandardTags.Current, user_tags=['AxonCompLength%d'%axon_compartment_length])

    # Define a series of points at 50um intervals along the axon to record voltage at:
    pts_along_cell = CellLocator.get_locations_at_distances_away_from_dummy(cell=cell, distances= [0] + list(range(20,4000, 10) ) )
    x0 = CellLocator.get_location_at_distance_away_from_dummy(cell=cell, distance=20 ).morphlocation

    for pt in pts_along_cell:
        dist = "Distance%04d"%MorphPath(x0, pt.morphlocation).get_length()
        sim.record(cell, what=StandardTags.Voltage, description=dist, user_tags=['AxonCompLength%d'%axon_compartment_length], cell_location = pt)

    # run the simulation
    results = sim.run()
    return results




axon_compartment_lengths = [20,50,100,200,500]
results = [ run_sim(axon_compartment_length=ax_comp_len) for ax_comp_len in axon_compartment_lengths]

TagViewer(results, 
          timerange=(98, 125)*units.ms,
          plots = 
                [ TagPlot("ALL{Voltage,AxonCompLength%d}"%ax_comp_len, ylabel='Axon comp \n Length:%dum\n (Voltage)'%ax_comp_len, yrange=(-80*units.mV, 50*units.mV), yunit=units.mV,  legend_labeller=None, yticklabel_quantisation=Decimal('1')) for ax_comp_len in axon_compartment_lengths] +
                [ TagPlot("ALL{Current,AxonCompLength20}", ylabel='Current', yunit=units.picoamp, yticklabel_quantisation=Decimal('1') ) ]
                  )



