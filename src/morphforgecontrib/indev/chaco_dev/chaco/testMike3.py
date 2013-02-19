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


#from chaco.api import Plot, ArrayPlotData, add_default_axes, add_default_grids, OverlayPlotContainer, PlotLabel, ScatterPlot, create_line_plot
#from chaco.example_support import COLOR_PALETTE

from chaco.api import Plot, ArrayPlotData
from chaco.tools.api import PanTool, ZoomTool, BroadcasterTool
from modelling.rbmodelling2.modelconstants import ChlType, Model, CellType

from traitsui.api import View, Item, Group, Tabbed
from enable.component_editor import ComponentEditor
from traits.has_traits import HasTraits, on_trait_change
from traits.trait_types import Instance, Range


from morphforgecontrib.simulation.channels.inftauinterpolated.core import MM_InfTauInterpolatedChannel

from channel_panels import HHChannelPaneInfTau1, HHChannelExistingChannel, HHChannelPaneLk, buildPaneFromExistingChannel,  buildPaneFromExistingChannelLk


from chaco_util import HGroup, VGroup
from channel_panels import buildPaneFromExistingChannelInfTau1State
from channel_panels import HHChannelPaneInfTau2, buildPaneFromExistingChannelInfTau2State



import morphforge.stdimports as mf
import numpy as np









vUnit = 'mV'
iUnit = 'pA/um2'
gUnit = 'pS/um2'
trace_names = [('SomaVoltage', vUnit),
                ('Kf_i', iUnit), ('Ks_i', iUnit), ('Lk_i', iUnit), ('Na_i', iUnit), ('Ca_i', iUnit),
                ('Kf_g', gUnit), ('Ks_g', gUnit), ('Lk_g', gUnit), ('Na_g', gUnit),
                ('Ks_ks', ''), ('Kf_kf', ''), ('Na_m', ''), ('Na_h', ''),
               ]


#trace_names = [('SomaVoltage', vUnit)]








class TracePlot(HasTraits):

    plot = Instance(Plot)
    view = View(
            Group(
                  Item('plot', editor=ComponentEditor(size=(30, 30)), show_label=False),
               ),
                resizable=True)

    def __init__(self, sim_conf, plot_what, colors, xRange=None, yRange=None):
        super(TracePlot, self).__init__()

        sim_conf.add_simulation_display_functor(self.update_display)

        self.plot = Plot(sim_conf.data, resizable='v')
        self.plot.padding =25
        self.plot.fill_padding=True



        # Setup the axis:
        if xRange:
            self.plot.x_mapper.range.set_bounds(*xRange)
        if yRange:
            self.plot.y_mapper.range.set_bounds(*yRange)

        for what, color in zip(plot_what, colors):
            self.plot.plot((what+"_t", what + "_d"), type='line', color=color)


        broadcaster = BroadcasterTool()
        broadcaster.tools.append(PanTool(self.plot))
        zoom = ZoomTool(component=self.plot, tool_mode="box", always_on=False, pointer = 'magnifier', border_color='black', border_size=3, alpha=0.5,  color='lightskyblue')
        broadcaster.tools.append(zoom)
        self.plot.tools.append(broadcaster)


    def update_display(self):
        pass






