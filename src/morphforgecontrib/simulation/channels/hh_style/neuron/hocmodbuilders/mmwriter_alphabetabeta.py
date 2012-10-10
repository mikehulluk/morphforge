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

from Cheetah.Template import Template
from morphforge.simulation.neuron import ModFile
from morphforge.simulation.neuron.simulationdatacontainers import MHocFileData
from morphforge.simulation.neuron.simulationdatacontainers import MHOCSections
from morphforge.simulation.neuron.hocmodbuilders import MM_ModFileWriterBase


class NEURONChlWriterAlphaBetaBeta(object):



    chlHoc = """

$(cell_name).internalsections [$section_index] {
    // AlphaBetaBeta Channels
    insert $neuron_suffix
    #for variable_name, variable_value_nounit, variable_value_with_unit, variable_unit in $variables:
    $(variable_name)_$(neuron_suffix) = $variable_value_nounit //(in $variable_unit, converted from $variable_value_with_unit)
    #end for
}
"""

    Units = {'gBar': 'S/cm2', 'e_rev': 'mV', 'gScale': ''}

    @classmethod
    def build_hoc_section(self, cell, section, hocfile_obj, mta):

        cell_hoc = hocfile_obj[MHocFileData.Cells][cell]
        cell_name = cell_hoc['cell_name']
        section_index = cell_hoc['section_indexer'][section]

        neuron_suffix = mta.mechanism.get_neuron_suffix()

        # Calculate the values of the variables for the section:
        variables = []
        for variable_name in mta.mechanism.get_variables():
            variable_value_with_unit = mta.applicator.get_variable_value_for_section(variable_name=variable_name, section=section)
            variable_unit = NEURONChlWriterAlphaBetaBeta.Units[variable_name]
            variable_value_nounit = variable_value_with_unit.rescale(variable_unit).magnitude
            variables.append([variable_name, variable_value_nounit, variable_value_with_unit, variable_unit])

        tmpl_dict = {
            'cell_name': cell_name,
            'section_index': section_index,
            'neuron_suffix': neuron_suffix,
            'variables': variables,
            }

        # Add the data to the HOC file
        hocfile_obj.add_to_section(MHOCSections.InitCellMembranes,  Template(NEURONChlWriterAlphaBetaBeta.chlHoc, tmpl_dict).respond())



    @classmethod
    def build_mod(cls, alphabeta_beta_chl, modfile_set):

        gbar_name = 'gBar'
        e_rev_name = 'eLk'
        g_scale_name = 'gScale'

        base_writer = MM_ModFileWriterBase(suffix=alphabeta_beta_chl.get_neuron_suffix())

        # Naming Conventions:
        state_tau = lambda s: '%stau' % s
        state_inf = lambda s: '%sinf' % s
        state_alpha = lambda s: '%s_alpha' % s
        state_beta = lambda s: '%s_beta' % s

        # State Equations and initial values:
        for s in alphabeta_beta_chl.statevars:
            base_writer.internalstates[s] = "%s" % state_inf(s) , "%s'=(%s-%s)/%s" % (s, state_inf(s), s, state_tau(s))

        # Parameters:
        # {name: (value, unit, range)}
        base_writer.parameters = {
                      #gbar_name: (alphabeta_beta_chl.conductance.toval(ounit="S/cm2"), ("S/cm2"), None),
                      #e_rev_name: (alphabeta_beta_chl.reversalpotential.toval("mV"), ("mV"), None)
                      gbar_name: (alphabeta_beta_chl.conductance.rescale("S/cm2").magnitude, ("S/cm2"), None),
                      e_rev_name: (alphabeta_beta_chl.reversalpotential.rescale("mV").magnitude, ("mV"), None),
                      g_scale_name: (1.0, None, None)
                      }

        # Rates:
        # name : (locals, code), unit
        for s in alphabeta_beta_chl.statevars:
            base_writer.rates[state_alpha(s)] = (("", state_alpha(s) + "= StdAlphaBeta(%f, %f, %f, %f, %f, v)" % tuple(alphabeta_beta_chl.statevars[s][0]))), None
            #base_writer.rates[state_beta(s)] = (("", state_beta(s) + "= StdBetaBeta(%f, %f, %f, %f, %f,  %f, %f, %f, %f, %f,  %f,  v)" % tuple(alphabeta_beta_chl.statevars[s][1] + alphabeta_beta_chl.statevars[s][2] + [alphabeta_beta_chl.beta2threshold.toval(ounit="mV")]))), None
            base_writer.rates[state_beta(s)] = (("", state_beta(s) + "= StdBetaBeta(%f, %f, %f, %f, %f,  %f, %f, %f, %f, %f,  %f,  v)" % tuple(alphabeta_beta_chl.statevars[s][1] + alphabeta_beta_chl.statevars[s][2] + [alphabeta_beta_chl.beta2threshold.rescale("mV").magnitude]))), None
            base_writer.rates[state_inf(s)] = (("", state_inf(s) + "= %s/(%s+%s)" % (state_alpha(s), state_alpha(s), state_beta(s))), None)
            base_writer.rates[state_tau(s)] = (("", state_tau(s) + "= 1.0/(%s+%s)" % (state_alpha(s), state_beta(s))), "ms")
            base_writer.ratecalcorder.extend([state_alpha(s), state_beta(s), state_inf(s), state_tau(s)])

        base_writer.currentequation = "(v-%s) * %s * %s * %s" % (e_rev_name, gbar_name, alphabeta_beta_chl.eqn, g_scale_name)
        base_writer.conductanceequation = "%s * %s * %s" % (gbar_name, alphabeta_beta_chl.eqn, g_scale_name)

        #base_writer.currentequation = "(v-%s) * %s * %s" % (e_rev_name, gbar_name, alphabeta_beta_chl.eqn)
        base_writer.functions = """
                    FUNCTION StdAlphaBeta(A, B, C, D, E, V){ StdAlphaBeta = (A + B*V) / (C + exp((D+V)/E)) }
                    FUNCTION StdBetaBeta(A, B, C, D, E, A2, B2, C2, D2, E2, beta2Threshold, V)
                    {
                        if(V < beta2Threshold)
                        {
                            StdBetaBeta = (A + B*V) / (C + exp((D+V)/E))
                        }
                        else
                        {
                           StdBetaBeta = (A2 + B2*V) / (C2 + exp((D2+V)/E2))
                        }
                    }
                    """
        txt = base_writer.generate_modfile()
        mod_file = ModFile(name=alphabeta_beta_chl.name, modtxt=txt)
        modfile_set.append(mod_file)


