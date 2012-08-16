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




import unittest
import StringIO
import tempfile
from morphforge.morphology.builders.morphologyloader import MorphologyLoader


class TestSWC(unittest.TestCase):

    swcSample = """
         1         1       1591.43         53.87         20.48        0.15        -1
         2         1       1590.78         50.61         20.48        5.80         1
         3         1       1591.43         46.99         20.48        5.16         2
         4         1       1592.74         43.50         20.48        5.16         3
         5         1       1593.39         41.12         20.48        2.02         4
         6        16       1593.39         40.50         20.48        0.64         5
         7        16       1595.35         39.01         20.48        1.43         6
    """



    def testBasicLoad(self):

        f = StringIO.StringIO(TestSWC.swcSample)
        m = MorphologyLoader.fromSWC(src=f, morphname=None, regionNames=None)
        print m

        self.assertEqual(len(m), 6)
        self.assertEqual(len(m.get_regions()), 2)

        root = m.get_root_section()
        self.assertAlmostEqual(root.p_x,  1591.43)
        self.assertAlmostEqual(root.p_y,  53.87  )
        self.assertAlmostEqual(root.p_z,  20.48  )
        self.assertAlmostEqual(root.p_r,  0.15   )

        self.assertAlmostEqual(root.d_x,  1590.78)
        self.assertAlmostEqual(root.d_y,  50.61  )
        self.assertAlmostEqual(root.d_z,  20.48  )
        self.assertAlmostEqual(root.d_r,  5.80   )



