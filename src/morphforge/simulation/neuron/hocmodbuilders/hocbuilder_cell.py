#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.  All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#  - Redistributions of source code must retain the above copyright notice, 
#    this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, 
#    this list of conditions and the following disclaimer in the documentation 
#    and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------
from Cheetah.Template import Template
from morphforge.morphology.visitor.visitorbaseclasses import SectionIndexerDF
from morphforge.simulation.neuron.simulationdatacontainers import MHOCSections,  MHocFileData 



cellTemplTmpl = """

v_init = $cell.initial_voltage.rescale('mV').magnitude

// Cell Template for: $cell_template_name
#set nSections = len( $section_indexer )
begintemplate $cell_template_name
    create internalsections[ $nSections ]
    public internalsections

    proc init() {
        create internalsections[ $nSections ]

        #for $section in $cell.morphology: 
        internalsections[ $section_indexer[ $section ] ] { 
            
            
            // Section Geometry:
            L = $section.getLength
            #set p_d = $section.p_r * 2.0
            #set d_d = $section.d_r * 2.0 
            diam(0.0) = $p_d
            diam(1.0) = $d_d
            
            // Passive Parameters:
            cm = $cell.getBiophysics().getPassivePropertyForSection($section, "SpecificCapacitance" ).rescale("uF/cm2").magnitude
            Ra = $cell.getBiophysics().getPassivePropertyForSection($section, "AxialResistance" ).rescale("ohmcm").magnitude
            
            // Segmentation:
            nseg = $cell.getSegmenter().getNumSegments($section) 
            
            
            

    
        }        
        #end for  
   
        
        
        
        // Section Connections
        ///////////////////////
        
        // Non-root sections:
        #for $section in $cell.morphology:
        #if $section.isARootSection(): #continue
        // Make a Connection
        connect internalsections[ $section_indexer[ $section.parent ] ](1.0),  internalsections[ $section_indexer[ $section ] ](0.0)   
        #end for
        
        
        // Root Sections:
        #set roots = $cell.morphology.getRootSections
        #for r in roots[1:]:
        connect internalsections[ $section_indexer[ $r ] ](0.0),  internalsections[ $section_indexer[ $r ] ](0.0)
        #end for
        
    }
endtemplate $cell_template_name

"""



cellObjDeclTmpl = """
objref $cell_name 
$cell_name = new  $cell_template_name ()
"""





class HocBuilder_Cell():
    @classmethod 
    def build(cls, hocFile, cell):

        
        data = {
            'cell':cell,
            'section_indexer' : SectionIndexerDF(morph=cell.morphology)(),
            'cell_template_name' : "CellTempl_%s"%cell.name,
            'cell_name' : "cell_%s"%cell.name,
               }
        
        # Create the Cell Topology Template:
        hocFile.addToSection( MHOCSections.InitTemplates,  Template(cellTemplTmpl, data).respond() )
        hocFile.addToSection( MHOCSections.InitCells,  Template(cellObjDeclTmpl, data).respond() )
        
        
        # Save the data about this cell:
        hocFile[MHocFileData.Cells][cell] = data
        
        
        # Create the membrane properties:
        cb = cell.getBiophysics()
        for section in cell.morphology:
            #print section, section.region
            for mta in cb.getResolvedMTAsForSection(section):
                mta.mechanism.build_HOC_Section( cell=cell, section=section, hocFile=hocFile, mta=mta )
                
