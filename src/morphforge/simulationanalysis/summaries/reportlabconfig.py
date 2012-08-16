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







from morphforge.core import Join

import os
from morphforge.core.mgrs.locmgr import LocMgr


grey = '#808080'

class ReportLabConfig(object):

    def __init__(self):
        from reportlab.lib.styles import getSampleStyleSheet

        self.styles = getSampleStyleSheet()

        ## Setup space to store images:
        self.images = []
        self.imageExt = "png"
        self.imageDir = os.path.normcase( os.path.join( LocMgr.get_tmp_path(), 'reportlab_image_build') )
        self.imagesize = (5,3)
        if not os.path.exists(self.imageDir):
            os.makedirs(self.imageDir)



    listTableStyle = [('ALIGN', (1,1), (-1,-1), 'LEFT'),
                      ('FONT', (0,0), (0,-1), 'Times-Bold'),
                      ('VALIGN',(0,0),(-1,-1),'TOP'),
                       ]

    defaultTableStyle = [('ALIGN', (1,1), (-1,-1), 'LEFT'),
                         ('VALIGN',(0,0),(-1,-1),'TOP'),
                     ('LINEABOVE', (0,0), (-1,0), 2, grey),
                     ('LINEBELOW', (0,0), (-1,0), 1, grey),
                     ('FONT', (0,0), (-1,0), 'Times-Bold'),
                     ('FONT', (0,1), (-1,-1), 'Times-Roman'),
                     ('LINEBELOW', (0,-1), (-1,-1), 2, grey),
                    ]



    def save_mpl_to_rl_image(self, figure, fig_desc):
        import pylab
        from reportlab.platypus import Image
        im_filename = Join( self.imageDir, "%s_%d.%s"% (fig_desc,len(self.images), self.imageExt) )
        self.images.append(im_filename)
        pylab.savefig(im_filename)
        return Image(im_filename)
