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



from morphforge.stdimports import *
from morphforgecontrib.stdimports import *
from morphforge.units import *




# tIN-> dIN
# ##########
PostSynapticTemplateLibrary.register_template_specialisation( modelsrc='HULL10', synapsetype='tIN-dIN-AMPA',
        template_type = PostSynapticMech_Exp2Syn_Base,
        tau_open = 0.2 * units.ms, tau_close=3.0*units.ms, e_rev=0 * units.mV, popening=0.5, peak_conductance=0.25*nS)


PostSynapticTemplateLibrary.register_template_specialisation( modelsrc='HULL10', synapsetype='tIN-dIN-NMDA',
        template_type = PostSynapticMech_Exp2SynNMDA_Base,
        tau_open=5.0*units.ms,  tau_close=80*units.ms, e_rev=0*mV,  popening=0.5, peak_conductance=0.300*nS, vdep=True,
        )

# dIN-> dIN
# ----------
PostSynapticTemplateLibrary.register_template_specialisation( modelsrc='HULL10', synapsetype='dIN-dIN-AMPA',
        template_type = PostSynapticMech_Exp2Syn_Base,
        tau_open = 0.2 * units.ms, tau_close=3.0*units.ms, e_rev=0 * units.mV, popening=1.0, peak_conductance=0.300*nS,
        )

PostSynapticTemplateLibrary.register_template_specialisation( modelsrc='HULL10', synapsetype='dIN-dIN-NMDA',
        template_type = PostSynapticMech_Exp2SynNMDA_Base,
        tau_open=5.0*units.ms,  tau_close=80.0*units.ms, e_rev=0*mV,  popening=1.0, peak_conductance=0.3*nS, vdep=True,
        )

PostSynapticTemplateLibrary.register_template_specialisation( modelsrc='HULL10', synapsetype='dIN-dIN-Background-NMDA',
        template_type = PostSynapticMech_Exp2SynNMDA_Base,
        tau_open=5.0*units.ms,  tau_close=10000*units.ms, e_rev=0*mV,  popening=1.0, peak_conductance=0.300*nS, vdep=True,
        )

# MHR -> dIN
# -----------
PostSynapticTemplateLibrary.register_template_specialisation( modelsrc='HULL10', synapsetype='MHR-dIN-Inhib',
        template_type = PostSynapticMech_Exp2Syn_Base,
        tau_open=1.5*units.ms,  tau_close=20*units.ms, e_rev=-70*mV,  popening=1.0, peak_conductance=2.0*nS,
        )







# tIN -> dIN
# ==============
def create_synapse_tIN_to_dIN_AMPA_spike_times_new( sim, times, postsynaptic, **kwargs ):
    env = sim.environment
    psm_tmpl = PostSynapticTemplateLibrary.get_template( modelsrc='HULL10', synapsetype='tIN-dIN-AMPA', sim=sim)
    return sim.create_synapse(
                trigger=env.SynapticTrigger(SynapticTriggerAtTimes, time_list=times),
                postsynaptic_mech=psm_tmpl.instantiate(cell_location=postsynaptic.soma, **kwargs)
                )

def create_synapse_tIN_to_dIN_NMDA_spike_times_new( sim, times, postsynaptic, **kwargs ):
    env = sim.environment
    psm_tmpl = PostSynapticTemplateLibrary.get_template( modelsrc='HULL10', synapsetype='tIN-dIN-NMDA', sim=sim)
    return sim.create_synapse(
                trigger=env.SynapticTrigger(SynapticTriggerAtTimes, time_list=times),
                postsynaptic_mech=psm_tmpl.instantiate(cell_location=postsynaptic.soma, **kwargs)
                )

def create_synapse_tIN_to_dIN_AMPA_new( sim, presynaptic, postsynaptic, delay=None, **kwargs ):
    env = sim.environment
    psm_tmpl = PostSynapticTemplateLibrary.get_template( modelsrc='HULL10', synapsetype='tIN-dIN-AMPA', sim=sim)
    return sim.create_synapse(
                trigger=env.SynapticTrigger( SynapticTriggerByVoltageThreshold,
                                    cell_location =  presynaptic.soma,
                                    voltage_threshold = 0*units.mV,
                                    delay=1.0*units.ms,
                                    ),
                postsynaptic_mech=psm_tmpl.instantiate(cell_location=postsynaptic.soma, **kwargs)
                )

