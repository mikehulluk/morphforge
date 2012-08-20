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



import sys


from morphforge.morphology.mesh import MeshWriterPLY
from morphforge.morphology.mesh import MeshBuilderRings

def swc_to_ply(swc_path, ply_path=None):
    ply_path = ply_path or swc_path.replace('.swc', '.ply')
    #morphologies = MorphologyLoader.fromSWCSet(src=open(swc_path))
    SWCLoader.LoadSet(src=open(swc_path), morphname="UnknownSWC", regionNames=regionNames)

    meshes = [MeshBuilderRings.build(morph) for morph in morphologies]

    # Save the individual meshes:
    for i, mesh in enumerate(meshes):
        MeshWriterPLY.write(mesh, ply_path.replace('.ply', '_%d.ply'%i))

    # Save a set of meshes:
    combined_mesh = TriangleMesh.merge(meshes)
    MeshWriterPLY.write(combined_mesh, ply_path)






def main():

    print sys.argv
    for swc_name in sys.argv[1:]:
        ply_name = swc_name.replace('.swc', '.ply')
        print "Converting: %s to %s " % (swc_name, ply_name)
        swc_to_ply(swc_name, ply_name)


main()
