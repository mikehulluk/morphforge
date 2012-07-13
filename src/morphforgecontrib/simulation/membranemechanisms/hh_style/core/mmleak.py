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



from morphforge.core.quantities import  unit
from morphforge.simulation.base import MembraneMechanism

from morphforge.constants import StandardTags

class MM_LeakChannel(MembraneMechanism):

    class Recordables():
        ConductanceDensity = StandardTags.ConductanceDensity
        CurrentDensity = StandardTags.CurrentDensity
        all = [ConductanceDensity, CurrentDensity]

    def __init__(self, name, conductance, reversalpotential, mechanism_id=None):
        if not mechanism_id:
            mechanism_id = "StdLeakChl"
        MembraneMechanism.__init__(self, mechanism_id=mechanism_id)
        self.name = name
        self.conductance = unit(conductance)
        self.reversalpotential = unit(reversalpotential)

    def get_variables(self):
        return ['gLk', 'eLk', 'gScale']

    def get_defaults(self):
        return {"gLk":self.conductance, "eLk":self.reversalpotential, "gScale": unit("1.0") }



