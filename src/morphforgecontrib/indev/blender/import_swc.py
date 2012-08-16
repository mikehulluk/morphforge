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
#!BPY

"""
Name: 'Neuron Morphologies'
Blender: 244
Group: 'Import'
Tooltip: 'Mike Hull - SWC Importer'
"""
import Blender
import bpy



import sys
print 'PYTHONPATH', sys.path

from morphforge.morphology.mesh import MeshWriterPLY
from morphforge.morphology.builders import MorphologyLoader
from morphforge.morphology.mesh import MeshBuilderRings

import Blender
def import_obj(path):
        Blender.Window.WaitCursor(1)
        name = path.split('\\')[-1].split('/')[-1]
        # parse the file

        m = MorphologyLoader.fromSWC(src=open(path), morphname="TestMorphlogy4")

        mf_mesh = MeshBuilderRings.build(morph=m)
        #MeshWriterPLY.write(mesh, '/tmp/testmesh.ply')

        mesh = Blender.NMesh.New(name) # create a new mesh
        for i in range(mf_mesh.nVertices):
          mesh.verts.append(Blender.NMesh.Vert(mf_mesh.vertices[i,0], mf_mesh.vertices[i,1],  mf_mesh.vertices[i,2]))

        for i in range(mf_mesh.nTriangles):
          faceVertList = [
              mesh.verts[ mf_mesh.triangles[0] ],
              mesh.verts[ mf_mesh.triangles[1] ],
              mesh.verts[ mf_mesh.triangles[2] ],
              ]
          newFace = Blender.NMesh.Face(faceVertList)
          mesh.addFace(newFace)


        #file = open(path, 'r')
        #for line in file:
        #        words = line.split()
        #        if len(words) == 0 or words[0].startswith('#'):
        #                pass
        #        elif words[0] == 'v':
        #                x, y, z = float(words[1]), float(words[2]), float(words[3])
        #                mesh.verts.append(Blender.NMesh.Vert(x, y, z))
        #        elif words[0] == 'f':
        #                faceVertList = []
        #                for faceIdx in words[1:]:
        #                        faceVert = mesh.verts[int(faceIdx)-1]
        #                        faceVertList.append(faceVert)
        #                newFace = Blender.NMesh.Face(faceVertList)
        #                mesh.addFace(newFace)

        # link the mesh to a new object
        ob = Blender.Object.New('Mesh', name) # Mesh must be spelled just this--it is a specific type
        ob.link(mesh) # tell the object to use the mesh we just made
        scn = Blender.Scene.GetCurrent()
        for o in scn.getChildren():
                o.sel = 0

        scn.link(ob) # link the object to the current scene
        ob.sel= 1
        ob.Layers = scn.Layers
        Blender.Window.WaitCursor(0)
        Blender.Window.RedrawAll()

Blender.Window.FileSelector(import_obj, 'Import')

