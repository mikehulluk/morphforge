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



from os.path import join as Join

from summariser_library import SummariserLibrary
from morphforge.simulationanalysis.summaries.reportlabconfig import ReportLabConfig
from morphforge.componentlibraries import ChannelLibrary

from morphforge.simulation.neuron.core.neuronsimulationenvironment import NeuronSimulationEnvironment








class MembraneMechanismSummariser(object):



    @classmethod
    def summarise_all(cls, cell_location, reportlabconfig=None):
        if not reportlabconfig: reportlabconfig = ReportLabConfig()

        for (modelsrc, celltype, channeltype), membranemechanismFunctor in ChannelLibrary.iteritems():
            print "Summarising:", modelsrc, celltype, channeltype
            membranemechanism = membranemechanismFunctor( NeuronSimulationEnvironment() )
            filename = "%s_%s_%s.pdf"%( modelsrc,celltype,channeltype)
            f_name = Join(cell_location, filename)
            cls.create_pdf(mechanism=membranemechanism, filename=f_name,reportlabconfig=reportlabconfig)



    @classmethod
    def create_pdf(cls, mechanism, filename, reportlabconfig =None ):
        from reportlab.platypus import SimpleDocTemplate, Paragraph
        from reportlab.lib.pagesizes import A4
        if not reportlabconfig: reportlabconfig = ReportLabConfig()


        doc = SimpleDocTemplate(filename,pagesize=A4)

        elements = [ Paragraph("Filename: %s"%filename, style=reportlabconfig.styles['Heading2'] ) ]
        elements.extend( cls.summarise_membranemechanism(mechanism, reportlabconfig ) )

        doc.build(elements)




    @classmethod
    def summarise_membranemechanism(self, membranemechanism,  reportlabconfig, make_graphs=True ):
        from reportlab.platypus import Paragraph, Table
        local_elements = []
        local_elements.append( Paragraph(membranemechanism.name, reportlabconfig.styles['Heading2'] ) )
        summariser = SummariserLibrary.get_summarisier( membranemechanism )

        # Parameters:
        local_elements.append( Paragraph("Parameters", reportlabconfig.styles['Heading2'] ) )
        table_header = ['Parameter Name', 'Default', ]

        data = [table_header, ]
        for param in membranemechanism.get_variables():
            data.append( [ param, membranemechanism.get_default(param) ] )


        local_elements.append( Table(data, style=reportlabconfig.listTableStyle) )


        # Detailed Summary:
        if summariser:
            local_elements.extend( summariser.to_report_lab( membranemechanism, reportlabconfig, make_graphs=make_graphs ) )
        else:
            local_elements.append( Paragraph("[No Summariser Available]", reportlabconfig.styles['Italic'] ) )


        return local_elements

