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




#from reportlab.platypus import *



from morphforge.simulationanalysis.summaries.summariser_library import SummariserLibrary
from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmleak import MM_LeakChannel


class Summarise_MM_LeakChannel(object):
    
    @classmethod
    def toReportLab(cls, leakChannel, reportlabconfig, make_graphs):
        from reportlab.platypus import Paragraph, Table
        chl = leakChannel
    
        localElements = []
        localElements.append( Paragraph("Overview",reportlabconfig.styles['Heading3']) )
        
        # Summary:
        overviewTableData = [
                             ["Conductance", chl.conductance],
                             ["Reversal Potential",  chl.reversalpotential],
                            ]
        
        localElements.append( Table(overviewTableData, style=reportlabconfig.listTableStyle) )
        
        return localElements
    
    
    
SummariserLibrary.register_summariser(channelBaseClass=MM_LeakChannel, summariserClass=Summarise_MM_LeakChannel)
