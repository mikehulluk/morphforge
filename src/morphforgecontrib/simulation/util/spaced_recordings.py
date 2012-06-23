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


from morphforge.stdimports import MorphLocator
from morphforge.stdimports import CellLocation
from morphforge.stdimports import Cell


def space_record_cell(cell, sim, distances, record_functor=None, user_tags=None):



    user_tags = user_tags or []
    user_tags.append( cell.name )

    #morph_locs = MorphLocator.get_locationsAtDistancesAwayFromSoma(morphology=cell.morphology, distances= distances )
    morph_locs = MorphLocator.get_locations_at_distances_away_from_dummy(morphology=cell.morphology, distances= distances )
    locations = [ CellLocation(cell=cell, morphlocation=ml) for ml in morph_locs ]
    for i,(loc,distance) in enumerate(zip(locations,distances)):
        sim.record( cell, location=loc, name='%sLoc%03d'%(cell.name,i), what=Cell.Recordables.MembraneVoltage, description="%s Distance Recording at %d (um)"%(cell.name, distance), user_tags=user_tags )



