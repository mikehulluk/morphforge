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
from ..core import MM_AlphaBetaBetaChannel
from morphforge.core.quantities import unit
from hocmodbuilders.mmwriter_alphabetabeta import MM_WriterAlphaBetaBeta
from morphforge.simulation.neuron.hocmodbuilders import HocModUtils
from morphforge.simulation.neuron import MM_Neuron_Base
from morphforge.constants.standardtags import StandardTags
from morphforge.simulation.neuron.neuronsimulationenvironment import NeuronSimulationEnvironment
from morphforge.simulation.neuron.objects.neuronrecordable import NeuronRecordableOnLocation









class MM_Neuron_AlphaBetaBeta_Record(NeuronRecordableOnLocation):
    def __init__(self, alphaBetaBetaChl, modvar, **kwargs):
        super( MM_Neuron_AlphaBetaBeta_Record, self).__init__(**kwargs)
        self.alphaBetaBetaChl = alphaBetaBetaChl
        self.modvar=modvar

    def buildMOD(self, modFileSet):
        pass   
 
    def buildHOC(self, hocFile):
        HocModUtils.CreateRecordFromModFile( hocFile, 
                                             vecname="RecVec%s"%self.name, 
                                             celllocation=self.where, 
                                             modvariable=self.modvar, 
                                             mod_neuronsuffix=self.alphaBetaBetaChl.getNeuronSuffix(), recordobj=self)

    def getDescription(self):
        return "%s %s %s" % (self.modvar, self.alphaBetaBetaChl.name, self.where.getLocationDescriptionStr() )




class MM_Neuron_AlphaBetaBeta_CurrentDensityRecord(MM_Neuron_AlphaBetaBeta_Record):
    def __init__(self, **kwargs):
        super( MM_Neuron_AlphaBetaBeta_CurrentDensityRecord, self).__init__( modvar='i', **kwargs)
    def getUnit(self):
        return unit("mA/cm2")
    def getStdTags(self):
        return [StandardTags.CurrentDensity]

class MM_Neuron_AlphaBetaBeta_ConductanceDensityRecord(MM_Neuron_AlphaBetaBeta_Record):
    def __init__(self, **kwargs):
        super( MM_Neuron_AlphaBetaBeta_ConductanceDensityRecord, self).__init__( modvar='cond', **kwargs)
    def getUnit(self):
        return unit("S/cm2")
    def getStdTags(self):
        return [StandardTags.ConductanceDensity]


class MM_Neuron_AlphaBetaBeta_StateVariableRecord(MM_Neuron_AlphaBetaBeta_Record):
    def __init__(self, state, **kwargs):
        super(MM_Neuron_AlphaBetaBeta_StateVariableRecord, self).__init__(modvar=state, **kwargs)
   
    def getUnit(self):
        return unit("")
    def getStdTags(self):
        return [StandardTags.StateVariable]

class MM_Neuron_AlphaBetaBeta_StateVariableTauRecord(MM_Neuron_AlphaBetaBeta_Record):
    def __init__(self, state, **kwargs):
        super(MM_Neuron_AlphaBetaBeta_StateVariableTauRecord, self).__init__(modvar=state+"tau", **kwargs)
    
    def getUnit(self):
        return unit("ms")
    def getStdTags(self):
        return [StandardTags.StateTimeConstant ] 

   
class MM_Neuron_AlphaBetaBeta_StateVariableInfRecord(MM_Neuron_AlphaBetaBeta_Record):
    def __init__(self, state, **kwargs):
        super(MM_Neuron_AlphaBetaBeta_StateVariableInfRecord, self).__init__(modvar=state+'inf', **kwargs)
     
    def getUnit(self):
        return unit("")
    def getStdTags(self):
        return [StandardTags.StateSteadyState ] 














