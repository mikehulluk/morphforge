#
##-------------------------------------------------------------------------------
## Copyright (c) 2012 Michael Hull.
## All rights reserved.
##
## Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
##
##  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
##  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
##-------------------------------------------------------------------------------
#


import numpy as np
from StringIO import StringIO

from morphforge.core import Join
from morphforge.core.mfrandom import MFRandom
from morphforge.core.mgrs.locmgr import LocMgr
from morphforge.morphology.comparison.comparearrays import MorphArrayComparison
from morphforge.morphology.core import MorphologyArray






swc_srcs = {
    'A':"""
    1 0 1.0 2.0 3.0 4.0 -1
    2 0 5.0 6.0 7.0 8.0 1
    """,

    'B':"""
    1 0 1.0 2.0 3.0 4.0 -1
    3 0 5.0 6.0 7.0 8.0 1
    2 0 3.0 6.0 7.0 8.0 1
    """,


    'Cii':"""
    1 0 1.0 2.0 3.0 4.0 -1
    3 0 6.0 6.0 7.0 8.0 1
    4 0 5.0 9.0 7.0 8.0 3
    2 0 5.0 6.0 7.0 8.0 1
    5 0 5.0 6.0 8.0 8.0 2
    """,
    'Ci':"""
    1 0 1.0 2.0 3.0 4.0 -1
    2 0 5.0 6.0 7.0 8.0 1
    5 0 5.0 6.0 8.0 8.0 2
    3 0 6.0 6.0 7.0 8.0 1
    4 0 5.0 9.0 7.0 8.0 3
    """,
}


