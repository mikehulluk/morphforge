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


from ..core import MM_AlphaBetaChannel
from morphforge.core.quantities import unit
from hocmodbuilders.mmwriter_alphabeta import MM_WriterAlphaBeta
from morphforge.simulation.neuron.hocmodbuilders import HocModUtils
from morphforge.simulation.neuron import MM_Neuron_Base
from morphforge.constants.standardtags import StandardTags
from morphforge.simulation.neuron.neuronsimulationenvironment import NeuronSimulationEnvironment
from morphforge.simulation.neuron.objects.neuronrecordable import NeuronRecordableOnLocation




class MM_Neuron_AlphaBeta_Record(NeuronRecordableOnLocation):
    def __init__(self, alphaBetaChl, modvar, **kwargs):
        super( MM_Neuron_AlphaBeta_Record, self).__init__(**kwargs)
        self.alphaBetaChl = alphaBetaChl
        self.modvar=modvar

    def build_mod(self, modfile_set):
        pass

    def build_hoc(self, hocfile_obj):
        HocModUtils.create_record_from_modfile( hocfile_obj,
                                             vecname="RecVec%s"%self.name,
                                             celllocation=self.where,
                                             modvariable=self.modvar,
                                             mod_neuronsuffix=self.alphaBetaChl.get_neuron_suffix(), recordobj=self)

    def get_description(self):
        return "%s %s %s" % (self.modvar, self.alphaBetaChl.name, self.where.get_location_description_str() )





class MM_Neuron_AlphaBeta_CurrentDensityRecord(MM_Neuron_AlphaBeta_Record):
    def __init__(self, **kwargs):
        super( MM_Neuron_AlphaBeta_CurrentDensityRecord, self).__init__( modvar='i', **kwargs)
    def get_unit(self):
        return unit("mA/cm2")
    def get_std_tags(self):
        return [StandardTags.CurrentDensity]

class MM_Neuron_AlphaBeta_ConductanceDensityRecord(MM_Neuron_AlphaBeta_Record):
    def __init__(self, **kwargs):
        super( MM_Neuron_AlphaBeta_ConductanceDensityRecord, self).__init__( modvar='g', **kwargs)
    def get_unit(self):
        return unit("S/cm2")
    def get_std_tags(self):
        return [StandardTags.ConductanceDensity]


class MM_Neuron_AlphaBeta_StateVariableRecord(MM_Neuron_AlphaBeta_Record):
    def __init__(self, state, **kwargs):
        super(MM_Neuron_AlphaBeta_StateVariableRecord, self).__init__(modvar=state, **kwargs)
        assert state in self.alphaBetaChl.statevars

    def get_unit(self):
        return unit("")
    def get_std_tags(self):
        return [StandardTags.StateVariable]

class MM_Neuron_AlphaBeta_StateVariableTauRecord(MM_Neuron_AlphaBeta_Record):
    def __init__(self, state, **kwargs):
        super(MM_Neuron_AlphaBeta_StateVariableTauRecord, self).__init__(modvar=state+"tau", **kwargs)
        assert state in self.alphaBetaChl.statevars

    def get_unit(self):
        return unit("ms")
    def get_std_tags(self):
        return [StandardTags.StateTimeConstant ]


class MM_Neuron_AlphaBeta_StateVariableInfRecord(MM_Neuron_AlphaBeta_Record):
    def __init__(self, state, **kwargs):
        super(MM_Neuron_AlphaBeta_StateVariableInfRecord, self).__init__(modvar=state+'inf', **kwargs)
        assert state in self.alphaBetaChl.statevars

    def get_unit(self):
        return unit("")
    def get_std_tags(self):
        return [StandardTags.StateSteadyState ]















class MM_Neuron_AlphaBeta(MM_AlphaBetaChannel,MM_Neuron_Base):




    def __init__(self, *args, **kwargs):
        MM_AlphaBetaChannel.__init__(self,*args,**kwargs)
        MM_Neuron_Base.__init__(self)

    def get_recordable(self, what,  **kwargs):

        recorders = {
              MM_AlphaBetaChannel.Recordables.CurrentDensity: MM_Neuron_AlphaBeta_CurrentDensityRecord,
              MM_AlphaBetaChannel.Recordables.ConductanceDensity: MM_Neuron_AlphaBeta_ConductanceDensityRecord,
              MM_AlphaBetaChannel.Recordables.StateVar: MM_Neuron_AlphaBeta_StateVariableRecord,
              MM_AlphaBetaChannel.Recordables.StateVarSteadyState:MM_Neuron_AlphaBeta_StateVariableInfRecord,
              MM_AlphaBetaChannel.Recordables.StateVarTimeConstant:MM_Neuron_AlphaBeta_StateVariableTauRecord,
        }

        return recorders[what]( alphaBetaChl=self,  **kwargs  )


    def build_hoc_section( self, cell, section, hocfile_obj, mta ):
        return MM_WriterAlphaBeta.build_hoc_section( cell=cell, section=section, hocfile_obj=hocfile_obj, mta=mta)

    def create_modfile(self, modfile_set):
        MM_WriterAlphaBeta.build_Mod(alphaBetaChl=self, modfile_set=modfile_set)


    def get_mod_file_changeables(self):

        # If this fails, then the attirbute probably needs to be added to the list below:
        change_attrs = set(['name','ion','eqn','conductance','statevars','reversalpotential','mechanism_id'])
        assert set( self.__dict__) == set( ['mm_neuronNumber','cachedNeuronSuffix'] ) | change_attrs
        #['conductance', 'name','ion','eqn','conductance','statevars','reversalpotential','mm_neuronNumber', 'mechanism_id' ] )

        return dict ( [ (a, getattr(self, a)) for a in change_attrs ] )

# Register the channel
NeuronSimulationEnvironment.membranemechanisms.register_plugin( MM_AlphaBetaChannel, MM_Neuron_AlphaBeta)
