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

from Cheetah.Template import Template


class MeshWriterPLY(object):
    ply_tmpl = """ply
format ascii 1.0
element vertex $mesh.nVertices
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
element face $mesh.nTriangles
property list uchar int vertex_index
end_header
#for i in range($mesh.nVertices):
$mesh.vertices[i,0] $mesh.vertices[i,1] $mesh.vertices[i,2] $conv($mesh.vertex_colors[i,0]) $conv($mesh.vertex_colors[i,1]) $conv($mesh.vertex_colors[i,2])
#end for
#for t in $mesh.triangles:
3 $t[0] $t[1] $t[2]
#end for"""

    @classmethod
    def build_string(cls, mesh):

        conv_color = lambda f: int(f * 255)
        ply_str = Template(cls.ply_tmpl, 
                     {'mesh': mesh, 'conv': conv_color}).respond()
        ply_str = ply_str[:-1]  # Trim the last, blank line.

        return ply_str


