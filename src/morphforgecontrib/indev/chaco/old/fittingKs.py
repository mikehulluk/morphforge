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

from enthought.traits.api import HasTraits,Instance,Int,Array,Float,Property,on_trait_change,Range, DelegatesTo
from enthought.traits.ui.api import View,Item,Group
from enthought.chaco.api import Plot,ArrayPlotData
from enthought.chaco.tools.api import PanTool, ZoomTool
from enthought.enable.component_editor import ComponentEditor
from enthought.enable.component_editor import ComponentEditor
from enthought.traits.ui.api import Item, Tabbed, View

import numpy as np
from numpy.random import randn
from scipy.interpolate import UnivariateSpline

from morphforge.stdimports import *

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
from morphforge.stdimports import *
from morphforgecontrib.stdimports import MM_InfTauInterpolatedChannel
from enthought.chaco.tools.api import BroadcasterTool, PanTool, ZoomTool

from enthought.chaco.api import add_default_grids, OverlayPlotContainer,  PlotLabel, Legend, PlotAxis
from enthought.chaco.tools.api import PanTool, LegendTool, TraitsTool, BroadcasterTool

from channel_panels import *

#class PointDraggingTool(DragTool):
#
#    component = Instance(Component)
#    # The pixel distance from a point that the cursor is still considered
#    # to be 'on' the point
#    threshold = Int(5)
#    # The index of the point being dragged
#    _drag_index = Int(-1)
#    # The original dataspace values of the index and value datasources
#    # corresponding to _drag_index
#    _orig_value = Tuple
#    def is_draggable(self, x, y):
#        # Check to see if (x,y) are over one of the points in self.component
#        if self._lookup_point(x, y) is not None:
#            return True
#        else:
#            return False
#    def normal_mouse_move(self, event):
#        plot = self.component
#
#        ndx = plot.map_index((event.x, event.y), self.threshold)
#        if ndx is None:
#            if plot.index.metadata.has_key('selections'):
#                del plot.index.metadata['selections']
#        else:
#            plot.index.metadata['selections'] = [ndx]
#        plot.invalidate_draw()
#        plot.request_redraw()
#    def drag_start(self, event):
#        plot = self.component
#        ndx = plot.map_index((event.x, event.y), self.threshold)
#        if ndx is None:
#            return
#        self._drag_index = ndx
#        self._orig_value = (plot.index.get_data()[ndx], plot.value.get_data()[ndx])
#    def dragging(self, event):
#        plot = self.component
#        data_x, data_y = plot.map_data((event.x, event.y))
#
#        data_x = self._orig_value[0]
#
#        plot.index._data[self._drag_index] = data_x
#        plot.value._data[self._drag_index] = data_y
#        plot.index.data_changed = True
#        plot.value.data_changed = True
#        plot.request_redraw()
#    def drag_cancel(self, event):
#        plot = self.component
#        plot.index._data[self._drag_index] = self._orig_value[0]
#        plot.value._data[self._drag_index] = self._orig_value[1]
#        plot.index.data_changed = True
#        plot.value.data_changed = True
#        plot.request_redraw()
#    def drag_end(self, event):
#        plot = self.component
#        if plot.index.metadata.has_key('selections'):
#            del plot.index.metadata['selections']
#        plot.invalidate_draw()
#        plot.request_redraw()
#    def _lookup_point(self, x, y):
#        """ Finds the point closest to a screen point if it is within self.threshold
#
#        Parameters
#        ==========
#        x : float
#            screen x-coordinate
#        y : float
#            screen y-coordinate
#        Returns
#        =======
#        (screen_x, screen_y, distance) of datapoint nearest to the input *(x,y)*.
#        If no data points are within *self.threshold* of *(x,y)*, returns None.
#        """
#        if hasattr(self.component, 'get_closest_point'):
#            # This is on BaseXYPlots
#            return self.component.get_closest_point((x,y), threshold=self.threshold)
#        return None
##===============================================================================
## # Create the Chaco plot.
##===============================================================================
#def _create_plot_component(title):
#
#    container = OverlayPlotContainer(padding = 25, fill_padding = True,
#                                     bgcolor = "lightgray", use_backbuffer=True)
#    # Create the initial X-series of data
#    numpoints = 30
#    low = -5
#    high = 15.0
#    x = linspace(low, high, numpoints)
#    y = jn(0, x)
#    lineplot = create_line_plot((x,y), color=tuple(COLOR_PALETTE[0]), width=2.0)
#    lineplot.selected_color = "none"
#    scatter = ScatterPlot(index = lineplot.index,
#                       value = lineplot.value,
#                       index_mapper = lineplot.index_mapper,
#                       value_mapper = lineplot.value_mapper,
#                       color = tuple(COLOR_PALETTE[0]),
#                       marker_size = 2)
#    scatter.index.sort_order = "ascending"
#    scatter.bgcolor = "white"
#    scatter.border_visible = True
#
#    add_default_grids(scatter)
#    add_default_axes(scatter)
#    scatter.tools.append(PanTool(scatter, drag_button="right"))
#
#    # The ZoomTool tool is stateful and allows drawing a zoom
#    # box to select a zoom region.
#    zoom = ZoomTool(scatter, tool_mode="box", always_on=False, drag_button=None)
#    scatter.overlays.append(zoom)
#    scatter.tools.append(PointDraggingTool(scatter))
#    container.add(lineplot)
#    container.add(scatter)
#    # Add the title at the top
#    container.overlays.append(PlotLabel(title,
#                              component=container,
#                              font = "swiss 16",
#                              overlay_position="top"))
#
#    return container

