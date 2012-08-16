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


from numpy import linspace, pi, sin, tan
from enthought.traits.api import HasTraits, Instance
from enthought.traits.ui.api import Item, Tabbed, View
from enthought.chaco.api import Plot, AbstractPlotData, ArrayPlotData
from enthought.chaco.tools.api import PanTool, ZoomTool
from enthought.enable.component_editor import ComponentEditor
class TabbedPlots(HasTraits):
    data = Instance(AbstractPlotData)
    plot1 = Instance(Plot)
    plot2 = Instance(Plot)
    view = View(
        Tabbed(
            Item('plot1', editor=ComponentEditor(), dock='tab'),
            Item('plot2', editor=ComponentEditor(), dock='tab'),
            show_labels=False
        ),
        width=0.67,
        height=0.4,
        resizable=True
    )
    def create_plot(self, data, name, color):
        p = Plot(self.data)
        p.plot(data, name=name, color=color)
        p.tools.append(PanTool(p))
        p.overlays.append(ZoomTool(p))
        return p
    def create_plots(self):
        self.plot1 = self.create_plot(("x", "y1"), "sin plot", "red")
        self.plot2 = self.create_plot(("x", "y2"), "tan plot", "blue")

        self.plot2.index_range = self.plot1.index_range
    def _data_changed(self):
        self.create_plots()
#===============================================================================
# # demo object that is used by the demo.py application.
#===============================================================================
x = linspace(-2*pi, 2*pi, 100)
demo = TabbedPlots(data = ArrayPlotData(x=x, y1=sin(x), y2=tan(x)))
if __name__ == "__main__":
    demo.configure_traits()
