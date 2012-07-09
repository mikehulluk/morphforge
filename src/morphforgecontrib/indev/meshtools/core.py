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


import os
from morphforge.morphology.importer.import_array_swc import NewSWCLoader
from morphforgecontrib.indev.highqualitymesh.create_mesh import MeshFromGTS
from morphforge.morphology.mesh.writer_ply import MeshWriterPLY
from morphforge.morphology.mesh.mesh import TriangleMesh
from morphforge.core.mgrs.locmgr import LocMgr
from morphforgecontrib.morphology.util.axontrimmer import AxonTrimmer
from morphforgecontrib.morphology.util.morphologytranslator import MorphologyTranslator
from morphforgecontrib.morphology.util.minimum_diameter import MorphologyMinimumDiameter
#import numpy as np

class MeshGenerationOptions:
    minimum_diameter = 'MinimumDiameter'

class Context(object):
    def __init__(self, src_zip_file, dst_zip_file):
        self.color_aliases = {}
        self.region_color_defaults = {}
        self.currentplyscope = None

        self.global_options = { 
                    #MeshGenerationOptions.minimum_diameter: 1.0
                    }

        self.src_zip_file = src_zip_file
        self.dst_zip_file = dst_zip_file
        self.op_files = []
        self.op_dir = "/tmp/mf/meshbuilder/"
        LocMgr.ensure_dir_exists(self.op_dir)


    def has_option_set(self, key):
        return key in self.global_options
    def get_option(self, key):
        return  self.global_options[key]

    def get_color(self, alias):
        return self.color_aliases[alias]

    def add_alias(self,id, color):
        assert not id in self.color_aliases
        self.color_aliases[id] = color

    def set_default_region_color(self, rgn_id, color):
        self.region_color_defaults[rgn_id] = color

    def new_ply_block(self, ):
        assert self.currentplyscope is None
        self.currentplyscope = PlyScope(global_scope=self)

    def close_ply_block(self, plyfilename):
        self.currentplyscope.finalise(plyfilename=plyfilename)
        self.currentplyscope = None

        for f in self.op_files:
            self.dst_zip_file.write(f,)
        self.op_files = []

    def getFileObjRead(self, filename):

        possible_filenames = [filename, "src/"+filename]
        for pf in possible_filenames:
            try:
                return self.src_zip_file.open(pf,"r")
            except KeyError:
                pass

        raise ValueError("Can't find file: %s"%filename)

    def getFileObjWrite(self, filename):
        filename = os.path.join(self.op_dir,filename)
        d = os.path.dirname(filename)
        if not os.path.exists(d):
            os.makedirs(d)
        self.op_files.append(filename)
        return open(filename,"w")



class PlyScope(object):
    def __init__(self,global_scope):
        self.global_scope = global_scope
        self.region_colors = {}

        self.meshes = []

    def get_region_color(self, rgn):
        assert isinstance(rgn, int)

        # Local colors?
        if rgn in self.region_colors:
            return self.region_colors[rgn]
        if None in self.region_colors:
            return self.region_colors[None]
        # Global colors?:
        if rgn in self.global_scope.region_color_defaults:
            return self.global_scope.region_color_defaults[rgn]
        if None in self.global_scope.region_color_defaults:
            return self.global_scope.region_color_defaults[None]
        assert False,' What do I do with region: %d '%rgn

        #return ColorDef(200,50, np.min((rgn*20,255) ))

    def include_file(self, filename, options):
        src_obj = self.global_scope.getFileObjRead( filename )
        morphs = NewSWCLoader.load_swc_set(src=src_obj)

        # Hack: only first:
        #morphs = [morphs[0]]

        for m in morphs:
            m = m.to_tree()

            # Create the color LUT:
            bi_dict = m.region_number_to_name_bidict

            rgn_colors = {}
            for rgn in m.get_regions():
                rgn_name = rgn.name
                rgn_int = bi_dict.region_name_to_int(rgn_name)
                rgn_color = self.get_region_color(rgn_int)
                print ' %s -> %s '%(rgn_name, rgn_int ), rgn_color
                rgn_colors[rgn_name] = rgn_color

            # Check for ignored Region:
            if None in rgn_colors.values():
                for v in rgn_colors.values():
                    if v is not None:
                        print "Partly ignoring Structure:",
                        for k,v in rgn_colors.iteritems():
                            print k,v
                        assert False, "Partly ignored structure!"
                continue

            # Apply the options:
            if 'trim' in options:
                m = AxonTrimmer.trim_axon_from_morphology(m, max_dist_to_parent=options['trim'] )
            if 'offset' in options:
                m = MorphologyTranslator.translate(morphology=m, offset=options['offset'] )
            if self.global_scope.has_option_set( MeshGenerationOptions.minimum_diameter):
                m = MorphologyMinimumDiameter.ensure(m, min_diameter =self.global_scope.get_option(MeshGenerationOptions.minimum_diameter) )




            mesh = MeshFromGTS.build( m, plot=False, region_color_map = rgn_colors)
            self.meshes.append(mesh)


    def set_region_color(self, region, color):
        self.region_colors[region] = color

    def finalise(self, plyfilename):

        m = TriangleMesh.merge(meshes=self.meshes)
        ply = MeshWriterPLY.build_string(m )

        with self.global_scope.getFileObjWrite(plyfilename) as f:
            f.write(ply)


class ColorDef(object):
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    def __str__(self):
        return "<ColorDef: (%d,%d,%d)>"%(self.r,self.g,self.b)


class RegionColorDef(object):
    def __init__(self, rgn, color_def):
        assert isinstance(rgn,int)
        assert isinstance(color_def,ColorDef)

        self.rgn = rgn
        self.color_def = color_def


