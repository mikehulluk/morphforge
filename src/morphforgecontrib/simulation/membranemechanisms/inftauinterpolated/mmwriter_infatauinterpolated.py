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



class MM_WriterInfTauInterpolated(object):
    
    
    
    chlHoc = """
    
$(cell_name).internalsections [ $section_index ] {
    // InfTauInterpolated Channels 
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
    def build_HOC_Section(cls, cell, section, hocFile, mta ):
        
        cell_name = hocFile[MHocFileData.Cells][cell]['cell_name']
        section_index = hocFile[MHocFileData.Cells][cell]['section_indexer'][section]
        
        neuronSuffix = mta.mechanism.getNeuronSuffix()
        
        
        # Calculate the values of the variables for the section:
        variables = []
        for variable_name in mta.mechanism.getVariables():
            variable_value_with_unit = mta.applicator.getVariableValueForSection(variable_name=variable_name, section=section)
            variable_unit = MM_WriterInfTauInterpolated.Units[variable_name]
            variable_value_nounit = variable_value_with_unit.rescale(variable_unit).magnitude 
            variables.append( [variable_name,variable_value_nounit, variable_value_with_unit,variable_unit] )
            
        tmplDict = {
                    "cell_name":cell_name,
                    "section_index":section_index,
                    "neuron_suffix":neuronSuffix,
                    "variables":variables
                    }
        
        # Add the data to the HOC file
        hocFile.addToSection( MHOCSections.InitCellMembranes,  Template(MM_WriterInfTauInterpolated.chlHoc,tmplDict ).respond() )
    


    @classmethod
    def build_Mod(cls, alphaBetaChl, modFileSet):
        
        gbarName = "gBar" 
        eRevName = "eRev"
        gScaleName = "gScale"  
         
        baseWriter = MM_ModFileWriterBase(suffix=alphaBetaChl.getNeuronSuffix())
        
        # Naming Conventions:
        stateTau = lambda s: "%stau" % s
        stateInf = lambda s: "%sinf" % s
        
        
        # State Equations and initial values:
        for s in alphaBetaChl.statevars_new:
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
        for s in alphaBetaChl.statevars_new:
            baseWriter.rates[ stateInf(s) ] = (("", stateInf(s) + "= %sInf(v)"%stateInf(s)), None)
            baseWriter.rates[ stateTau(s) ] = (("", stateTau(s) + "= %sTau(v)"%stateTau(s)), "ms")
            baseWriter.ratecalcorder.extend([stateInf(s), stateTau(s)])
            
        baseWriter.currentequation = "(v-%s) * %s * %s * %s" % (eRevName, gbarName, alphaBetaChl.eqn, gScaleName)
        baseWriter.conductanceequation = " %s * %s * %s" % (gbarName, alphaBetaChl.eqn, gScaleName)
        
        
        
        baseWriter.functions = """
        VERBATIM
        #include <gsl_wrapper.h>
        ENDVERBATIM"""
        
        
        def buildInterpolatorFunc(state, inftau, funcname):
            if inftau=='inf':
                interp_strX = ",".join( ["%2.2f"%x for x in  alphaBetaChl.statevars_new[s].V ] )
                interp_strY = ",".join( ["%2.2f"%x for x in  alphaBetaChl.statevars_new[s].inf ] )
            elif inftau=='tau':
                interp_strX = ",".join( ["%2.2f"%x for x in  alphaBetaChl.statevars_new[s].V ] )
                interp_strY = ",".join( ["%2.2f"%x for x in  alphaBetaChl.statevars_new[s].tau ] )
            else: 
                assert False
                
            
            vars = {'chlname':stateTau(s),'nPts':len(alphaBetaChl.statevars_new[s].V), 'x0':interp_strX,'y0':interp_strY, 'funcname':funcname }
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
                        pInterpolator = makeIntWrapper(x,y, nPts);
                    }
                    _l%(funcname)s= interpolate2( _lV, pInterpolator);
                }
                ENDVERBATIM
            } 
            \n\n""" % vars
            return f
        
        
        for s in alphaBetaChl.statevars_new:
            baseWriter.functions +=  buildInterpolatorFunc(state=s, inftau='inf', funcname='%sinfInf'%s )
            baseWriter.functions +=  buildInterpolatorFunc(state=s, inftau='tau', funcname='%stauTau'%s )

         
         
        txt =  baseWriter.GenerateModFile()

        # TODO: Remove hard dependancy here
        additional_compile_flags = "-I/home/michael/hw_to_come/morphforge/src/morphforgecontrib/simulation/neuron_gsl/cpp"
        additional_link_flags = "-L/home/michael/hw_to_come/morphforge/src/morphforgecontrib/simulation/neuron_gsl/cpp -lgslwrapper -lgsl -lgslcblas"
        modFile =  ModFile(name=alphaBetaChl.name, modtxt=txt, additional_compile_flags=additional_compile_flags, additional_link_flags=additional_link_flags )
        modFileSet.append(modFile)
        