def create_synapse_tIN_to_dIN_NMDA_new( sim, presynaptic, postsynaptic, **kwargs ):
    env = sim.environment
    psm_tmpl = PostSynapticTemplateLibrary.get_template( modelsrc='HULL10', synapsetype='tIN-dIN-NMDA', sim=sim)
    return sim.create_synapse(
                trigger=env.SynapticTrigger( SynapticTriggerByVoltageThreshold,
                                    cell_location =  presynaptic.soma,
                                    voltage_threshold = 0*units.mV,
                                    delay=1.0*units.ms,
                                    ),
                postsynaptic_mech=psm_tmpl.instantiate(cell_location=postsynaptic.soma, **kwargs)
                )

def create_synapse_tIN_to_dIN_AMPANMDA_spike_times_new(sim, times, postsynaptic, multiplier=1.0, ampa_multiplier=1.0, nmda_multiplier=1.0, parameter_overrides=None ):
    parameter_overrides = parameter_overrides or {}
    down_factor = 1.0
    s1 = create_synapse_tIN_to_dIN_AMPA_spike_times_new( sim, times, postsynaptic, parameter_multipliers={'peak_conductance':multiplier*down_factor * ampa_multiplier},parameter_overrides=parameter_overrides  )
    s2 = create_synapse_tIN_to_dIN_NMDA_spike_times_new( sim, times, postsynaptic, parameter_multipliers={'peak_conductance':multiplier*down_factor * nmda_multiplier},parameter_overrides=parameter_overrides  )
    return [s1,s2]

def create_synapse_tIN_to_dIN_AMPANMDA_new(sim, times, postsynaptic,multiplier=1.0, ampa_multiplier=1.0, nmda_multiplier=1.0, parameter_overrides=None):
    parameter_overrides = parameter_overrides or {}
    down_factor = 1.0
    s1 = create_synapse_tIN_to_dIN_AMPA_new( sim, times, postsynaptic, parameter_multipliers = {'peak_conductance':multiplier*down_factor * ampa_multiplier},parameter_overrides=parameter_overrides )
    s2 = create_synapse_tIN_to_dIN_NMDA_new( sim, times, postsynaptic, parameter_multipliers = {'peak_conductance':multiplier*down_factor * nmda_multiplier},parameter_overrides=parameter_overrides )
    return s1,s2






def create_synapse_dIN_to_dIN_AMPA_spike_times_new( sim, times, postsynaptic, **kwargs ):
    env = sim.environment
    psm_tmpl = PostSynapticTemplateLibrary.get_template( modelsrc='HULL10', synapsetype='dIN-dIN-AMPA', sim=sim)
    return sim.create_synapse(
                trigger=env.SynapticTrigger(SynapticTriggerAtTimes, time_list=times),
                postsynaptic_mech=psm_tmpl.instantiate(cell_location=postsynaptic.soma, **kwargs)
                )

def create_synapse_dIN_to_dIN_NMDA_spike_times_new( sim, times, postsynaptic, **kwargs ):
    env = sim.environment
    psm_tmpl = PostSynapticTemplateLibrary.get_template( modelsrc='HULL10', synapsetype='dIN-dIN-NMDA', sim=sim)
    return sim.create_synapse(
                trigger=env.SynapticTrigger(SynapticTriggerAtTimes, time_list=times),
                postsynaptic_mech=psm_tmpl.instantiate(cell_location=postsynaptic.soma, **kwargs)
                )

def create_synapse_dIN_to_dIN_AMPA_new( sim, presynaptic, postsynaptic, **kwargs ):
    env = sim.environment
    psm_tmpl = PostSynapticTemplateLibrary.get_template( modelsrc='HULL10', synapsetype='dIN-dIN-AMPA', sim=sim)
    return sim.create_synapse(
                trigger=env.SynapticTrigger( SynapticTriggerByVoltageThreshold,
                                    cell_location =  presynaptic.soma,
                                    voltage_threshold = 0*units.mV,
                                    delay=1.0*units.ms,
                                    ),
                postsynaptic_mech=psm_tmpl.instantiate(cell_location=postsynaptic.soma, **kwargs)
                )

def create_synapse_dIN_to_dIN_NMDA_new( sim, presynaptic, postsynaptic, **kwargs ):
    env = sim.environment
    psm_tmpl = PostSynapticTemplateLibrary.get_template( modelsrc='HULL10', synapsetype='dIN-dIN-NMDA', sim=sim)
    return sim.create_synapse(
                trigger=env.SynapticTrigger( SynapticTriggerByVoltageThreshold,
                                    cell_location =  presynaptic.soma,
                                    voltage_threshold = 0*units.mV,
                                    delay=1.0*units.ms,
                                    ),
                postsynaptic_mech=psm_tmpl.instantiate(cell_location=postsynaptic.soma, **kwargs)
                )

