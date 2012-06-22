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
from core import MM_InfTauInterpolatedChannel
from morphforge.core.quantities import unit
from mmwriter_infatauinterpolated import MM_WriterInfTauInterpolated
from morphforge.simulation.neuron.hocmodbuilders import MM_ModFileWriterBase
from morphforge.simulation.neuron.hocmodbuilders import HocModUtils
from morphforge.simulation.neuron import MM_Neuron_Base
from morphforge.constants.standardtags import StandardTags
from morphforge.simulation.neuron.neuronsimulationenvironment import NeuronSimulationEnvironment
from morphforge.simulation.neuron.objects.neuronrecordable import NeuronRecordable, NeuronRecordableOnLocation


class MM_Neuron_InfTauInterpolated_Record(NeuronRecordableOnLocation):
    def __init__(self, alphaBetaChl, modvar, **kwargs):
        super( MM_Neuron_InfTauInterpolated_Record, self).__init__(**kwargs)
        self.alphaBetaChl = alphaBetaChl
        self.modvar=modvar

    def build_mod(self, modFileSet):
        pass   
 
    def build_hoc(self, hocFile):
        HocModUtils.create_record_from_modfile( hocFile, 
                                             vecname="RecVec%s"%self.name, 
                                             celllocation=self.where, 
                                             modvariable=self.modvar, 
                                             mod_neuronsuffix=self.alphaBetaChl.get_neuron_suffix(), recordobj=self)





class MM_Neuron_InfTauInterpolated_CurrentDensityRecord(MM_Neuron_InfTauInterpolated_Record):
    def __init__(self, **kwargs):
        super( MM_Neuron_InfTauInterpolated_CurrentDensityRecord, self).__init__( modvar='i', **kwargs)
    def getUnit(self):
        return unit("mA/cm2")
    def get_std_tags(self):
        return [StandardTags.CurrentDensity]

class MM_Neuron_InfTauInterpolated_ConductanceDensityRecord(MM_Neuron_InfTauInterpolated_Record):
    def __init__(self, **kwargs):
        super( MM_Neuron_InfTauInterpolated_ConductanceDensityRecord, self).__init__( modvar='g', **kwargs)
    def getUnit(self):
        return unit("S/cm2")
    def get_std_tags(self):
        return [StandardTags.ConductanceDensity]


class MM_Neuron_InfTauInterpolated_StateVariableRecord(MM_Neuron_InfTauInterpolated_Record):
    def __init__(self, state, **kwargs):
        super(MM_Neuron_InfTauInterpolated_StateVariableRecord, self).__init__(modvar=state, **kwargs)
   
    def getUnit(self):
        return unit("")
    def get_std_tags(self):
        return [StandardTags.StateVariable]

class MM_Neuron_InfTauInterpolated_StateVariableTauRecord(MM_Neuron_InfTauInterpolated_Record):
    def __init__(self, state, **kwargs):
        super(MM_Neuron_InfTauInterpolated_StateVariableTauRecord, self).__init__(modvar=state+"tau", **kwargs)
    
    def getUnit(self):
        return unit("ms")
    def get_std_tags(self):
        return [StandardTags.StateTimeConstant ] 

   
class MM_Neuron_InfTauInterpolated_StateVariableInfRecord(MM_Neuron_InfTauInterpolated_Record):
    def __init__(self, state, **kwargs):
        super(MM_Neuron_InfTauInterpolated_StateVariableInfRecord, self).__init__(modvar=state+'inf', **kwargs)
     
    def getUnit(self):
        return unit("")
    def get_std_tags(self):
        return [StandardTags.StateSteadyState ] 

      













class MM_Neuron_InfTauInterpolated(MM_InfTauInterpolatedChannel,MM_Neuron_Base):

    


    def __init__(self, *args, **kwargs):
        MM_InfTauInterpolatedChannel.__init__(self,*args,**kwargs)
        MM_Neuron_Base.__init__(self)

    def get_recordable(self, what,  **kwargs):
        
        print 'Getting Reordable', what
        print kwargs
        
        recorders = {
              MM_InfTauInterpolatedChannel.Recordables.CurrentDensity: MM_Neuron_InfTauInterpolated_CurrentDensityRecord,
              MM_InfTauInterpolatedChannel.Recordables.ConductanceDensity: MM_Neuron_InfTauInterpolated_ConductanceDensityRecord,
              MM_InfTauInterpolatedChannel.Recordables.StateVar: MM_Neuron_InfTauInterpolated_StateVariableRecord,
              MM_InfTauInterpolatedChannel.Recordables.StateVarSteadyState:MM_Neuron_InfTauInterpolated_StateVariableInfRecord,
              MM_InfTauInterpolatedChannel.Recordables.StateVarTimeConstant:MM_Neuron_InfTauInterpolated_StateVariableTauRecord,
        }
        print 'Getting Reordable', what, recorders[what]
        print kwargs
        
        return recorders[what]( alphaBetaChl=self,  **kwargs  )
    
    
    def build_HOC_Section( self, cell, section, hocFile, mta ):
        return MM_WriterInfTauInterpolated.build_HOC_Section( cell=cell, section=section, hocFile=hocFile, mta=mta)
    
    def createModFile(self, modFileSet):
        MM_WriterInfTauInterpolated.build_Mod(alphaBetaChl=self, modFileSet=modFileSet)
        

    def getModFileChangeables(self):
        
         # If this fails, then the attirbute probably needs to be added to the list below:
        change_attrs = set(['conductance', 'name','ion','eqn','conductance','statevars_new','reversalpotential', 'mechanism_id' ])
        assert set( self.__dict__) == set( ['mm_neuronNumber', 'cachedNeuronSuffix' ] ) | change_attrs
        
        #attrs = ['name','ion','eqn','conductance','statevars_new','reversalpotential','mechanism_id']
        return dict ( [ (a, getattr(self, a)) for a in change_attrs ] )
    
    
        
# Register the channel
#NeuronSimulationEnvironment.registerMembraneMechanism( MM_InfTauInterpolatedChannel, MM_Neuron_InfTauInterpolated)
NeuronSimulationEnvironment.membranemechanisms.register_plugin(MM_InfTauInterpolatedChannel, MM_Neuron_InfTauInterpolated)         
