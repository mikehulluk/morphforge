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


from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import MHocFileData
from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import MHOCSections
from morphforge.simulation.neuron.objects.neuronobject import NeuronObject
from Cheetah.Template import Template
from morphforge.simulation.base.networks import Synapse
from morphforge.simulation.base.networks import GapJunction
from morphforge.simulation.neuron.biophysics.modfile import ModFile
from morphforge.constants.standardtags import StandardTags


class NeuronSynapse(NeuronObject, Synapse):




    def __init__(self, simulation, presynaptic_mech, postsynaptic_mech, name=None):
        NeuronObject.__init__(self, name=name,simulation=simulation)
        Synapse.__init__(self, presynaptic_mech=presynaptic_mech, postsynaptic_mech=postsynaptic_mech)


    def build_hoc(self, hocfile_obj):
        self.postSynapticMech.build_hoc(hocfile_obj)
        self.preSynapticTrigger.build_hoc(hocfile_obj)

    def build_mod(self, modfile_set):
        self.postSynapticMech.build_mod(modfile_set)
        self.preSynapticTrigger.build_mod(modfile_set)


    def get_recordable(self, what, **kwargs):
        if what == StandardTags.Conductance:
            what = Synapse.Recordables.SynapticConductance
        if what == StandardTags.Current:
            what = Synapse.Recordables.SynapticCurrent

        if what in [Synapse.Recordables.SynapticCurrent,
                    Synapse.Recordables.SynapticConductance,
                    StandardTags.NMDAVoltageDependancy,
                    StandardTags.NMDAVoltageDependancySS]:
            return self.postSynapticMech.get_recordable(what=what,
                    **kwargs)
        if what in ['g']:
            return self.postSynapticMech.get_recordable(what=what, **kwargs)


        assert False











expTmpl = """
// Gap Junction [$name]
objref $name1
objref $name2
${cellname1}.internalsections[$sectionindex1] $name1 = new Gap ($sectionpos1)
${cellname2}.internalsections[$sectionindex2] $name2 = new Gap ($sectionpos2)

${name1}.r = $resistance.rescale("MOhm").magnitude
${name2}.r = $resistance.rescale("MOhm").magnitude

setpointer ${name1}.vgap,  ${cellname2}.internalsections[$sectionindex2].v($sectionpos2)
setpointer ${name2}.vgap,  ${cellname1}.internalsections[$sectionindex1].v($sectionpos1)

"""






gapMod = """
NEURON {
    POINT_PROCESS Gap
    POINTER vgap
    RANGE r, i
    NONSPECIFIC_CURRENT i
}

PARAMETER{
    r = 1e10 (megohm)
}

ASSIGNED {
    v (millivolt)
    vgap (millivolt)
    i (nanoamp)
}
BREAKPOINT{
    i = (v-vgap)/r
    }

"""









class NeuronGapJunction(GapJunction, NeuronObject):

    def __init__(self, **kwargs):        
        super(NeuronGapJunction, self).__init__(**kwargs)



    isFirstBuild = True
    def build_mod(self, modfile_set):

        if NeuronGapJunction.isFirstBuild:
            NeuronGapJunction.isFirstBuild = False
            m = ModFile(modtxt=gapMod, name='GapJunction')
            modfile_set.append(m)


    def build_hoc(self, hocfile_obj):
        cell1 = self.celllocation1.cell
        cell2 = self.celllocation2.cell
        section1 = self.celllocation1.morphlocation.section
        section2 = self.celllocation2.morphlocation.section

        gp_obj1_name = self.get_name() + 'A'
        gp_obj2_name = self.get_name() + 'B'
        data = {
               "name": self.get_name(),
               "name1":gp_obj1_name,
               "name2":gp_obj2_name,
               "cell1":cell1,
               "cell2":cell2,
               "cellname1":hocfile_obj[MHocFileData.Cells][cell1]['cell_name'],
               "cellname2":hocfile_obj[MHocFileData.Cells][cell2]['cell_name'],
               "sectionindex1":hocfile_obj[MHocFileData.Cells][cell1]['section_indexer'][section1],
               "sectionindex2":hocfile_obj[MHocFileData.Cells][cell2]['section_indexer'][section2],
               "sectionpos1":self.celllocation1.morphlocation.sectionpos,
               "sectionpos2":self.celllocation2.morphlocation.sectionpos,

               "resistance": self.resistance
               }

        hocfile_obj.add_to_section(MHOCSections.InitGapJunction,  Template(expTmpl, data).respond())

        hocfile_obj[MHocFileData.GapJunctions][self] = data








