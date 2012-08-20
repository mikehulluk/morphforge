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


from chaco.api import  OverlayPlotContainer
from enable.component_editor import ComponentEditor

from traits.api import HasTraits, Instance,  on_trait_change, Range
from traitsui.api import View, Item, Group

from chaco_util import VGroup, HGroup


import numpy as np


from morphforgecontrib.simulation.membranemechanisms.inftauinterpolated.core import MM_InfTauInterpolatedChannel, \
    InfTauInterpolation
from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmleak import MM_LeakChannel
from chaco_util import _create_plot_component
from morphforge.core.misc import SeqUtils
from morphforge.simulation.neuron.core.neuronsimulationenvironment import NeuronSimulationEnvironment







class PlotOptions:
    ShowAlphaBeta = False







# The Chaco Panes:
# ------------------

## SUBPANES
#===========

class HHGeneralPanel(HasTraits):
    vrev = Range(-100., 50., -70.)
    gbar = Range(0., 200, 3)

    view = View(Group(
                  Item('gbar', show_label=True),
                  Item('vrev', show_label=True),
               ),
                resizable=True, title='HHGeneral')

    def __init__(self, vrev, gbar):
        self.parentchlpane = None
        HasTraits.__init__(self, vrev=vrev, gbar=gbar)

    @on_trait_change('gbar, vrev')
    def on_change(self):
        if self.parentchlpane:
            self.parentchlpane.notify_chl_changed()


class HHGeneralStatePanel(HasTraits):

    plottau = Instance(OverlayPlotContainer)
    plotinf = Instance(OverlayPlotContainer)


    if PlotOptions.ShowAlphaBeta:
        plotalpha = Instance(OverlayPlotContainer)
        plotbeta = Instance(OverlayPlotContainer)

        traits_view = View(
            VGroup(
                HGroup(
                    Item('plottau', editor=ComponentEditor(size = (50, 50)), show_label=False, resizable=True),
                    Item('plotinf', editor=ComponentEditor(size = (50, 50)), show_label=False, resizable=True),
                    padding=0,
                   ),
                HGroup(
                    Item('plotalpha', editor=ComponentEditor(size = (50, 50)), show_label=False, resizable=True),
                    Item('plotbeta', editor=ComponentEditor(size = (50, 50)), show_label=False, resizable=True),
                  padding=0,
                   ),
                 ),
           )


    else:

        traits_view = View(
                VGroup(
                HGroup(
                    Item('plottau', editor=ComponentEditor(size = (50, 50)), show_label=False, resizable=True),
                    Item('plotinf', editor=ComponentEditor(size = (50, 50)), show_label=False, resizable=True),
                    padding=0,
               ),

                   ), resizable=True)


    def on_change_inftau(self):
        self.parentchlpane.notify_chl_changed()



    def __init__(self, initial_tau=None, initial_inf=None):
        HasTraits.__init__(self)
        self.parentchlpane = None

        self.initial_tau = initial_tau
        self.initial_inf = initial_inf

    def _plottau_default(self):
        return _create_plot_component(title='tau', on_change_functor=self.on_change_inftau, initial_values = self.initial_tau)
    def _plotinf_default(self):
        return _create_plot_component(title='inf', on_change_functor=self.on_change_inftau, initial_values = self.initial_inf)







## Channel Specific Panes
#========================









class HHChannelPaneLk(HasTraits):
    general = Instance(HHGeneralPanel)
    view = View(
            VGroup(
              Item('general', style='custom', show_label=True),
              padding=0
             ))

    def __init__(self,  sim_config, general_pane=None, chlname=None):
        HasTraits.__init__(self)

        self.sim_config = sim_config
        self.sim_config.add_simulation_chl_functor(self)

        self.general=general_pane

        self.general.parentchlpane = self
        self.chlname=chlname

    def notify_chl_changed(self):
        self.sim_config.resimulate()



    def getMechanism(self, env):
        lk = env.MembraneMechanism( MM_LeakChannel,
                                     name='Leak',
                                     mechanism_id='LKID',
                                     conductance = '%2.2f:mS/cm2' % self.general.gbar,
                                     reversalpotential = '%2.2f:mV' % self.general.vrev)
        return lk






