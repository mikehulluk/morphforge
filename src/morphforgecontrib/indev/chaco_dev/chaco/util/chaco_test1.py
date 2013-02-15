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



from scipy import arange
from scipy.special import jn

from enable.api import ComponentEditor
from traits.api import HasTraits, Instance
from traitsui.api import Item, View

from chaco.api import create_line_plot, HPlotContainer
from chaco.tools.api import PanTool


class PlotExample(HasTraits):
    container = Instance(HPlotContainer)

    traits_view = View(Item('container', editor=ComponentEditor(),
                            show_label=False, width=800, height=600),
                       title="Chaco Tutorial")

    def _container_default(self):
        x = arange(-5.0, 15.0, 20.0/100)

        y = jn(0, x)
        left_plot = create_line_plot((x, y), bgcolor="white",
                                     add_grid=True, add_axis=True)
        left_plot.tools.append(PanTool(left_plot))
        self.left_plot = left_plot

        y = jn(1, x)
        right_plot = create_line_plot((x, y), bgcolor="white",
                                      add_grid=True, add_axis=True)
        right_plot.tools.append(PanTool(right_plot))
        right_plot.y_axis.orientation = "right"
        self.right_plot = right_plot

        # Tone down the colors on the grids
        right_plot.hgrid.line_color = (0.3, 0.3, 0.3, 0.5)
        right_plot.vgrid.line_color = (0.3, 0.3, 0.3, 0.5)
        left_plot.hgrid.line_color = (0.3, 0.3, 0.3, 0.5)
        left_plot.vgrid.line_color = (0.3, 0.3, 0.3, 0.5)

        container = HPlotContainer(spacing=20, padding=50, bgcolor="lightgray")
        container.add(left_plot)
        container.add(right_plot)
        return container

demo = PlotExample()

class PlotExample2(PlotExample):
    def _container_default(self):
        container = super(PlotExample2, self)._container_default()

        rplot, lplot = self.right_plot, self.left_plot
        rplot.index_mapper.range = lplot.index_mapper.range
        lplot.value_mapper.range.low = min(rplot.value_mapper.range.low,
                                           lplot.value_mapper.range.low,  )
        rplot.value_mapper.range = lplot.value_mapper.range

        return container

demo = PlotExample2()

if __name__ == "__main__":
    demo.configure_traits()
