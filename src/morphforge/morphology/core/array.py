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

"""Vertex-based object-model of morphologies.


In this scheme, each *node* has a position :math:`$(x,y,z)$`, and a radius denoted by the green line. 
Each node, except one, has a single parent.    


.. image:: /img_srcs/morphology_overview_simpledetails.svg
    :align: center
"""

import numpy as np
from morphforge.morphology.core.base import MorphologyBase





class MorphologyArray(MorphologyBase):
    

    
    def to_array(self):
        return self
        
    def to_tree(self, **kwargs):
        from morphforge.morphology.conversion import MorphologyConverter
        return MorphologyConverter.array_to_tree(self, **kwargs)
    
    
    


    
    def __init__(self, vertices, connectivity, dummy_vertex_index=0, section_types=None,region_number_to_name_bidict=None, name=None, metadata=None):
        MorphologyBase.__init__(self, region_number_to_name_bidict=region_number_to_name_bidict, name=name, metadata=metadata)
        
        
        
        # Save the data in the correct formats:
        self._connectivity = np.array( connectivity).reshape(-1, 2)
        N = self._connectivity.shape[0]
        self._vertices = np.array(vertices).reshape(-1,4)
        M = self._vertices.shape[0]
                
        self._section_types = np.array(section_types) if section_types else np.zeros( len(connectivity) )
        
        self._dummy_vertex_index= dummy_vertex_index
        

        # Some Error Checking:
        assert N == M-1
        
        
        if self.is_directed():
            # Lets check connectivity forms a tree:
            pass
        
                
        # If we store the data in arrays, then we no longer store which
        # is our dummy vertex, which we will need for generating trees
        
    
    def get_leaf_vertices_indices(self):
        vertex_connections = np.zeros( len(self._vertices) )
        for i,j in self._connectivity:
            vertex_connections[i] = vertex_connections[i] + 1
            vertex_connections[j] = vertex_connections[j] + 1
        leaf_vertices = np.where( vertex_connections== 1)[0]
        return leaf_vertices  

    
    def is_directed(self):
        return self._dummy_vertex_index is not None
    
    def get_vertex_by_index(self, i):
        return self._vertices[i,:]
    
    def get_connection_by_index(self, i):
        return self._connectivity[i,:]
    
    def __len__(self):
        """ Returns the number of cylinders in the morphology 
        (Chosen over the number for vertices, in order to maintain compatibility with MorphologyTree, 
        """
        return self._connectivity.size/2
    
        
    def connections_to_index(self, pid):
        return [ i for (i,j) in self._connectivity if j == pid] + [ j for (i,j) in self._connectivity if i == pid]  
    
    def index_of_connection(self, id, pid):
        for index, (i,j) in enumerate(self._connectivity):
            if i==id and j==pid:
                return index
            if i==pid and j==id:
                return index
        assert False, ' Connection not found'
    
        
        
