#!/usr/bin/python
# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  - Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------

from morphforge.simulation.neuron.objects.neuronrecordable import NEURONRecordable
from morphforge.constants.standardtags import StandardTags
from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import MHocFileData
from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import MHOCSections
from morphforge.simulation.neuron.hocmodbuilders.hocmodutils import HocModUtils
from morphforgecontrib.simulation.stimulation.currentclamps.ramp.currentclamp_ramp_core import CurrentClampRamp
from morphforge.simulation.neuron.objects.neuronobject import NEURONObject
from morphforge.units import qty
from morphforge.simulation.neuron.biophysics.modfile import ModFile
from Cheetah.Template import Template
from morphforge.core import ObjectLabeller



currentclamprampTxt = """
COMMENT
TODO: ATTRIBUTION.
ENDCOMMENT


NEURON {
        POINT_PROCESS CurrentClampRamp
        RANGE amp0, amp1, time0, time1, time2
        ELECTRODE_CURRENT i
}

UNITS {
        (nA) = (nanoamp)
             }

PARAMETER {
        amp0=0   (nA)
        amp1=0   (nA)
        time0=1  (ms)
        time1=2  (ms)
        time2=3  (ms)
        
}

ASSIGNED {
        i (nA)
}

UNITSOFF
BREAKPOINT {
    at_time(time0)
    at_time(time1)
    at_time(time2)
    

    if (t < time0) {
          i=0
       }else{ 
          if (t < time1) {
               i = (t-time0) /(time1-time0) * (amp1-amp0) + amp0
          }else{
            if (t < time2) {
               i=amp1
            }
        else{
            i=0
            }
        
}}}
"""




ccRampHOCTmpl = """
// Post-Synapse [$stimname]
objref $stimname
${cellname}.internalsections[$sectionindex] $stimname = new CurrentClampRamp ($sectionpos)
${stimname}.amp0 =   $amp0.rescale("nA").magnitude
${stimname}.amp1 =   $amp1.rescale("nA").magnitude

${stimname}.time0 =   $time0.rescale("ms").magnitude
${stimname}.time1 =   $time1.rescale("ms").magnitude
${stimname}.time2 =   $time2.rescale("ms").magnitude

"""
from morphforge import units


class NeuronRampCurrentClampCurrentRecord(NEURONRecordable):

    def __init__(self, cclamp, **kwargs):
        super(NeuronRampCurrentClampCurrentRecord, self).__init__(**kwargs)
        self.cclamp = cclamp

    def get_unit(self):
        return units.nA

    def get_std_tags(self):
        return [StandardTags.Current]

    def build_hoc(self, hocfile_obj):
        objNameHoc = hocfile_obj[MHocFileData.CurrentClamps][self.cclamp]["stimname"]
        HocModUtils.create_record_from_object(hocfile_obj=hocfile_obj, vecname="RecVec%s" % self.name, objname=objNameHoc, objvar="i", recordobj=self)

    def build_mod(self, modfile_set):
        pass
    def get_description(self):
        return 'Ramp CurrentClamp Injection: %s' % self.cclamp.name


class NEURONCurrentClampRamp(CurrentClampRamp, NEURONObject):

    def __init__(self, **kwargs):
        super(NEURONCurrentClampRamp, self).__init__(**kwargs)

    def build_hoc(self, hocfile_obj):
        cell = self.cell_location.cell
        section = self.cell_location.morphlocation.section

        cell_hoc = hocfile_obj[MHocFileData.Cells][cell]
        data = {
            'stimname': self.get_name(),
            'cell': cell,
            'cellname': cell_hoc['cell_name'],
            'sectionindex': cell_hoc['section_indexer'][section],
            'sectionpos': self.cell_location.morphlocation.sectionpos,
            
            'amp0': self.amp0,
            'amp1': self.amp1,
            'time0': self.time0,
            'time1': self.time1,
            'time2': self.time2,
            }

        hoc_txt = Template(ccRampHOCTmpl, data).respond()
        hocfile_obj.add_to_section(MHOCSections.InitCurrentClamps, hoc_txt)
        hocfile_obj[MHocFileData.CurrentClamps][self] = data



    def build_mod(self, modfile_set):
        modfile = ModFile(modtxt=currentclamprampTxt,
                          name='NeuronRampCurrentClamp')
        modfile_set.append(modfile)

    def get_recordable(self, what, **kwargs):
        if what == StandardTags.Current:
            return NeuronRampCurrentClampCurrentRecord(cclamp=self,
                    **kwargs)
        assert False


from morphforge.stdimports import NEURONEnvironment
NEURONEnvironment.currentclamps.register_plugin(CurrentClampRamp, NEURONCurrentClampRamp)




