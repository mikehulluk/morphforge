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


class MHOCSections(object):

    InitHeader = 'InitHeader'
    InitTemplates = 'InitTemplates'
    InitCells = 'InitCells'
    InitCellMembranes = 'InitCellMembranes'
    InitVoltageClamps = 'InitVoltageClamps'
    InitCurrentClamps = 'InitCurrentClamps'
    InitSynapsesChemPost = 'InitSynapsesChemPost'
    InitSynapsesChemPre = 'InitSynapsesChemPre'
    InitGapJunction = 'InitGapJunctions'
    InitRecords = 'InitRecords'
    InitSimParams = 'InitSimParams'
    run = 'run'

    ordered = [
        InitHeader,
        InitTemplates,
        InitCells,
        InitCellMembranes,
        InitVoltageClamps,
        InitCurrentClamps,
        InitSynapsesChemPost,
        InitSynapsesChemPre,
        InitGapJunction,
        InitRecords,
        InitSimParams,
        run,
        ]


class MHocFileData(object):

    Cells = 'Cells'
    Recordables = 'Recordables'
    CurrentClamps = 'CurrentClamps'
    VoltageClamps = 'VoltageClamps'
    Synapses = 'Synapses'
    GapJunctions = 'GapJunctions'
    root_infos = [
        Cells,
        Recordables,
        CurrentClamps,
        VoltageClamps,
        Synapses,
        GapJunctions,
        ]


class MHocFile(object):

    def __setitem__(self, key, value):
        self.info[key] = value

    def __getitem__(self, key):
        if not key in self.info:
            return None
        return self.info[key]

    def __init__(self):
        _info = [(inf, {}) for inf in MHocFileData.root_infos]
        self.info = dict(_info)
        self.sections = dict([(s, []) for s in MHOCSections.ordered])

    def add_to_section(self, section_name, text):
        self.sections[section_name].append(text)

    def __str__(self):

        def str_sect(sect):
            h = '// Section: %s ' % sect
            hu = '/' * len(h)
            d = '\n'.join(self.sections[sect])
            return '\n'.join([h, hu, d, '\n', '\n'])

        return '\n'.join(str_sect(s) for s in MHOCSections.ordered)


