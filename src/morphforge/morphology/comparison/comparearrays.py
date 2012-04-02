#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------








class MorphArrayComparison():
    
    @classmethod
    def are_same(cls, m1, m2, max_node_distance = 0.01):
        
        m1 = m1.to_array()
        m2 = m2.to_array()
        
        if len(m1) != len(m2):
            return False
            
        # Create a map between indices in each morphology,
        # based on positions: 
        index_map = cls.getIDMappingFromPositions(m1,m2, max_node_distance)
        if index_map is None:
            return False
        
        # Check the connectivity:
        m2_connectivity = set(  [ tuple(t) for t in m2._connectivity.tolist()]  )
        for i1,j1 in m1._connectivity:
            i2 = index_map[i1]
            j2 = index_map[j1]
            if not (i2,j2) in m2_connectivity:
                return False
        
        
        # Check the region types:
        for c1,(i1,j1) in enumerate(m1._connectivity):
            i2 = index_map[i1]
            j2 = index_map[j1]
            c2 = m2.index_of_connection(i2,j2)
            
            if m1._section_types[c1] != m2._section_types[c2]:
                return False 
            
        
        return True
        
        
        
        
    @classmethod
    def getIDMappingFromPositions(cls,m1,m2, max_node_distance):
        
        import scipy.spatial
        kdTree = scipy.spatial.KDTree( m2._vertices )
        
        idMap = {}
        max_dist = 0
        for vi, v in enumerate( m1._vertices):
            dist, nearest_neighbour = kdTree.query( v )
            if dist > max_node_distance:
                return None

            if vi in idMap:
                return None            
            #assert not vi in idMap, 'Unabe '
            
            idMap[vi] = nearest_neighbour
            max_dist = max(max_dist, dist)
            
        return idMap
        
