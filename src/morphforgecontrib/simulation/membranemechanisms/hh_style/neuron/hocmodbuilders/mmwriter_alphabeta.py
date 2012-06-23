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

from Cheetah.Template import Template
from morphforge.simulation.neuron import ModFile
from morphforge.simulation.neuron.simulationdatacontainers import MHOCSections, MHocFileData
from morphforge.simulation.neuron.hocmodbuilders import MM_ModFileWriterBase



class MM_WriterAlphaBeta(object):
    
    
    
    chlHoc = """
    
$(cell_name).internalsections [ $section_index ] {
    // AlphaBeta Channels 
    insert $neuron_suffix         
    #for variable_name,variable_value_nounit, variable_value_with_unit,variable_unit in $variables:
    $(variable_name)_$(neuron_suffix) = $variable_value_nounit //( in $variable_unit, converted from $variable_value_with_unit)
    #end for
}
"""

    Units = { 
        "gBar": "S/cm2",
        "eRev": "mV",
        "gScale":"",
            }


    @classmethod
    def build_hoc_section(cls, cell, section, hocfile_obj, mta ):
        
        cell_name = hocfile_obj[MHocFileData.Cells][cell]['cell_name']
        section_index = hocfile_obj[MHocFileData.Cells][cell]['section_indexer'][section]
        
        neuronSuffix = mta.mechanism.get_neuron_suffix()
        
        
        # Calculate the values of the variables for the section:
        variables = []
        for variable_name in mta.mechanism.get_variables():
            variable_value_with_unit = mta.applicator.get_variable_value_for_section(variable_name=variable_name, section=section)
            variable_unit = MM_WriterAlphaBeta.Units[variable_name]
            variable_value_nounit = variable_value_with_unit.rescale(variable_unit).magnitude 
            variables.append( [variable_name,variable_value_nounit, variable_value_with_unit,variable_unit] )
            
        tmplDict = {
                    "cell_name":cell_name,
                    "section_index":section_index,
                    "neuron_suffix":neuronSuffix,
                    "variables":variables
                    }
        
        # Add the data to the HOC file
        hocfile_obj.add_to_section( MHOCSections.InitCellMembranes,  Template(MM_WriterAlphaBeta.chlHoc,tmplDict ).respond() )
    


    @classmethod
    def build_Mod(cls, alphaBetaChl, modfile_set):
        
        gbarName = "gBar" 
        eRevName = "eRev"
        gScaleName = "gScale"  
        
        #gbarUnits = MM_WriterAlphaBeta.Units[gbarName]
        #eRevUnits = MM_WriterAlphaBeta.Units[eRevName]
        
        
        
        baseWriter = MM_ModFileWriterBase(suffix=alphaBetaChl.get_neuron_suffix())
        
        # Naming Conventions:
        stateTau = lambda s: "%stau" % s
        stateInf = lambda s: "%sinf" % s
        stateAlpha = lambda s: "%s_alpha" % s
        stateBeta = lambda s: "%s_beta" % s
        
        #gbarName = "g%sbar" % alphaBetaChl.ion
        #eRevName = "e%s" % alphaBetaChl.ion
        
        
        # State Equations and initial values:
        for s in alphaBetaChl.statevars:
            baseWriter.internalstates[s] = "%s" % stateInf(s) , "%s'=(%s-%s)/%s" % (s, stateInf(s), s, stateTau(s)) 
        
        # Parameters:
        # {name: (value, unit,range)}
        baseWriter.parameters = { 
                      gbarName: (alphaBetaChl.conductance.rescale("S/cm2").magnitude, ("S/cm2"), None),
                      eRevName: (alphaBetaChl.reversalpotential.rescale("mV").magnitude, ("mV"), None),
                      gScaleName: (1.0, None, None)
                      }
        
        # Rates:
        # name : (locals, code), unit
        for s in alphaBetaChl.statevars:
            baseWriter.rates[ stateAlpha(s) ] = (("", stateAlpha(s) + "= StdAlphaBeta( %f,%f,%f,%f,%f, v)" % tuple(alphaBetaChl.statevars[s][0]))), None
            baseWriter.rates[ stateBeta(s) ] = (("", stateBeta(s) + "= StdAlphaBeta( %f,%f,%f,%f,%f, v)" % tuple(alphaBetaChl.statevars[s][1]))), None
            baseWriter.rates[ stateInf(s) ] = (("", stateInf(s) + "= %s/(%s+%s)" % (stateAlpha(s), stateAlpha(s), stateBeta(s))), None)
            baseWriter.rates[ stateTau(s) ] = (("", stateTau(s) + "= 1.0/(%s+%s)" % (stateAlpha(s), stateBeta(s))), "ms")
            baseWriter.ratecalcorder.extend([stateAlpha(s), stateBeta(s), stateInf(s), stateTau(s)])
            
        baseWriter.currentequation = "(v-%s) * %s * %s * %s" % (eRevName, gbarName, alphaBetaChl.eqn, gScaleName)
        baseWriter.conductanceequation = " %s * %s * %s" % (gbarName, alphaBetaChl.eqn, gScaleName)
        baseWriter.functions = """FUNCTION StdAlphaBeta(A,B,C,D,E,V){ StdAlphaBeta = (A + B*V) / (C + exp((D+V)/E)) } """
         
        txt =  baseWriter.generate_modfile()
        modFile =  ModFile(name=alphaBetaChl.name, modtxt=txt )
        modfile_set.append(modFile)
        
