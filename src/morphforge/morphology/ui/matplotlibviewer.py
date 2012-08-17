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

from morphmaths import MorphologyForRenderingOperator

from morphforge.morphology.visitor import DictBuilderSectionVisitorHomo

import numpy
import numpy as np


class MatPlotLibViewer(object):

    """
    Plot Projections of a morphology onto XY, XZ, and YZ axes.
    """

    plotViews = [0, 1, 2]


    projMatXY = numpy.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    projMatXZ = numpy.array([[0.0, 0.0, 1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]])
    projMatYZ = numpy.array([[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]])

    figureProjections = {0:projMatXY, 1:projMatXZ, 2:projMatYZ}
    figureLabels = {0: ('X', 'Y'), 1: ('Z', 'Y'), 2: ('X', 'Z')}
    figurePositions = {0:221, 1:222, 2:223}
    figureTitles = {0:'View From Above', 1:'View From Side', 2:'View From Front'}


    def __init__(self, morph, use_pca=True):

        if morph == None:
            raise ValueError('No Cell')

        self.morph = morph

        self.fig = None
        self.subplots = {}

        self.build_plot(use_pca)

    def build_draw_sub_plot(self, rotatedSectionDict, fig, i, plotLims):
        import pylab
        from matplotlib.path import Path
        from matplotlib import patches

        subplotnum = self.figurePositions[i]
        title = self.figureTitles[i]
        proj_matrix = self.figureProjections[i]
        labels = self.figureLabels[i]

        ax = fig.add_subplot(subplotnum, aspect='equal')

        # Find the depth extremes for coloring:

        (zMin, zMax) = (None, None)
        for seg in self.morph:
            xyzProj = numpy.dot(proj_matrix, rotatedSectionDict[seg])
            zMin = (xyzProj[2] if not zMin else min(zMin, xyzProj[2]))
            zMax = (xyzProj[2] if not zMax else max(zMax, xyzProj[2]))
        zrange = zMax - zMin

        for seg in self.morph:
            xyzProj = numpy.dot(proj_matrix, rotatedSectionDict[seg])
            xy_proj = numpy.array([xyzProj[0], xyzProj[1]])

            xyz_proj_parent = numpy.dot(proj_matrix, rotatedSectionDict[seg.parent])
            xy_proj_parent = numpy.array([xyz_proj_parent[0], xyz_proj_parent[1]])

            color = str((xyzProj[2] - zMin) / zrange) if zrange > 0.001 else 'grey'

            linewidth = (seg.d_r + seg.p_r) / 2.0 * 2.0

            # Test if we have just tried to draw a point, if so then draw a circle:
            if numpy.linalg.norm(xy_proj - xy_proj_parent) < 0.0001:
                try:
                    ax.add_patch(pylab.Circle(xy_proj, radius=linewidth, color=color))
                    ax.plot(xy_proj[0], xy_proj[1], '+', markersize=linewidth, color='red')
                except:
                    pass
            else:

                # Simple version, which doesn't work so well:
                # ax.plot([xy_proj[0], xy_proj_parent[0]], [xy_proj[1], xy_proj_parent[1]], linewidth=linewidth, color=color)

                # More complex patch version:
                joining_vec = xy_proj - xy_proj_parent
                joining_vec_norm = joining_vec / numpy.linalg.norm(joining_vec)

                perp_vec = np.array((joining_vec_norm[1],joining_vec_norm[0] * -1))

                assert np.fabs(np.dot(joining_vec_norm, perp_vec)) < 0.01

                # The points:
                p1 = xy_proj + (perp_vec * seg.d_r)
                p2 = xy_proj - (perp_vec * seg.d_r)

                p3 = xy_proj_parent - (perp_vec * seg.p_r)
                p4 = xy_proj_parent + (perp_vec * seg.p_r)

                verts = [p1, p2, p3, p4, (0,0)]
                codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY,]
                path = Path(verts, codes)
                patch = patches.PathPatch(path, facecolor=color, lw=1)
                ax.add_patch(patch)

        ax.set_title(title)
        ax.set_xlim(plotLims)
        ax.set_ylim(plotLims)
        ax.set_xlabel(labels[0])
        ax.set_ylabel(labels[1])
        ax.grid(True)
        return ax

    def build_plot(self, usePCA):
        import pylab

        self.normaliser = MorphologyForRenderingOperator(self.morph,
                                                         usePCA=usePCA)

        # Find the Point that is the furthest distance way from
        # the centre when the cell is centred and rotated:
        rotator = lambda s: self.normaliser(s.get_distal_npa3())

        rotatedSectionDict = DictBuilderSectionVisitorHomo(morph=self.morph, functor=rotator) ()

        # Add in the parents manually:
        p = self.morph._dummysection
        rotatedSectionDict[p] = self.normaliser(p.get_distal_npa3())



        max_axis = max([numpy.linalg.norm(rs) for rs in rotatedSectionDict.values()])
        plotLims = (max_axis * -1.1, max_axis * 1.1)

        maxX = max([numpy.fabs(rs[0]) for rs in rotatedSectionDict.values()])
        maxY = max([numpy.fabs(rs[1]) for rs in rotatedSectionDict.values()])
        maxZ = max([numpy.fabs(rs[2]) for rs in rotatedSectionDict.values()])

        maxes = [maxX, maxY, maxZ]

        # allMax = max(maxes)
        for i in self.plotViews:
            maxes[i] = maxes[i] + 0.2 * max([maxX, maxY, maxZ])

        self.fig = pylab.figure(figsize=(7, 7))
        self.fig.subplots_adjust(
            left=0.05,
            top=0.95,
            right=0.95,
            bottom=0.05,
            wspace=0.1,
            hspace=0.1,
            )

        self.subplots = {}
        for i in self.plotViews:
            self.subplots[i] = self.build_draw_sub_plot(rotatedSectionDict, self.fig, i, plotLims)


