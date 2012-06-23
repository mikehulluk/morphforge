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



import numpy as np
import itertools
import os
from morphforge.morphology.core.tree import MorphPath, MorphLocation
from scipy.spatial.distance import pdist, squareform
from morphforge.morphology.mesh.mesh import TriangleMesh
from morphforge.morphology.mesh.writer_ply import MeshWriterPLY


class GeomTools(object):
    @classmethod
    def produce_sphere(cls, location, radius, n_steps):

        angles_step = ((2*np.pi)/n_steps)


        az_angles = [ i*angles_step for i in range(n_steps) ]
        theta_angles = [ i*angles_step for i in range(n_steps) ]

        pts = []
        for az in az_angles:
            for th in theta_angles:
                r = 1.0 # np.random.normal(loc=1.0, scale=0.001)
                x = r * radius * np.cos(th) + location[0]
                y = r * radius * np.sin(th) * np.sin(az) + location[1]
                z = r * radius * np.sin(th) * np.cos(az) + location[2]
                pts.append ( (x,y,z) )

        return pts


class MeshFromGTS(object):




    @classmethod
    def build(cls, m, plot=True, region_color_map=None):
        import gts
        surface_sections = cls.buildsurface_sectiondict( m.to_tree() )


        meshes = []
        for sect,sect_surface in surface_sections.iteritems():
            print sect
            assert sect.region is not None

            # Look up the region color:
            if not sect.region.name in region_color_map:
                for rgn,color in region_color_map.iteritems():
                    print rgn.name, rgn, color
                print 'Looking for:',sect.region.name, sect.region
                assert False, "Can't find region in color map!"
            sect_color = region_color_map[sect.region.name]
            print sect_color


            vertex_objs = sect_surface.vertices()
            N = len(vertex_objs)
            dShape = (N,3)
            v = np.array( [(v.x,v.y,v.z) for v in vertex_objs ] ).reshape( dShape)

            color = np.array( (sect_color.r,sect_color.g,sect_color.b) )
            colors = np.repeat( color, len(vertex_objs)).reshape( dShape, order='F' )

            triangles= sect_surface.face_indices( vertex_objs )

            tm = TriangleMesh(vertices=v, triangles=triangles, vertex_colors=colors )
            meshes.append(tm)
        m = TriangleMesh.merge(meshes=meshes)
        #with open("/home/michael/Desktop/output.ply","w") as f:
        #    f.write( MeshWriterPLY.build_string(m) )
        #print 'Done building mesh'
        #assert False

        if plot:
            from mayavi import mlab
            mlab.figure(size=(1024,768) )
            for surface in surface_sections:
                x,y,z,t = gts.get_coords_and_face_indices(surface,True)
                mlab.triangular_mesh(x,y,z,t,color=(0.9,0.9,0.9))
            mlab.show()

        return m



    @classmethod
    def only_pts_at_min_dist(cls, pts, min_dist):

        pts = np.array(pts)

        # Create a distance matrix of all the points:
        Y = squareform( pdist(pts, 'euclidean') )

        # We accept points that at not at a lower index and
        # are at a minumum distance to the other points. To do this,
        # we mask out the lower part of the distance matrix:
        assert min_dist < 1.0
        Y_to_close = (Y + np.tri(Y.shape[0], ) ) < min_dist

        # Now look for inices with no False in the columns
        any_indices =  ( ~Y_to_close.any(axis=0) ).nonzero()[0]

        return  pts[any_indices,:]




    @classmethod
    def buildsurface_sectiondict(cls, m):
        #m = m.to_tree()
        surface_sections = {}
        for s in m:
            #if MorphPath( MorphLocation(m.get_root_sections()[0], 0.5), MorphLocation(s, 0.5) ).get_length() > 150:
            #    continue
            sect_surface = cls.buildsectionsurface(s)
            surface_sections[s] = sect_surface

        return surface_sections





    @classmethod
    def buildsectionsurface(cls, s):
        import gts
        from morphforge.core import LocMgr
        from os.path import join as Join
        print 'Building Mesh'



        working_dir = LocMgr.ensure_dir_exists("/tmp/mf/mesh/")
        fTemp1 = Join( working_dir, "pts.txt")
        fTemp2  =Join( working_dir, "pts.off")
        fTemp3  =Join( working_dir, "pts.stl")
        fTemp2b =Join( working_dir, "pts_postSub.off")
        fTemp4  =Join( working_dir, "pts.gts")

        nstep = 5
        print 'Building Spheres'
        distal_offset = np.array((0.05,0.05,0.05) )
        ptsP = GeomTools.produce_sphere(location=s.get_proximal_npa3(),radius=s.p_r,n_steps=nstep  )
        ptsD = GeomTools.produce_sphere(location=s.get_distal_npa3()+distal_offset,radius=s.d_r,n_steps=nstep  )

        print 'Removing Close Points'
        pts = cls.only_pts_at_min_dist( ptsP+ ptsD, min_dist=0.01 )


        print 'Writing:', fTemp2
        with open(fTemp1,"w") as f:
            f.write("3 %d\n"%len(pts) )
            np.savetxt(f, np.array( pts  ))


        if os.path.exists(fTemp2):
            os.unlink(fTemp2)
        os.system("qhull T1 QJ o < %s > %s"%(fTemp1,fTemp2))


        # Don't do the subdivision, just copy the files:
        os.system("cp %s %s"%(fTemp2,fTemp2b))
        #fTemp2 = fTemp2b


        f = open(fTemp2b).read().split()
        nVertex,nFace,nEdge = [int(i) for i in f[1:4] ]
        assert nVertex > 5
        vertices = np.array( [float(t) for t in f[4:4+nVertex*3 ] ] ).reshape( nVertex, 3)


        triangles = np.array( [ int(t) for t in  f[4+nVertex*3: ] ] )
        triangles = triangles.reshape( (nFace,4) )
        triangles = triangles[ : , (1,2,3) ]



        print 'Writing STL'
        with open(fTemp3,'w') as fSTL:
            fSTL.write( "solid name\n" )
            for i in range( triangles.shape[0]):
                a,b,c = triangles[i,:]
                #print a,b,c
                #print 'a',  vertices[a,:]
                #print 'b',  vertices[b,:]
                #print 'c',  vertices[c,:]
                #assert np.sum( np.fabs( vertices[a,:] - vertices[b,:]) ) > 0.01
                #assert np.sum( np.fabs( vertices[b,:] - vertices[c,:]) ) > 0.01
                #assert np.sum( np.fabs( vertices[a,:] - vertices[c,:]) ) > 0.01

                fSTL.write("facet normal 0 0 0\n")
                fSTL.write("outer loop \n")
                fSTL.write("vertex %f %f %f\n"%(vertices[a,0],vertices[a,1],vertices[a,2] ) )
                fSTL.write("vertex %f %f %f\n"%(vertices[b,0],vertices[b,1],vertices[b,2] ) )
                fSTL.write("vertex %f %f %f\n"%(vertices[c,0],vertices[c,1],vertices[c,2] ) )
                fSTL.write("endloop \n")
                fSTL.write("endfacet\n")

            fSTL.write( "solid end" )


        print 'Running stl2gts...'
        if os.path.exists(fTemp4):
            os.unlink(fTemp4)

        os.system( "stl2gts < %s > %s"%(fTemp3,fTemp4) )

        assert os.path.exists(fTemp4)

        import gts
        f = open(fTemp4)
        s = gts.Surface()
        s = gts.read(f)

        s.cleanup()
        assert s.is_closed()
        assert s.is_orientable()

        #s.tessellate()
        return s

