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


# pylint: disable=W0401,W0611,W0614


# Move to morphforge:
#TODO: move to morphforge
from morphforgecontrib.simulation.populations import NeuronPopulation, Connectors, PopAnalSpiking, SynapsePopulation



from morphology.util import AxonTrimmer
from morphology.util import cell_location_distance_from_soma
from morphology.util import MorphologyTranslator


# Pre synaptic mechanisms
from morphforgecontrib.simulation.presynapticmechanisms.core import PreSynapticMech_TimeList
from morphforgecontrib.simulation.presynapticmechanisms.core import PreSynapticMech_VoltageThreshold



# Traces tagging:
from traces import AutoTaggerFromUnit
from morphforgecontrib.tags import StdTagFunctors, UserTagFunctorCellLocation

# Simulation utility functions:
from morphforgecontrib.simulation.util.voltageclampchannel import get_voltageclamp_soma_current_trace
from morphforgecontrib.simulation.util.calculate_input_resistance import CellAnalysis_IVCurve
from morphforgecontrib.simulation.util.calculate_input_resistance import CellAnalysis_IVCurve, CellAnalysis_StepInputResponse, CellAnalysis_ReboundResponse
from morphforgecontrib.traces.tracetools import SpikeFinder
from morphforgecontrib.simulation.util.spaced_recordings import space_record_cell
from morphforgecontrib.simulation.util import exec_with_prob
from morphforgecontrib.simulation_analysis.spikinggrouping import DBScan


# Simulation Channels:
from morphforgecontrib.simulation.membranemechanisms.inftauinterpolated.core import MM_InfTauInterpolatedChannel, InfTauInterpolation
from morphforgecontrib.simulation.membranemechanisms.hh_style.core import StdChlAlphaBeta, StdChlLeak, StdChlAlphaBetaBeta
from morphforgecontrib.simulation.membranemechanisms.exisitingmodfile.core import SimulatorSpecificChannel
from morphforgecontrib.simulation.membranemechanisms.neurounits.neuro_units_bridge import NeuroUnitEqnsetMechanism
from morphforgecontrib.simulation.membranemechanisms.neurounits.neuro_units_bridge import Neuron_NeuroUnitEqnsetMechanism

# Mike Hull development:
from socket import gethostname
if gethostname() in ['michael-DQ57TM']:
    from morphforgecontrib.mhdev import *

# Syanptic Templates:
from morphforgecontrib.simulation.synapse_templates.neurounit import * 
from morphforgecontrib.simulation.synapse_templates.exponential_form.expsyn.core import * 
from morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core import * 
from morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core import * 

# Constants for accessing standard models:
from morphforgecontrib.data_library.stdmodels import StandardModels
