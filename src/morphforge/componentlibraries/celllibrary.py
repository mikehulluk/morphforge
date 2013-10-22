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


class CellLibrary(object):

    _cells = dict()

    @classmethod
    def register_cell(cls, cell_builder):
        celltype = cell_builder.get_cell_type()
        modelsrc = cell_builder.get_model()
        cls._cells[(modelsrc, celltype)] = cell_builder

    @classmethod
    def register(cls, celltype, modelsrc, cell_functor):
        cls._cells[(modelsrc, celltype)] = cell_functor

    @classmethod
    def get_cellfunctor(cls, modelsrc, celltype):
        return cls._cells[(modelsrc, celltype)]

    @classmethod
    def create_cell(cls, sim,  modelsrc, celltype=None, **kwargs):
        return cls.get_cellfunctor(modelsrc, celltype)(sim, **kwargs)


    @classmethod
    def summary_table(cls, ):
        import mredoc
        summary_data = []
        for ((modelsrc,celltype), functor) in sorted(cls._cells.iteritems()):
            summary_data.append( ( modelsrc, celltype ))# , functor.__file__)
        summary_table = mredoc.VerticalColTable( ('Model','CellType'), summary_data)
        return mredoc.Section('Cell Library Summary', summary_table )


