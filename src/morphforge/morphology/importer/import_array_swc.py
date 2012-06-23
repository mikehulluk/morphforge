#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
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
from morphforge.morphology.core import MorphologyArray
from morphforge.morphology.importer.morphologyimporter import MorphologyImporter
from StringIO import StringIO
from morphforge.morphology.errors import MorphologyImportError
from morphforge.morphology.core import MorphologyTree


class NewSWCLoader(object):

    @classmethod
    def load_swc_single(cls,  src, name=None):

        dtype= {'names':   ('id', 'type', 'x','y','z','r','pid'),
                'formats': ('int32', 'int32', 'f4','f4','f4','f4','int32') }

        d = np.loadtxt(src,dtype=dtype )

        if len( np.nonzero( d['pid']==-1)) != 1:
            assert False, "Unexpected number of id's of -1 in file"

        # We might not nessesarily have continuous indices in the
        # SWC file, so lets convert them:
        index_to_id = d['id']
        id_to_index_dict = dict( [(id,index) for index,id in enumerate(index_to_id) ] )
        if len(id_to_index_dict) != len(index_to_id):
            s =  "Internal Error Loading SWC: Index and ID map are different lengths."
            s += " [ID:%d, Index:%d]"%( len(index_to_id), len(id_to_index_dict) )
            raise MorphologyImportError(s)

        # Vertices are easy:
        vertices =  d[ ['x','y','z','r'] ]
        vertices =  np.vstack( [d['x'], d['y'],d['z'],d['r'] ]).T

        # Connections need to translate id_to_index:
        connection_indices = [ (id_to_index_dict[ID], id_to_index_dict[pID]) for ID,pID in d[['id','pid']] if pID != -1 ]

        # Types are specified per connection:
        section_types = [ swctype for ID,swctype,pID in d[['id','type','pid']] if pID != -1 ]

        return MorphologyArray(vertices=vertices, connectivity=connection_indices, section_types=section_types, dummy_vertex_index=0, name=name )


    @classmethod
    def load_swc_set(cls, src):
        """Naive implementation, that doesn't take account of interleaving of nodes"""
        lines = [l.strip() for l in src.readlines()]
        lines = [l for l in lines if l and l[0] != '#']

        # Break into sections where we get a new parent:
        splits = [[]]
        for l in lines:

            if int( l.split()[-1] ) == -1:
                splits.append( [] )
            splits[-1].append(l)

        splits = splits[1:]

        data_blocks = [ "\n".join( blk  ) for blk in splits ]
        fileObjs = [ StringIO(blk) for blk in data_blocks ]


        morphs = [ cls.load_swc_single( src=fO)  for fO in  fileObjs ]
        return morphs


# To Array:
MorphologyImporter.register("fromSWC", NewSWCLoader.load_swc_single, as_type=MorphologyArray)

# To Tree:
def _load_swc_single_tree(*args,**kwargs):
    return NewSWCLoader.load_swc_single(*args,**kwargs).to_tree()
MorphologyImporter.register("fromSWC", _load_swc_single_tree,  as_type=MorphologyTree)






