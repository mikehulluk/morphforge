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

#from reportlab.pdfgen import canvas
#from reportlab.lib.styles import getSampleStyleSheet
#from reportlab.platypus import *
#import itertools
#from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, Paragraph
#from reportlab.lib import colors
#import os
#from reportlab.lib.pagesizes import A4

from mhlibs.quantities_plot import QuantitiesFigure
from mhlibs.quantities_plot import QuantitiesAxis

#from morphforge.core.quantities import unit
#
#from scipy.integrate import odeint
import numpy as np
#from morphforge.traces import TraceFixedDT

from morphforge.simulationanalysis.summaries.summariser_library import SummariserLibrary

from core import MM_InfTauInterpolatedChannel
from morphforge.simulationanalysis.summaries.stdlimits import StdLimits

from morphforge.stdimports import pq







class Summarise_MM_InfTauInterpolatedChannel(object):

        @classmethod
        def plot_alpha_beta_curves(cls, ax1, ax2, alphabeta_chl, state, color="blue"):
            chl = alphabeta_chl




            inf_v =  np.array(alphabeta_chl.statevars_new[state].V)
            inf =   np.array(alphabeta_chl.statevars_new[state].inf)
            tau =   np.array(alphabeta_chl.statevars_new[state].tau)

            #tauV =  np.array(zip(*alphabeta_chl.statevars[state]['tau'])[0])
            #tau =   np.array(zip(*alphabeta_chl.statevars[state]['tau'])[1])

            # Check the two voltage arrays are the same:
            #assert np.max((inf_v-tauV)**2) < 1.0

            alpha = inf/tau
            beta = (1 - alpha*tau) / tau


            if isinstance(ax1, QuantitiesAxis):

                ax1.setYUnit("")
                ax1.plot(inf_v * pq.mV, alpha * pq.s/pq.s, color=color)
                ax1.set_xlabel("Voltage")
                ax1.set_ylabel("Alpha")

                ax2.plot(inf_v * pq.mV, beta * pq.s/pq.s, color=color)
                ax2.set_xlabel("Voltage")
                ax2.set_ylabel("Beta")
                ax2.setYUnit("")

            else:

                ax1.plot(inf_v, alpha, color=color)
                ax1.set_xlabel("Voltage (mV)")
                ax1.set_ylabel("Alpha")

                ax2.plot(inf_v, beta, color=color)
                ax2.set_xlabel("Voltage (mV)")
                ax2.set_ylabel("Beta")





            return

            V = StdLimits.get_default_voltage_array().rescale("mV")

            alpha, beta = cls.getResolvedInfTauInterpolatedCurves(V, chl, state)


            ax1.plot(V, alpha, color="blue")
            ax1.set_xlabel("Voltage")
            ax1.set_ylabel("Alpha")

            ax2.plot(V, beta, color="blue")
            ax2.set_xlabel("Voltage")
            ax2.set_ylabel("Beta")


        @classmethod
        def plot_inf_tau_curves(cls, ax1, ax2, alphabeta_chl, state, color="blue"):

            if isinstance(ax1, QuantitiesAxis):