#from morphforge.simulation.core.biophysics.membranemechanisms.mmalphaBetaBetabeta import MM_AlphaBetaBetaBetaChannel
##from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import MHocFileData,\
##    MHOCSections
##from Cheetah.Template import Template
#
#from morphforge.core import unit
#from ..hocmodbuilders.membranemechanisms.mmwriter_alphaBetaBetabeta import MM_WriterAlphaBetaBetaBeta
#
#
#    
#from ..hocmodbuilders import HocModUtils
#
#from mm_neuron import MM_Neuron_Base
#from morphforge.simulation.neuron.neuronsimulationenvironment import NeuronSimulationEnvironment


#    
#
#class MM_Neuron_AlphaBetaBetaBeta_CurrentRecord(NeuronRecordableOnLocation):
#
# def __init__(self, alphaBetaBetaChl, modvar, **kwargs):
#        super( MM_Neuron_AlphaBetaBeta_Record, self).__init__(**kwargs)
#        self.alphaBetaBetaChl = alphaBetaBetaChl
#        self.modvar=modvar
#
#
#    def __init__(self, alphaBetaBetaChl, modvar, **kwargs):
#        super( MM_Neuron_AlphaBetaBetaBeta_CurrentRecord, self).__init__(**kwargs)
#        
#        #self.name = name
#        self.alphaBetaBetaBetaChl = alphaBetaBetaBetaChl
#        self.modvar=modvar
#        #self.celllocation = celllocation
#
#    def getUnit(self):
#        return unit("mA/cm2")
#    def getStdTags(self):
#        return [StandardTags.CurrentDensity]
#
#
#    def buildHOC(self, hocFile):
#        HocModUtils.CreateRecordFromModFile( hocFile, vecname="RecVec%s"%self.name, celllocation=self.celllocation, modvariable="i", mod_neuronsuffix=self.alphaBetaBetaBetaChl.getNeuronSuffix(), recordobj=self)
#                
#    def buildMOD(self, modFileSet):
#        pass    



















class MM_Neuron_AlphaBetaBeta(MM_AlphaBetaBetaChannel,MM_Neuron_Base):


    def __init__(self, *args, **kwargs):
        MM_AlphaBetaBetaChannel.__init__(self,*args,**kwargs)
        MM_Neuron_Base.__init__(self)

    
        
    
    
    def build_HOC_Section( self, cell, section, hocFile, mta ):
        return MM_WriterAlphaBetaBeta.build_HOC_Section( cell=cell, section=section, hocFile=hocFile, mta=mta)
    
    
    
    def createModFile(self, modFileSet):
        MM_WriterAlphaBetaBeta.build_Mod(alphaBetaBetaChl=self, modFileSet=modFileSet)
        
    
    def getRecordable(self, what, name, **kwargs):
        #assert False
        
        celllocation = kwargs["celllocation"] if "celllocation" in kwargs else kwargs["where"]
        if "celllocation" in kwargs: del kwargs["celllocation"]
        if "where" in kwargs: del kwargs["where"]
        
        recorders = {
              MM_AlphaBetaBetaBetaChannel.Recordables.CurrentDensity: MM_Neuron_AlphaBetaBeta_CurrentDensityRecord,
             
        }
        
        return recorders[what]( alphaBetaBetaChl=self, celllocation= celllocation, name=name, **kwargs  )
        
        
    def getModFileChangeables(self):
        
         # If this fails, then the attirbute probably needs to be added to the list below:
        change_attrs = set(['conductance','beta2threshold', 'name','ion','eqn','conductance','statevars','reversalpotential', 'mechanism_id' ] )
        assert set( self.__dict__) == set( ['mm_neuronNumber', 'cachedNeuronSuffix'] ) | change_attrs
        
        attrs = ['name','ion','eqn','conductance','statevars','reversalpotential','mechanism_id','beta2threshold']
        return dict ( [ (a, getattr(self, a)) for a in attrs ] )
        
        
        
# Register the channel
#NeuronSimulationEnvironment.registerMembraneMechanism( MM_AlphaBetaBetaChannel, MM_Neuron_AlphaBetaBeta)
NeuronSimulationEnvironment.membranemechanisms.registerPlugin(MM_AlphaBetaBetaChannel, MM_Neuron_AlphaBetaBeta)