def getDINMorphology(axonDiam):

    mDict  = {'root': { 'length': 17.5, 'diam': 17.5, 'id':'soma', 'region':'soma', 'sections':
                           [
                            {'absangle': 0, 'length': 1, 'diam': 1.0, 'region':'soma','sections':
                            [
                                {'diam': axonDiam, 'absangle': 0, 'length': 10, 'region':'axonhillock', 'sections':
                                [
                                    {'diam': axonDiam, 'absangle': 900, 'length': 500,'region':'axon', 'sections':
                                        [{'diam': axonDiam , 'absangle': 90, 'length': 100, 'region':'axon', 'id':'axontip' }]
                                     }
                               ]
                                }
                             ]
                              }
                           ]
                }
        }

    return MorphologyLoader.fromDictionary(mDict,
            morphname='SimpleMorphology3')


vUnit = 'mV'
iUnit = 'pA/um2'
gUnit = 'pS/um2'
trace_names = [
    ('SomaVoltage', vUnit),
    ('Kf_i', iUnit),
    ('Ks_i', iUnit),
    ('Lk_i', iUnit),
    ('Na_i', iUnit),
    ('Ca_i', iUnit),
    ('Kf_g', gUnit),
    ('Ks_g', gUnit),
    ('Lk_g', gUnit),
    ('Na_g', gUnit),
    ('Ks_ks', ''),
    ('Kf_kf', ''),
    ('Na_m', ''),
    ('Na_h', ''),
    ]

from enthought.chaco.tools.api import BroadcasterTool, PanTool, ZoomTool

#
#
#class TracePlot(HasTraits):
#
#    plot = Instance(Plot)
#    view = View(
#            Group(
#                  Item('plot',editor=ComponentEditor(size=(50,50)),show_label=False),
#               ),
#                resizable=True) #,title='TracePlot')
#
#    def __init__(self, sim_conf, plot_what, colors, xRange=None, yRange=None):
#        super(TracePlot, self).__init__()
#
#        sim_conf.add_simulation_display_functor(self.update_display)
#
#        self.plot = Plot(sim_conf.data,resizable='v')
#        self.plot.padding =25
#        self.plot.fill_padding=True
#
#
#
#        # Setup the axis:
#        if xRange:
#            self.plot.x_mapper.range.set_bounds(*xRange)
#        if yRange:
#            self.plot.y_mapper.range.set_bounds(*yRange)
#        #if xMapper:
#        #    self.plot.x_mapper = xMapper
#
#        legend = Legend(component=self.plot, padding=10, align="ur")
#        legend.tools.append(LegendTool(legend, drag_button="right"))
#        self.plot.overlays.append(legend)
#
#        for what,color in zip(plot_what,colors):
#            render = self.plot.plot((what+"_t",what + "_d"),type='line' ,color=color)
#            legend.plots[what] = render
#
#        broadcaster = BroadcasterTool()
#        broadcaster.tools.append(PanTool(self.plot))
#        zoom = ZoomTool(component=self.plot, tool_mode="box", always_on=False,pointer = 'magnifier', border_color='black', border_size=3, alpha=0.5,  color='lightskyblue')
#        broadcaster.tools.append(zoom)
#        self.plot.tools.append(broadcaster)
#
#
#
#
#    def update_display(self):
#        pass
#
#

