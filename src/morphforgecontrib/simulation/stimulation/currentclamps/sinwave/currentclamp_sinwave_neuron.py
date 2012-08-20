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

from morphforge.simulation.neuron.objects.neuronrecordable import NeuronRecordable
from morphforge.constants.standardtags import StandardTags
from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import MHocFileData
from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import MHOCSections
from morphforge.simulation.neuron.hocmodbuilders.hocmodutils import HocModUtils
from morphforgecontrib.simulation.stimulation.currentclamps.sinwave.currentclamp_sinwave_core import CurrentClamp_SinWave
from morphforge.simulation.neuron.objects.neuronobject import NeuronObject
from morphforge.core.quantities.fromcore import unit
from morphforge.simulation.neuron.biophysics.modfile import ModFile
from Cheetah.Template import Template
from morphforge.core import ObjectLabeller



currentclampsinwaveTxt = """
COMMENT
TODO: ATTRIBUTION.
ENDCOMMENT


NEURON {
        POINT_PROCESS CurrentClampSinWave
        RANGE del, dur, pkamp, freq, phase, bias
        ELECTRODE_CURRENT i
}

UNITS {
        (nA) = (nanoamp)
             }

PARAMETER {
        del=5   (ms)
        dur=1000   (ms)
        pkamp=10 (nA)
        freq=10  (Hz)
        phase=0 (rad)
        bias=0  (nA)
        PI=3.14159265358979323846
}

ASSIGNED {
        i (nA)
}

BREAKPOINT {
    at_time(del)
    at_time(del + dur)

    if (t < del) {
          i=0
       }else{
                if (t < del+dur) {
               i = pkamp*sin(2*PI*freq*(t-del)/1000+phase)+bias
          }else{
               i = 0
}}}
"""




ccSinWaveHOCTmpl = """
// Post-Synapse [$stimname]
objref $stimname
${cellname}.internalsections[$sectionindex] $stimname = new CurrentClampSinWave ($sectionpos)
${stimname}.freq =     $freq.rescale("Hz").magnitude
${stimname}.pkamp =      $amp.rescale("nA").magnitude
${stimname}.del =    $delay.rescale("ms").magnitude
${stimname}.bias = $bias.rescale("nA").magnitude

"""


class NeuronSinwaveCurrentClampCurrentRecord(NeuronRecordable):

    def __init__(self, cclamp, **kwargs):
        super(NeuronSinwaveCurrentClampCurrentRecord, self).__init__(**kwargs)
        self.cclamp = cclamp

    def get_unit(self):
        return unit('nA')

    def get_std_tags(self):
        return [StandardTags.Current]

    def build_hoc(self, hocfile_obj):
        objNameHoc = hocfile_obj[MHocFileData.CurrentClamps][self.cclamp]["stimname"]
        HocModUtils.create_record_from_object(hocfile_obj=hocfile_obj, vecname="RecVec%s"%self.name, objname=objNameHoc, objvar="i", recordobj=self)

    def build_mod(self, modfile_set):
        pass


class Neuron_CurrentClamp_SinWave(CurrentClamp_SinWave, NeuronObject):

    def __init__(self, **kwargs):
        super(Neuron_CurrentClamp_SinWave, self).__init__(**kwargs)

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
            'freq': self.freq,
            'amp': self.amp,
            'delay': self.delay,
            'bias': self.bias,
            }

        hoc_txt = Template(ccSinWaveHOCTmpl, data).respond()
        hocfile_obj.add_to_section(MHOCSections.InitCurrentClamps, hoc_txt)
        hocfile_obj[MHocFileData.CurrentClamps][self] = data


    def build_mod(self, modfile_set):
        modfile = ModFile(modtxt=currentclampsinwaveTxt,
                          name='NeuronSinWaveCurrentClmap')
        modfile_set.append(modfile)

    def get_recordable(self, what, **kwargs):
        if what == StandardTags.Current:
            return NeuronSinwaveCurrentClampCurrentRecord(cclamp=self,
                    **kwargs)
        assert False






#NeuronSimulationEnvironment.registerMembraneMechanism(CurrentClamp_SinWave, Neuron_CurrentClamp_SinWave)
