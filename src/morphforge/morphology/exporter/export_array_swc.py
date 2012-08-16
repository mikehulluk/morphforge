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





import numpy as np
from cStringIO import StringIO
from morphforge.morphology.exporter.morphologyexporter import MorphologyExporter
from morphforge.morphology.core.array import MorphologyArray

class ExportArray_SWC(object):

    @classmethod
    def _export_single_swc(cls, morphology, swc_vertex_offset = 1, op=None, fmt='%d %d %0.2f %0.2f %0.2f %0.2f %d'):

        def vertexToData(v_index, v_index_parent, rgn):
            x,y,z,r = morphology._vertices[v_index,:]
            return [ v_index+swc_vertex_offset, rgn,  x, y, z, r,  v_index_parent+swc_vertex_offset if v_index_parent is not None else -1 ]

        #Root Vertex:
        data = [ vertexToData(morphology._dummy_vertex_index, None, 0)  ]

        # Add Each Vertex
        for conn_index,(v_index, v_index_parent) in enumerate(morphology._connectivity):
            rgn =  morphology._section_types[conn_index]
            data.append( vertexToData(v_index, v_index_parent, rgn) )

        # Save the file:
        if op:
            np.savetxt(op, np.array(data), fmt=fmt )
        else:
            op = StringIO()
            np.savetxt(op, np.array(data), fmt=fmt )
            return op.getvalue()


#Wrapper function to avoid binding error:
def _export_single_swc( morphology, **kwargs):
    return ExportArray_SWC._export_single_swc(morphology=morphology, **kwargs)


MorphologyExporter.register("toSWC",_export_single_swc, allow_override=False, from_type=MorphologyArray )
