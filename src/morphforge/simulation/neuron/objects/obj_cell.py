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
from morphforge.core.quantities  import unit

 
from neuronobject import NeuronObject
from morphforge.simulation.core import Cell

from morphforge.simulation.neuron.hocmodbuilders import HocBuilder
from morphforge.simulation.neuron.simulationdatacontainers import MHOCSections,  MHocFileData 
from morphforge.simulation.neuron.objects.neuronrecordable import NeuronRecordable


from Cheetah.Template import Template
from morphforge.constants.standardtags import StandardTags





class MembraneVoltageRecord(NeuronRecordable):
    
    initial_buffer_size = 50000
    
    tmplObjRef = """
objref $recVecName
$recVecName = new Vector()
${recVecName}.buffer_size(%d)
${recVecName}.record(& ${cellname}.internalsections[${sectionindex}].v ( $sectionpos ) )
    """%initial_buffer_size

    def __init__(self, cell, location=None, **kwargs):
        
        
        super(MembraneVoltageRecord,self).__init__(**kwargs)
        self.cell = cell
        self.location = location if location is not None else cell.getLocation("soma")
        
        
        
    def getUnit(self):
        return unit("mV")
    
    def getStdTags(self):
        return [StandardTags.Voltage] 
    
    def getDescription(self):
        r = "Vm %s"%self.location.cell.name
        t = ":%s"% self.location.morphlocation.section.idTag if self.location.morphlocation.section.idTag else "" 
        return r + t
    
    
    def buildHOC(self, hocFile):
        cell = self.location.cell
        section = self.location.morphlocation.section
        cell_name = hocFile[MHocFileData.Cells][cell]['cell_name']
        section_index = hocFile[MHocFileData.Cells][cell]['section_indexer'][section]
        
        
        
        #nameHoc = hocFile[MHocFileData.CurrentClamps][self.cclamp]["stimname"]
        #HocModUtils.CreateRecordFromObject( hocFile=hocFile, vecname="RecVec%s"%self.name, objname=cell_name, objvar="v", recordobj=self )
        
        
        tmplDict = {
                    "recVecName": self.name,
                    "cellname":cell_name,
                    "sectionindex":section_index,
                    "sectionpos":self.location.morphlocation.sectionpos,
                    }
        print tmplDict
        
        hocFile.addToSection( MHOCSections.InitRecords,  Template(MembraneVoltageRecord.tmplObjRef,tmplDict).respond() )
        
        hocFile[MHocFileData.Recordables][self] = tmplDict
        
        
    def buildMOD(self, modFileSet):
        pass








class MNeuronCell(Cell, NeuronObject):
    def buildHOC(self, hocFile):
        HocBuilder.Cell(hocFile=hocFile, cell=self)
    
    def buildMOD(self, modFileSet):
        mechanisms = set( [ mta.mechanism for mta in self.getBiophysics().appliedmechanisms ] )
        for m in mechanisms:
            m.createModFile( modFileSet)
     
    def getRecordable(self, what, **kwargs): 
        recordables = {
            MNeuronCell.Recordables.MembraneVoltage : MembraneVoltageRecord,
        }
        return recordables[what](cell=self, **kwargs)
