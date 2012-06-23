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





from morphforge.simulation.neuron.biophysics.mm_neuron import MM_Neuron_Base

from morphforge.simulation.neuron.biophysics.modfile import ModFile
from morphforge.simulation.neuron.neuronsimulationenvironment import NeuronSimulationEnvironment
from morphforgecontrib.simulation.membranemechanisms.common.neuron import  build_hoc_default


from morphforgecontrib.simulation.membranemechanisms.neuroml_via_xsl.neuroml_via_xsl_core import NeuroML_Via_XSL_Channel




from lxml import etree
from morphforgecontrib.simulation.membranemechanisms.neurounits.neuro_units_bridge import MM_Neuron_RecGen
#from morphforge.core.quantities.fromcore import unit
#from morphforge.core.misc import ExpectSingle
from neurounits.importers.neuroml import ChannelMLReader
from morphforge.simulation.neuron.simulationdatacontainers.mhocfile import MHocFileData,\
    MHOCSections








class NeuroML_Via_XSL_ChannelNEURON(MM_Neuron_Base, NeuroML_Via_XSL_Channel):

    def __init__(self, xml_filename,xsl_filename, chlname=None, mechanism_id=None, ):
        self.mechanism_id = mechanism_id
        MM_Neuron_Base.__init__(self)
        NeuroML_Via_XSL_Channel.__init__(self, xml_filename=xml_filename, xsl_filename=xsl_filename, chlname=chlname, mechanism_id=mechanism_id)


        xslt_root = etree.parse( open(self.xsl_filename) )
        xsl_transform = etree.XSLT(xslt_root)

        xml_root = etree.parse( open(self.xml_filename) )
        self.modtxt = str( xsl_transform(xml_root) )
        nrnsuffix = ModFile.extract_nrn_suffix_from_text(self.modtxt)

        self.name = nrnsuffix
        self.nrnsuffix = nrnsuffix
        self.NRNSUFFIX = nrnsuffix



        # ISSUE 'A': Extract out the reversal potential; and set it manually since the XSL method does not work:
        self.chlData = ChannelMLReader.LoadChlRaw(xml_filename)




    def build_hoc_section(self, cell, section, hocfile_obj, mta ):
        build_hoc_default( cell=cell, section=section, hocfile_obj=hocfile_obj, mta=mta , units={}, nrnsuffix=self.nrnsuffix )


        # ISSUE 'A': Hack around the reversal potential initialisation issue:
        if self.chlData.iv_default_erev:

            # Get the reversal potential out, takling care of the
            # units (expected in 'mV') :
            vrev = float(self.chlData.iv_default_erev)
            if self.chlData.units == "Physiological Units":
                pass
            elif self.chlData.units == "SI Units":
                vrev = vrev * 1000.
            else:
                assert False

            tmpl_dict = hocfile_obj[MHocFileData.Cells][cell]
            cell_name = tmpl_dict["cell_name"]
            section_indexer = tmpl_dict['section_indexer']
            d = []
            for s in cell.morphology:
                d.append("""%s.internalsections [ %d ] { e%s=%f
                        }"""%(cell_name, section_indexer[s] ,
                            self.chlData.iv_ion,
                            vrev) )
            hocfile_obj.add_to_section(MHOCSections.InitCellMembranes, "\n".join(d) )



    def create_modfile(self, modfile_set):
        modFile =  ModFile(name='NeuroMLViaXSLChannelNEURON_%s'%self.name, modtxt=self.modtxt )
        modfile_set.append(modFile)



    # No Internal recording or adjusting of parameters for now:
    class Recordables:
        all = []


    def get_variables(self):
        return []

    def get_defaults(self):
        return {}

    def get_recordable(self, what, celllocation, nrn_unit, **kwargs):
        return MM_Neuron_RecGen( src_chl=self, modvar=what, where=celllocation, unit_in_nrn=nrn_unit, std_tags=[], **kwargs)



NeuronSimulationEnvironment.membranemechanisms.register_plugin(NeuroML_Via_XSL_Channel, NeuroML_Via_XSL_ChannelNEURON)


