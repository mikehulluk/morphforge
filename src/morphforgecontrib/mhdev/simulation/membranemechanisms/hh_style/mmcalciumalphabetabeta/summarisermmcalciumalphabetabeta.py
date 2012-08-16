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


import numpy as np


# from numpy import power
#
from ..stdlimits import StdLimits
#import morphforge


from mhlibs.quantities_plot import QuantitiesFigure

# import numpy as np

# import morphforge.core.quantities as pq
# from morphforge.core import unit

from util import AlphaBetaCalculator, AlphaBetaBetaCalculator
from util import InfTauCalculator, ReportLabTools




from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import *
import itertools
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import *
from reportlab.lib import colors
import os
from reportlab.lib.pagesizes import A4

from morphforge.simulationanalysis.summaries.summariser_library import SummariserLibrary
from morphforgecontrib.default.core.mmalphabetabeta import MM_AlphaBetaBetaChannel
from morphforgecontrib.default.core.mmalphabeta import MM_AlphaBetaChannel
from morphforgecontrib.default.core.mmcalciumalphabetabeta import MM_CalciumAlphaBetaBetaChannel





class Summarise_MM_CalciumAlphaBetaBetaChannel(object):


        @classmethod
        def getResolvedAlphaBetaCurves(cls, V, chl, state ):
            return AlphaBetaBetaCalculator.getAlphaBetaBeta(V, chl.statevars[state][0],chl.statevars[state][1],chl.statevars[state][2], chl.beta2threshold   )


        @classmethod
        def plot_alpha_beta_curves(cls, ax1,ax2, calciumAlphaBetaBetaChannel, state):
            chl = calciumAlphaBetaBetaChannel

            V = StdLimits.get_default_voltage_array().rescale("mV")

            alpha,beta = cls.getResolvedAlphaBetaCurves(V, chl, state)

            ax1.plot(V,alpha)
            ax1.set_xlabel("Voltage")
            ax1.set_ylabel("Alpha")

            ax2.plot(V,beta)
            ax2.set_xlabel("Voltage")
            ax2.set_ylabel("Beta")

        @classmethod
        def plot_inf_tau_curves(cls, ax1,ax2,calciumAlphaBetaBetaChannel, state ):

            chl = calciumAlphaBetaBetaChannel

            V = StdLimits.get_default_voltage_array().rescale("mV")

            alpha,beta = cls.getResolvedAlphaBetaCurves(V, chl, state)
            inf,tau = InfTauCalculator.alpha_beta_to_inf_tau(alpha,beta)

            ax1.plot(V,inf)
            ax1.set_xlabel("Voltage")
            ax1.set_ylabel("Inf")

            ax2.setYUnit("ms")
            ax2.plot(V,tau)
            ax2.set_xlabel("Voltage")
            ax2.set_ylabel("Tau")



        @classmethod
        def plot_state_curve_summary(cls,  alphabeta_chl, state, figsize):
            fig = QuantitiesFigure(figsize=figsize)
            fig.suptitle("Calcium AlphaBetaBeta Channel - %s : %s"%(alphabeta_chl.name, state))
            ax1 = fig.add_subplot(221)
            ax2 = fig.add_subplot(222)
            cls.plot_alpha_beta_curves(ax1, ax2, alphabeta_chl,state )

            ax3 = fig.add_subplot(223)
            ax4 = fig.add_subplot(224)
            cls.plot_inf_tau_curves(ax3, ax4, alphabeta_chl,state )
            return fig


        @classmethod
        def PlotGHKMaxCurrentFlow(cls,calciumAlphaBetaBetaChannel, figsize ):
            V = StdLimits.get_default_voltage_array().rescale("mV")
            # Plot the
            fig = QuantitiesFigure(figsize=figsize)
            ax1 = fig.add_subplot(221, xUnit="mV",yUnit="pA/cm2", xlabel="Voltage", ylabel="")


            #Plot the 'I_ca' as defined in Biophysics of Computations:
            chl = calciumAlphaBetaBetaChannel
            nmp = (chl.CaZ * chl.F) / (chl.R * chl.T)
            nmpV = (nmp * V).rescale("")

            iCa = chl.permeability * nmpV * chl.F * ( chl.intracellular_concentration - chl.extracellular_concentration * np.exp( -1.0 * nmpV) ) / ( 1.0 - np.exp( -1.0 * nmpV))

            iCa.rescale("pA/cm2")


            ax1.plot(V,iCa)


        @classmethod
        def to_screen(cls, calciumAlphaBetaBetaChannel, state):
            cls.plot_state_curve_summary(cls, calciumAlphaBetaBetaChannel, state, figsize=(5,5))
            cls.PlotGHKMaxCurrentFlow(cls, calciumAlphaBetaBetaChannel, figsize=(4,4) )


        @classmethod
        def to_report_lab(cls, calciumAlphaBetaBetaChannel, reportlabconfig, make_graphs):
            chl = calciumAlphaBetaBetaChannel

            localElements = []
            localElements.append( Paragraph("Overview",reportlabconfig.styles['Heading3']) )

            # Summary:
            overviewTableData = [
                                 ["permeability", chl.permeability],
                                 ["intracellular_concentration",  chl.intracellular_concentration],
                                 ["extracellular_concentration",  chl.extracellular_concentration],
                                 ["Equation EXPLAIN", chl.eqn ],
                                 ["beta2threshold", chl.beta2threshold ],
                                 ["Temperature ", chl.T ],
                                 ["F", chl.F ],
                                 ["R", chl.R ],
                                 ["CaZ", chl.CaZ ],
                                ]


            localElements.append( Table(overviewTableData, style=reportlabconfig.listTableStyle) )

            #GHK Max Current Flow
            localElements.append( Paragraph("MaxCurrentFlow From GHK", reportlabconfig.styles['Heading3']) )
            fig = cls.PlotGHKMaxCurrentFlow( calciumAlphaBetaBetaChannel, figsize=(4,4) )
            localElements.append( reportlabconfig.save_mpl_to_rl_image(fig, "ghk") )

            # Plot out the States:
            for state,params in calciumAlphaBetaBetaChannel.statevars.iteritems():
                localElements.append( Paragraph("State: %s"%state, reportlabconfig.styles['Heading3']) )

                if make_graphs:
                    fig = cls.plot_state_curve_summary(chl, state, figsize=(5,5))
                    localElements.append( reportlabconfig.save_mpl_to_rl_image(fig, "somestate") )
                    fig.close()

                #Equations:
                eqns = [
                        "beta2Threshold = %s"%calciumAlphaBetaBetaChannel.beta2threshold,
                        "beta = beta1 if V less than beta2Threshold otherwise beta2",
                        "alpha(V) = (A+BV)/(C+exp( (V+D)/E) )",
                        "beta(V) = (A+BV)/(C+exp( (V+D)/E) )",
                        ]
                for eqn in eqns:
                    localElements.append( Paragraph(eqn,reportlabconfig.styles['Normal']) )

                # Alpha Beta
                ReportLabTools.build_alpha_beta_table( elements=localElements,
                                         reportlabconfig=reportlabconfig,
                                         title="Alpha", params=params[0] )
                ReportLabTools.build_alpha_beta_table( elements=localElements,
                                         reportlabconfig=reportlabconfig,
                                         title="Beta1", params=params[1] )
                ReportLabTools.build_alpha_beta_table( elements=localElements,
                                         reportlabconfig=reportlabconfig,
                                         title="Beta2", params=params[2] )

            return localElements


SummariserLibrary.register_summariser(channel_baseclass=MM_CalciumAlphaBetaBetaChannel, summariser_class=Summarise_MM_CalciumAlphaBetaBetaChannel)
