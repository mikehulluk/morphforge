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


"""
Allows editing of a line plot.
Left-dragging a point will move its position.
Right-drag pans the plot.
Mousewheel up and down zooms the plot in and out.
Pressing "z" brings up the Zoom Box, and you can click-drag a rectangular region to
zoom.  If you use a sequence of zoom boxes, pressing alt-left-arrow and
alt-right-arrow moves you forwards and backwards through the "zoom history".
"""
# Major library imports
from numpy import linspace
from scipy.special import jn
from enthought.enable.example_support import DemoFrame, demo_main
from enthought.chaco.example_support import COLOR_PALETTE
# Enthought library imports
from enthought.enable.tools.api import DragTool
from enthought.enable.api import Component, ComponentEditor, Window
from enthought.traits.api import HasTraits, Instance, Int, Tuple
from enthought.traits.ui.api import Item, Group, View
# Chaco imports
from enthought.chaco.api import add_default_axes, add_default_grids, \
        OverlayPlotContainer, PlotLabel, ScatterPlot, create_line_plot
from enthought.chaco.tools.api import PanTool, ZoomTool


class PointDraggingTool(DragTool):

    component = Instance(Component)
    # The pixel distance from a point that the cursor is still considered
    # to be 'on' the point
    threshold = Int(5)
    # The index of the point being dragged
    _drag_index = Int(-1)
    # The original dataspace values of the index and value datasources
    # corresponding to _drag_index
    _orig_value = Tuple

    def is_draggable(self, x, y):
        # Check to see if (x, y) are over one of the points in self.component
        if self._lookup_point(x, y) is not None:
            return True
        else:
            return False

    def normal_mouse_move(self, event):
        plot = self.component

        ndx = plot.map_index((event.x, event.y), self.threshold)
        if ndx is None:
            if plot.index.metadata.has_key('selections'):
                del plot.index.metadata['selections']
        else:
            plot.index.metadata['selections'] = [ndx]
        plot.invalidate_draw()
        plot.request_redraw()

    def drag_start(self, event):
        plot = self.component
        ndx = plot.map_index((event.x, event.y), self.threshold)
        if ndx is None:
            return
        self._drag_index = ndx
        self._orig_value = (plot.index.get_data()[ndx], plot.value.get_data()[ndx])
    def dragging(self, event):
        plot = self.component
        (data_x, data_y) = plot.map_data((event.x, event.y))
        plot.index._data[self._drag_index] = data_x
        plot.value._data[self._drag_index] = data_y
        plot.index.data_changed = True
        plot.value.data_changed = True
        plot.request_redraw()

    def drag_cancel(self, event):
        plot = self.component
        plot.index._data[self._drag_index] = self._orig_value[0]
        plot.value._data[self._drag_index] = self._orig_value[1]
        plot.index.data_changed = True
        plot.value.data_changed = True
        plot.request_redraw()

    def drag_end(self, event):
        plot = self.component
        if plot.index.metadata.has_key('selections'):
            del plot.index.metadata['selections']
        plot.invalidate_draw()
        plot.request_redraw()

    def _lookup_point(self, x, y):
        """ Finds the point closest to a screen point if it is within self.threshold

        Parameters
        ==========
        x : float
            screen x-coordinate
        y : float
            screen y-coordinate
        Returns
        =======
        (screen_x, screen_y, distance) of datapoint nearest to the input *(x, y)*.
        If no data points are within *self.threshold* of *(x, y)*, returns None.
        """

        if hasattr(self.component, 'get_closest_point'):
            # This is on BaseXYPlots
            return self.component.get_closest_point((x, y), threshold=self.threshold)
        return None


# ===============================================================================
## Create the Chaco plot.
# ===============================================================================

def _create_plot_component():

    container = OverlayPlotContainer(padding=50, fill_padding=True,
            bgcolor='lightgray', use_backbuffer=True)
    # Create the initial X-series of data
    numpoints = 30
    low = -5
    high = 15.0
    x = linspace(low, high, numpoints)
    y = jn(0, x)
    lineplot = create_line_plot((x, y), color=tuple(COLOR_PALETTE[0]),
                                width=2.0)
    lineplot.selected_color = 'none'
    scatter = ScatterPlot(
        index=lineplot.index,
        value=lineplot.value,
        index_mapper=lineplot.index_mapper,
        value_mapper=lineplot.value_mapper,
        color=tuple(COLOR_PALETTE[0]),
        marker_size=5,
        )
    scatter.index.sort_order = 'ascending'
    scatter.bgcolor = 'white'
    scatter.border_visible = True

    add_default_grids(scatter)
    add_default_axes(scatter)
    scatter.tools.append(PanTool(scatter, drag_button='right'))

    # The ZoomTool tool is stateful and allows drawing a zoom
    # box to select a zoom region.
    zoom = ZoomTool(scatter, tool_mode='box', always_on=False,
                    drag_button=None)
    scatter.overlays.append(zoom)
    scatter.tools.append(PointDraggingTool(scatter))
    container.add(lineplot)
    container.add(scatter)
    # Add the title at the top
    container.overlays.append(PlotLabel('Line Editor',
                              component=container, font='swiss 16',
                              overlay_position='top'))

    return container


# ===============================================================================
# Attributes to use for the plot view.
size = (800, 700)
title = 'Simple line plot'


# ===============================================================================
## Demo class that is used by the demo.py application.
# ===============================================================================

class Demo(HasTraits):

    plot = Instance(Component)

    traits_view = View(Group(Item('plot',
                       editor=ComponentEditor(size=size),
                       show_label=False), orientation='vertical'),
                       resizable=True, title=title)

    def _plot_default(self):
        return _create_plot_component()


demo = Demo()


# ===============================================================================
# Stand-alone frame to display the plot.
# ===============================================================================

class PlotFrame(DemoFrame):

    def _create_window(self):
        # Return a window containing our plots
        return Window(self, -1, component=_create_plot_component())


if __name__ == '__main__':
    demo_main(PlotFrame, size=size, title=title)
# --EOF---
