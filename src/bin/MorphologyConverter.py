#! /usr/bin/python


#import morphforge.stdimports as mf

import sys

#from morphforge.morphology.builders import MorphologyLoader
from morphforge.morphology.mesh import MeshWriterPLY
from morphforge.morphology.mesh import MeshBuilderRings

def swc_to_ply(swc_path, ply_path=None):
    ply_path = ply_path or swc_path.replace('.swc','.ply')
    #morphologies = MorphologyLoader.fromSWCSet(src=open(swc_path))
    SWCLoader.LoadSet(src=open(swc_path), morphname="UnknownSWC", regionNames=regionNames)
    
    meshes = [ MeshBuilderRings.build(morph) for morph in morphologies ]

    # Save the individual meshes:
    for i,mesh in enumerate(meshes):
        MeshWriterPLY.write(mesh, ply_path.replace('.ply', '_%d.ply'%i) )

    # Save a set of meshes:
    combined_mesh = TriangleMesh.merge( meshes )
    MeshWriterPLY.write(combined_mesh, ply_path )


    

        
        
def main():
    
    print sys.argv
    for swc_name in sys.argv[1:]:
        ply_name = swc_name.replace('.swc','.ply')
        print "Converting: %s to %s " % (swc_name, ply_name)
        swc_to_ply(swc_name, ply_name)
        
    
main()