def create_synapse_background_NMDA_spike_times_new( sim, times,  postsynaptic, **kwargs):
    env = sim.environment
    psm_tmpl = PostSynapticTemplateLibrary.get_template( modelsrc='HULL10', synapsetype='dIN-dIN-Background-NMDA', sim=sim)
    return sim.create_synapse(
                trigger=env.SynapticTrigger(SynapticTriggerAtTimes, time_list=times),
                postsynaptic_mech=psm_tmpl.instantiate(cell_location=postsynaptic.soma, **kwargs)
                )

def create_synapse_mhr_to_dIN_inhib_spike_times_new( sim, times, postsynaptic, **kwargs ):
    env = sim.environment
    psm_tmpl = PostSynapticTemplateLibrary.get_template( modelsrc='HULL10', synapsetype='MHR-dIN-Inhib', sim=sim)
    return sim.create_synapse(
                trigger=env.SynapticTrigger(SynapticTriggerAtTimes, time_list=times),
                postsynaptic_mech=psm_tmpl.instantiate(cell_location=postsynaptic.soma, **kwargs)
                )







#def create_synapse_tIN_to_dIN_AMPANMDA_spike_times_new(sim, times, postsynaptic, multiplier=1.0, ampa_multiplier=1.0, nmda_multiplier=1.0, parameter_overrides=None ):
#    parameter_overrides = parameter_overrides or {}
#    down_factor = 1.0
#    s1 = create_synapse_tIN_to_dIN_AMPA_spike_times_new( sim, times, postsynaptic, parameter_multipliers={'peak_conductance':multiplier*down_factor * ampa_multiplier},parameter_overrides=parameter_overrides  )
#    s2 = create_synapse_tIN_to_dIN_NMDA_spike_times_new( sim, times, postsynaptic, parameter_multipliers={'peak_conductance':multiplier*down_factor * nmda_multiplier},parameter_overrides=parameter_overrides  )
#    return [s1,s2]
#
#def create_synapse_tIN_to_dIN_AMPANMDA_new(sim, times, postsynaptic,multiplier=1.0, ampa_multiplier=1.0, nmda_multiplier=1.0, parameter_overrides=None):
#    parameter_overrides = parameter_overrides or {}
#    down_factor = 1.0
#    s1 = create_synapse_tIN_to_dIN_AMPA_new( sim, times, postsynaptic, parameter_multipliers = {'peak_conductance':multiplier*down_factor * ampa_multiplier},parameter_overrides=parameter_overrides )
#    s2 = create_synapse_tIN_to_dIN_NMDA_new( sim, times, postsynaptic, parameter_multipliers = {'peak_conductance':multiplier*down_factor * nmda_multiplier},parameter_overrides=parameter_overrides )
#    return s1,s2









"""Defining populations of neurons.

"""

from morphforge.stdimports import *
from morphforgecontrib.stdimports import *

import itertools
import random

import numpy as np
import pickle
import os
import pylab
from functools import partial
















@cached_functor
def get_leak_chls(env):
    lk_chl = env.Channel(
			StdChlLeak, name='LkChl',
            conductance=qty('0.3:mS/cm2'),
            reversalpotential=qty('-54.3:mV'),)
    return lk_chl

@cached_functor
def get_na_chls(env):
    na_state_vars = { "m": {
                          "alpha":[-4.00,-0.10,-1.00,40.00,-10.00],
                          "beta": [ 4.00, 0.00, 0.00,65.00, 18.00]},
                    "h": {
                            "alpha":[0.07,0.00,0.00,65.00,20.00] ,
                            "beta": [1.00,0.00,1.00,35.00,-10.00]}
                      }

    na_chl = env.Channel(
        StdChlAlphaBeta,
        name='NaChl',
        ion='na',
        equation='m*m*m*h',
        conductance=qty('120:mS/cm2'),
        reversalpotential=qty('50:mV'),
        statevars=na_state_vars,
        )
    return na_chl


@cached_functor
def get_k_chls(env):
    k_state_vars = { "n": {
                          "alpha":[-0.55,-0.01,-1.0,55.0,-10.0],
                          "beta": [0.125,0,0,65,80]},
                       }
    k_chl = env.Channel(
        StdChlAlphaBeta,
        name='KChl',
        ion='k',
        equation='n*n*n*n',
        conductance=qty('36:mS/cm2'),
        reversalpotential=-77*mV,#qty('-77:mV'),
        statevars=k_state_vars,
        )
    return k_chl