#                print alphabeta_chl.statevars[state]['inf']
                inf_v =  np.array(alphabeta_chl.statevars_new[state].V)
                inf =   np.array(alphabeta_chl.statevars_new[state].inf)
                tau =   np.array(alphabeta_chl.statevars_new[state].tau)

                #inf_v =  np.array(zip(*alphabeta_chl.statevars[state]['inf'])[0])
                #inf =   np.array(zip(*alphabeta_chl.statevars[state]['inf'])[1])

                #tauV =  np.array(zip(*alphabeta_chl.statevars[state]['tau'])[0])
                #tau =   np.array(zip(*alphabeta_chl.statevars[state]['tau'])[1])



                ax1.setYUnit("")
                ax1.plot(inf_v * pq.mV, inf * pq.s/pq.s, color=color)
                ax1.set_xlabel("Voltage")
                ax1.set_ylabel("Inf")

                ax2.plot(inf_v * pq.mV, tau* pq.ms, color=color)
                ax2.set_xlabel("Voltage")
                ax2.set_ylabel("Tau")
                ax2.setYUnit("ms")

            else:

                ax1.plot(inf_v, inf, color=color)
                ax1.set_xlabel("Voltage (mV)")
                ax1.set_ylabel("Infs")

                ax2.plot(inf_v, tau, color=color)
                ax2.set_xlabel("Voltage (mV)")
                ax2.set_ylabel("Tau (ms)")



        @classmethod
        def plot_state_curve_summary(cls,  alphabeta_chl, state, figsize):
            fig = QuantitiesFigure(figsize=figsize)
            fig.suptitle("InfTauInterpolated Channel - %s : %s"%(alphabeta_chl.name, state))
            ax1 = fig.add_subplot(221)
            ax2 = fig.add_subplot(222)
            cls.plot_inf_tau_curves(ax1, ax2, alphabeta_chl, state)

            ax3 = fig.add_subplot(223)
            ax4 = fig.add_subplot(224)
            cls.plot_alpha_beta_curves(ax3, ax4, alphabeta_chl, state)
            return fig

        @classmethod
        def to_screen(cls, alphabeta_chl, state):

            cls.plot_state_curve_summary(alphabeta_chl, state, figsize=(5, 5))






        @classmethod
        def to_report_lab(cls, alphabeta_chl, reportlabconfig, make_graphs):
            local_elements = []
            local_elements.append(Paragraph("Overview", reportlabconfig.styles['Heading3']))

            # Summary:
            overview_table_data = [
                                 ["Max Conductance (gBar)", alphabeta_chl.conductance.rescale("mS/cm2")],
                                 ["Reversal Potential", alphabeta_chl.reversalpotential.rescale("mV")],
                                 ["Conductance Equation", "gBar * " + alphabeta_chl.eqn],
                               ]

            local_elements.append(Table(overview_table_data, style=reportlabconfig.listTableStyle))


            #return local_elements

            # Plot out the States:
            for state, params in alphabeta_chl.statevars_new.iteritems():
                local_elements.append(Paragraph("State: %s" % state, reportlabconfig.styles['Heading3']))

                # Interpolated_values:
                inf_table  = [
                                 ["Voltage", 'Inf'],
                           ] + [("%2.2f" % p0, "%2.2f" % p1) for (p0, p1) in zip(params.V, params.inf)]

                tau_table  = [
                                 ["Voltage", 'Tau'],
                           ] + [("%2.2f" % p0, "%2.2f" % p1) for (p0, p1) in zip(params.V, params.tau)]

                #mergeTable = zip(inf_table, tau_table)


                local_elements.append(Table(inf_table, style=reportlabconfig.listTableStyle))
                local_elements.append(Table(tau_table, style=reportlabconfig.listTableStyle))
                #local_elements.append(Table(mergeTable, style=reportlabconfig.listTableStyle))


                #continue

                ##Equations:
                #eqns = [
                #        "alpha(V) = (A+BV)/(C+exp((V+D)/E))",
                #        "beta(V) = (A+BV)/(C+exp((V+D)/E))",
                #       ]
                #for eqn in eqns:
                #    local_elements.append(Paragraph(eqn, reportlabconfig.styles['Normal']))
                # Alpha Beta
                #ReportLabTools.buildInfTauInterpolatedTable(elements=local_elements,
                #                         reportlabconfig=reportlabconfig,
                #                         title="Alpha", params=params[0])
                #ReportLabTools.buildInfTauInterpolatedTable(elements=local_elements,
                #                         reportlabconfig=reportlabconfig,
                #                         title="Beta1", params=params[1])


                # Figures:
                if make_graphs:
                    fig = cls.plot_state_curve_summary(alphabeta_chl, state, figsize=(7, 7))
                    local_elements.append(reportlabconfig.save_mpl_to_rl_image(fig, "somestate"))
                    fig.close()




            return local_elements



SummariserLibrary.register_summariser(channel_baseclass=MM_InfTauInterpolatedChannel, summariser_class=Summarise_MM_InfTauInterpolatedChannel)
