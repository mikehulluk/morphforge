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


import numpy
import itertools

from morphforge.core import SeqUtils
from morphforge.morphology.visitor import ListBuilderSectionVisitor
from morphforge.morphology.visitor.visitorfactory import SectionVistorFactory



class MayaViRenderer(object):

    """
    Display a morphology using the MayaVi interface
    """

    def __init__(self, morph=None, morphs=None, scalefactor=1.0):
        self.colormap = 'copper'
        self.scale_factor = scalefactor

        assert morph or morphs
        if morph:
            self.morphs = [morph]
        elif morphs:
            self.morphs = morphs

    def show_as_points(self):
        """
        Very simple plotting for speed with complex neurons - plot each
        section as a sphere about its endpoint. Only works for neurons
        with very small section lengths compared to radii
        """

        # MonkeyPatchMayaVi()

        from mayavi import mlab

        @mlab.show
        def _showSimple():
            morph_pts = [SectionVistorFactory.array4_all_points(morph)() for morph in self.morphs]
            pts = numpy.concatenate(morph_pts)
            return mlab.points3d(
                pts[:, 0],
                pts[:, 1],
                pts[:, 2],
                pts[:, 3],
                colormap=self.colormap,
                scale_factor=self.scale_factor,
                )
        _showSimple()

    def show_as_points_interpolated(self, lToRRatio=2.0):
        """
        Draws the points as spheres, but also interpolates inbetween the points, so the structure looks
        more 'whole'
        """

        # MonkeyPatchMayaVi()
        import enthought.mayavi.mlab as mlab
        from mayavi import mlab

        @mlab.show
        def _showSimple():
            max_interpol_pts = 10

            def interpolate_section(section):
                sec_start = section.get_distal_npa4()
                sec_end = section.get_proximal_npa4()
                length = section.get_length()
                rad = min(section.d_r, section.p_r)
                n = min(max(int(lToRRatio * length / rad), 1), max_interpol_pts)
                j_vec_steps = (sec_end - sec_start) / n

                int_pts = [sec_start + k * j_vec_steps for k in range(0, n)]
                return int_pts

            lbs = []
            for morph in self.morphs:
                lb = SeqUtils.flatten(ListBuilderSectionVisitor(functor=interpolate_section,  morph=morph) ())
                lbs.extend(lb)

            pts = numpy.array(lbs)

            x = pts[:, 0]
            y = pts[:, 1]
            z = pts[:, 2]
            s = pts[:, 3]

            mlab.points3d(x, y, z, s, colormap=self.colormap, scale_factor=self.scale_factor)
            mlab.outline()
        _showSimple()

    def showSimpleCylinders(self):
        """
        Slightly more complex plotting - plot each
        section as a cylinders.
        """

        import sys
        sys.path.append('/usr/share/pyshared/')

        from morphforge.morphology.mesh import MeshBuilderRings
        # MonkeyPatchMayaVi()

        from mayavi import mlab

        assert len(self.morphs) == 1
        mesh = MeshBuilderRings().build(self.morphs[0])

        @mlab.show
        def _showSimpleCylinders():
            mlab.triangular_mesh(mesh.vertices[:, 0], mesh.vertices[:, 1], mesh.vertices[:, 2], mesh.triangles, colormap=self.colormap)
        _showSimpleCylinders()

    def make_video(self):
        """
        Slightly more complex plotting - plot each
        section as a cylinders.
        """

        import sys
        sys.path.append('/usr/share/pyshared/')

        from morphforge.morphology.mesh import MeshBuilderRings
        # MonkeyPatchMayaVi()

        from mayavi import mlab

        assert len(self.morphs) == 1
        mesh = MeshBuilderRings().build(self.morphs[0])

        @mlab.show
        @mlab.animate(delay=100) #, ui=False) #(delay=500, ui=False)
        def _showSimpleCylinders():

            fig = mlab.figure(bgcolor=None, fgcolor=None, engine=None, size=(1024, 768))
            mlab.triangular_mesh(mesh.vertices[:, 0], mesh.vertices[:, 1], mesh.vertices[:, 2], mesh.triangles, colormap=self.colormap)

            for i in itertools.count():
                print i
                fig.scene.camera.azimuth(0.1)
                mlab.savefig('/home/michael/Desktop/out/O%04d.png' % i)
                fig.scene.render()
                if i > 3600:
                    break
                yield None

        _showSimpleCylinders()

    @classmethod
    def dummy_test(cls):
        """
        Does not plot neuron - code copied from enthought
        website and only used to make sure that MayaVi is
        install propery for testing purposes.
        """

        # MonkeyPatchMayaVi()
        import enthought.mayavi.mlab as mlab
        from mayavi import mlab

        @mlab.show
        def _show_test():
            """ Example from Enthought website: """

            t = numpy.linspace(0, 4 * numpy.pi, 20)
            cos = numpy.cos
            sin = numpy.sin

            x = sin(2 * t)
            y = cos(t)
            z = cos(2 * t)
            s = 2 + sin(t)
            return mlab.points3d(x, y, z, s, colormap="copper", scale_factor=.25)
        _show_test()

