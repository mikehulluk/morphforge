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
import os
from morphforge.stdimports import ChannelLibrary, LocMgr
from morphforgecontrib.stdimports import NeuroML_Via_XSL_Channel


xsl_filename = os.path.join(LocMgr.get_test_srcs_path(), "neuroml/channelml/ChannelML_v1.8.1_NEURONmod.xsl")


def apply_hh_chls_neuroml_neurounits_na(env):
    return env.Channel(NeuroML_Via_XSL_Channel,
            xml_filename = os.path.join(LocMgr.get_test_srcs_path(), "neuroml/channelml/NaChannel_HH.xml"),
            xsl_filename=xsl_filename)
    
def apply_hh_chls_neuroml_neurounits_k(env):
    return env.Channel(NeuroML_Via_XSL_Channel,
        xml_filename = os.path.join(LocMgr.get_test_srcs_path(), "neuroml/channelml/KChannel_HH.xml"),
        xsl_filename=xsl_filename)



ChannelLibrary.register_channel(modelsrc="_test_neuroml_via_xsl_HH52", channeltype='Na', chl_functor=apply_hh_chls_neuroml_neurounits_na)
ChannelLibrary.register_channel(modelsrc="_test_neuroml_via_xsl_HH52", channeltype='K', chl_functor=apply_hh_chls_neuroml_neurounits_k)
