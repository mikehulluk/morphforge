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

from core.cell import Cell
from core.celllocation import CellLocation
from core.simulation import Simulation
from core.simulationenvironment import SimulationEnvironment
from stimulation import CurrentClamp, VoltageClamp
from stimulation import CurrentClampStepChange, VoltageClampStepChange
from result import SimulationResult
from segmentation import AbstCellSegmenter
from segmentation import CellSegmenter_MaxCompartmentLength
from biophysics import CellBiophysics, Channel, \
    ChannelApplicator, ChannelApplicatorUniform, \
    Targeter
from biophysics import ChannelTargeterEverywhere, \
    ChannelTargeterRegion, \
    ChannelTargeterSection, \
    ChannelTargeterSectionPath
from biophysics import PassiveTargetterEverywhere, \
    PassiveTargetterEverywhereDefault
from biophysics import PassiveProperty

from networks import Synapse, GapJunction
from networks import PostSynapticMech, SynapticTrigger
from base_classes import NamedSimulationObject

# New Synapse implementation
from networks import PostSynapticMechTemplate
from networks import PostSynapticMechInstantiation

__all__ = [
    'CurrentClamp',
    'VoltageClamp',
    'CurrentClampStepChange',
    'VoltageClampStepChange',
    'Simulation',
    'SimulationResult',
    'Cell',
    'CellLocation',
    'SimulationEnvironment',
    'AbstCellSegmenter',
    'CellSegmenter_MaxCompartmentLength',
    'CellBiophysics',
    'Channel',
    'ChannelApplicator',
    'ChannelApplicatorUniform',
    'Targeter',
    'ChannelTargeterEverywhere',
    'ChannelTargeterRegion',
    'ChannelTargeterSection',
    'ChannelTargeterSectionPath',
    'PassiveTargetterEverywhere',
    'PassiveTargetterEverywhereDefault',
    'PassiveProperty',

    'Synapse',
    'GapJunction',
    'PostSynapticMech',
    'SynapticTrigger',
    'NamedSimulationObject',

    'PostSynapticMechTemplate',
    'PostSynapticMechInstantiation',
    ]