class HHChannelPaneInfTau1(HasTraits):
    general = Instance(HHGeneralPanel)
    state = Instance(HHGeneralStatePanel)
    view = View(
            VGroup(
              Item('general', style='custom', show_label=True),
              Item('state', style='custom', show_label=True),
              padding=0
             ))

    def __init__(self,  sim_config, general_pane=None, state_pane=None, eqn=None, mechanism_id=None, chlname=None, state_var_name=None):
        HasTraits.__init__(self)

        self.sim_config = sim_config
        self.sim_config.add_simulation_chl_functor(self)

        self.general=general_pane
        self.state= state_pane

        self.general.parentchlpane = self
        self.state.parentchlpane = self

        self.eqn = eqn
        self.mechanism_id = mechanism_id
        self.state_var_name = state_var_name
        self.chlname = chlname

    def notify_chl_changed(self):
        self.sim_config.resimulate()


    def getMechanism(self, env):

        gbar = self.general.gbar
        vrev = self.general.vrev

        intp = { self.state_var_name: InfTauInterpolation(V=self.state.plotinf.mx.tolist(),
                                                          inf=self.state.plotinf.my.tolist(),
                                                          tau=self.state.plottau.my.tolist()) }

        ks = env.MembraneMechanism(MM_InfTauInterpolatedChannel,
                                      name='InfTau1',
                                      ion='ks',
                                      equation=self.eqn,
                                      mechanism_id=self.mechanism_id,
                                      conductance = '%2.2f:mS/cm2' % gbar,
                                      reversalpotential = '%2.2f:mV' % vrev,
                                      statevars_new = intp
                                      )
        return ks






class HHChannelPaneInfTau2(HasTraits):
    general = Instance(HHGeneralPanel)
    state1 = Instance(HHGeneralStatePanel)
    state2 = Instance(HHGeneralStatePanel)
    view = View(
            VGroup(
              Item('general', style='custom', show_label=True),
              Item('state1', style='custom', show_label=True),
              Item('state2', style='custom', show_label=True),
              padding=0
             ))

    def __init__(self,  sim_config, general_pane=None, state_pane1=None, state_pane2=None, eqn=None, mechanism_id=None, chlname=None, state_var_name1=None, state_var_name2=None):
        HasTraits.__init__(self)

        self.sim_config = sim_config
        self.sim_config.add_simulation_chl_functor(self)

        self.general=general_pane
        self.state1= state_pane1
        self.state2= state_pane2

        self.general.parentchlpane = self
        self.state1.parentchlpane = self
        self.state2.parentchlpane = self


        self.eqn = eqn
        self.mechanism_id = mechanism_id
        self.state_var_name1 = state_var_name1
        self.state_var_name2 = state_var_name2
        self.chlname = chlname

    def notify_chl_changed(self):
        self.sim_config.resimulate()


    def getMechanism(self, env):

        gbar = self.general.gbar
        vrev = self.general.vrev

        intp = { self.state_var_name1: InfTauInterpolation(V=self.state1.plotinf.mx.tolist(),
                                                          inf=self.state1.plotinf.my.tolist(),
                                                          tau=self.state1.plottau.my.tolist()) ,
                 self.state_var_name2: InfTauInterpolation(V=self.state2.plotinf.mx.tolist(),
                                                          inf=self.state2.plotinf.my.tolist(),
                                                          tau=self.state2.plottau.my.tolist()),
                }
        self.state1.label='m'
        self.state1.label='h'
        ks = env.MembraneMechanism(MM_InfTauInterpolatedChannel,
                                      name='InfTau1',
                                      ion='ks',
                                      equation=self.eqn,
                                      mechanism_id=self.mechanism_id,
                                      conductance = '%2.2f:mS/cm2' % gbar,
                                      reversalpotential = '%2.2f:mV' % vrev,
                                      statevars_new = intp
                                      )
        return ks






