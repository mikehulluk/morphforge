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

from morphforge.stdimports import CurrentClamp, Cell, qty, StandardTags
from morphforge.stdimports import NEURONEnvironment
#from morphforge.stdimports import factorise_units_from_list


import numpy as np
from mhlibs.quantities_plot import QuantitiesFigure

import itertools
from morphforge.traces.methods.MMtrace_conversion import TraceConverter
from morphforge.simulationanalysis.tagviewer.tagviewer import TagViewer
from mreorg import PM
from morphforge import units
import morphforge


class CellAnalysis_StepInputResponse(object):

    def __init__(
        self,
        cell_functor,
        currents,
        env,
        cell_description=None,
        plot_all=False,
        sim_kwargs=None,
        tagviewer_kwargs=None,
        include_internal_currents=True
        ):

        self.cell_functor = cell_functor
        self.currents = currents
        self.env = env
        self.sim_kwargs = sim_kwargs or {}
        self.tagviewer_kwargs = tagviewer_kwargs or {}
        self.include_internal_currents=include_internal_currents
        self.fig=None

        self.result_traces = {}

        self.cell_description = cell_description

        self.simulate_all()



        if plot_all:
            self.plot()

    def simulate_all(self):
        for c in self.currents:
            (tr_v, tr_i) = self.simulate(c)
            self.result_traces[c] = (tr_v, tr_i)

    def plot(self):
        #trs = list(itertools.chain(*self.result_traces.values()))
        trs = itertools.chain( *[v for (k,v) in sorted(self.result_traces.items()) ] )

        #title = '%s- Step Current Inject Responses' \
        #    % self.cell_description
        self.fig = TagViewer(
                    trs, 
                    show=False, 
                    #figtitle=title,
                    **self.tagviewer_kwargs
                    )

    def simulate(self, current):

        sim = self.env.Simulation(**self.sim_kwargs)
        cell = self.cell_functor(sim=sim)

        #soma_loc = cell.get_location('soma')

        cc = sim.create_currentclamp(name='cclamp%03d'%( int( current.rescale('pA') )) , amp=current,
                dur='80:ms', delay='50:ms', cell_location=cell.soma)


        if self.include_internal_currents:
            for chl in cell.biophysics.get_all_channels_applied_to_cell():
                sim.record(chl, what=StandardTags.CurrentDensity, cell_location=cell.soma)
                print 'chl',chl

        sim.record(cc, name='Current',
                   what=CurrentClamp.Recordables.Current,
                   description='CurrentClampCurrent')
        sim.record(cell, name='SomaVoltage', cell_location=cell.soma,
                   what=Cell.Recordables.MembraneVoltage,
                   description='Response to i_inj=%s ' % current)

        res = sim.run()

        return (res.get_trace('SomaVoltage'), res.get_trace('Current'))




class CellAnalysis_IFCurve(object):

    def __init__(
        self,
        cell_functor,
        currents,
        env,
        cell_description=None,
        plot_all=False,
        sim_kwargs=None,
        tagviewer_kwargs=None,
        include_internal_currents=True,
        inject_all_cells = False
        ):

        self.cell_functor = cell_functor
        self.currents = currents
        self.env = env
        self.sim_kwargs = sim_kwargs or {}
        self.tagviewer_kwargs = tagviewer_kwargs or {}
        self.include_internal_currents=include_internal_currents
        self.fig1=None
        self.fig2=None
        self.inject_all_cells = inject_all_cells

        self.result_traces = {}
        self.freqs = {}

        self.cell_description = cell_description

        self.simulate_all()



        if plot_all:
            self.plot()

    def simulate_all(self):
        for c in self.currents:
            (current,v, freq) = self.simulate(c)
            self.result_traces[c] = (current, v)
            self.freqs[float( c.rescale('pA') )]=freq

    def plot(self):
        trs = list(itertools.chain(*self.result_traces.values()))
        title = '%s- Step Current Inject Responses' \
            % self.cell_description
        self.fig1 = TagViewer(trs, show=False, figtitle=title,
                  **self.tagviewer_kwargs)

        import pylab
        self.fig2 = pylab.figure()
        ax = self.fig2.add_subplot(1,1,1)
        
        cur,freq = zip( *sorted(self.freqs.items() ) )
        ax.plot( cur,freq, 'x-')



    def simulate(self, current):

        sim = self.env.Simulation(**self.sim_kwargs)
        cell = self.cell_functor(sim=sim)

        #soma_loc = cell.get_location('soma')
        if self.inject_all_cells:
            for c in sim.cells:
                if c != cell:
                    sim.create_currentclamp(amp=current, dur='300:ms', delay='50:ms', cell_location=c.soma)

        cc = sim.create_currentclamp(name='cclamp', amp=current, dur='300:ms', delay='50:ms', cell_location=cell.soma)


        if self.include_internal_currents:
            for chl in cell.biophysics.get_all_channels_applied_to_cell():
                sim.record(chl, what=StandardTags.CurrentDensity, cell_location=cell.soma)
                #print 'chl',chl

        sim.record(cc, name='Current',
                   what=CurrentClamp.Recordables.Current,
                   description='CurrentClampCurrent')
        sim.record(cell, name='SomaVoltage', cell_location=cell.soma,
                   what=Cell.Recordables.MembraneVoltage,
                   description='Response to i_inj=%s ' % current)

        res = sim.run()


        v = res.get_trace('SomaVoltage')
        from morphforgecontrib.stdimports import SpikeFinder
        n_spikes = len( SpikeFinder.find_spikes(trace=v) )
        freq = n_spikes / 0.3


        current =  res.get_trace('Current')
        return (current,v, freq)











