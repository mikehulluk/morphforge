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
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import *
import itertools
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import *
from reportlab.lib import colors
import os
from reportlab.lib.pagesizes import A4

#from ..stdlimits import StdLimits
from mhlibs.quantities_plot import QuantitiesFigure
from mhlibs.quantities_plot import QuantitiesAxis
#from util import InfTauInterpolatedCalculator
#from util import InfTauCalculator
#from util import ReportLabTools

from morphforge.core.quantities import unit

from scipy.integrate import odeint
import numpy as np
from morphforge.traces import Trace_FixedDT
#import sympy
from morphforge.simulationanalysis.summaries.summariser_library import SummariserLibrary
#from morphforgecontrib.default.core.mmalphabetabeta import MM_InfTauInterpolatedBetaChannel
from core  import MM_InfTauInterpolatedChannel
from morphforge.simulationanalysis.summaries.stdlimits import StdLimits

from morphforge.stdimports import pq

#
#class Summarise_MM_InfTauInterpolatedChannelVClamp(object):
#
#    @classmethod
#    def getVoltageClampTrace(cls, V, chl, duration, cellArea, t=np.arange(0,300,0.1) * unit("1:ms"), ) :
#        
#        vInMv = V.rescale("mV").magnitude
#        
#        stateNames = chl.statevars.keys()
#        nStates = len(stateNames)
#        m_inf, m_tau =  InfTauCalculator.evaluateInfTauForV( chl.statevars[stateNames[0]], V)
#        m_tauMS = m_tau.rescale("ms").magnitude
#        
#        infTaus = [ InfTauCalculator.evaluateInfTauForV( chl.statevars[stateName], V)  for stateName in stateNames ]
#        infTausMS = [ (inf, tau.rescale("ms").magnitude)  for (inf,tau) in infTaus ]
#        
#        stateToIndex = dict( [ (state,index) for state,index in enumerate(stateNames) ] ) 
#        
#        def odeFunc(y,t0):
#            res = [None] * nStates
#            for i in range(0,nStates):
#                stateInf,stateTau = infTausMS[i]
#                stateVal = y[i]
#                dState = ( stateInf - stateVal ) / stateTau
#                res[i] = dState
#            return res
#        
#        # Run the ODE for each variable:            
#        t = t.rescale("ms").magnitude
#        y0 = np.zeros( (nStates, ) )
#        res = odeint(func=odeFunc, y0=y0, t= t  )
#        
#        stateFunctor = sympy.lambdify( stateNames, sympy.sympify(chl.eqn)  )
#        stateData = [ res[:,i] for i in range(0,nStates) ]
#        
#        stateEquationEvaluation = stateFunctor( *stateData )
#        
#        cellDensity = (chl.conductance * cellArea)
#        iChl =  (chl.conductance * cellArea)  * stateEquationEvaluation * (V- chl.reversalpotential) 
#        
#        return Trace_FixedDT( time=t * unit("1:ms"), data=iChl.rescale("pA")  )








class Summarise_MM_InfTauInterpolatedChannel(object):
    
    
    
        
        
        #@classmethod
        #def getResolvedInfTauInterpolatedCurves(cls, V, chl, state ):
        #    return InfTauInterpolatedCalculator.getInfTauInterpolated(V, chl.statevars[state][0], chl.statevars[state][1]   )


        @classmethod
        def PlotAlphaBetaCurves(cls, ax1,ax2, alphaBetaChannel, state, color="blue"):
            chl = alphaBetaChannel
            
            
            
            
            infV =  np.array( alphaBetaChannel.statevars_new[state].V )
            inf =   np.array( alphaBetaChannel.statevars_new[state].inf ) 
            tau =   np.array( alphaBetaChannel.statevars_new[state].tau )
                
            #tauV =  np.array( zip(*alphaBetaChannel.statevars[state]['tau'])[0] )
            #tau =   np.array( zip(*alphaBetaChannel.statevars[state]['tau'])[1] ) 
            
            # Check the two voltage arrays are the same:
            #assert np.max( (infV-tauV)**2 ) < 1.0
            
            alpha = inf/tau
            beta = (1 - alpha*tau) / tau
            
            
            if isinstance(ax1, QuantitiesAxis):
                               
                ax1.setYUnit("")
                ax1.plot(infV * pq.mV, alpha * pq.s/pq.s,color=color)
                ax1.set_xlabel("Voltage")
                ax1.set_ylabel("Alpha")
                
                ax2.plot(infV * pq.mV, beta * pq.s/pq.s, color=color)
                ax2.set_xlabel("Voltage")
                ax2.set_ylabel("Beta")
                ax2.setYUnit("")
                
            else:
                
                ax1.plot(infV,alpha,color=color)
                ax1.set_xlabel("Voltage (mV)")
                ax1.set_ylabel("Alpha")
                
                ax2.plot(infV, beta,color=color)
                ax2.set_xlabel("Voltage (mV)")
                ax2.set_ylabel("Beta")
            
            
            
            
            
            return 
        
            V = StdLimits.get_defaultVoltageArray().rescale("mV")
            
            alpha,beta = cls.getResolvedInfTauInterpolatedCurves(V, chl, state)
            
            
            ax1.plot(V,alpha, color="blue")
            ax1.set_xlabel("Voltage")
            ax1.set_ylabel("Alpha")
            
            ax2.plot(V,beta, color="blue")
            ax2.set_xlabel("Voltage")
            ax2.set_ylabel("Beta")
            
            
        @classmethod 
        def PlotInfTauCurves(cls, ax1,ax2,alphaBetaChannel, state, color="blue" ):
            
            if isinstance(ax1, QuantitiesAxis):
                