#class SimulationConfig(HasTraits):
#
#    data = Instance(ArrayPlotData)
#
#    def get_nextSimSumOutputLocation(self,):
#        self.simulation_no += 1
#        l = LocMgr.ensure_dir_exists('out/%s/'%self.date_string) + 'Sim%d.pdf'%self.simulation_no
#        return l
#
#    def __init__(self):
#
#        self.simulation_no = 0
#        self.date_string = strftime("%Y%m%d %H:%M:%S (%a, %d %b)", gmtime())
#
#
#        super(SimulationConfig, self).__init__()
#
#
#        self.x = np.linspace(0,100,1000)
#        y1 = np.sin(self.x)
#
#        rec_dict = {}
#        for tn, tunit in trace_names:
#            rec_dict[tn+'_t'] = self.x
#            rec_dict[tn+'_d'] = y1
#
#        #self.data = ArrayPlotData(SomaVoltage_t=self.x,SomaVoltage_d=y1,y2=y2)
#        self.data = ArrayPlotData(**rec_dict)
#
#        self.cell_builder_func = None
#        self.input_stimulus_builder = None
#        self.simulation_chl_functors = []
#        self.display_functors = []
#
#
#    def add_simulation_chl_functor(self, simulation_chl_functor):
#        self.simulation_chl_functors.append(simulation_chl_functor)
#
#
#    def add_simulation_display_functor(self, display_functor):
#        self.display_functors.append(display_functor)
#
#
#
#
#    def resimulate(self):
#
#
#        # Get the cell size, the input stimulus
#
#
#        env = NeuronSimulationEnvironment()
#        sim = env.Simulation()
#
#        cell = self.cell_builder_func(env=env, sim=sim)
#        self.input_stimulus_builder(sim=sim, cell=cell)
#
#
#        mech_dict = {}
#        # Apply the channels:
#        for chl in self.simulation_chl_functors:
#            mech = chl.getMechanism(env=env)
#            mech_dict[chl.chlname] = mech
#            if mech:
#                # Apply the mechanism:
#                shortcuts.apply_mechanism_everywhere_uniform(cell=cell, mechanism=mech)
#
#
#
#        #Record the Currents & Conductances:
#        for chlname, mech in mech_dict.iteritems():
#                sim.record(mech,  what = StandardTags.CurrentDensity, where=cell.get_location('soma'), name="%s_i"%chlname, description="")
#                if chlname != 'Ca':
#                    sim.record(mech,  what = StandardTags.ConductanceDensity, where=cell.get_location('soma'), name="%s_g"%chlname, description="")
#
#        # States:
#        print mech_dict.keys()
#        #['Ks', 'Na', 'Kf', 'Lk']
#
#        sim.record(mech_dict['Kf'], what=MM_InfTauInterpolatedChannel.Recordables.StateVar, state='kf',  name="Kf_kf",  where = cell.get_location('soma'), description='Kf State')
#        sim.record(mech_dict['Ks'], what=MM_InfTauInterpolatedChannel.Recordables.StateVar, state='ks',  name="Ks_ks",  where = cell.get_location('soma'), description='Ks State')
#        sim.record(mech_dict['Na'], what=MM_InfTauInterpolatedChannel.Recordables.StateVar, state='m',  name="Na_m",  where = cell.get_location('soma'), description='Na-m State')
#        sim.record(mech_dict['Na'], what=MM_InfTauInterpolatedChannel.Recordables.StateVar, state='h',  name="Na_h",  where = cell.get_location('soma'), description='Na-h State')
#
#
#
#        # Record Voltages:
#        sim.record(cell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = cell.get_location('soma'), description='Membrane Voltage')
#
#
#
#
#
#        res = sim.run()
#
#
#        # Update the array of data:
#        for trace_name, trace_unit in trace_names:
#            tr = res.get_trace(trace_name)
#            self.data.set_data(trace_name+'_t', tr.time_pts_ms)
#            self.data.set_data(trace_name+'_d', tr._data.rescale(trace_unit).magnitude)
#
#
#        # Update the display:
#        for display_func in self.display_functors:
#            display_func()
#
#        filename = self.get_nextSimSumOutputLocation()
#        print 'Writing Simulation Results to', filename
#        s = SimulationSummariser(res, filename=filename)
#        print 'Done simulating'
#
#
#
#
#
#
#







