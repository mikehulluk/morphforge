#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------
from morphforge.stdimports import *



import scipy.stats as stats

import numpy as np
#import pylab
from mhlibs.quantities_plot import QuantitiesFigure
#from mhlibs.quantities_plot.quantities_plot_new import QuantitiesFigureNew


import itertools
from morphforge.traces.std_methods.MMtrace_conversion import TraceConverter
from mreorg.scriptplots import PM
from morphforge.traces.tagviewer.tagviewer import TagViewer




class CellAnalysis_StepInputResponse(object):
    def __init__(self, cell_functor, currents, env, cell_description, plot_all=False, sim_kwargs=None,tagviewer_kwargs=None ):
        self.cell_functor = cell_functor
        self.currents = currents
        self.env = env
        self.sim_kwargs = sim_kwargs or {}
        self.tagviewer_kwargs = tagviewer_kwargs or {}

        self.result_traces = {}

        self.cell_description = cell_description

        self.simulate_all()

        if plot_all:
            self.plot()


    def simulate_all(self):
        for c in self.currents:
            trV,trI = self.simulate(c)
            self.result_traces[c] = trV,trI

    def plot(self,):
        trs = list( itertools.chain( *self.result_traces.values() ) )

        title = '%s- Step Current Inject Responses'%(self.cell_description)
        TagViewer( trs, show=False, figtitle= title,**self.tagviewer_kwargs  )




    def simulate(self, current):


        sim = self.env.Simulation(**self.sim_kwargs)
        cell = self.cell_functor(sim=sim)

        somaLoc = cell.get_location("soma")

        cc = sim.create_currentclamp( name="cclamp", amp=current, dur="80:ms", delay="50:ms", celllocation=somaLoc)

        sim.record( cc, name="Current",      what=CurrentClamp.Recordables.Current,  description="CurrentClampCurrent")
        sim.record( cell, name="SomaVoltage", location=somaLoc,  what=Cell.Recordables.MembraneVoltage,  description="Response to iInj=%s "%current )

        res = sim.run()


        return res.get_trace('SomaVoltage'), res.get_trace('Current')













class CellAnalysis_ReboundResponse(object):
    def __init__(self, cell_functor, currents_base,currents_rebound, env, cell_description, plot_all=False, sim_kwargs=None,tagviewer_kwargs=None):
        self.cell_functor = cell_functor
        self.currents_base = currents_base
        self.currents_rebound = currents_rebound
        self.env = env
        self.sim_kwargs = sim_kwargs or {}
        self.tagviewer_kwargs = tagviewer_kwargs or {}
        self.result_traces = {}

        self.cell_description=cell_description
        self.plot_all=plot_all

        self.simulate_all()

        if plot_all:
            self.plot()


    def simulate_all(self):
        for c1 in self.currents_base:
            for c2 in self.currents_rebound:
                trV,trI = self.simulate(c1,c2)
                self.result_traces[( int(c1.rescale('pA').magnitude),int(c2.rescale('pA').magnitude))] = trV,trI




    def plot(self):
        self.plot_traces()



    #def plot_rebound_graphs(self):
    #    c1Values = set( [k[0] for k in self.result_traces ])
    #    c2Values = set( [k[1] for k in self.result_traces ])
    #
    #    f = pylab.figure()
    #    ax = f.add_subplot(1,1,1)
    #
    #    tested_pts = []
    #    spiking_pts = []
    #    rebound_pts = []
    #
    #    for c1 in c1Values:
    #        for c2 in c2Values:
    #            self.result_traces[(c1,c2)]
    #
    #            # Plot a dot to show that the simulation was run:
    #            ax.plot(c1,c2, 'o', markersize=10, color='black')
    #            #tr =
    #
                #            trs = []



    def plot_traces(self,):
        c1Values = set( [k[0] for k in self.result_traces ])
        c2Values = set( [k[1] for k in self.result_traces ])

        #print self.result_traces.keys()
        for c1 in c1Values:
            trs = []
            for c2 in c2Values:
                if c2>c1:
                    continue
                trs.extend( self.result_traces[(c1,c2)] )

            title = "%s- (Response to Current Injections [BaseCurrent %s pA ] )"%(self.cell_description, c1)
            TagViewer( trs, show=False, figtitle=title, **self.tagviewer_kwargs )





    def simulate(self, current_base, current_rebound):


        sim = self.env.Simulation(**self.sim_kwargs)
        cell = self.cell_functor(sim=sim)

        somaLoc = cell.get_location("soma")

        cc1 = sim.create_currentclamp( name="cclamp", amp=current_base, dur="100:ms", delay="50:ms", celllocation=somaLoc)
        cc2 = sim.create_currentclamp( name="cclamp2", amp=-1*current_rebound, dur="5:ms", delay="80:ms", celllocation=somaLoc)
        cc3 = sim.create_currentclamp( name="cclamp3", amp=-1*current_rebound, dur="5:ms", delay="120:ms", celllocation=somaLoc)

        sim.record( cc1, name="Current1",      what=CurrentClamp.Recordables.Current,  description="CurrentClampCurrent")
        sim.record( cc2, name="Current2",      what=CurrentClamp.Recordables.Current,  description="CurrentClampCurrent")
        sim.record( cc3, name="Current3",      what=CurrentClamp.Recordables.Current,  description="CurrentClampCurrent")

        sim.record( cell, name="SomaVoltage", location=somaLoc,  what=Cell.Recordables.MembraneVoltage,  description="Response to iInj1=%s iInj2=%s"%(current_base,current_rebound) )

        res = sim.run()

        #from morphforge.simulationanalysis.summaries.simsummariser import SimulationSummariser
        #SimulationSummariser(res, "/home/michael/Desktop/ForRoman.pdf")

        i = res.get_trace('Current1').convert_to_fixed( unit("0.5:ms") ) + res.get_trace('Current2').convert_to_fixed( unit("0.5:ms") ) + res.get_trace('Current3').convert_to_fixed( unit("0.5:ms") )

        i = TraceConverter.rebase_to_fixed_dt(res.get_trace('Current1'), dt = unit("0.5:ms") ) + TraceConverter.rebase_to_fixed_dt(res.get_trace('Current2'), dt = unit("0.5:ms") ) + TraceConverter.rebase_to_fixed_dt(res.get_trace('Current3'), dt = unit("0.5:ms") )
        i.tags=[StandardTags.Current]
        return res.get_trace('SomaVoltage'), i











