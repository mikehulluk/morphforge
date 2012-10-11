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


import morphforge.stdimports as mf
#import morphforgecontrib.stdimports as mfc
#from  morphforge.stdimports import * 
from  morphforgecontrib.stdimports import * 

from morphforgecontrib.data_library import StandardModels

def build_passive_cell(sim, input_resistance, capacitance=None, area=None, name=None, reversalpotential=None):
    unit = mf.unit
    env = sim.environment
    
    if area is None:
        area = unit('1000:um2')
        
    if capacitance is None:
        capacitance = unit('10:pF')
        
    if reversalpotential is None:
        reversalpotential = unit('-60:mV')
    
    lk = env.Channel( StdChlLeak, 
            conductance = ((1/input_resistance) / area ),
            reversalpotential = reversalpotential,
            )
            
    cell = sim.create_cell(area=area, name=name)
    cell.apply_channel(lk)
    cell.set_passive(mf.PassiveProperty.SpecificCapacitance, capacitance / area)

    return cell
    
    

mf.CellLibrary.register(celltype=None, modelsrc=StandardModels.SingleCompartmentPassive, cell_functor=build_passive_cell)
    
    
        
        
    
