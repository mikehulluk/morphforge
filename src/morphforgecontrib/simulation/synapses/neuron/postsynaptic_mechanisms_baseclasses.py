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
from morphforge.simulation.neuron.objects.neuronrecordable import NeuronRecordable
from morphforge.core.quantities import unit
from morphforge.constants.standardtags import StandardTags
from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import MHocFileData

from morphforge.simulation.neuron.hocmodbuilders.hocmodutils import HocModUtils
from morphforge.simulation.core.networks import Synapse





class Neuron_PSM_Std_CurrentRecord(NeuronRecordable):

    def __init__(self, neuron_syn_post, **kwargs):
        super(Neuron_PSM_Std_CurrentRecord, self).__init__(**kwargs)
        self.neuron_syn_post = neuron_syn_post

    def get_unit(self):
        return unit("nA")
    def get_std_tags(self):
        return [StandardTags.Current, Synapse.Recordables.SynapticCurrent]

    def build_hoc(self, hocfile_obj):
        objNameHoc = hocfile_obj[MHocFileData.Synapses][self.neuron_syn_post.synapse]["POST"]["synnamepost"]
        HocModUtils.create_record_from_object( hocfile_obj=hocfile_obj, vecname="RecVec%s"%self.name, objname=objNameHoc, objvar="i", recordobj=self )
                
    def build_mod(self, modfile_set):
        pass    
        
    
class Neuron_PSM_Std_ConductanceRecord(NeuronRecordable):

    def __init__(self, neuron_syn_post, **kwargs):
        super(Neuron_PSM_Std_ConductanceRecord, self).__init__(**kwargs)
        self.neuron_syn_post = neuron_syn_post

    def get_unit(self):
        return unit("uS")
    def get_std_tags(self):
        return [StandardTags.Conductance,Synapse.Recordables.SynapticConductance]

    def build_hoc(self, hocfile_obj):
        objNameHoc = hocfile_obj[MHocFileData.Synapses][self.neuron_syn_post.synapse]["POST"]["synnamepost"]
        HocModUtils.create_record_from_object( hocfile_obj=hocfile_obj, vecname="RecVec%s"%self.name, objname=objNameHoc, objvar="g", recordobj=self )

    def build_mod(self, modfile_set):
        pass    
    
    
      
        
