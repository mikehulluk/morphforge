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









from util import InfTauCalculator
from util import ReportLabTools

from morphforge.core.quantities import unit

import numpy as np
from morphforge.traces import TraceFixedDT
from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmalphabetabeta import MM_AlphaBetaBetaChannel
from morphforge.simulationanalysis.summaries.summariser_library import SummariserLibrary
from morphforgecontrib.simulation.membranemechanisms.hh_style.summarisers.mmalphabeta import Summarise_MM_AlphaBetaChannel




class Summarise_MM_AlphaBetaChannelVClamp(object):

    @classmethod
    def get_voltage_clamp_trace(cls, V, chl, duration, cell_area, t=np.arange(0,300,0.1) * unit("1:ms"), ) :
        from scipy.integrate import odeint
        import sympy

        v_in_mv = V.rescale("mV").magnitude

        state_names = chl.statevars.keys()
        n_states = len(state_names)
        m_inf, m_tau =  InfTauCalculator.evaluate_inf_tau_for_v( chl.statevars[state_names[0]], V)
        m_tau_ms = m_tau.rescale("ms").magnitude

        inf_taus = [ InfTauCalculator.evaluate_inf_tau_for_v( chl.statevars[stateName], V)  for stateName in state_names ]
        inf_taus_ms = [ (inf, tau.rescale("ms").magnitude)  for (inf,tau) in inf_taus ]

        state_to_index = dict( [ (state,index) for state,index in enumerate(state_names) ] )

        def odeFunc(y,t0):
            res = [None] * n_states
            for i in range(0,n_states):
                state_inf,state_tau = inf_taus_ms[i]
                state_val = y[i]
                d_state = ( state_inf - state_val ) / state_tau
                res[i] = d_state
            return res

        # run the ODE for each variable:
        t = t.rescale("ms").magnitude
        y0 = np.zeros( (n_states, ) )
        res = odeint(func=odeFunc, y0=y0, t= t  )

        state_functor = sympy.lambdify( state_names, sympy.sympify(chl.eqn)  )
        state_data = [ res[:,i] for i in range(0,n_states) ]

        state_equation_evaluation = state_functor( *state_data )

        cell_density = (chl.conductance * cell_area)
        i_chl =  (chl.conductance * cell_area)  * state_equation_evaluation * (V- chl.reversalpotential)

        return TraceFixedDT( time=t * unit("1:ms"), data=i_chl.rescale("pA")  )





class Summarise_MM_AlphaBetaBetaChannel(object):


        #@classmethod
        #def getResolvedAlphaBetaBetaCurves(cls, V, chl, state ):
        #    alpha,beta = chl.get_alpha_beta_at_voltage(V, state)
        #    return  alpha,beta
        #    #return AlphaBetaBetaCalculator.getAlphaBetaBeta(V, chl.statevars[state][0], chl.statevars[state][1],chl.statevars[state][2], chl.beta2threshold   )
#

        #@classmethod
        #def plot_alpha_beta_curves(cls, ax1, ax2, alphabeta_chl, state, color="blue"):
        #    #chl = alphabeta_chl
        #
        #    V = StdLimits.get_default_voltage_array().rescale("mV")
        #
        #    #get_alpha_beta_at_voltage(self, V, statevar):
        #    alpha,beta = alphabeta_chl.get_alpha_beta_at_voltage(V, state)
        #
        #    #cls.getResolvedAlphaBetaBetaCurves(V, chl, state)
        #
        #
        #    ax1.plot(V,alpha, color)
        #    ax1.set_xlabel("Voltage")
        #    ax1.set_ylabel("Alpha")
        #
        #    ax2.plot(V,beta, color)
        #    ax2.set_xlabel("Voltage")
        #    ax2.set_ylabel("Beta")
        #
        #
        #@classmethod
        #def plot_inf_tau_curves(cls, ax1,ax2,alphabeta_chl, state, color="blue" ):
        #
        #    chl = alphabeta_chl
        #
        #    V = StdLimits.get_default_voltage_array().rescale("mV")
        #
        #    alpha,beta = cls.getResolvedAlphaBetaBetaCurves(V, chl, state)
        #    inf,tau = InfTauCalculator.alpha_beta_to_inf_tau(alpha,beta)
        #
        #    if isinstance(ax1, QuantitiesAxis):
        #
        #        ax1.setYUnit("")
        #        ax1.plot(V,inf,color)
        #        ax1.set_xlabel("Voltage")
        #        ax1.set_ylabel("Inf")
        #
        #        ax2.plot(V,tau, color)
        #        ax2.set_xlabel("Voltage")
        #        ax2.set_ylabel("Tau")
        #        ax2.setYUnit("ms")

        #    else:
        #
        #        ax1.plot(V,inf,color)
        #        ax1.set_xlabel("Voltage (mV)")
        #        ax1.set_ylabel("Infs")
        #
        #        ax2.plot(V,tau.rescale("ms"),color)
        #        ax2.set_xlabel("Voltage (mV)")
        #        ax2.set_ylabel("Tau (ms)")



        #@classmethod
        #def plot_state_curve_summary(cls,  alphabeta_chl, state, figsize):
        #    fig = QuantitiesFigure(figsize=figsize)
        #    fig.suptitle("AlphaBeta Channel - %s : %s"%(alphabeta_chl.name, state))
        #    ax1 = fig.add_subplot(221)
        #    ax2 = fig.add_subplot(222)
        #    cls.plot_alpha_beta_curves(ax1, ax2, alphabeta_chl,state )
        #
        #    ax3 = fig.add_subplot(223)
        #    ax4 = fig.add_subplot(224)
        #    cls.plot_inf_tau_curves(ax3, ax4, alphabeta_chl,state )
        #    return fig
        #
        #
        #


        #@classmethod
        #def plot_steddy_state_curve(cls, ax1,alphabeta_chl, state, power, color="blue" ):
        #
        #    chl = alphabeta_chl
        #
        #    V = StdLimits.get_default_voltage_array().rescale("mV")
        #
        #    alpha,beta = cls.getResolvedAlphaBetaBetaCurves(V, chl, state)
        #    inf,tau = InfTauCalculator.alpha_beta_to_inf_tau(alpha,beta)
        #
        #    infpower = np.power(inf,power)
        #    if isinstance(ax1, QuantitiesAxis):
        #        ax1.setYUnit("")
        #        ax1.plot(V,infpower,color)
        #        ax1.set_xlabel("Voltage")
        #        ax1.set_ylabel("Inf**%d"%power)
        #
        #    else:
        #        ax1.plot(V,infpower,color)
        #        ax1.set_xlabel("Voltage (mV)")
        #        ax1.set_ylabel("Inf**%d"%power)







        @classmethod
        def to_screen(cls, alphabeta_chl, state):
            cls.plot_state_curve_summary(alphabeta_chl, state, figsize=(5,5))



