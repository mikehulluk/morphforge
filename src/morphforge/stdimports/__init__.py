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

# pylint: disable=W0401
# (don't complain about wildcard imports)
from morphforge.core.quantities import *
import morphforge.core.quantities as u

from mhlibs.quantities_plot import *

# CORE
from morphforge.core import *

from morphforge.traces import *
from morphforge.traces.eventset import EventSet, Event

from morphforge.simulationanalysis.tagviewer import TagViewer
from morphforge.simulationanalysis.tagviewer import PlotSpec_DefaultNew
from morphforge.simulationanalysis.tagviewer import DefaultPlotSpec

#
from morphforge.constants import *

# MORPHOLOGY:
from morphforge.morphology import *
from morphforge.morphology.core import *
from morphforge.morphology.builders import *
from morphforge.morphology.visitor import *
from morphforge.morphology.util.morphlocator import MorphLocator

# SIMULATION
from morphforge.simulation.base import *
from morphforge.simulation.neuron import *
from morphforge.simulation.base.util.celllocator import CellLocator

# Simulation Analysis
#from morphforge.simulationanalysis.summaries import *

from morphforge.componentlibraries import *

from morphforge.simulation.base.biophysics.mta_helpers import *

import morphforge.simulation.neuron.objects.obj_cclamp
import morphforge.simulation.neuron.objects.obj_vclamp

from morphforge.morphology.conventions import SWCRegionCodes

try:
    import pylab
    import numpy as np
except ImportError:
    print 'Problem importing Numpy or Matplotlib'
    pass

import neurounits

import os

from morphforge.morphology.core.tree import MorphPath
from morphforge.simulation.base.segmentation.cellsegmenter import CellSegmenter_MaxLengthByID

import quantities as pq