class SimulationConfig(HasTraits):

    data = Instance(ArrayPlotData)


    def __init__(self):
        super(SimulationConfig, self).__init__()


        self.x = np.linspace(0, 100, 1000)
        y1 = np.sin(self.x)

        rec_dict = {}
        for tn, tunit in trace_names:
            rec_dict[tn+'_t'] = self.x
            rec_dict[tn+'_d'] = y1

        #self.data = ArrayPlotData(SomaVoltage_t=self.x, SomaVoltage_d=y1, y2=y2)
        self.data = ArrayPlotData(**rec_dict)

        self.cell_builder_func = None
        self.input_stimulus_builder = None
        self.simulation_chl_functors = []
        self.display_functors = []


    def add_simulation_chl_functor(self, simulation_chl_functor):
        self.simulation_chl_functors.append(simulation_chl_functor)


    def add_simulation_display_functor(self, display_functor):
        self.display_functors.append(display_functor)




    def resimulate(self):


        # Get the cell size, the input stimulus


        env = mf.NEURONEnvironment()
        sim = env.Simulation()

        cell = self.cell_builder_func(env=env, sim=sim)
        self.input_stimulus_builder(sim=sim, cell=cell)



        mech_dict = {}
        # Apply the channels:
        for chl in self.simulation_chl_functors:
            mech = chl.getMechanism(env=env)
            mech_dict[chl.chlname] = mech
            if mech:
                # Apply the mechanism:
                cell.apply_channel(mech)



        #Record the Currents & Conductances:
        for chlname, mech in mech_dict.iteritems():
                sim.record(mech,  what = mf.StandardTags.CurrentDensity, cell_location=cell.get_location('soma'), name="%s_i" % chlname, description="")
                if chlname != 'Ca':
                    sim.record(mech,  what = mf.StandardTags.ConductanceDensity, cell_location=cell.get_location('soma'), name="%s_g" % chlname, description="")




        sim.record(mech_dict['Kf'], what=MM_InfTauInterpolatedChannel.Recordables.StateVar, state='kf',  name="Kf_kf",  cell_location = cell.get_location('soma'), description='Kf State')
        sim.record(mech_dict['Ks'], what=MM_InfTauInterpolatedChannel.Recordables.StateVar, state='ks',  name="Ks_ks",  cell_location = cell.get_location('soma'), description='Ks State')
        sim.record(mech_dict['Na'], what=MM_InfTauInterpolatedChannel.Recordables.StateVar, state='m',  name="Na_m",  cell_location = cell.get_location('soma'), description='Na-m State')
        sim.record(mech_dict['Na'], what=MM_InfTauInterpolatedChannel.Recordables.StateVar, state='h',  name="Na_h",  cell_location = cell.get_location('soma'), description='Na-h State')

        # Record Voltages:
        sim.record(cell, what=mf.StandardTags.Voltage, name="SomaVoltage", cell_location = cell.get_location('soma'), description='Membrane Voltage')





        res = sim.run()


        # Update the array of data:
        for trace_name, trace_unit in trace_names:
            tr = res.get_trace(trace_name)
            self.data.set_data(trace_name+'_t', tr.time_pts_ms)
            self.data.set_data(trace_name+'_d', tr._data.rescale(trace_unit).magnitude)


        # Update the display:
        for display_func in self.display_functors:
            display_func()


        print 'Done simulating'














class MorphologyConfig(HasTraits):
    area = Range(1.0, 1000., 590)
    capacitance = Range(0.1, 10.0, 1.0)
    view = View(Group(
                  Item('area'),
                  Item('capacitance'),
               ),
                resizable=True, title='Morphology')

    def __init__(self, sim_conf):
        super(MorphologyConfig, self).__init__()
        self.sim_conf = sim_conf
        sim_conf.cell_builder_func = self.get_cell



    @on_trait_change('area, capacitance')
    def m_update(self):
        self.sim_conf.resimulate()



    def get_cell(self, env, sim):
        m1 = mf.MorphologyBuilder.get_single_section_soma(area= float(self.area) * mf.units.um2)

        morph_functor = mf.MorphologyLibrary.get_morphology_functor(modelsrc=Model.Hull12SWithAxon, celltype=CellType.dIN)
        m1 = morph_functor(axonDiam = 0.4)

        myCell = sim.create_cell(name="Cell1", morphology=m1)
        myCell.set_passive( mf.PassiveProperty.SpecificCapacitance, mf.qty('%f:uF/cm2' % self.capacitance) )
        return myCell



class InputConfig(HasTraits):
    amp1 =      Range(-1000.0, 1000., 200)
    delay1 =    Range(0.0, 1000., 100)
    dur1 =      Range(0.0, 1000., 100)
    amp2 =      Range(-1000.0, 1000., 0)
    delay2 =    Range(0.0, 1000., 105)
    dur2 =      Range(0.0, 1000., 5)

    sim_conf = Instance(SimulationConfig)
    view = View(
            Group(
                  Item('amp1'),
                  Item('delay1'),
                  Item('dur1'),
                  label='Stim1'
               ),
            Group(
                  Item('amp2'),
                  Item('delay2'),
                  Item('dur2'),
                  label='Stim2'
               ),
                resizable=True, title='Current Inj')

    def __init__(self, sim_conf):
        super(InputConfig, self).__init__()
        self.sim_conf = sim_conf
        self.sim_conf.input_stimulus_builder = self.getInputStimulus

    @on_trait_change('amp1, amp2, dur1, dur2, delay1, delay2')
    def on_update(self):
        self.sim_conf.resimulate()

    def getInputStimulus(self, sim, cell):
        somaLoc = cell.get_location("soma")
        s1 = sim.create_currentclamp(name="Stim1", amp=mf.qty("%2.2f:pA" % self.amp1), dur=mf.qty("%f:ms" % self.dur1), delay=mf.qty("%f:ms" % self.delay1), cell_location=somaLoc)
        s2 = sim.create_currentclamp(name="Stim2", amp=mf.qty("%2.2f:pA" % self.amp2), dur=mf.qty("%f:ms" % self.dur2), delay=mf.qty("%f:ms" % self.delay2), cell_location=somaLoc)
        return None





