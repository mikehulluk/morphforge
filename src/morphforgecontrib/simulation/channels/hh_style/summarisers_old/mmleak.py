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

#from morphforge.simulationanalysis.summaries.summariser_library import SummariserLibrary
from morphforgecontrib.simulation.channels.hh_style.core.mmleak import StdChlLeak


class Summarise_MM_LeakChannel(object):

    @classmethod
    def to_report_lab(cls, leak_chl, reportlabconfig, make_graphs):
        from reportlab.platypus import Paragraph, Table
        chl = leak_chl

        local_elements = []
        local_elements.append(Paragraph('Overview',
                              reportlabconfig.styles['Heading3']))

        # Summary:
        overview_table_data = [
                  ['Conductance', chl.conductance],
                  ['Reversal Potential', chl.reversalpotential],
                           ]

        local_elements.append(Table(overview_table_data, style=reportlabconfig.listTableStyle))

        return local_elements



#SummariserLibrary.register_summariser(channel_baseclass=StdChlLeak, summariser_class=Summarise_MM_LeakChannel)
