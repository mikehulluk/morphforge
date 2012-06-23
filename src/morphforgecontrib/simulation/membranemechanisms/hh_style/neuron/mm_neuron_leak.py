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
from ..core import MM_LeakChannel
from morphforge.core.quantities import unit
from hocmodbuilders.mmwriter_leak import MM_WriterLeak
from morphforge.simulation.neuron.hocmodbuilders import HocModUtils
from morphforge.simulation.neuron import MM_Neuron_Base
from morphforge.constants.standardtags import StandardTags
from morphforge.simulation.neuron.neuronsimulationenvironment import NeuronSimulationEnvironment

from morphforge.simulation.neuron.objects.neuronrecordable import NeuronRecordableOnLocation



class MM_Neuron_Leak_Record(NeuronRecordableOnLocation):
    def __init__(self, lkchannel, modvar, **kwargs):
        super( MM_Neuron_Leak_Record, self).__init__(**kwargs)
        self.leakChl = lkchannel
        self.modvar=modvar

    def build_mod(self, modfile_set):
        pass

    def build_hoc(self, hocfile_obj):
        HocModUtils.create_record_from_modfile( hocfile_obj,
                                             vecname="RecVec%s"%self.name,
                                             celllocation=self.where,
                                             modvariable=self.modvar,
                                             mod_neuronsuffix=self.leakChl.get_neuron_suffix(), recordobj=self)





class MM_Neuron_Leak_ConductanceDensityRecord(MM_Neuron_Leak_Record):
    def __init__(self, **kwargs):
        super( MM_Neuron_Leak_ConductanceDensityRecord, self).__init__( modvar='g', **kwargs)
    def get_unit(self):
        return unit("S/cm2")
    def get_std_tags(self):
        return [StandardTags.ConductanceDensity]


    def get_description(self):
        t1 ="g %s "%( self.leakChl.name)
        r = "%s"%self.where.cell.name
        t = ":%s"% self.where.morphlocation.section.idTag if self.where.morphlocation.section.idTag else ""
        return t1 + r + t


class MM_Neuron_Leak_CurrentDensityRecord(MM_Neuron_Leak_Record):
    def __init__(self, **kwargs):
        super( MM_Neuron_Leak_CurrentDensityRecord, self).__init__( modvar='i', **kwargs)

    def get_unit(self):
        return unit("mA/cm2")
    def get_std_tags(self):
        return [StandardTags.CurrentDensity]

    def get_description(self):
        t1 ="i %s "%( self.leakChl.name)
        r = "%s"%self.where.cell.name
        t = ":%s"% self.where.morphlocation.section.idTag if self.where.morphlocation.section.idTag else ""
        return t1 + r + t



class MM_Neuron_Leak(MM_LeakChannel,MM_Neuron_Base):


    def __init__(self, *args, **kwargs):
        MM_LeakChannel.__init__(self,*args,**kwargs)
        MM_Neuron_Base.__init__(self)

    def get_recordable(self, what, **kwargs):

        recorders = {
              MM_LeakChannel.Recordables.CurrentDensity: MM_Neuron_Leak_CurrentDensityRecord,
              MM_LeakChannel.Recordables.ConductanceDensity: MM_Neuron_Leak_ConductanceDensityRecord,
        }

        return recorders[what]( lkchannel=self,  **kwargs )


    def build_hoc_section( self, cell, section, hocfile_obj, mta ):
        return MM_WriterLeak.build_hoc_section( cell=cell, section=section, hocfile_obj=hocfile_obj, mta=mta)

    def create_modfile(self, modfile_set):
        m = MM_WriterLeak.build_Mod(leakChl=self, modfile_set=modfile_set)

    def get_mod_file_changeables(self):

        # If this fails, then the attirbute probably needs to be added to the list below:
        change_attrs = set( ['conductance', 'name','reversalpotential','mechanism_id' ] )
        assert set( self.__dict__) == set( ['mm_neuronNumber','cachedNeuronSuffix'] ) | change_attrs
        return dict ( [ (a, getattr(self, a)) for a in change_attrs ] )


# Register the channel
#NeuronSimulationEnvironment.registerMembraneMechanism( MM_LeakChannel, MM_Neuron_Leak)
NeuronSimulationEnvironment.membranemechanisms.register_plugin( MM_LeakChannel, MM_Neuron_Leak)

