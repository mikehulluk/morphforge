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


# Make these functions available through morphforge.units,
# since they are commonly used
from morphforge.units.util import factorise_units_from_list
from morphforge.units.util import qty
from morphforge.units.wrappers import NpPqWrappers

from morphforge.units.util import parse_unit_str


# Import all the units from quantities:
#from quantities import *
from quantities import pA


# Import some commonly-used neuroscience units:
from morphforge.units.common_neuroscience_defs import mS, uS, nS, pS
from morphforge.units.common_neuroscience_defs import mF, uF, nF, pF
from morphforge.units.common_neuroscience_defs import um2, cm2, mm2, m2
from morphforge.units.common_neuroscience_defs import ohmcm 
from morphforge.units.common_neuroscience_defs import MOhm
from morphforge.units.common_neuroscience_defs import mV
from morphforge.units.common_neuroscience_defs import molar, millimolar, micromolar, nanomolar
from morphforge.units.common_neuroscience_defs import mM, uM
from morphforge.units.common_neuroscience_defs import per_mM, per_mV