#                print alphaBetaChannel.statevars[state]['inf']
                infV =  np.array( alphaBetaChannel.statevars_new[state].V )
                inf =   np.array( alphaBetaChannel.statevars_new[state].inf ) 
                tau =   np.array( alphaBetaChannel.statevars_new[state].tau )
            
                #infV =  np.array( zip(*alphaBetaChannel.statevars[state]['inf'])[0] )
                #inf =   np.array( zip(*alphaBetaChannel.statevars[state]['inf'])[1] ) 
                
                #tauV =  np.array( zip(*alphaBetaChannel.statevars[state]['tau'])[0] )
                #tau =   np.array( zip(*alphaBetaChannel.statevars[state]['tau'])[1] ) 
                

                
                ax1.setYUnit("")
                ax1.plot(infV * pq.mV, inf * pq.s/pq.s,color=color)
                ax1.set_xlabel("Voltage")
                ax1.set_ylabel("Inf")
                
                ax2.plot(tauV * pq.mV, tau* pq.ms, color=color)
                ax2.set_xlabel("Voltage")
                ax2.set_ylabel("Tau")
                ax2.setYUnit("ms")
                
            else:
                
                ax1.plot(infV,inf,color=color)
                ax1.set_xlabel("Voltage (mV)")
                ax1.set_ylabel("Infs")
                
                ax2.plot(infV,tau,color=color)
                ax2.set_xlabel("Voltage (mV)")
                ax2.set_ylabel("Tau (ms)")

                
            
        @classmethod
        def PlotStateCurveSummary(cls,  alphaBetaChl, state, figsize):
            fig = QuantitiesFigure(figsize=figsize)
            fig.suptitle("InfTauInterpolated Channel - %s : %s"%(alphaBetaChl.name, state))
            ax1 = fig.add_subplot(221)
            ax2 = fig.add_subplot(222)
            cls.PlotInfTauCurves(ax1, ax2, alphaBetaChl,state )
            
            ax3 = fig.add_subplot(223)
            ax4 = fig.add_subplot(224)
            cls.PlotAlphaBetaCurves(ax3, ax4, alphaBetaChl,state )
            return fig
            
        @classmethod
        def toScreen(cls, alphaBetaChannel, state):
            
            cls.PlotStateCurveSummary(alphaBetaChannel, state, figsize=(5,5))
            
            
            
            


        @classmethod
        def toReportLab(cls, alphaBetaChl, reportlabconfig, make_graphs):
            localElements = []
            localElements.append( Paragraph("Overview",reportlabconfig.styles['Heading3']) )
            
            # Summary:
            overviewTableData = [
                                 ["Max Conductance (gBar)", alphaBetaChl.conductance.rescale("mS/cm2") ],
                                 ["Reversal Potential", alphaBetaChl.reversalpotential.rescale("mV") ],
                                 ["Conductance Equation", "gBar * " + alphaBetaChl.eqn ],
                                ]
            
            localElements.append( Table(overviewTableData, style=reportlabconfig.listTableStyle) )
            
            
            #return localElements
            
            # Plot out the States:
            for state,params in alphaBetaChl.statevars_new.iteritems():
                localElements.append( Paragraph("State: %s"%state,reportlabconfig.styles['Heading3']) )

                # Interpolated_values:
                infTable  = [
                                 ["Voltage", 'Inf'],
                            ] + [ ("%2.2f"%p0,"%2.2f"%p1) for (p0,p1) in zip(params.V,params.inf) ]
                
                tauTable  = [
                                 ["Voltage", 'Tau'],
                            ] + [ ("%2.2f"%p0,"%2.2f"%p1) for (p0,p1) in zip(params.V,params.tau) ]
                            
                #mergeTable = zip( infTable,tauTable )
                
            
                localElements.append( Table(infTable, style=reportlabconfig.listTableStyle) )
                localElements.append( Table(tauTable, style=reportlabconfig.listTableStyle) )
                #localElements.append( Table(mergeTable, style=reportlabconfig.listTableStyle) )
                
                
                #continue
                
                ##Equations:
                #eqns = [
                #        "alpha(V) = (A+BV)/(C+exp( (V+D)/E) )",
                #        "beta(V) = (A+BV)/(C+exp( (V+D)/E) )",
                #        ]
                #for eqn in eqns:
                #    localElements.append( Paragraph(eqn,reportlabconfig.styles['Normal']) )  
                # Alpha Beta
                #ReportLabTools.buildInfTauInterpolatedTable( elements=localElements, 
                #                         reportlabconfig=reportlabconfig, 
                #                         title="Alpha", params=params[0] )   
                #ReportLabTools.buildInfTauInterpolatedTable( elements=localElements, 
                #                         reportlabconfig=reportlabconfig, 
                #                         title="Beta1", params=params[1] )
                
                
                # Figures:
                if make_graphs:
                    fig = cls.PlotStateCurveSummary(alphaBetaChl, state, figsize=(7,7))
                    localElements.append( reportlabconfig.save_mpl_to_rl_image(fig, "somestate") )
                    fig.close()

                
            
            
            return localElements



SummariserLibrary.register_summariser(channelBaseClass=MM_InfTauInterpolatedChannel, summariserClass=Summarise_MM_InfTauInterpolatedChannel)
