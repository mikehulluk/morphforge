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


class NEURONChlWriterInfTauInterpolated(object):



    chlHoc = """

$(cell_name).internalsections [$section_index] {
    // InfTauInterpolated Channels
    insert $neuron_suffix
    #for variable_name, variable_value_nounit, variable_value_with_unit, variable_unit in $variables:
    $(variable_name)_$(neuron_suffix) = $variable_value_nounit //(in $variable_unit, converted from $variable_value_with_unit)
    #end for
}
"""

    Units = {'gBar': 'S/cm2', 'e_rev': 'mV', 'gScale': ''}

    @classmethod
    def build_hoc_section(cls, cell, section, hocfile_obj, mta):

        cell_name = hocfile_obj[MHocFileData.Cells][cell]['cell_name']
        section_index = hocfile_obj[MHocFileData.Cells][cell]['section_indexer'][section]

        neuron_suffix = mta.mechanism.get_neuron_suffix()

        # Calculate the values of the variables for the section:
        variables = []
        for variable_name in mta.mechanism.get_variables():
            variable_value_with_unit = mta.applicator.get_variable_value_for_section(variable_name=variable_name, section=section)
            variable_unit = NEURONChlWriterInfTauInterpolated.Units[variable_name]
            variable_value_nounit = variable_value_with_unit.rescale(variable_unit).magnitude
            variables.append([variable_name, variable_value_nounit, variable_value_with_unit, variable_unit])

        tmpl_dict = {
            'cell_name': cell_name,
            'section_index': section_index,
            'neuron_suffix': neuron_suffix,
            'variables': variables,
            }

        # Add the data to the HOC file
        hoc_text = Template(NEURONChlWriterInfTauInterpolated.chlHoc, tmpl_dict).respond()
        hocfile_obj.add_to_section(MHOCSections.InitCellMembranes, hoc_text)



    @classmethod
    def build_mod(cls, alphabeta_chl, modfile_set):

        gbar_name = 'gBar'
        e_rev_name = 'e_rev'
        g_scale_name = 'gScale'

        base_writer = \
            MM_ModFileWriterBase(suffix=alphabeta_chl.get_neuron_suffix())

        # Naming Conventions:
        state_tau = lambda s: '%stau' % s
        state_inf = lambda s: '%sinf' % s

        # State Equations and initial values:
        for s in alphabeta_chl.statevars_new:
            base_writer.internalstates[s] = '%s' % state_inf(s), "%s'=(%s-%s)/%s" % (s, state_inf(s), s, state_tau(s))

        # Parameters:
        # {name: (value, unit, range)}
        base_writer.parameters = {
                      gbar_name: (alphabeta_chl.conductance.rescale("S/cm2").magnitude, ("S/cm2"), None),
                      e_rev_name: (alphabeta_chl.reversalpotential.rescale("mV").magnitude, ("mV"), None),
                      g_scale_name: (1.0, None, None)
                      }

        # Rates:
        # name : (locals, code), unit
        for s in alphabeta_chl.statevars_new:
            base_writer.rates[state_inf(s)] = (('', state_inf(s) + "= %sInf(v)" % state_inf(s)), None)
            base_writer.rates[state_tau(s)] = (('', state_tau(s) + "= %sTau(v)" % state_tau(s)), "ms")
            base_writer.ratecalcorder.extend([state_inf(s), state_tau(s)])

        base_writer.currentequation = '(v-%s) * %s * %s * %s' % (e_rev_name, gbar_name, alphabeta_chl.eqn, g_scale_name)
        base_writer.conductanceequation = '%s * %s * %s' % (gbar_name, alphabeta_chl.eqn, g_scale_name)

        base_writer.functions = """
        VERBATIM
        #include <gsl_wrapper.h>
        ENDVERBATIM"""

        def buildInterpolatorFunc(state, inftau, funcname):
            if inftau == 'inf':
                interp_str_x = ','.join(['%2.2f' % x for x in alphabeta_chl.statevars_new[s].V])
                interp_str_y = ','.join(['%2.2f' % x for x in alphabeta_chl.statevars_new[s].inf])
            elif inftau == 'tau':
                interp_str_x = ','.join(['%2.2f' % x for x in alphabeta_chl.statevars_new[s].V])
                interp_str_y = ','.join(['%2.2f' % x for x in alphabeta_chl.statevars_new[s].tau])
            else:
                assert False


            variables = {'chlname':state_tau(s), 'nPts':len(alphabeta_chl.statevars_new[s].V), 'x0':interp_str_x, 'y0':interp_str_y, 'funcname':funcname }
            f = """
            FUNCTION %(funcname)s(V)
            {
                VERBATIM {
                    static void* pInterpolator = NULL;
                    if(!pInterpolator)
                    {
                        double x[%(nPts)s] = { %(x0)s };
                        double y[%(nPts)s] = { %(y0)s };
                        int nPts = %(nPts)d;
                        pInterpolator = makeIntWrapper(x, y, nPts);
                    }
                    _l%(funcname)s= interpolate2(_lV, pInterpolator);
                }
                ENDVERBATIM
            }
            \n\n""" % variables
            return f

        for s in alphabeta_chl.statevars_new:
            base_writer.functions +=  buildInterpolatorFunc(state=s, inftau='inf', funcname='%sinfInf' % s)
            base_writer.functions +=  buildInterpolatorFunc(state=s, inftau='tau', funcname='%stauTau' % s)



        txt =  base_writer.generate_modfile()

        # TODO: Remove hard dependancy here
        additional_compile_flags = "-I/home/michael/hw_to_come/morphforge/src/morphforgecontrib/simulation/neuron_gsl/cpp"
        additional_link_flags = "-L/home/michael/hw_to_come/morphforge/src/morphforgecontrib/simulation/neuron_gsl/cpp -lgslwrapper -lgsl -lgslcblas"
        mod_file =  ModFile(name=alphabeta_chl.name, modtxt=txt, additional_compile_flags=additional_compile_flags, additional_link_flags=additional_link_flags)
        modfile_set.append(mod_file)


