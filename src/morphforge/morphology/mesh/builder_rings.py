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
import numpy as np
from morphforge.morphology.mesh import TriangleMesh
from morphforge.morphology.mesh import find_closest_points, get_point_circle_about







  

def build_triangle_mesh_between_rings( pts1, pts2, pts1_offset, pts2_offset):
    
    assert len( pts1 ) == len( pts2 )
    n =  len( pts1 )
    tris = []
    
    i_p,i_d = find_closest_points( pts1, pts2 )
    
    #i_p,i_d = get_best_joining_offset( pts1, pts2 )
    
    for i in range(0,n):
        v_p1 = pts1_offset + (i_p + i) % n
        v_p2 = pts1_offset + (i_p + i + 1 ) % n
        v_d1 = pts2_offset +   (i_d + i ) % n
        v_d2 = pts2_offset +   (i_d + i + 1 ) % n
        tris.append( [v_p1, v_d2, v_p2] )
        tris.append( [v_d1, v_d2, v_p1] )
    return tris






class MeshBuilderRings(object):
    
    @classmethod
    def build(cls, morph,region_color_map=None, n=20):

        section_distal_offsets = {}
                
        vertices = np.empty( (0,3) )
        vertex_colors = np.empty( (0,3) )
        triangles = []
        
        default_color= np.array( ((128,128,128),)  )
        
#         = { 
#              morph.getRegion('axon123'):   np.array( [[0,0,255]] ) , 
#              morph.getRegion('dendrite2'): np.array( [[255,0,0]] ) 
#              }
        
        if region_color_map:
            for r in morph.getRegions():
                assert r in region_color_map
        
        

        for s in morph:
          
            # Get the offset of the proximal point circle:
            if s.isARootSection():
                proximal_points = get_point_circle_about( s.getProximalNPA3(), s.getDistalVectorNP3(), s.p_r,n=n )
                vertices = np.vstack( (vertices, proximal_points ) )
                
                color = region_color_map[s.region] if region_color_map else default_color
                vertex_colors = np.vstack( (vertex_colors,np.repeat(color, n, axis=0 )  ) ) 
                proximal_offset = 0
            
            else:
                proximal_offset = section_distal_offsets[ s.parent ]
            
            
            # What direction do we want to point in?
            if len( s.children ) == 0:
                distal_points_circle_norm_vector = s.getDistalVectorNP3()
            elif len( s.children ) == 1:
                distal_points_circle_norm_vector = ( s.getDistalVectorNP3() + s.children[0].getDistalVectorNP3() ) / 2.0
            else:
                distal_points_circle_norm_vector = s.getDistalVectorNP3()
            
            
            
            # Build the ring of distal points:
            distal_points = get_point_circle_about( s.getDistalNPA3(), distal_points_circle_norm_vector, s.d_r,n=n )
            distal_offset = vertices.shape[0]
            section_distal_offsets[s] = distal_offset
            vertices = np.vstack( (vertices, distal_points ) )
            color = region_color_map[s.region] if region_color_map else default_color
            vertex_colors = np.vstack( (vertex_colors,np.repeat(color, n, axis=0 )  ) ) 
            
            # Create the triangles to make a mesh
            tris = build_triangle_mesh_between_rings(
                  vertices[ proximal_offset:proximal_offset+n, :], 
                  vertices[ distal_offset:distal_offset+n, :], 
                  pts1_offset = proximal_offset, 
                  pts2_offset = distal_offset,
                  )
            triangles.extend(tris)
            
        
        return TriangleMesh(vertices=vertices, triangles=triangles, vertex_colors = vertex_colors )
    




