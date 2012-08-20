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


def addTitleOverlay(component, title):
    component.overlays.append(PlotLabel(title,
                              component=component,
                              font = "swiss 16",
                              overlay_position="top"))

class SimulationManager(HasTraits):
    surface_area_um2 = Range(low=1.0, high=5000.0, value=1000.0)

    leak_density_pS = Range(low=1.0, high=100.0, value=50.0)



    def trait_view (self, name = None, view_element = None):
        return View(self._instance_traits().keys())


    def _createVoltageTraceComponent(self):

        x = arange(-5, 15, 100)
        tracedata = ArrayPlotData(x=x, y1=np.sin(x), y2=np.cos(x))

        plot = Plot(tracedata)
        plot.x_axis.title = "time"
        plot.y_axis.title = "Voltage"
        renderer = plot.plot(("x", "y1"), type="line", color="blue",
                                  width=2.0)[0]
        renderer.overlays.append(LineInspector(renderer, axis='value',
                                                write_metadata=True,
                                                is_listener=True))
        renderer.overlays.append(LineInspector(renderer, axis="index",
                                                write_metadata=True,
                                                is_listener=True))
        plot.overlays.append(ZoomTool(plot, tool_mode="range"))
        plot.tools.append(PanTool(plot))

        # Make the container:
        container = VPlotContainer(resizable = "hv", bgcolor="lightgray", fill_padding=True, padding = 10)
        container.add(plot)
        return container


    def _create_cellConfigComponent(self):

        x = arange(-5, 15, 100)
        tracedata = ArrayPlotData(x=x, y1=np.sin(x), y2=np.cos(x))

        plot = Plot(tracedata)
        plot.x_axis.title = "time"
        plot.y_axis.title = "Voltage"
        renderer = plot.plot(("x", "y1"), type="line", color="blue",
                                  width=2.0)[0]
        renderer.overlays.append(LineInspector(renderer, axis='value',
                                                write_metadata=True,
                                                is_listener=True))
        renderer.overlays.append(LineInspector(renderer, axis="index",
                                                write_metadata=True,
                                                is_listener=True))
        plot.overlays.append(ZoomTool(plot, tool_mode="range"))
        plot.tools.append(PanTool(plot))

        # Make the container:
        container = VPlotContainer(resizable = "hv", bgcolor="lightgray", fill_padding=True, padding = 10)
        container.add(plot)
        return container


    def _createConfigurationPane(self):
        container = VPlotContainer(resizable = "hv", bgcolor="lightgray", fill_padding=True, padding = 10)
        #container = Container(resizable = "hv", bgcolor="lightgray", fill_padding=True, padding = 10)
        addTitleOverlay(container, 'Configuration Pane')

        container.add(self._create_cellConfigComponent())
        container.add_trait ('self.surface_area_um2', self.surface_area_um2)
        #traits_view = View(Item('self.surface_area_um2', editor=ComponentEditor(), show_label=False), width=500, height=500, resizable=True, title="Chaco Plot")

        #container.add(traits_view)
        return container

    def _createResultsPane(self):
        container = VPlotContainer(resizable = "hv", bgcolor="lightgray", fill_padding=True, padding = 10)
        #container = Container(resizable = "hv", bgcolor="lightgray", fill_padding=True, padding = 10)
        addTitleOverlay(container, 'Results Pane')

        container.add(self._createVoltageTraceComponent())

        return container

    def _createWindow(self):

        container = HPlotContainer(resizable = "hv", bgcolor="lightgray",
        #container = Container(resizable = "hv", bgcolor="lightgray",
                                   fill_padding=True, padding = 10)
        container.add(self._createConfigurationPane())
        container.add(self._createResultsPane())
        #container.add(self._create_plot_component())
        return container




def _create_plot_component():
    # Create the index
    numpoints = 100
    low = -5
    high = 15.0
    x = arange(low, high, (high-low)/numpoints)
    plotdata = ArrayPlotData(x=x, y1=jn(0, x), y2=jn(1, x))
    # Create the left plot
    left_plot = Plot(plotdata)
    left_plot.x_axis.title = "X"
    left_plot.y_axis.title = "j0(x)"
    renderer = left_plot.plot(("x", "y1"), type="line", color="blue",
                              width=2.0)[0]
    renderer.overlays.append(LineInspector(renderer, axis='value',
                                            write_metadata=True,
                                            is_listener=True))
    renderer.overlays.append(LineInspector(renderer, axis="index",
                                            write_metadata=True,
                                            is_listener=True))
    left_plot.overlays.append(ZoomTool(left_plot, tool_mode="range"))
    left_plot.tools.append(PanTool(left_plot))
    # Create the right plot
    right_plot = Plot(plotdata)
    right_plot.index_range = left_plot.index_range
    right_plot.orientation = "v"
    right_plot.x_axis.title = "j1(x)"
    right_plot.y_axis.title = "X"
    renderer2 = right_plot.plot(("x", "y2"), type="line", color="red", width=2.0)[0]
    renderer2.index = renderer.index
    renderer2.overlays.append(LineInspector(renderer2, write_metadata=True, is_listener=True))
    renderer2.overlays.append(LineInspector(renderer2, axis="value", is_listener=True))
    right_plot.overlays.append(ZoomTool(right_plot, tool_mode="range"))
    right_plot.tools.append(PanTool(right_plot))
    container = HPlotContainer(background="lightgray")
    container.add(left_plot)
    container.add(right_plot)


    right_plot = Plot(plotdata)
    right_plot.index_range = left_plot.index_range
    right_plot.orientation = "v"
    right_plot.x_axis.title = "j1(x)"
    right_plot.y_axis.title = "X"
    renderer2 = right_plot.plot(("x", "y2"), type="line", color="red", width=2.0)[0]
    renderer2.index = renderer.index
    renderer2.overlays.append(LineInspector(renderer2, write_metadata=True, is_listener=True))
    renderer2.overlays.append(LineInspector(renderer2, axis="value", is_listener=True))
    right_plot.overlays.append(ZoomTool(right_plot, tool_mode="range"))
    right_plot.tools.append(PanTool(right_plot))
    container.add(right_plot)

    return container
#===============================================================================
# Attributes to use for the plot view.
size=(750, 500)
title="Two Plots"



class PlotFrame(DemoFrame):
    def _create_window(self):
        # Return a window containing our plots
        #return Window(self, -1, component=_create_plot_component())
        sim = SimulationManager()
        return Window(self, -1, component=sim._createWindow())

if __name__ == "__main__":
    demo_main(PlotFrame, size=size, title=title)


















#===============================================================================
# # Demo class that is used by the demo.py application.
#===============================================================================
#class Demo(HasTraits):
#    plot = Instance(Component)
#
#    traits_view = View(
#                    Group(
#                        Item('plot', editor=ComponentEditor(size=size),
#                             show_label=False),
#                        orientation = "vertical"),
#                    resizable=True, title=title,
#                    width=size[0], height=size[1]
#                   )
#
#    def _plot_default(self):
#         return _create_plot_component()
#
#demo = Demo()