class HHChannelExistingChannel(HasTraits):

    def __init__(self,  sim_config, mechanism_functor, chlname, **kwargs):
        HasTraits.__init__(self)

        self.sim_config = sim_config
        self.sim_config.add_simulation_chl_functor(self)

        self.mechanism_functor = mechanism_functor
        self.chlname = chlname

    def notify_chl_changed(self):
        self.sim_config.resimulate()


    def getMechanism(self, env):
        return self.mechanism_functor(env=env)






# Construct Panes out of other channels:
# ==========================================
def buildStatePane(chl, state_name):
    aP = chl.statevars[state_name][0]
    bP = chl.statevars[state_name][1]
    nPts = 10
    intV = np.linspace(-100, 60, nPts)
    alphaV = (aP[0] + aP[1]*intV)/(aP[2] + np.exp((aP[3]+intV)/aP[4]))
    betaV  = (bP[0] + bP[1]*intV)/(bP[2] + np.exp((bP[3]+intV)/bP[4]))

    tauV = 1.0/(alphaV + betaV)
    infV = alphaV/(alphaV + betaV)

    state=HHGeneralStatePanel(initial_tau= [intV, tauV], initial_inf=[intV, infV])
    return state


def buildPaneFromExistingChannelInfTau1State(existing_channel_functor, sim_config, chlname):


    # Setup the channel, so we can look at inf_tau:
    chl =  existing_channel_functor(NeuronSimulationEnvironment())

    state_name = SeqUtils.expect_single(chl.statevars.keys())

    state=buildStatePane(chl, state_name)
    general=HHGeneralPanel(
            gbar=float(chl.conductance.rescale('mS/cm2').magnitude),
            vrev=float(chl.reversalpotential.rescale("mV").magnitude)
           )


    return  HHChannelPaneInfTau1(sim_config=sim_config,
                                 general_pane=general,
                                 state_pane=state,
                                 eqn = chl.eqn,
                                 mechanism_id = chl.mechanism_id,
                                 state_var_name = state_name,
                                 chlname = chlname
                               )



def buildPaneFromExistingChannelInfTau2State(existing_channel_functor, sim_config, chlname):


    # Setup the channel, so we can look at inf_tau:
    chl =  existing_channel_functor(NeuronSimulationEnvironment())

    assert set(["m", "h"]) == set(chl.statevars.keys())


    state1=buildStatePane(chl, "m")
    state2=buildStatePane(chl, "h")
    general=HHGeneralPanel(
            gbar=float(chl.conductance.rescale('mS/cm2').magnitude),
            vrev=float(chl.reversalpotential.rescale("mV").magnitude)
           )


    return  HHChannelPaneInfTau2(sim_config=sim_config,
                                 general_pane=general,
                                 state_pane1=state1,
                                 state_pane2=state2,
                                 eqn = chl.eqn,
                                 mechanism_id = chl.mechanism_id,
                                 state_var_name1 = 'm',
                                 state_var_name2 = 'h',
                                 chlname = chlname
                               )


def buildPaneFromExistingChannelLk(lkFunctor , sim_config, chlname):

    lkChl = lkFunctor(env=NeuronSimulationEnvironment())

    general=HHGeneralPanel(
                gbar=float(lkChl.conductance.rescale('mS/cm2').magnitude),
                vrev=float(lkChl.reversalpotential.rescale("mV").magnitude)
           )

    return HHChannelPaneLk(sim_config=sim_config,
                            general_pane=general,
                            chlname=chlname,
                               )



def buildPaneFromExistingChannel(existing_channel_functor, sim_config, chlname):
    return HHChannelExistingChannel(sim_config=sim_config,
                                     mechanism_functor = existing_channel_functor,
                                     chlname = chlname
                                    )


def buildPaneFromExistingChannelWithInfTau(existing_channel_functor, sim_config):

    return HHChannelExistingChannel(sim_config=sim_config,
                                     mechanism_functor = existing_channel_functor)
