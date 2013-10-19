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


import morphforge
""" Load morphologies from MorphML, and plot using MayaVI

"""
import morphforge.stdimports as mf
import morphforgecontrib.morphology.importers.import_tree_morphml
import pylab

testSrcsPath = mf.LocMgr().get_test_srcs_path()
srcMorphMLFile = mf.Join(testSrcsPath, "neuroml/morphml/CablesIncluded.xml")
m = mf.MorphologyTree.fromMorphML(src=open(srcMorphMLFile),
#mf.MayaViRenderer(m).show_as_points_interpolated()



# TODO - SPEAK TO PADRAIG:
raise NotImplementedError()
srcMorphMLFile = mf.Join(testSrcsPath, "neuroml/morphml/L23PyrFRB.morph.xml",)
m = mf.MorphologyTree.fromMorphML(
        src=open(srcMorphMLFile),
        regions={
            'all':'Rgn1',
            'ModelViewParmSubset_1':'Rgn2',
            'ModelViewParmSubset_3':'Rgn2',
            'ModelViewParmSubset_8':'Rgn2',
            'OneSecGrp_SectionRef_1':'Rgn1',
        }
)
mf.MayaViRenderer(m).show_as_points_interpolated()




