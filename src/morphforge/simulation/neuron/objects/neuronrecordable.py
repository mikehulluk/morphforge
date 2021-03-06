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

from morphforge.simulation.base.core.recordable import Recordable
from morphforge.simulation.neuron.objects.neuronobject import NEURONObject


class NEURONRecordable(Recordable, NEURONObject):

    def get_recordable(self, *args, **kwargs):
        raise Exception("Can't record a recordable!")

    def get_unit(self):
        raise NotImplementedError()

    def build_hoc(self, hocfile_obj):
        raise NotImplementedError()

    def build_mod(self, modfile_set):
        raise NotImplementedError()


class NEURONRecordableOnLocation(NEURONRecordable):

    def __init__(self, cell_location, **kwargs):
        super(NEURONRecordableOnLocation, self).__init__(**kwargs)
        self.cell_location = cell_location

    def get_tags(self):
        return NEURONRecordable.get_tags(self) \
            + list(self.cell_location.cell.cell_tags)

    def get_unit(self):
        raise NotImplementedError()

    def build_hoc(self, hocfile_obj):
        raise NotImplementedError()

    def build_mod(self, modfile_set):
        raise NotImplementedError()


