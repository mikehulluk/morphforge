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

from morphforge.core.quantities.fromcore import factorise_units_from_list
from morphforge.core.quantities.fromcore import unit
import common_neuroscience_defs
from morphforge.core.quantities.wrappers import NpPqWrappers
from morphforge.core.quantities.common_neuroscience_defs import mS, uS, nS, pS
from morphforge.core.quantities.common_neuroscience_defs import mF, uF, nF, pF
from morphforge.core.quantities.common_neuroscience_defs import um2, cm2
from morphforge.core.quantities.common_neuroscience_defs import mm2, m2
from morphforge.core.quantities.common_neuroscience_defs import Molar, nMolar
from morphforge.core.quantities.common_neuroscience_defs import uMolar
from morphforge.core.quantities.common_neuroscience_defs import ohmcm
from morphforge.core.quantities.common_neuroscience_defs import MOhm
from morphforge.core.quantities.common_neuroscience_defs import mV
from morphforge.core.quantities.common_neuroscience_defs import pA_um2
from quantities import ms, Quantity, millivolt, milliamp, picoamp
from quantities import milli, siemens, millisecond, volt, J, second

U = unit
__all__ = [
   'factorise_units_from_list',
   'unit',
   'NpPqWrappers',
   'common_neuroscience_defs',
   'mS', 'uS', 'nS', 'pS',
   'mF', 'uF', 'nF', 'pF',
   'um2', 'cm2', 'mm2', 'm2',
   'Molar', 'uMolar', 'nMolar',
   'ohmcm', 'MOhm',

   'mV','pA_um2',
   'ms',
   'Quantity',
   'millivolt','milliamp','picoamp',
   'milli', 'siemens',
   'millisecond',
   'volt','J','second'
]


