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




class MM_WriterAlphaBetaBeta(object):
    
    
    
    chlHoc = """
    
$(cell_name).internalsections [ $section_index ] {
    // AlphaBetaBeta Channels 
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
    def build_HOC_Section(self, cell, section, hocFile, mta ):
        
        cell_name = hocFile[MHocFileData.Cells][cell]['cell_name']
        section_index = hocFile[MHocFileData.Cells][cell]['section_indexer'][section]
        
        neuronSuffix = mta.mechanism.get_neuron_suffix()
        
        
        # Calculate the values of the variables for the section:
        variables = []
        for variable_name in mta.mechanism.get_variables():
            variable_value_with_unit = mta.applicator.get_variable_value_for_section(variable_name=variable_name, section=section)
            variable_unit = MM_WriterAlphaBetaBeta.Units[variable_name]
            variable_value_nounit = variable_value_with_unit.rescale(variable_unit).magnitude 
            variables.append( [variable_name,variable_value_nounit, variable_value_with_unit,variable_unit] )
            
        tmplDict = {
                    "cell_name":cell_name,
                    "section_index":section_index,
                    "neuron_suffix":neuronSuffix,
                    "variables":variables
                    }
        
        # Add the data to the HOC file
        hocFile.add_to_section( MHOCSections.InitCellMembranes,  Template(MM_WriterAlphaBetaBeta.chlHoc,tmplDict ).respond() )
    


    @classmethod
    def build_Mod(cls, alphaBetaBetaChl, modFileSet):
        
        gbarName = "gBar" 
        eRevName = "eLk"
        gScaleName = "gScale"  
        
        #gbarUnits = MM_WriterAlphaBetaBeta.Units[gbarName]
        #eRevUnits = MM_WriterAlphaBetaBeta.Units[eRevName]
        
        
        
        baseWriter = MM_ModFileWriterBase( suffix=alphaBetaBetaChl.get_neuron_suffix() )
        
        # Naming Conventions:
        stateTau = lambda s: "%stau" % s
        stateInf = lambda s: "%sinf" % s
        stateAlpha = lambda s: "%s_alpha" % s
        stateBeta = lambda s: "%s_beta" % s
        
        
        
        # State Equations and initial values:
        for s in alphaBetaBetaChl.statevars:
            baseWriter.internalstates[s] = "%s" % stateInf(s) , "%s'=(%s-%s)/%s" % (s, stateInf(s), s, stateTau(s)) 
        
        # Parameters:
        # {name: (value, unit,range)}
        baseWriter.parameters = { 
                      #gbarName: (alphaBetaBetaChl.conductance.toval(ounit="S/cm2"), ("S/cm2"), None),
                      #eRevName: (alphaBetaBetaChl.reversalpotential.toval("mV"), ("mV"), None)
                      gbarName: (alphaBetaBetaChl.conductance.rescale("S/cm2").magnitude, ("S/cm2"), None),
                      eRevName: (alphaBetaBetaChl.reversalpotential.rescale("mV").magnitude, ("mV"), None),
                      gScaleName: (1.0, None, None)
                      }
        
        # Rates:
        # name : (locals, code), unit
        for s in alphaBetaBetaChl.statevars:
            baseWriter.rates[ stateAlpha(s) ] = (("", stateAlpha(s) + "= StdAlphaBeta( %f,%f,%f,%f,%f, v)" % tuple(alphaBetaBetaChl.statevars[s][0]))), None
            #baseWriter.rates[ stateBeta(s) ] = (("", stateBeta(s) + "= StdBetaBeta( %f,%f,%f,%f,%f,  %f,%f,%f,%f,%f,  %f,  v)" % tuple(alphaBetaBetaChl.statevars[s][1] + alphaBetaBetaChl.statevars[s][2] + [alphaBetaBetaChl.beta2threshold.toval(ounit="mV")]))), None
            baseWriter.rates[ stateBeta(s) ] = (("", stateBeta(s) + "= StdBetaBeta( %f,%f,%f,%f,%f,  %f,%f,%f,%f,%f,  %f,  v)" % tuple(alphaBetaBetaChl.statevars[s][1] + alphaBetaBetaChl.statevars[s][2] + [alphaBetaBetaChl.beta2threshold.rescale("mV").magnitude]))), None
            baseWriter.rates[ stateInf(s) ] = (("", stateInf(s) + "= %s/(%s+%s)" % (stateAlpha(s), stateAlpha(s), stateBeta(s))), None)
            baseWriter.rates[ stateTau(s) ] = (("", stateTau(s) + "= 1.0/(%s+%s)" % (stateAlpha(s), stateBeta(s))), "ms")
            baseWriter.ratecalcorder.extend([stateAlpha(s), stateBeta(s), stateInf(s), stateTau(s)])
            
        baseWriter.currentequation = "(v-%s) * %s * %s * %s" % (eRevName, gbarName, alphaBetaBetaChl.eqn, gScaleName)
        baseWriter.conductanceequation = " %s * %s * %s" % (gbarName, alphaBetaBetaChl.eqn, gScaleName)
        
        #baseWriter.currentequation = "(v-%s) * %s * %s" % (eRevName, gbarName, alphaBetaBetaChl.eqn)
        baseWriter.functions = """
                    FUNCTION StdAlphaBeta(A,B,C,D,E,V){ StdAlphaBeta = (A + B*V) / (C + exp((D+V)/E)) } 
                    FUNCTION StdBetaBeta(A,B,C,D,E, A2,B2,C2,D2,E2, beta2Threshold, V)
                    {
                        if( V < beta2Threshold )
                        {
                            StdBetaBeta = (A + B*V) / (C + exp((D+V)/E))
                        }
                        else
                        {
                           StdBetaBeta = (A2 + B2*V) / (C2 + exp((D2+V)/E2))
                        } 
                    } 
                    """
        txt =  baseWriter.generate_modfile()
        modFile = ModFile(name=alphaBetaBetaChl.name, modtxt=txt )
        modFileSet.append(modFile)
        
        