class Double(HasTraits):

    s3 = Instance(TracePlot)
    s4 = Instance(TracePlot)
    s5 = Instance(TracePlot)
    s6 = Instance(TracePlot)
    conf_morph= Instance(MorphologyConfig)
    conf_input = Instance(InputConfig)

    hhKf = Instance(HHChannelPaneInfTau1)
    hhKs = Instance(HHChannelPaneInfTau1)
    hhNa = Instance(HHChannelPaneInfTau2)
    hhCa = Instance(HHChannelExistingChannel)
    hhLk = Instance(HHChannelPaneLk)

    view = View(
            HGroup(
             VGroup(
                 Tabbed(
                     Item('hhLk', style='custom', show_label=False),
                     Item('hhKf', style='custom', show_label=False),
                     Item('hhKs', style='custom', show_label=False),
                     Item('hhNa', style='custom', show_label=False),
                     Item('hhCa', style='custom', show_label=False),
                    )
            ),
              VGroup(
               Item('s3', style='custom', show_label=False),
               Item('s4', style='custom', show_label=False),
               Item('s5', style='custom', show_label=False),
               Item('s6', style='custom', show_label=False),
             ),
              VGroup(
               Item('conf_morph', style='custom', show_label=False),
               Item('conf_input', style='custom', show_label=False),
             ),
             ),

            resizable=True, width=1200, height=1200)





caMult = 1.0
naMult = 5.0
lkMult = 1.0
ksMult = 0.5
kfMult = 2.5
lkFunctorBase = mf.ChannelLibrary.get_channel_functor(modelsrc=Model.Hull12, celltype=CellType.dIN, channeltype=ChlType.Lk)
caFunctorBase = mf.ChannelLibrary.get_channel_functor(modelsrc=Model.Hull12, celltype=CellType.dIN, channeltype=ChlType.Ca)
naFunctorBase = mf.ChannelLibrary.get_channel_functor(modelsrc=Model.Dale95, celltype=CellType.RB,  channeltype=ChlType.Na)
kfFunctorBase = mf.ChannelLibrary.get_channel_functor(modelsrc=Model.Hull12, celltype=CellType.DL,  channeltype=ChlType.Kf)
ksFunctorBase = mf.ChannelLibrary.get_channel_functor(modelsrc=Model.Hull12, celltype=CellType.RB,  channeltype=ChlType.Ks)

def caFunctor(env):
    chl = caFunctorBase(env)
    chl.permeability *= caMult
    return chl

def naFunctor(env):
    chl = naFunctorBase(env)
    chl.conductance *= naMult
    return chl

def kfFunctor(env):
    chl = kfFunctorBase(env)
    chl.conductance *= kfMult
    return chl

def ksFunctor(env):
    chl = ksFunctorBase(env)
    chl.conductance *= ksMult
    return chl

def lkFunctor(env):
    chl = lkFunctorBase(env)
    chl.conductance *= lkMult
    return chl







def main():

    sim_conf = SimulationConfig()
    sim_config = sim_conf

    xRange=(95, 130)

    d = Double(
            s3 = TracePlot(sim_conf=sim_conf, plot_what=['SomaVoltage'], colors=['green'], yRange=(-80, 50), xRange=xRange),
            s4 = TracePlot(sim_conf=sim_conf, plot_what=['Kf_i', 'Ks_i', 'Lk_i', 'Na_i', 'Ca_i'], colors=['cyan', 'blue', 'red', 'green', 'orange'], xRange=xRange),
            #s5 = TracePlot(sim_conf=sim_conf, plot_what=['Kf_g', 'Ks_g', 'Lk_g', 'Na_g'], colors=['cyan', 'blue', 'red', 'green'], xRange=xRange),
            #s6 = TracePlot(sim_conf=sim_conf, plot_what=['Kf_kf', 'Ks_ks', 'Na_m', 'Na_h'], colors=['cyan', 'blue', 'red', 'green'], xRange=xRange),
            conf_morph= MorphologyConfig(sim_conf=sim_conf),
            conf_input= InputConfig(sim_conf=sim_conf),

            hhKs = buildPaneFromExistingChannelInfTau1State(ksFunctor, sim_config=sim_config, chlname='Ks') ,
            hhKf = buildPaneFromExistingChannelInfTau1State(kfFunctor, sim_config=sim_config, chlname='Kf') ,
            hhNa = buildPaneFromExistingChannelInfTau2State(naFunctor, sim_config=sim_config, chlname='Na') ,
            hhCa = buildPaneFromExistingChannel(caFunctor, sim_config=sim_config, chlname='Ca') ,
            hhLk = buildPaneFromExistingChannelLk(lkFunctor, sim_config=sim_config, chlname='Lk') ,
           )
    d.configure_traits()



if __name__ == '__main__':
    main()

