class CellAnalysis_ReboundResponse(object):

    def __init__(
        self,
        cell_functor,
        currents_base,
        currents_rebound,
        env,
        cell_description,
        plot_all=False,
        sim_kwargs=None,
        tagviewer_kwargs=None,
        ):
        self.cell_functor = cell_functor
        self.currents_base = currents_base
        self.currents_rebound = currents_rebound
        self.env = env
        self.sim_kwargs = sim_kwargs or {}
        self.tagviewer_kwargs = tagviewer_kwargs or {}
        self.result_traces = {}

        self.cell_description = cell_description
        self.plot_all = plot_all

        self.simulate_all()

        if plot_all:
            self.plot()

    def simulate_all(self):
        for current1 in self.currents_base:
            for current2 in self.currents_rebound:
                (tr_v, tr_i) = self.simulate(current1, current2)
                key = (int(current1.rescale('pA').magnitude), int(current2.rescale('pA').magnitude))
                self.result_traces[key] = (tr_v, tr_i)


    def plot(self):
        self.plot_traces()



    def plot_traces(self):
        c1_values = set([k[0] for k in self.result_traces])
        c2_values = set([k[1] for k in self.result_traces])

        # print self.result_traces.keys()
        for current1 in c1_values:
            trs = []
            for current2 in c2_values:
                if current2 > current1:
                    continue
                trs.extend(self.result_traces[(current1, current2)])

            title = "%s- (Response to Current Injections [BaseCurrent %s pA])"%(self.cell_description, current1)
            TagViewer(trs, show=False, figtitle=title, **self.tagviewer_kwargs)





    def simulate(self, current_base, current_rebound):

        sim = self.env.Simulation(**self.sim_kwargs)
        cell = self.cell_functor(sim=sim)

        soma_loc = cell.get_location('soma')

        cc1 = sim.create_currentclamp(name="cclamp", amp=current_base, dur="100:ms", delay="50:ms", cell_location=soma_loc)
        cc2 = sim.create_currentclamp(name="cclamp2", amp=-1*current_rebound, dur="5:ms", delay="80:ms", cell_location=soma_loc)
        cc3 = sim.create_currentclamp(name="cclamp3", amp=-1*current_rebound, dur="5:ms", delay="120:ms", cell_location=soma_loc)

        sim.record(cc1, name="Current1",      what=CurrentClamp.Recordables.Current,  description="CurrentClampCurrent")
        sim.record(cc2, name="Current2",      what=CurrentClamp.Recordables.Current,  description="CurrentClampCurrent")
        sim.record(cc3, name="Current3",      what=CurrentClamp.Recordables.Current,  description="CurrentClampCurrent")

        sim.record(cell, name="SomaVoltage", cell_location=soma_loc,  what=Cell.Recordables.MembraneVoltage,  description="Response to iInj1=%s iInj2=%s"%(current_base, current_rebound))

        res = sim.run()


        #SimulationSummariser(res, "/home/michael/Desktop/ForRoman.pdf")

        i = res.get_trace('Current1').convert_to_fixed(qty("0.5:ms")) + res.get_trace('Current2').convert_to_fixed(qty("0.5:ms")) + res.get_trace('Current3').convert_to_fixed(qty("0.5:ms"))

        i = TraceConverter.rebase_to_fixed_dt(res.get_trace('Current1'
               ), dt=qty('0.5:ms')) \
            + TraceConverter.rebase_to_fixed_dt(res.get_trace('Current2'
               ), dt=qty('0.5:ms')) \
            + TraceConverter.rebase_to_fixed_dt(res.get_trace('Current3'
               ), dt=qty('0.5:ms'))
        i.tags = [StandardTags.Current]
        return (res.get_trace('SomaVoltage'), i)











