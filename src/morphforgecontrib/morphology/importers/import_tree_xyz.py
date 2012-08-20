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

assert False, 'Do not use this module ~ currently in development'

from morphforge.morphology.core.morphologytree import MorphologyTree
from morphforge.morphology.core.section import Section

import numpy as np
from morphforge.morphology.core.region import Region
from morphforge.core.mgrs.logmgr import LogMgr

class xyzXYZLoader(object):
    defaultxyzXYZRegionNames = {"S":"soma", "D":"dendrite", "A":"axon", "H":"hillock", 0:"Something",
                                    10:"soma",
                                    11:"dendrite",
                                    12:"axon",
                                    13:"hillock",
                                    14:"Unknown",
                                    15:"Unknown",
                                    17:"Unknown",
                                    16:"Unknown",
                                    1:"Unknown",
                                    2:"Unknown",
                                    3:"Unknown",
                                    4:"Unknown",
                                    5:"Unknown",
                                    6:"Unknown",
                                    7:"Unknown",
                                    8:"Unknown",
                                    9:"Unknown",
                                    18:"Unknown",


         }
    @classmethod
    def Load(self, morphname, src, regionNames=None):

        regionNames = regionNames if regionNames else self.defaultxyzXYZRegionNames
        lines = [l.strip() for l in src.readlines()]
        lines = [l for l in lines if l and l[0] != '#' and l[0] != ':']


        # Check the header:
        line1 = lines[0].translate(None, '\t ')
        assert line1 == 'n,T,x,y,z,X,Y,Z,P'

        line1 = lines[0].translate(None, '\t ')
        assert line1 == 'n,T,x,y,z,X,Y,Z,P'


        for l in lines[1:]:
            toks = l.split(',')
            T = int(toks[1])
            xyz = (float(toks[2]), float(toks[3]), float(toks[4]))
            XYZ = (float(toks[5]), float(toks[6]), float(toks[7]))

            centre = ((xyz[0] + XYZ[0]) / 2.0, (xyz[1] + XYZ[1]) / 2.0, (xyz[2] + XYZ[2]) / 2.0)
            rad = np.sqrt(sum([(xyz[i] - centre[i]) ** 2.0 for i in [0, 1, 2]]))

            if rad < 0.3:
                rad = 0.3

            if sections:
                LogMgr.info("Loading ID: %d" % int(toks[0]))
                newSect = sections[-1].create_distal_section(regions=[regionTypes[T]], x=centre[0], y=centre[1], z=centre[2], r=rad)
            else:
                newSect = Section (regions=[regionTypes[T]], x=centre[0], y=centre[1], z=centre[2], r=rad)

            sections.append(newSect)

        # Create the Cell
        c = MorphologyTree(name=morphname, root=sections[0],
                           metadata={})
        return c


class xyzXYZMultiLoader(object):

    @classmethod
    def Load(self, src, regionNames=None, minimumradius=0.15):
        #assert False
        defaultxyzXYZRegionNames = {"S":"soma", "D":"dendrite", "A":"axon", "H":"hillock", 0:"Something",
                                    10:"soma",
                                    11:"dendrite",
                                    12:"axon",
                                    13:"hillock",
                                    14:"Unknown",
                                    15:"Unknown",
                                    17:"Unknown",
                                    16:"Unknown",
                                    1:"Unknown",
                                    2:"Unknown",
                                    3:"Unknown",
                                    4:"Unknown",
                                    5:"Unknown",
                                    6:"Unknown",
                                    7:"Unknown",
                                    8:"Unknown",
                                    9:"Unknown",
                                    18:"Unknown",


         }


        regionNames = regionNames if regionNames else defaultxyzXYZRegionNames
        lines = [l.strip() for l in src.readlines()]
        lines = [l for l in lines if l and l[0] != '#' and l[0] != ':']


        # Check the header:
        line1 = lines[0].translate(None, '\t ')
        assert line1 == 'n,T,x,y,z,X,Y,Z,P'

        #Create the regions:
        regionTypes = dict([(index, Region(name)) for index, name, in regionNames.iteritems() ])
        sections = []

        morphRoots = []
        for l in lines[1:]:
            toks = l.split(',')
            T = int(toks[1])
            xyz = (float(toks[2]), float(toks[3]), float(toks[4]))
            XYZ = (float(toks[5]), float(toks[6]), float(toks[7]))

            centre = ((xyz[0] + XYZ[0]) / 2.0, (xyz[1] + XYZ[1]) / 2.0, (xyz[2] + XYZ[2]) / 2.0)
            rad = np.sqrt(sum([(xyz[i] - centre[i]) ** 2.0 for i in [0, 1, 2]]))
            rad = max(rad, minimumradius)

            cellid = int(toks[0])
            parent = int(toks[8])

            if parent == -1:
                sections = {}
                sections[-1] = Section(regions=[regionTypes[T]], x=centre[0], y=centre[1], z=centre[2], r=rad ,)
                newSect = sections[-1].create_distal_section(regions=[regionTypes[T]], x=centre[0], y=centre[1], z=centre[2], r=rad ,)
                morphRoots.append(sections[-1])
            else:
                newSect = sections[parent].create_distal_section(regions=[regionTypes[T]], x=centre[0], y=centre[1], z=centre[2], r=rad ,)


            sections[cellid] = newSect

        morphs = []
        for mR in morphRoots:
            nM = MorphologyTree(name='M', root=mR, metadata={})
            morphs.append(nM)
        return morphs

        c = MorphologyTree(name='M', root=sections[0], metadata={})
        return c


