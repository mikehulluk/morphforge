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




from morphforge.componentlibraries.channellibrary import ChannelLibrary, cached_functor
from morphforge.componentlibraries.celllibrary import CellLibrary
from morphforge.core.quantities.fromcore import unit
from morphforgecontrib.data_library.stdmodels import StandardModels

from morphforge.morphology.builders import MorphologyBuilder


def build_hh_cell(sim, cell_area=None):
    
    if cell_area is None:
        cell_area = unit('5000:um2')
    
    morphology = MorphologyBuilder.get_single_section_soma(area = cell_area)
    cell = sim.create_cell(morphology=morphology)

    # Apply the channels uniformly over the cell
    env = sim.environment
    modelsrc=StandardModels.HH52
    cell.apply_channel( ChannelLibrary.get_channel(modelsrc=modelsrc, celltype=None, channeltype="Na", env=env) )
    cell.apply_channel( ChannelLibrary.get_channel(modelsrc=modelsrc, celltype=None, channeltype="K", env=env)  )
    cell.apply_channel( ChannelLibrary.get_channel(modelsrc=modelsrc, celltype=None, channeltype="Lk", env=env) )

    return cell
CellLibrary.register(celltype=None, modelsrc=StandardModels.HH52, cell_functor=build_hh_cell)