#class MorphologyConfig(HasTraits):
#    surfacearea = Range(1.0, 1000., 980)
#    capacitance = Range(0.1, 10.0, 1.0)
#    view = View(Group(
#                  Item('surfacearea',),
#                  Item('capacitance',),
#               ),
#                resizable=True,title='Morphology')
#
#    def __init__(self,sim_conf):
#        super(MorphologyConfig, self).__init__()
#        self.sim_conf = sim_conf
#        sim_conf.cell_builder_func = self.get_cell
#
#
#
#    @on_trait_change('surfacearea, capacitance')
#    def m_update(self):
#        self.sim_conf.resimulate()
#
#
#
#    def get_cell(self, env, sim):
#        m1 = MorphologyBuilder.get_single_section_soma(area= float(self.surfacearea) * um2)
#        #m1 = getDINMorphology(axonDiam=0.4)
#        myCell = sim.create_cell(name="Cell1", morphology=m1)
#        shortcuts.apply_passive_everywhere_uniform(myCell, PassiveProperty.SpecificCapacitance, unit('%f:uF/cm2'%self.capacitance))
#        return myCell
#


#class InputConfig(HasTraits):
#    amp1 =      Range(-1000.0, 1000., 100)
#    delay1 =    Range(0.0, 1000., 100)
#    dur1 =      Range(0.0, 1000., 100)
#    amp2 =      Range(-1000.0, 1000., 0)
#    delay2 =    Range(0.0, 1000., 105)
#    dur2 =      Range(0.0, 1000., 5)
#
#    sim_conf = Instance(SimulationConfig)
#    view = View(
#            Group(
#                  Item('amp1'),
#                  Item('delay1'),
#                  Item('dur1'),
#               ),
#            Group(
#                  Item('amp2'),
#                  Item('delay2'),
#                  Item('dur2'),
#               ),
#                resizable=True,title='Current Inj')
#
#    def __init__(self,sim_conf):
#        super(InputConfig, self).__init__()
#        self.sim_conf = sim_conf
#        self.sim_conf.input_stimulus_builder = self.getInputStimulus
#
#    @on_trait_change('amp1, amp2, dur1, dur2, delay1, delay2')
#    def on_update(self):
#        self.sim_conf.resimulate()
#
#    def getInputStimulus(self, sim, cell):
#        somaLoc = cell.get_location("soma")
#        s1 = sim.create_currentclamp(name="Stim1", amp=unit("%2.2f:pA"%self.amp1), dur=unit("%f:ms"%self.dur1), delay=unit("%f:ms"%self.delay1), cell_location=somaLoc)
#        s2 = sim.create_currentclamp(name="Stim2", amp=unit("%2.2f:pA"%self.amp2), dur=unit("%f:ms"%self.dur2), delay=unit("%f:ms"%self.delay2), cell_location=somaLoc)
#        return None





class Double(HasTraits):


    hhKs = Instance(HHChannelPaneInfTau1)

    view = View(
            HGroup(
                Item('hhKs', style='custom',show_label=False),
           ),
            resizable=True, width=1200, height=1200,)


from modelling.rbmodelling2.modelconstants import ChlType, Model, CellType








ksFunctor = ChannelLibrary.get_channel_functor(modelsrc=Model.Hull12Interpolated, celltype=CellType.dIN, channeltype=ChlType.Ks)



def main():

    #sim_conf = SimulationConfig()
    #sim_config = sim_conf


    d = Double(
            hhKs = buildPaneFromExistingChannelInfTau1StateNoConv(ksFunctor, sim_config=None, chlname='Ks') ,
           )
    d.configure_traits()



if __name__ == '__main__':
    main()

