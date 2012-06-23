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

#
#
#
#
#
#
## Invalid SWC:
#sEmpty = ""
#sInvalidSingleSegment = """
#1 0 0.0 0.0 0.0 1.0 -1
#"""
#
## Valid SWC:
#sValidSingleSegment = """
#1 0 0.0 0.0 0.0 1.0 -1
#2 0 1.0 0.0 0.0 2.0 1
#"""
#sValidSingleSegment2 = """
#1 1 2.5 3.5 4.5 5.5 -1
#2 1 6.5 7.5 8.5 9.5 1
#"""
#
##test positive radii
#
#sValidTwoSegment = """
#1 2 0.0 0.0 0.0 1.0 -1
#2 2 7.5 8.5 9.5 10.5 1
#3 1 3.5 4.5 5.5 6.5 2
#4 3 1.5 2.5 3.5 4.5 2
#"""
#
#class TestSWCLoading(unittest.TestCase):
#    def setUp(self):
#        pass
#
#
#    def testSWCContructionSWCData(self):
#
#        # Can't Construct an empty cell:
#        self.assertRaises(ValueError, lambda :MorphologyFactory.fromSWC(morphname="Cell1", src=sIO(sEmpty)))
#        self.assertRaises(ValueError, lambda :MorphologyFactory.fromSWC(morphname="Cell1", src=sIO(sInvalidSingleSegment)))
#
#        # Construct a single segment cell:
#        singleSegCell = MorphologyFactory.fromSWC(morphname="Cell1", src=sIO(sValidSingleSegment))
#        self.assert_(len(singleSegCell) == 1)
#        self.assertAlmostEqual(linalg.norm(singleSegCell.root.get_nPA3() - numpy.array((0.0, 0.0, 0.0))), 0.0, 4)
#        self.assert_(singleSegCell.root.r == 1.0)
#        self.assert_((singleSegCell.root.children[0].get_nPA3() == (1.0, 0.0, 0.0)).all())
#        self.assert_(singleSegCell.root.children[0].r == 2.0)
#
#
#
#        # Construct a slighty different Single Segment Cell:
#        singleSegCell = MorphologyFactory.fromSWC(morphname="Cell1", src=sIO(sValidSingleSegment2))
#        self.assert_(singleSegCell.root != None)
#        self.assert_((singleSegCell.root.get_nPA3() == (2.5, 3.5, 4.5)).all())
#        self.assert_(singleSegCell.root.r == 5.5)
#        self.assertAlmostEqual(linalg.norm(singleSegCell.root.children[0].get_nPA3() - numpy.array((6.5, 7.5, 8.5))), 0.0, 4)
#        self.assert_(singleSegCell.root.children[0].r == 9.5)
#
#
#        #Test a 3 compartement Valid Single Cell
#        twoSegCell = MorphologyFactory.fromSWC(morphname="Cell1", src=sIO(sValidTwoSegment))
#        self.assert_(twoSegCell.root != None)
#        self.assert_(len(twoSegCell.root.children[0].children) == 2)
#        self.assert_(len(twoSegCell) == 3)
#        seg1 = twoSegCell.root.children[0]
#        seg2 = twoSegCell.root.children[0].children[0]
#        seg3 = twoSegCell.root.children[0].children[1]
#        self.assert_(seg2.parent == seg1 and seg3.parent == seg1)
#        self.assert_(seg2.children == [] and seg3.children == [])
#
#        self.assert_(seg1.x == 7.5 and seg1.y == 8.5 and
#					 seg1.z == 9.5 and seg1.r == 10.5)
#        self.assert_(seg2.x == 3.5 and seg2.y == 4.5 and
#					 seg2.z == 5.5 and seg2.r == 6.5)
#        self.assert_(seg3.x == 1.5 and seg3.y == 2.5 and
#					 seg3.z == 3.5 and seg3.r == 4.5)
#
#        # Iteration
#        children = [s for s in twoSegCell]
#        self.assert_(len(children) == 3)
#        for s in [seg1, seg2, seg3]: self.assert_(s in children)
#
#
#
