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


import numpy as np

from mhlibs.quantities_plot import QuantitiesFigure
from mhlibs.quantities_plot.quantities_plot_new import QuantitiesAxisNew

from util import InfTauCalculator
from util import ReportLabTools

from morphforge.core.quantities import unit

from morphforge.traces import Trace_FixedDT

from morphforge.simulationanalysis.summaries.summariser_library import SummariserLibrary
from morphforge.simulationanalysis.summaries.stdlimits import StdLimits
from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmalphabeta import MM_AlphaBetaChannel




class Summarise_MM_AlphaBetaChannelVClamp(object):

    @classmethod
    def getVoltageClampTrace(cls, V, chl, duration, cellArea, t=np.arange(0,300,0.1) * unit("1:ms"), ) :
        
        from scipy.integrate import odeint
        
        vInMv = V.rescale("mV").magnitude
        
        stateNames = chl.statevars.keys()
        nStates = len(stateNames)
        m_inf, m_tau =  InfTauCalculator.evaluateInfTauForV( chl.statevars[stateNames[0]], V)
        m_tauMS = m_tau.rescale("ms").magnitude
        
        infTaus = [ InfTauCalculator.evaluateInfTauForV( chl.statevars[stateName], V)  for stateName in stateNames ]
        infTausMS = [ (inf, tau.rescale("ms").magnitude)  for (inf,tau) in infTaus ]
        
        stateToIndex = dict( [ (state,index) for state,index in enumerate(stateNames) ] ) 
        
        def odeFunc(y,t0):
            res = [None] * nStates
            for i in range(0,nStates):
                stateInf,stateTau = infTausMS[i]
                stateVal = y[i]
                dState = ( stateInf - stateVal ) / stateTau
                res[i] = dState
            return res
        
        # Run the ODE for each variable:            
        t = t.rescale("ms").magnitude
        y0 = np.zeros( (nStates, ) )
        res = odeint(func=odeFunc, y0=y0, t= t  )
        
        stateFunctor = sympy.lambdify( stateNames, sympy.sympify(chl.eqn)  )
        stateData = [ res[:,i] for i in range(0,nStates) ]
        
        stateEquationEvaluation = stateFunctor( *stateData )
        
        cellDensity = (chl.conductance * cellArea)
        iChl =  (chl.conductance * cellArea)  * stateEquationEvaluation * (V- chl.reversalpotential) 
        
        return Trace_FixedDT( time=t * unit("1:ms"), data=iChl.rescale("pA")  )






class Curve(object):
    Alpha = "Alpha"
    Beta = "Beta"
    Inf = "Inf"
    InfPowered = "InfPowered"
    Tau = "Tau"