def makehh(sim, name=None, cell_tags=None):
    m = MorphologyBuilder.get_single_section_soma(area=1000.*um2)
    cell = sim.create_cell(name=name, morphology=m)
    cell.apply_channel(get_leak_chls(sim.environment))
    cell.apply_channel(get_na_chls(sim.environment))
    cell.apply_channel(get_k_chls(sim.environment))
    return cell


class UserTags:
    dINs = 'dINs'
    RHS = 'RHS'



def _run_sim(i, stim_level, nmda_multiplier_feedback):

    env = NEURONEnvironment()
    sim = env.Simulation(cvode=True, tstop=1600 * units.ms, dt=0.10 * units.ms)

    R_dINs = NeuronPopulation(sim=sim, n=30, neuron_functor=makehh, pop_name="RHS_dIN" )

    R_dINs.record_from_all( description="dIN RHS", user_tags=[UserTags.dINs, UserTags.RHS,'Soma'] )

    sim.record(R_dINs[5], what=Cell.Recordables.MembraneVoltage,  user_tags=[UserTags.dINs, 'RHS_dIN_5'] )
    sim.record(R_dINs[10], what=Cell.Recordables.MembraneVoltage, user_tags=[UserTags.dINs, 'RHS_dIN_10'] )
    sim.record(R_dINs[15], what=Cell.Recordables.MembraneVoltage, user_tags=[UserTags.dINs, 'RHS_dIN_15'] )
    sim.record(R_dINs[20], what=Cell.Recordables.MembraneVoltage, user_tags=[UserTags.dINs, 'RHS_dIN_20'] )
    sim.record(R_dINs[25], what=Cell.Recordables.MembraneVoltage, user_tags=[UserTags.dINs, 'RHS_dIN_25'] )


    # Connect tIN -> dIN:
    tINSpikeTimesRHS = EventSet( np.random.normal(100,1,40) * units.ms )
    synapses_tIN_to_dIN1 = Connectors.times_to_all( sim=sim,
                                                 syncronous_times=tINSpikeTimesRHS,
                                                 postsynaptic_population=R_dINs,
                                                 connect_functor = partial( create_synapse_tIN_to_dIN_AMPANMDA_spike_times_new, multiplier=1.0, nmda_multiplier=1.0, parameter_overrides={'popening':1.0} ),
                                                 synapse_pop_name = "dIN_NMDA_background",)

    tINSpikeTimesRHS = EventSet( np.random.normal(600,1,40) * units.ms )
    synapses_tIN_to_dIN2 = Connectors.times_to_all( sim=sim,
                                                 syncronous_times=tINSpikeTimesRHS,
                                                 postsynaptic_population=R_dINs,
                                                 connect_functor = partial( create_synapse_tIN_to_dIN_AMPANMDA_spike_times_new, multiplier=1.0, nmda_multiplier=1.0, parameter_overrides={'popening':1.0} ),
                                                 synapse_pop_name = "dIN_NMDA_background2",)
    # Connect MHR -> dIN:
    MHRSpikeTimesRHS = EventSet( np.random.normal(300,2,3) * units.ms )
    synapses_MHR_to_dIN1 = Connectors.times_to_all( sim=sim,
                                                 syncronous_times=MHRSpikeTimesRHS,
                                                 postsynaptic_population=R_dINs,
                                                 connect_functor = partial( create_synapse_mhr_to_dIN_inhib_spike_times_new, parameter_multipliers={'peak_conductance':1.5},   ),
                                                 synapse_pop_name = "mhr_inhib",
                                               )
    # Connect MHR -> dIN:
    MHRSpikeTimesRHS = EventSet( np.random.normal(1400,2,3) * units.ms )
    synapses_MHR_to_dIN2 = Connectors.times_to_all( sim=sim,
                                                 syncronous_times=MHRSpikeTimesRHS,
                                                 postsynaptic_population=R_dINs,
                                                 connect_functor = partial( create_synapse_mhr_to_dIN_inhib_spike_times_new, parameter_multipliers={'peak_conductance':1.5},   ),
                                                 synapse_pop_name = "mhr_inhib2",
                                               )

    # dIN -> dIN
    synapses_dIN_to_dIN_AMPA = Connectors.all_to_all(sim,
                            presynaptic_population=R_dINs,
                            postsynaptic_population=R_dINs,
                            connect_functor = exec_with_prob(0.15, partial(create_synapse_dIN_to_dIN_AMPA_new, parameter_multipliers={'peak_conductance':0.1}))  )
    synapses_dIN_to_dIN = Connectors.all_to_all(sim,
                            presynaptic_population=R_dINs,
                            postsynaptic_population=R_dINs,
                            connect_functor = exec_with_prob(0.15, partial(create_synapse_dIN_to_dIN_NMDA_new, parameter_multipliers={'peak_conductance':nmda_multiplier_feedback})))


    # Record from the tIN -> dIN population:
    synapses_tIN_to_dIN1.record_from_all(what=Synapse.Recordables.SynapticConductance, user_tags=['PREPOP:RHS_tINs'] )
    synapses_tIN_to_dIN2.record_from_all(what=Synapse.Recordables.SynapticConductance, user_tags=['PREPOP:RHS_tINs'] )

    synapses_MHR_to_dIN1.record_from_all(what=Synapse.Recordables.SynapticConductance, user_tags=['PREPOP:RHS_mhrs'] )
    synapses_MHR_to_dIN2.record_from_all(what=Synapse.Recordables.SynapticConductance, user_tags=['PREPOP:RHS_mhrs'] )

    return sim.run(), tINSpikeTimesRHS



