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

from enthought.traits.api import *
from enthought.traits.ui.api import *
from enthought.chaco import *
from enthought.chaco.plot_component import *
from enthought.enable import *
""" Demonstrates plots sharing datasources, ranges, etc. """
# Major library imports
from numpy import arange
from scipy.special import jn

from enthought.enable.example_support import DemoFrame, demo_main
# Enthought library imports
from enthought.enable.api import Window, Component, ComponentEditor, Container
from enthought.traits.api import HasTraits, Instance#, false
from enthought.traits.ui.api import Item, Group, View
# Chaco imports
from enthought.chaco.api import HPlotContainer, ArrayPlotData, Plot, VPlotContainer
from enthought.chaco.tools.api import LineInspector, ZoomTool, PanTool
#===============================================================================
# # Create the Chaco plot.
#===============================================================================

from enthought.chaco.api import add_default_axes, add_default_grids, \
        OverlayPlotContainer, PlotLabel, ScatterPlot, create_line_plot

import numpy as np
from enthought.traits.api \
    import HasTraits, Array, Range, Float, Enum, on_trait_change, Property
from enthought.traits.ui.api import View, Item
from enthought.chaco.chaco_plot_editor import ChacoPlotItem
from numpy import arange


def _create_plot_component():
    # Create the index
    numpoints = 100
    low = -5
    high = 15.0
    x = arange(low, high, (high - low) / numpoints)
    plotdata = ArrayPlotData(x=x, y1=jn(0, x), y2=jn(1, x))
    # Create the left plot
    left_plot = Plot(plotdata)
    left_plot.x_axis.title = 'X'
    left_plot.y_axis.title = 'j0(x)'
    renderer = left_plot.plot(('x', 'y1'), type='line', color='blue',
                              width=2.0)[0]
    renderer.overlays.append(LineInspector(renderer, axis='value',
                             write_metadata=True, is_listener=True))
    renderer.overlays.append(LineInspector(renderer, axis='index',
                             write_metadata=True, is_listener=True))
    left_plot.overlays.append(ZoomTool(left_plot, tool_mode='range'))
    left_plot.tools.append(PanTool(left_plot))
    # Create the right plot
    right_plot = Plot(plotdata)
    right_plot.index_range = left_plot.index_range
    right_plot.orientation = 'v'
    right_plot.x_axis.title = 'j1(x)'
    right_plot.y_axis.title = 'X'
    renderer2 = right_plot.plot(('x', 'y2'), type='line', color='red',
                                width=2.0)[0]
    renderer2.index = renderer.index
    renderer2.overlays.append(LineInspector(renderer2,
                              write_metadata=True, is_listener=True))
    renderer2.overlays.append(LineInspector(renderer2, axis='value',
                              is_listener=True))
    right_plot.overlays.append(ZoomTool(right_plot, tool_mode='range'))
    right_plot.tools.append(PanTool(right_plot))
    container = HPlotContainer(background='lightgray')
    container.add(left_plot)
    container.add(right_plot)

    right_plot = Plot(plotdata)
    right_plot.index_range = left_plot.index_range
    right_plot.orientation = 'v'
    right_plot.x_axis.title = 'j1(x)'
    right_plot.y_axis.title = 'X'
    renderer2 = right_plot.plot(('x', 'y2'), type='line', color='red',
                                width=2.0)[0]
    renderer2.index = renderer.index
    renderer2.overlays.append(LineInspector(renderer2,
                              write_metadata=True, is_listener=True))
    renderer2.overlays.append(LineInspector(renderer2, axis='value',
                              is_listener=True))
    right_plot.overlays.append(ZoomTool(right_plot, tool_mode='range'))
    right_plot.tools.append(PanTool(right_plot))
    container.add(right_plot)

    return container












class Camera(HasTraits):
    gain = Enum(1, 2, 3,)
    exposure = CInt(10, label="Exposure",)

class TextDisplay(HasTraits):
    string = String()

    view = View(Item('string', show_label=False, springy=True,
                style='custom'))


class GraphDisplay(HasTraits):

    # plotcontainer = PlotComponent()
    # plotcontainer = VPlotContainer()
    plot = Instance(Plot)
    string = String()

    view= View(
            Item('string', show_label=False, springy=True, style='custom'),
            Item('plot', show_label=False,  editor=ComponentEditor()),
            resizable=True
           )

    def __init__(self):
        HasTraits.__init__(self)
        print 'GraphDisplay.__init__()'

        x = arange(0, 10, 0.5)
        plotdata = ArrayPlotData(x=x, y1=np.sin(x))
        # Create the left plot
        left_plot = Plot(plotdata)
        renderer = left_plot.plot(('x', 'y1'), type='line', color='blue'
                                  , width=2.0)[0]
        renderer.overlays.append(LineInspector(renderer, axis='value',
                                 write_metadata=True, is_listener=True))
        renderer.overlays.append(LineInspector(renderer, axis='index',
                                 write_metadata=True, is_listener=True))

        self.plot = left_plot


class AppContainer(HasTraits):

    camera = Instance(Camera)
    display = Instance(TextDisplay)
    graphdisplay = Instance(GraphDisplay)

    view = View(
        Item('camera', style='custom', show_label=False),
        Item('display', style='custom', show_label=False),
        Item('graphdisplay', style='custom', show_label=False),
        resizable=True,
        width=300,
        height=300,
        )

#container = Container(camera=Camera(), display=TextDisplay())
container = AppContainer(display=TextDisplay(),camera=Camera(), graphdisplay=GraphDisplay())
print container.__dict__
container.configure_traits()