class CellAnalysis_IVCurve(object):


    def __init__(self, cell_functor, currents, cell_description=None, v_regressor_limit= unit("-30:mV"), sim_kwargs=None, plot_all=False ):
        self.cell_functor = cell_functor
        self.v_regressor_limit = v_regressor_limit

        self.sim_kwargs = sim_kwargs or {}

        self.tCurrentInjStart = unit('50:ms')
        self.tCurrentInjStop = unit('200:ms')

        self.tSteaddyStateStart = unit( '100:ms' )
        self.tSteaddyStateStop = unit( '151:ms' )

        self.traces = {}

        self.currents = currents
        self.cell_description = cell_description or 'Unknown Cell'

        self.input_resistance=unit("-1:MOhm")

        if plot_all:
            self.plotAll()

    def plotAll(self):
        self.plot_traces()
        self.plot_iv_curve()



    def _get_cc_simulation_trace( self, current,   ):

        if self.cell_functor:
            env = NeuronSimulationEnvironment()
            sim = env.Simulation(**self.sim_kwargs)
            cell = self.cell_functor(sim=sim)

        else:
            assert False
            sim = self.sim
            cell = self.cell

        somaLoc = cell.get_location("soma")

        cc = sim.create_currentclamp( name="cclamp", amp=current, dur=self.tCurrentInjStop-self.tCurrentInjStart, delay=self.tCurrentInjStart, celllocation=somaLoc)
        sim.record( cell, name="SomaVoltage", location=somaLoc,  what=Cell.Recordables.MembraneVoltage,  description="Response to iInj=%s "%current )

        res = sim.run()

        return res.get_trace('SomaVoltage')



    def get_trace(self, iInj):
        if not iInj in self.traces:
            self.traces[iInj] = self._get_cc_simulation_trace(iInj)
        return self.traces[iInj]


    def get_iv_point_steaddy_state(self, iInj):
        return  self.get_trace(iInj).window( time_window=(self.tSteaddyStateStart, self.tSteaddyStateStop )).Mean()



    def plotAll(self):
        self.plot_traces()
        self.plot_iv_curve()



    def plot_traces(self, ax=None):
        title = "%s: (Voltage Responses to Current Injections)"%(self.cell_description)
        if not ax:
            f = QuantitiesFigure()
            f.suptitle( title )
            ax = f.add_subplot(1,1,1)
            ax.set_xlabel('Time')
            ax.set_ylabel('Voltage')

        # Plot the traces
        for iInj in self.currents:
            ax.plotTrace( self.get_trace(iInj), label='iInj: %s'%iInj)

        # Add the regions:
        ax.axvspan(self.tSteaddyStateStart, self.tSteaddyStateStop, facecolor='g', alpha=0.25)
        ax.legend()

        PM.save_figure(figname= title)


    def plot_iv_curve(self, ax=None):
        title = "%s: IV Curve"%(self.cell_description)
        if not ax:
            f = QuantitiesFigure()
            f.suptitle(title )
            ax = f.add_subplot( 1,1,1)
            ax.set_xlabel('Injected Current')
            ax.set_ylabel('SteadyStateVoltage')


        V = [self.get_iv_point_steaddy_state(c) for c in self.currents ]
        i = factorise_units_from_list(self.currents)
        v = factorise_units_from_list(V)


        lowV = v<self.v_regressor_limit

        ax.plot( i[lowV], v[lowV], 'ro' )
        ax.plot( i[np.logical_not(lowV)], v[np.logical_not(lowV)], 'rx' )
        ax.plot( i[np.logical_not(lowV)], v[np.logical_not(lowV)], 'rx' )


        # Plot the regressor:
        iUnits = unit('1:pA').units
        vUnits = unit('1:mV').units
        iv = np.vstack(   (i.rescale(iUnits).magnitude, v.rescale(vUnits).magnitude) ).T

        if not len(iv[lowV,0]):
            return
        (a_s,b_s,r,tt,stderr)=stats.linregress( iv[lowV,0], iv[lowV,1])
        input_resistance = (a_s * (vUnits/iUnits ) ).rescale('MOhm')
        reversal_potential = b_s * vUnits

        #print ' Input Resistance = ', input_resistance
        #print ' Reversal Potential = ', reversal_potential

        self.input_resistance =input_resistance
        self.reversal_potential =reversal_potential

        ax.plot( i, i*input_resistance + reversal_potential, label = "Fit: [V(mV) = %2.3f * I(pA)  + %2.3f]"%(a_s,b_s) + " \n[Input Resistance: %2.2fMOhm  Reversal Potential: %2.2f mV"%(input_resistance, reversal_potential)   )
        ax.legend()

        PM.save_figure(figname= title)