def testSingleSynapseAMPANMDA(i,stim_level, nmda_multiplier_feedback):
    res, tINSpikeTimesRHS = _run_sim(i=i, stim_level=stim_level, nmda_multiplier_feedback=nmda_multiplier_feedback )

    first_spikes = PopAnalSpiking.evset_first_spike( res=res, tag_selector=TagSelector.from_string("ALL{dINs,Voltage}"), comment="dIN First Spike" )
    all_spikes = PopAnalSpiking.evset_all_spikes( res=res, tag_selector=TagSelector.from_string("ALL{dINs,Voltage}"), comment="dIN All Spikes" )


    rasters = []
    for i in range(0, 30):
        if i % 4 != 0:
            continue
        nrn_all_spikes = PopAnalSpiking.evset_all_spikes( res=res, tag_selector=TagSelector.from_string("ALL{dINs,Voltage, RHS_dIN_%d}"%i ),  )
        nrn_all_spikes.tags.add("SpikesFor%d"%i)
        nrn_all_spikes.tags.add("Raster")
        rasters.append( nrn_all_spikes)

    ps = [
          TagPlot( "ALL{Conductance,POSTCELL:RHS_dIN_0} AND ANY{PREPOP:RHS_mhrs,PREPOP:RHS_tINs}",
                    yunit=units.nS,
                    ylabel='Conductance',
                    yticks=(0,15)*units.nS,
                    yrange=(0,20)*units.nS,
                    legend_labeller=None,
                    show_yticklabels_with_units=True,
                    yticklabel_quantisation=Decimal('1'),
          ),
          TagPlot( "ALL{Voltage, RHS_dIN_10}",
                    yunit=units.mV,
                    colors=['blue'],
                    ylabel='Voltage (dIN #10)',
                    legend_labeller=None,
                    yticks=(-80,-40,0,40)*units.mV,
                    show_yticklabels_with_units=True,
                    yticklabel_quantisation=Decimal('1')
          ),
          TagPlot( "ALL{Raster}", ylabel='Spike\nraster',legend_labeller=None, show_yticklabels=False   ),
          ]



    TagViewer( [res, tINSpikeTimesRHS,first_spikes, all_spikes] + rasters,
                    plots=ps,
                    timerange=(50,1600)*units.ms,
                    xticks=(200,600,1000,1400,)*units.ms,
                    show_xlabel = False,
                    show_xticklabels = 'only-once',
                    show_xaxis_position = 'top',
                    show_xticklabels_with_units = True,
                    xticklabel_quantisation=Decimal('1'),
                    linkage= StandardLinkages(linkage_rules=[
                                    LinkageRuleTag('ALL{PREPOP:RHS_mhrs,Conductance}', preferred_color='red'),
                                    LinkageRuleTag('ALL{PREPOP:RHS_tINs,Conductance}', preferred_color='green'),
                                    LinkageRuleTag('ALL{Voltage, RHS_dIN_10}', preferred_color='blue'),
                                                ])
                    )

    #t = TagViewer(
    #        [res, tINSpikeTimesRHS,first_spikes, all_spikes] + rasters,
    #        timerange=(200,300)*units.ms,
    #        show_xlabel=False,
    #        xticks=[200,250,300]*units.ms,
    #        plots=[TagPlot( "ALL{Raster}", ylabel='Spike\nraster',legend_labeller=None),],
    #        )


MFRandom.seed(1000)
testSingleSynapseAMPANMDA(i=0, stim_level=130,nmda_multiplier_feedback=1.5)