class Summarise_MM_AlphaBetaChannel(object):
    
        @classmethod
        def PlotCurve(cls, ax, curve, chl, state, infpower=None, *args, **kwargs):
            
            V = StdLimits.getDefaultVoltageArray().rescale("mV")
            
            alpha,beta = chl.getAlphaBetaAtVoltage(V, state)
            inf,tau = InfTauCalculator.AlphaBetaToInfTau(alpha,beta)
            infpower = np.power(inf, infpower) if infpower else None
            plot_what_LUT = { 
                         Curve.Alpha :     ( alpha,    "Rate Constant", None ), 
                         Curve.Beta :      ( beta,     "Rate Constant", None ),
                         Curve.Inf :       ( inf,      "Steady-State",  None ),
                         Curve.InfPowered :( infpower, "Steady-State",  None ),
                         Curve.Tau :       ( tau,      "Time-Constant", "ms" ),
                         }
            plot_what, y_label, y_unit = plot_what_LUT[curve]
            
            #print kwargs
            
            if isinstance(ax, QuantitiesAxisNew):
                
                ax.plot(V,plot_what, *args,**kwargs)
                ax.set_xlabel("Voltage")
                ax.set_ylabel(y_label)
                
                if y_unit:
                    ax.set_yunit( unit(y_unit) )
                
            else:
                ax.plot(V,plot_what, *args,**kwargs)
                ax.set_xlabel("Voltage (mV)")
                ax.set_ylabel(y_label)
            
            
            
            
            
        @classmethod
        def PlotAlphaBetaCurves(cls, ax1,ax2, alphaBetaChannel, state, *args,**kwargs):
            cls.PlotCurve( ax=ax1, curve=Curve.Alpha, chl=alphaBetaChannel, state=state, *args, **kwargs)
            cls.PlotCurve( ax=ax2, curve=Curve.Beta, chl=alphaBetaChannel, state=state, *args, **kwargs)
            
            
        @classmethod 
        def PlotInfTauCurves(cls, ax1,ax2,alphaBetaChannel, state,  *args,**kwargs ):
            cls.PlotCurve( ax=ax1, curve=Curve.Inf, chl=alphaBetaChannel, state=state, *args, **kwargs)
            cls.PlotCurve( ax=ax2, curve=Curve.Tau, chl=alphaBetaChannel, state=state, *args, **kwargs)
            
        @classmethod 
        def PlotSteddyStateCurve(cls, ax1,alphaBetaChannel, state, power,  *args,**kwargs ):
            cls.PlotCurve( ax=ax1, curve=Curve.InfPowered, chl=alphaBetaChannel, state=state, infpower=power, *args, **kwargs)
                
            
        @classmethod
        def PlotStateCurveSummary(cls,  alphaBetaChl, state, figsize):
            fig = QuantitiesFigure(figsize=figsize)
            fig.suptitle("AlphaBeta Channel - %s : %s"%(alphaBetaChl.name, state))
            ax1 = fig.add_subplot(221)
            ax2 = fig.add_subplot(222)
            cls.PlotAlphaBetaCurves(ax1, ax2, alphaBetaChl,state )
            
            ax3 = fig.add_subplot(223)
            ax4 = fig.add_subplot(224)
            cls.PlotInfTauCurves(ax3, ax4, alphaBetaChl,state )
            return fig
            
            
            
            
            
            
        @classmethod
        def toScreen(cls, alphaBetaChannel, state):
            cls.PlotStateCurveSummary(alphaBetaChannel, state, figsize=(5,5))
            
            
            

        @classmethod
        def toReportLab(cls, alphaBetaChl, reportlabconfig, make_graphs):
            from reportlab.platypus import Paragraph, Table
            localElements = []
            localElements.append( Paragraph("Overview",reportlabconfig.styles['Heading3']) )
            
            # Summary:
            overviewTableData = [
                                 ["Max Conductance (gBar)", alphaBetaChl.conductance.rescale("mS/cm2") ],
                                 ["Reversal Potential", alphaBetaChl.reversalpotential.rescale("mV") ],
                                 ["Conductance Equation", "gBar * " + alphaBetaChl.eqn ],
                                ]
            
            localElements.append( Table(overviewTableData, style=reportlabconfig.listTableStyle) )
            
            
            # Plot out the States:
            for state,params in alphaBetaChl.statevars.iteritems():
                localElements.append( Paragraph("State: %s"%state,reportlabconfig.styles['Heading3']) )

            
                #Equations:
                eqns = [
                        "alpha(V) = (A+BV)/(C+exp( (V+D)/E) )",
                        "beta(V) = (A+BV)/(C+exp( (V+D)/E) )",
                        ]
                for eqn in eqns:
                    localElements.append( Paragraph(eqn,reportlabconfig.styles['Normal']) )  
                # Alpha Beta
                ReportLabTools.buildAlphaBetaTable( elements=localElements, 
                                         reportlabconfig=reportlabconfig, 
                                         title="Alpha", params=params[0] )   
                ReportLabTools.buildAlphaBetaTable( elements=localElements, 
                                         reportlabconfig=reportlabconfig, 
                                         title="Beta1", params=params[1] )
                
                
                if make_graphs:
                    # Figures:
                    fig = cls.PlotStateCurveSummary(alphaBetaChl, state, figsize=(5,5))
                    localElements.append( reportlabconfig.saveMPLToRLImage(fig, "somestate") )
                    import pylab
                    pylab.close( fig.fig )

            
            return localElements



SummariserLibrary.registerSummariser(channelBaseClass=MM_AlphaBetaChannel, summariserClass=Summarise_MM_AlphaBetaChannel)
