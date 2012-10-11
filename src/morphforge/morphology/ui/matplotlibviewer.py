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

from morphforge.morphology.ui.morphmaths import MorphologyForRenderingOperator

from morphforge.morphology.visitor import DictBuilderSectionVisitorHomo

import numpy
import numpy as np


class MatPlotLibViewer(object):

    """
    Plot Projections of a morphology onto XY, XZ, and YZ axes.
    """

    plot_views = [0, 1, 2]


    _projMatXY = numpy.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    _projMatXZ = numpy.array([[0.0, 0.0, 1.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0]])
    _projMatYZ = numpy.array([[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]])

    _figure_projections = {0: _projMatXY, 1: _projMatXZ, 2: _projMatYZ}
    _figure_labels = {0: ('X', 'Y'), 1: ('Z', 'Y'), 2: ('X', 'Z')}
    _figure_positions = {0:221, 1:222, 2:223}
    _figure_titles = {0:'View From Above', 1:'View From Side', 2:'View From Front'}


    def __init__(self, morph, use_pca=True, fig_kwargs=None):

        if morph == None:
            raise ValueError('No Cell')

        self.morph = morph

        self.fig = None
        self.fig_kwargs = fig_kwargs if fig_kwargs is not None else {}
        self.subplots = {}
        self.normaliser = None

        self.build_plot(use_pca)

    def build_draw_sub_plot(self, rotatedSectionDict, fig, i, plotLims):
        import pylab
        from matplotlib.path import Path
        from matplotlib import patches

        subplotnum = self._figure_positions[i]
        title = self._figure_titles[i]
        proj_matrix = self._figure_projections[i]
        labels = self._figure_labels[i]

        ax = fig.add_subplot(subplotnum, aspect='equal')

        # Find the depth extremes for coloring:

        (z_min, z_max) = (None, None)
        for seg in self.morph:
            xyzProj = numpy.dot(proj_matrix, rotatedSectionDict[seg])
            z_min = (xyzProj[2] if not z_min else min(z_min, xyzProj[2]))
            z_max = (xyzProj[2] if not z_max else max(z_max, xyzProj[2]))
        zrange = z_max - z_min

        for seg in self.morph:
            xyzProj = numpy.dot(proj_matrix, rotatedSectionDict[seg])
            xy_proj = numpy.array([xyzProj[0], xyzProj[1]])

            xyz_proj_parent = numpy.dot(proj_matrix, rotatedSectionDict[seg.parent])
            xy_proj_parent = numpy.array([xyz_proj_parent[0], xyz_proj_parent[1]])

            color = str((xyzProj[2] - z_min) / zrange) if zrange > 0.001 else 'grey'

            linewidth = (seg.d_r + seg.p_r) / 2.0 * 2.0

            # Test if we have just tried to draw a point, if so then draw a circle:
            if numpy.linalg.norm(xy_proj - xy_proj_parent) < 0.0001:
                try:
                    ax.add_patch(pylab.Circle(xy_proj, radius=linewidth/2.0, color=color))
                    ax.plot(xy_proj[0], xy_proj[1], '+', markersize=linewidth/2.0, color='red')
                except:
                    pass
            else:

                # Simple version, which doesn't work so well:
                # ax.plot([xy_proj[0], xy_proj_parent[0]], [xy_proj[1], xy_proj_parent[1]], linewidth=linewidth, color=color)

                # More complex patch version:
                joining_vec = xy_proj - xy_proj_parent
                joining_vec_norm = joining_vec / numpy.linalg.norm(joining_vec)

                perp_vec = np.array((joining_vec_norm[1], joining_vec_norm[0] * -1))

                assert np.fabs(np.dot(joining_vec_norm, perp_vec)) < 0.01

                # The points:
                p1 = xy_proj + (perp_vec * seg.d_r)
                p2 = xy_proj - (perp_vec * seg.d_r)

                p3 = xy_proj_parent - (perp_vec * seg.p_r)
                p4 = xy_proj_parent + (perp_vec * seg.p_r)

                verts = [p1, p2, p3, p4, (0, 0)]
                codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
                path = Path(verts, codes)
                patch = patches.PathPatch(path, facecolor=color, lw=1)
                ax.add_patch(patch)

        ax.set_title(title)
        ax.set_xlim(plotLims)
        ax.set_ylim(plotLims)
        ax.set_xlabel(labels[0])
        ax.set_ylabel(labels[1])
        
        from matplotlib.ticker import MaxNLocator
        ax.xaxis.set_major_locator(MaxNLocator(4))
        ax.yaxis.set_major_locator(MaxNLocator(4))

        ax.grid(True)
        return ax

    def build_plot(self, usePCA):
        import pylab

        self.normaliser = MorphologyForRenderingOperator(self.morph,
                                                         usePCA=usePCA)

        # Find the Point that is the furthest distance way from
        # the centre when the cell is centred and rotated:
        rotator = lambda s: self.normaliser(s.get_distal_npa3())

        rotated_section_dict = DictBuilderSectionVisitorHomo(morph=self.morph, functor=rotator) ()

        # Add in the parents manually:
        dummy_scetion = self.morph._dummysection
        rotated_section_dict[dummy_scetion] = self.normaliser(dummy_scetion.get_distal_npa3())



        max_axis = max([numpy.linalg.norm(rotated_section_pt) for rotated_section_pt in rotated_section_dict.values()])
        plot_lims = (max_axis * -1.1, max_axis * 1.1)

        max_x = max([numpy.fabs(rotated_section_pt[0]) for rotated_section_pt in rotated_section_dict.values()])
        max_y = max([numpy.fabs(rotated_section_pt[1]) for rotated_section_pt in rotated_section_dict.values()])
        max_z = max([numpy.fabs(rotated_section_pt[2]) for rotated_section_pt in rotated_section_dict.values()])

        maxes = [max_x, max_y, max_z]

        # allMax = max(maxes)
        for i in self.plot_views:
            maxes[i] = maxes[i] + 0.2 * max([max_x, max_y, max_z])

        self.fig = pylab.figure(**self.fig_kwargs) #figsize=(7, 7))
        self.fig.subplots_adjust(
            left=0.05,
            top=0.95,
            right=0.95,
            bottom=0.05,
            wspace=0.15,
            hspace=0.15,
            )

        self.subplots = {}
        for i in self.plot_views:
            self.subplots[i] = self.build_draw_sub_plot(rotated_section_dict, self.fig, i, plot_lims)