class CellAnalysis_IVCurve(object):


    def __init__(self, cell_functor, currents, cell_description=None, sim_functor=None, v_regressor_limit=None, sim_kwargs=None, plot_all=False):
        self.cell_functor = cell_functor
        self.v_regressor_limit = v_regressor_limit
        self.fig=None
        #Previously = qty("-30:mV")

        self.sim_kwargs = sim_kwargs or {}

        self.tCurrentInjStart = qty('50:ms')
        self.tCurrentInjStop = qty('200:ms')

        self.tSteaddyStateStart = qty('100:ms')
        self.tSteaddyStateStop = qty('151:ms')

        self.traces = {}

        self.currents = currents
        self.cell_description = cell_description or 'Unknown Cell'

        self.input_resistance = qty('-1:MOhm')

        if plot_all:
            self.plot_all()

    def plot_all(self):
        self.plot_traces()
        self.plot_iv_curve()

    def _get_cc_simulation_trace(self, current):

        if self.cell_functor:
            env = NEURONEnvironment()
            sim = env.Simulation(**self.sim_kwargs)
            cell = self.cell_functor(sim=sim)
        else:
            assert False

        soma_loc = cell.get_location('soma')

        cc = sim.create_currentclamp(name='cclamp', amp=current,
                dur=self.tCurrentInjStop - self.tCurrentInjStart,
                delay=self.tCurrentInjStart, cell_location=soma_loc)
        sim.record(cell, name='SomaVoltage', cell_location=soma_loc,
                   what=Cell.Recordables.MembraneVoltage,
                   description='Response to i_inj=%s ' % current)

        res = sim.run()

        return res.get_trace('SomaVoltage')

    def get_trace(self, i_inj):
        if not i_inj in self.traces:
            self.traces[i_inj] = self._get_cc_simulation_trace(i_inj)
        return self.traces[i_inj]

    def get_iv_point_steaddy_state(self, i_inj):
        return self.get_trace(i_inj).window(time_window=(self.tSteaddyStateStart, self.tSteaddyStateStop)).Mean()


    def plot_traces(self, ax=None):
        title = '%s: (Voltage Responses to Current Injections)' \
            % self.cell_description
        if not ax:
            self.fig = QuantitiesFigure()
            self.fig.suptitle(title)
            ax = self.fig.add_subplot(1, 1, 1)
            ax.set_xlabel('Time')
            ax.set_ylabel('Voltage')

        # Plot the traces
        for i_inj in self.currents:
            ax.plotTrace(self.get_trace(i_inj), label='i_inj: %s'
                         % i_inj)

        # Add the regions:
        ax.axvspan(self.tSteaddyStateStart, self.tSteaddyStateStop, facecolor='g', alpha=0.25)
        ax.legend()

        from mreorg.scriptplots import PM
        PM.save_figure(figname=title)

    def plot_iv_curve(self, ax=None):
        # pylint: disable=E1103
        title = '%s: IV Curve' % (self.cell_description or None)
        if not ax:
            f = QuantitiesFigure()
            f.suptitle(title)
            ax = f.add_subplot(1, 1, 1)
            ax.set_xlabel('Injected Current')
            ax.set_ylabel('SteadyStateVoltage')

        V_in_mV = [self.get_iv_point_steaddy_state(c).rescale('mV').magnitude for c in self.currents]
        v = np.array(V_in_mV) * units.mV
        i = morphforge.units.factorise_units_from_list(self.currents)

        low_v = V_in_mV < self.v_regressor_limit if self.v_regressor_limit else range( len(V_in_mV))



        print 'i[low_v]', i[low_v]
        print 'v[low_v]', v[low_v]
        ax.plot(i[low_v], v[low_v], )
        ax.plot(i[np.logical_not(low_v)], v[np.logical_not(low_v)], )
        ax.plot(i[np.logical_not(low_v)], v[np.logical_not(low_v)], )

        # Plot the regressor:
        i_units = qty('1:pA').units
        v_units = qty('1:mV').units
        iv = np.vstack((i.rescale(i_units).magnitude,
                       v.rescale(v_units).magnitude)).T

        if not len(iv[low_v, 0]):
            return
        import scipy.stats as stats
        (a_s, b_s, r, tt, stderr) = stats.linregress(iv[low_v, 0], iv[low_v, 1])
        input_resistance = (a_s * (v_units / i_units)).rescale('MOhm')
        reversal_potential = b_s * v_units

        self.input_resistance = input_resistance
        self.reversal_potential = reversal_potential

        ax.plot(i, i*input_resistance + reversal_potential,'o-', label = "Fit: [V(mV) = %2.3f * I(pA)  + %2.3f]"%(a_s, b_s) + " \n[Input Resistance: %2.2fMOhm  Reversal Potential: %2.2f mV"%(input_resistance, reversal_potential)  )
        ax.legend()

        PM.save_figure(figname=title)


