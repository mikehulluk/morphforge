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




from morphforge.simulation.neuron.core.neuronsimulationenvironment import NeuronSimulationEnvironment
from morphforgecontrib.simulation.membranemechanisms.neuroml_via_neurounits.neuroml_via_neurounits_core import NeuroML_Via_NeuroUnits_Channel
from neurounits.importers.neuroml import ChannelMLReader
from morphforgecontrib.simulation.membranemechanisms.neurounits.neuro_units_bridge import Neuron_NeuroUnitEqnsetMechanism



class NeuroML_Via_NeuroUnits_ChannelNEURON(Neuron_NeuroUnitEqnsetMechanism, NeuroML_Via_NeuroUnits_Channel):

    def __init__(self, xml_filename, chlname=None, mechanism_id=None):
        #self.mechanism_id = mechanism_id

        eqnset,chlinfo,default_params = ChannelMLReader.BuildEqnset( xml_filename )
        #eqnset,chlinfo,default_params = EqnSetFromNeuroML.load(xml_filename)

        default_params = dict( [(k,v.as_quantities_quantity()) for (k,v) in default_params.iteritems()] )

        Neuron_NeuroUnitEqnsetMechanism.__init__(self, name=chlname, eqnset=eqnset, mechanism_id=mechanism_id, default_parameters=default_params, recordables_map=None, recordables_data=None)
        NeuroML_Via_NeuroUnits_Channel.__init__(self, xml_filename=xml_filename, chlname=chlname, mechanism_id=mechanism_id)


NeuronSimulationEnvironment.membranemechanisms.register_plugin(NeuroML_Via_NeuroUnits_Channel, NeuroML_Via_NeuroUnits_ChannelNEURON)


