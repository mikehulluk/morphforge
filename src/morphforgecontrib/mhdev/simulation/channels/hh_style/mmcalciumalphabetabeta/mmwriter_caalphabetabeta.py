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

from morphforge.simulation.neuron.hocmodbuilders import ModFileSectioned, NeuronParameter

#from morphforge.core import quantities
import quantities


class NEURONChlWriterCalciumAlphaBetaBeta(object):

    chlHoc = """

$(cell_name).internalsections [$section_index] {
    // AlphaBeta Channels
    insert $neuron_suffix
    #for variable_name, variable_value_nounit, variable_value_with_unit, variable_unit in $variables:
    $(variable_name)_$(neuron_suffix) = $variable_value_nounit //(in $variable_unit, converted from $variable_value_with_unit)
    #end for
}
"""

    Units = {'gScale': '','pca':'cm/sec'}

    @classmethod
    def build_hoc_section(cls, cell, section, hocfile_obj, mta):

        cell_name = hocfile_obj[MHocFileData.Cells][cell]['cell_name']
        section_index = hocfile_obj[MHocFileData.Cells][cell]['section_indexer'][section]

        neuronSuffix = mta.mechanism.get_neuron_suffix()

        # Calculate the values of the variables for the section:
        variables = []
        for variable_name in mta.mechanism.get_variables():
            variable_value_with_unit = mta.applicator.get_variable_value_for_section(variable_name=variable_name, section=section)
            variable_unit = NEURONChlWriterCalciumAlphaBetaBeta.Units[variable_name]
            variable_value_nounit = variable_value_with_unit.rescale(variable_unit).magnitude
            variables.append([variable_name, variable_value_nounit, variable_value_with_unit, variable_unit])

        tmplDict = {
            'cell_name': cell_name,
            'section_index': section_index,
            'neuron_suffix': neuronSuffix,
            'variables': variables,
            }

        # Add the data to the HOC file
        hoc_text = Template(NEURONChlWriterCalciumAlphaBetaBeta.chlHoc, tmplDict).respond()
        hocfile_obj.add_to_section(MHOCSections.InitCellMembranes, hoc_text)



    @classmethod
    def build_mod(cls, caAlphaBetaBetaChl, modfile_set):

        m = ModFileSectioned(title='Some title')

        # User Functions:

        m.add_unit_definition(unitname='milliamp', unitsymbol='mA')
        m.add_unit_definition(unitname='millivolt', unitsymbol='mV')
        m.add_unit_definition(unitname='siemens', unitsymbol='S')

        m.add_unit_definition(unitname='1/liter', unitsymbol='molar')
        m.add_unit_definition(unitname='micromolar', unitsymbol='uM')
        m.add_unit_definition(unitname='molar', unitsymbol='M')
        m.add_unit_definition(unitname='nanomolar', unitsymbol='nM')

        m.add_unit_definition(unitname='(joule/K-mole)', unitsymbol='rUnits')
        m.add_unit_definition(unitname='(C/mole)', unitsymbol='fUnits')


        m.create_neuron_interface(suffix= caAlphaBetaBetaChl.get_neuron_suffix(), nonspecificcurrents=["i"], ioncurrents=None, ranges = ["pca", "SCa_i", "Sca_o", "T"])

        neuronUnitsToQuantities = {
                                   "cm/sec" : "cm/sec",
                                   "rUnits" : quantities.joule / (quantities.Kelvin * quantities.mol),
                                   "K": "K",
                                   "fUnits":"C/mol",
                                   "M":   quantities.mol / quantities.litre,
                                   "mA/cm2":"mA/cm2",
                                   "mV":"mV",
                                   }

        ## Params:
        params = [
                  ("pca",   "cm/sec",  caAlphaBetaBetaChl.permeability),
                  ("R",     "rUnits",   caAlphaBetaBetaChl.R),
                  ("T",     "K",       caAlphaBetaBetaChl.T),
                  ("F",     "fUnits",       caAlphaBetaBetaChl.F),
                  ("SCa_i", "M",      caAlphaBetaBetaChl.intracellular_concentration),
                  ("SCa_o", "M",      caAlphaBetaBetaChl.extracellular_concentration),
                 ]
        for name, unit, initialvalueUnit in params:
            initval = initialvalueUnit.rescale(neuronUnitsToQuantities[unit]).magnitude
            m.add_parameter(NeuronParameter(parametername=name, parameterunit=unit, initialvalue = initval, parameterrange=None))

        # Fixed Values:
        m.add_parameter(NeuronParameter(parametername="CaZ", parameterunit="1", initialvalue = caAlphaBetaBetaChl.CaZ.rescale("").magnitude, parameterrange=None))
        m.add_parameter(NeuronParameter(parametername="gScale", parameterunit="1", initialvalue = 1.0 , parameterrange=None))


        # Assignments:
        assignments = [
                    ("i", "mA/cm2"),
                    ("v", "mV"),
                    ('c', None),
                    ('cV', None),
       ]
        for name, unit in assignments:
            m.add_assigned(NeuronParameter(parametername=name, parameterunit=unit, parameterrange=None))



        # States
        m.add_state_group(groupname = "states",
                         states = [
                                   NeuronParameter(parametername="m", parameterunit=None),
                                   NeuronParameter(parametername="mtau", parameterunit="ms"),
                                   NeuronParameter(parametername="minf", parameterunit=None),
                                  ],
                         derivative_code = ["rates(v)", "m' = (minf-m)/(mtau)"] ,
                         initial_code = ["rates(v)", "m=minf"],
                        )


        ## Proceedures:

        assert len(caAlphaBetaBetaChl.statevars) == 1
        statevars = caAlphaBetaBetaChl.statevars.values()[0]
        #print statevars
        ratesFunctionTmpl = """
PROCEDURE rates(v(mV)) {
    LOCAL alpha, beta, sum

    alpha = DoStdFormAlphaBeta($alpha[0] , $alpha[1] , $alpha[2] , $alpha[3] , $alpha[4] , v)

    if(v < $betathreshold (mV))
    {
        beta = DoStdFormAlphaBeta($beta1[0] , $beta1[1] , $beta1[2] , $beta1[3] , $beta1[4] , v)
    }
    else
    {
        beta = DoStdFormAlphaBeta($beta2[0] , $beta2[1] , $beta2[2] , $beta2[3] , $beta2[4] , v)
    }

    sum = alpha + beta
    UNITSOFF
    mtau = 1.0/sum
    UNITSON
    minf = alpha/sum
}
"""

        ratesFunction = Template(ratesFunctionTmpl, {
            'alpha': statevars[0],
            'beta1': statevars[1],
            'beta2': statevars[2],
            'betathreshold': caAlphaBetaBetaChl.beta2threshold.rescale('mV').magnitude,
            }).respond()

        m.add_function(ratesFunction)

        stdFormAlphaBeta = """
FUNCTION DoStdFormAlphaBeta(A,B,C,D,E,V (mV))
{
    UNITSOFF
    DoStdFormAlphaBeta = (A+B*V)/(C+exp((D+V)/E))

    UNITSON
}

FUNCTION vtrap(x,y)
{
   if(fabs(x/y) < 1e-6)
   {
       vtrap = y*(1 - x/y/2)
    }
    else
    {
        vtrap = x/(exp(x/y) -1)
    }
}


"""
        m.add_function(stdFormAlphaBeta)


        m.add_breakpoint('c = (CaZ * F) / (R * T)')
        m.add_breakpoint('cV = c * v * 1e-3')
        m.add_breakpoint('i = pca * cV * 1e-3 *  CaZ * F *(SCa_i - SCa_o * exp(-1.0 * cV)) / (1.0-exp(-1.0*cV)) *m *m * gScale')

        modtxt = m.get_text()
        modFile = ModFile(name=caAlphaBetaBetaChl.name, modtxt=modtxt)
        modfile_set.append(modFile)

