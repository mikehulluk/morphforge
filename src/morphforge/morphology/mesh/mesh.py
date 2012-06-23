#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------
import numpy as np


class TriangleMesh(object):
    def __init__(self, vertices, triangles, vertex_colors):
        """ Vertices is an n,3 array, triangles is a list, vertex_colors is a n,3 array"""
        self.vertices = vertices
        self.triangles = triangles
        self.vertex_colors = vertex_colors

        if np.isnan(self.vertices).any():
          raise ValueError("Mesh contains NaNs")
        if np.isnan(self.vertex_colors).any():
          raise ValueError("Mesh contains NaNs")

        assert vertices.shape == self.vertex_colors.shape
        assert vertices.shape[1] == 3

        print self.vertex_colors.dtype
        if self.vertex_colors.dtype in ['float64']:
            assert np.logical_and( self.vertex_colors>=0.0, self.vertex_colors <=1.0).all()
        elif self.vertex_colors.dtype in ['int32']:
            assert np.logical_and( self.vertex_colors>=0, self.vertex_colors <=255).all()
            self.vertex_colors = self.vertex_colors / 255.0

        else:
            assert False

    def downshrink(self):
        self.vertices /=1000.0
    @property
    def nTriangles(self):
        return len(self.triangles)
    @property
    def nVertices(self):
        return len(self.vertices)


    @classmethod
    def merge(cls, meshes):


        vertices = np.zeros( (0,3) )
        triangles = list()
        vertex_colors = np.zeros( (0,3) )

        for mesh in meshes:
            offset = vertices.shape[0]
            vertices = np.vstack( (vertices, mesh.vertices) )
            vertex_colors = np.vstack( (vertex_colors, mesh.vertex_colors) )

            new_triangles = [ [a+offset, b+offset, c+offset] for a,b,c in mesh.triangles]
            triangles.extend(new_triangles)

        return TriangleMesh( vertices = vertices, triangles=triangles, vertex_colors=vertex_colors)

        assert False