#        @classmethod
#        def build_alpha_beta_table(cls, elements, reportlabconfig, title, params ):
#            elements.append( Paragraph(title,reportlabconfig.styles['Heading4']) )
#            alphaParams = "%2.2f %2.2f %2.2f %2.2f %2.2f"%tuple(params)
#            alphaTableData = [ ["A","B","C","D","E"], alphaParams.split()  ]
#            elements.append( Table(alphaTableData, style=reportlabconfig.defaultTableStyle) )

        @classmethod
        def to_report_lab(cls, alphabeta_beta_chl, reportlabconfig, make_graphs):
            from reportlab.platypus import Paragraph, Table
            local_elements = []
            local_elements.append( Paragraph("Overview",reportlabconfig.styles['Heading3']) )

            # Summary:
            overview_table_data = [
                                 ["Channel Type", "AlphaBetaBetaChl"],
                                 ["Max Conductance (gBar)", alphabeta_beta_chl.conductance],
                                 ["Reversal Potential", alphabeta_beta_chl.reversalpotential],
                                 ["Conductance Equation", "gBar * " + alphabeta_beta_chl.eqn],
                                ]
            local_elements.append( Table(overview_table_data, style=reportlabconfig.listTableStyle) )


            # Plot out the States:
            for state,params in alphabeta_beta_chl.statevars.iteritems():
                local_elements.append( Paragraph("State: %s"%state,reportlabconfig.styles['Heading3']) )


                if make_graphs:
                    fig = Summarise_MM_AlphaBetaChannel.plot_state_curve_summary(alphabeta_beta_chl, state, figsize=(5,5))
                    local_elements.append( reportlabconfig.save_mpl_to_rl_image(fig, "somestate") )


                local_elements.append( Paragraph("Equations",reportlabconfig.styles['Heading4']) )

                #Equations:
                eqns = [
                        "beta2Threshold = %s"%alphabeta_beta_chl.beta2threshold,
                        "beta = beta1 if V less than beta2Threshold otherwise beta2",
                        "alpha(V) = (A+BV)/(C+exp( (V+D)/E) )",
                        "beta(V) = (A+BV)/(C+exp( (V+D)/E) )",
                        ]
                for eqn in eqns:
                    local_elements.append( Paragraph(eqn,reportlabconfig.styles['Normal']) )

                # Alpha Beta
                ReportLabTools.build_alpha_beta_table( elements=local_elements,
                                         reportlabconfig=reportlabconfig,
                                         title="Alpha", params=params[0] )
                ReportLabTools.build_alpha_beta_table( elements=local_elements,
                                         reportlabconfig=reportlabconfig,
                                         title="Beta1", params=params[1] )
                ReportLabTools.build_alpha_beta_table( elements=local_elements,
                                         reportlabconfig=reportlabconfig,
                                         title="Beta2", params=params[2] )



            return local_elements


SummariserLibrary.register_summariser(channel_baseclass=MM_AlphaBetaBetaChannel, summariser_class=Summarise_MM_AlphaBetaBetaChannel)