class TestMorphologyArrayComparison(object):
    """Testing class for morphology.comparison
    This class tests that MorphArrayComparison is properly
    checking if two morphologies are the same or not.
    Since this class is used for testing; it is important that
    it is detecting differences properly, since it is used by other testing classes
    to check that round-trip testing is sucessful.


    Should return Same:
     * [DONE] Loading the same file
     * [TODO] Array, in which the connectivity matrix has been arranged.
     * [TODO] Array, in which the vertex indices have been re-arranged.

    Should return different:
     * [DONE] 2 Arrays, in which one of the values is changed by epsilon
     * [TODO] Removal of an connection object.
     *
    """



    def testComparisonSucessful(self):
        """Verify simple .swc snippets are the same"""

        # Loading
        m1 = MorphologyArray.fromSWC(StringIO(swc_srcs['A']))
        m2 = MorphologyArray.fromSWC(StringIO(swc_srcs['A']))
        assert MorphArrayComparison.are_same(m1, m2, max_node_distance= 0.00001)


        m1 = MorphologyArray.fromSWC(StringIO(swc_srcs['B']))
        m2 = MorphologyArray.fromSWC(StringIO(swc_srcs['B']))
        assert MorphArrayComparison.are_same(m1, m2, max_node_distance= 0.00001)

        m1 = MorphologyArray.fromSWC(StringIO(swc_srcs['Ci']))
        m2 = MorphologyArray.fromSWC(StringIO(swc_srcs['Cii']))
        assert MorphArrayComparison.are_same(m1, m2, max_node_distance= 0.00001)

    def testComparisonFailureDifferentMorphologies(self):
        """Verify simple .swc snippets are different to each other"""

        m1 = MorphologyArray.fromSWC(StringIO(swc_srcs['A']))
        m2 = MorphologyArray.fromSWC(StringIO(swc_srcs['B']))
        m3 = MorphologyArray.fromSWC(StringIO(swc_srcs['Ci']))

        assert not MorphArrayComparison.are_same(m1, m2, max_node_distance= 0.00001)
        assert not MorphArrayComparison.are_same(m1, m3, max_node_distance= 0.00001)
        assert not MorphArrayComparison.are_same(m2, m3, max_node_distance= 0.00001)


    def testComparisonFailureAddingEpsilon1(self):
        """Load simple .swc snippets, and change each [x,y,z,r] value in the vertices matrix
        individually, to check that it is not the same. """

        m = MorphologyArray.fromSWC(StringIO(swc_srcs['Ci']))

        for i in range( len(m) ):
            for j in range(4):

                m1 = MorphologyArray.fromSWC(StringIO(swc_srcs['Ci']))
                m1._vertices[i,j] = m1._vertices[i,j] + 0.01
                assert MorphArrayComparison.are_same(m, m1, max_node_distance= 0.02)
                assert not MorphArrayComparison.are_same(m, m1, max_node_distance= 0.005)

                m1 = MorphologyArray.fromSWC(StringIO(swc_srcs['Ci']))
                m1._vertices[i,j] = m1._vertices[i,j] - 0.001
                assert MorphArrayComparison.are_same(m, m1, max_node_distance= 0.002)
                assert not MorphArrayComparison.are_same(m, m1, max_node_distance= 0.0005)

                m1 = MorphologyArray.fromSWC(StringIO(swc_srcs['Cii']))
                m1._vertices[i,j] = m1._vertices[i,j] + 0.01
                assert MorphArrayComparison.are_same(m, m1, max_node_distance= 0.02)
                assert not MorphArrayComparison.are_same(m, m1, max_node_distance= 0.005)

                m1 = MorphologyArray.fromSWC(StringIO(swc_srcs['Cii']))
                m1._vertices[i,j] = m1._vertices[i,j] - 0.001
                assert MorphArrayComparison.are_same(m, m1, max_node_distance= 0.002)
                assert not MorphArrayComparison.are_same(m, m1, max_node_distance= 0.0005)





    def testComparisonFailureAddingEpsilon2(self):
        """Load and complex .swc file, and
        change each [x,y,z,r] value in the vertices matrix
        individually, to check that it is not the same.
        """
        testSrcsPath = LocMgr().get_test_srcs_path()
        srcSWCFile = Join(testSrcsPath, "swc_srcs/28o_spindle20aFI.CNG.swc")

        m = MorphologyArray.fromSWC(srcSWCFile)
        MFRandom.seed(0)
        for i in range( len(m) ):
            print i, len(m)
            for j in range(4):

                # Only test 2% of cases:
                if not np.random.rand() < 0.02:
                    continue

                m1 = MorphologyArray.fromSWC(srcSWCFile)
                m1._vertices[i,j] = m1._vertices[i,j] + 0.01
                assert MorphArrayComparison.are_same(m, m1, max_node_distance= 0.02)
                assert not MorphArrayComparison.are_same(m, m1, max_node_distance= 0.005)



    def testComparisonFailureTransplantingALeafNode(self):
        """Remap each leaf node in a complex swc file, onto
        different internal nodes of the morphology,
        and check that the morphology is considered different
        """

        testSrcsPath = LocMgr().get_test_srcs_path()
        srcSWCFile = Join(testSrcsPath, "swc_srcs/28o_spindle20aFI.CNG.swc")

        m = MorphologyArray.fromSWC(srcSWCFile)

        # Find the leaf nodes:
        leaf_nodes = m.get_leaf_vertices_indices()

        for new_parent in [0, 10, 20, leaf_nodes[-1] ]:

            for l in leaf_nodes[:-1]:
                v = m._vertices.copy()
                c = m._connectivity.copy()

                # Rewrite the connectivity matrix, mapping the
                # leaf to a new_parent:
                c[c==l]=new_parent

                mNew = MorphologyArray(vertices=v, connectivity=c)
                assert not MorphArrayComparison.are_same(m, mNew, max_node_distance= 0.00001)



if __name__ == "__main__":
    TestMorphologyArrayComparison().testComparisonSucessful()
    TestMorphologyArrayComparison().testComparisonFailureDifferentMorphologies()
    TestMorphologyArrayComparison().testComparisonFailureAddingEpsilon1()
    TestMorphologyArrayComparison().testComparisonFailureAddingEpsilon2()
    TestMorphologyArrayComparison().testComparisonFailureTransplantingALeafNode()



