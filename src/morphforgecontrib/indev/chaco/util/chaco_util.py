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

from __future__ import division

from enthought.traits.api import on_trait_change, Range, Bool
from enthought.traits.api import HasTraits, Instance, Int, Tuple
from enthought.traits.ui.api import View, Item, Group
from enthought.traits.ui.api import Tabbed
from enthought.chaco.tools.api import PanTool, ZoomTool, DragTool
from enthought.chaco.api import add_default_axes, add_default_grids, \
    OverlayPlotContainer, PlotLabel, ScatterPlot, create_line_plot

import numpy as np

# Major library imports
from numpy import linspace
from scipy.special import jn
from enthought.chaco.example_support import COLOR_PALETTE
from enthought.enable.api import Component, ComponentEditor

from morphforge.stdimports import *
from morphforgecontrib.stdimports import *

from misc import VGroup, HGroup


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


    def __init__(self, *args,**kwargs):
        DragTool.__init__(self,*args, **kwargs)
        self.on_change_functor = None # o#n_change_functor
        #assert False


    def is_draggable(self, x, y):
        # Check to see if (x,y) are over one of the points in self.component
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
        self._orig_value = (plot.index.get_data()[ndx],
                            plot.value.get_data()[ndx])

    def dragging(self, event):
        plot = self.component
        (data_x, data_y) = plot.map_data((event.x, event.y))

        data_x = self._orig_value[0]

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

        # Notify about the change:
        if self.on_change_functor:
            self.on_change_functor()

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
        (screen_x, screen_y, distance) of datapoint nearest to the input *(x,y)*.
        If no data points are within *self.threshold* of *(x,y)*, returns None.
        """

        if hasattr(self.component, 'get_closest_point'):
            # This is on BaseXYPlots
            return self.component.get_closest_point((x, y),
                    threshold=self.threshold)
        return None
#===============================================================================
# # Create the Chaco plot.
#===============================================================================
def _create_draggable_plot_component(title, initial_values=None,on_change_functor=None, ):

    container = OverlayPlotContainer(padding = 30, fill_padding = True,
                                     bgcolor = "lightgray", use_backbuffer=True)


    if initial_values:
        x = initial_values[0]
        y = initial_values[1]
    else:
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
        marker_size=2,
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

    point_dragging_tool = PointDraggingTool(scatter)
    point_dragging_tool.on_change_functor = on_change_functor
    scatter.tools.append(point_dragging_tool)

    container.add(lineplot)
    container.add(scatter)
    # Add the title at the top
    container.overlays.append(PlotLabel(title, component=container,
                              font='swiss 16', overlay_position='top'))

    container.mx = lineplot.index.get_data()
    container.my = lineplot.value.get_data()

    container.lineplot = lineplot
    return container


