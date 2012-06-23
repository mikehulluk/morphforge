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
from hocbuilder_cell import HocBuilder_Cell


from Cheetah.Template import Template

from morphforge.simulation.neuron.simulationdatacontainers import MHOCSections,  MHocFileData
from morphforge.simulation.neuron.settings import MNeuronSettings



ccTmpl = """
// Current Clamp [ $stimname ]
objref $stimname
${cellname}.internalsections[$sectionindex] $stimname = new IClamp( $sectionpos )
${stimname}.dur = $dur
${stimname}.del = $delay
${stimname}.amp = $amp
"""



vcTmpl = """
// Current Clamp [ $stimname ]
objref $stimname
${cellname}.internalsections[$sectionindex] $stimname = new $VClampType ( $sectionpos )
${stimname}.dur1 = $dur1
${stimname}.dur2 = $dur2
${stimname}.dur3 = $dur3
${stimname}.amp1 = $amp1
${stimname}.amp2 = $amp2
${stimname}.amp3 = $amp3
#if $VClampType == "SEClamp"
${stimname}.rs = $rs
#end if

"""

k="""
${stim.name}.dur1 = $stim.dur1.rescale('ms').magnitude
${stim.name}.dur2 = $stim.dur2.rescale('ms').magnitude
${stim.name}.dur3 = $stim.dur3.rescale('ms').magnitude
${stim.name}.amp1 = $stim.amp1.rescale('mV').magnitude
${stim.name}.amp2 = $stim.amp2.rescale('mV').magnitude
${stim.name}.amp3 = $stim.amp3.rescale('mV').magnitude
if VClamp
${stim.name}.rs = $stim.rs
"""





class HocBuilder(object):

    @classmethod
    def VoltageClamp(cls, hocfile_obj, voltageclamp ):

        cell = voltageclamp.celllocation.cell
        section = voltageclamp.celllocation.morphlocation.section
        data = {
                "stimname":voltageclamp.name,
                "cell":cell,
                "cellname":hocfile_obj[MHocFileData.Cells][cell]['cell_name'],
                "sectionindex":hocfile_obj[MHocFileData.Cells][cell]['section_indexer'][section],
                "sectionpos":voltageclamp.celllocation.morphlocation.sectionpos,

                "dur1":voltageclamp.dur1.rescale("ms").magnitude,
                "dur2":voltageclamp.dur2.rescale("ms").magnitude,
                "dur3":voltageclamp.dur3.rescale("ms").magnitude,

                "amp1":voltageclamp.amp1.rescale("mV").magnitude,
                "amp2":voltageclamp.amp2.rescale("mV").magnitude,
                "amp3":voltageclamp.amp3.rescale("mV").magnitude,

                "rs":voltageclamp.rs.rescale("MOhm").magnitude,

                "VClampType": MNeuronSettings.get_voltageclamp_type()
                }

        # Save the data about this Current Clamp:
        hocfile_obj[MHocFileData.VoltageClamps][voltageclamp] = data

        # Create the HOC
        hocfile_obj.add_to_section( MHOCSections.InitVoltageClamps,  Template(vcTmpl, data).respond() )



    @classmethod
    def CurrentClamp(cls, hocfile_obj, currentclamp ):
        cell = currentclamp.celllocation.cell
        section = currentclamp.celllocation.morphlocation.section
        data = {
                "stimname":currentclamp.name,
                "cell":cell,
                "cellname":hocfile_obj[MHocFileData.Cells][cell]['cell_name'],
                "sectionindex":hocfile_obj[MHocFileData.Cells][cell]['section_indexer'][section],
                "sectionpos":currentclamp.celllocation.morphlocation.sectionpos,
                "dur":currentclamp.dur.rescale("ms").magnitude,
                "delay":currentclamp.delay.rescale("ms").magnitude,
                "amp":currentclamp.amp.rescale("nA").magnitude
                }

        # Save the data about this Current Clamp:
        hocfile_obj[MHocFileData.CurrentClamps][currentclamp] = data

        # Create the HOC
        hocfile_obj.add_to_section( MHOCSections.InitCurrentClamps,  Template(ccTmpl, data).respond() )






    @classmethod
    def Cell(cls, hocfile_obj, cell):
        HocBuilder_Cell.build(hocfile_obj=hocfile_obj, cell=cell)




