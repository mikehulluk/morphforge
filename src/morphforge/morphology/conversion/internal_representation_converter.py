

from morphforge.morphology.core import Section
import collections
from morphforge.morphology.visitor.visitorbaseclasses import SectionIndexerDF
from morphforge.morphology.core.array import MorphologyArray
from morphforge.morphology.conversion import AutoRegionToIntMapTable
from morphforge.morphology.core import Region
import copy

class MorphologyConverter():
    
    @classmethod
    def tree_to_array(cls, tree, region_number_to_name_bidict=None):
            
        if region_number_to_name_bidict is None:
            if tree.region_number_to_name_bidict is not None:
                region_number_to_name_bidict = copy.deepcopy( tree.region_number_to_name_bidict ) 
            else:
                region_number_to_name_bidict = AutoRegionToIntMapTable()
                
        
        vertices= [ None ] * ( len(tree) + 1 )
        connectivity = [] 
        section_types = []
        section_index = SectionIndexerDF(morph=tree, offset=1).dict
        section_index[tree.getDummySection()] = 0 
        
        
        for seg in tree._every_section():
            index = section_index[seg]
            
            # Store the vertices:
            vertices[ index ] = seg.get_distal_npa4()
            
            # Store the link to the parent:
            if not seg.is_dummy_section():
                connectivity.append( (index,section_index[seg.parent]  ) )
            
            # Store the type:
            if not seg.is_dummy_section():
                region = seg.region
                if region:
                    section_types.append( region_number_to_name_bidict.regionNameToInt(region.name) )
                else:
                    section_types.append( 0 )
                 
        m = MorphologyArray(vertices=vertices, connectivity=connectivity, dummy_vertex_index=0, section_types=section_types, )
        return m
        
    
    @classmethod
    def array_to_tree(cls, array, region_number_to_name_bidict=None):
    
        if region_number_to_name_bidict is None:
            if array.region_number_to_name_bidict is not None:
                region_number_to_name_bidict = copy.deepcopy( array.region_number_to_name_bidict ) 
            else:
                region_number_to_name_bidict = AutoRegionToIntMapTable()
                
                
        name_to_region_map= {}
        
        
        dummy_vertex_index = array._dummy_vertex_index
        
        
        index_to_section_map = {}
        
        # Create the root section:
        x,y,z,r = array._vertices[dummy_vertex_index]
        dummySection = Section( region=None,x=x,y=y,z=z,r=r )
                                
        
        index_to_section_map[dummy_vertex_index] = dummySection
        

        indices_to_visit = collections.deque([dummy_vertex_index])
        
        while indices_to_visit:
            index = indices_to_visit.pop()
            section = index_to_section_map[index]
            
            connections_to_index = array.connections_to_index(index)
            
            for conn in connections_to_index:
                
                # Have we made this connection already?:
                if conn in index_to_section_map:
                    continue
                
                # No? Lets make a connection:
                else:
                    x,y,z,r = array._vertices[conn]
                    index_of_connection = array.index_of_connection(index,conn)
                    
                    # Create the region, if it doesn't already exist:
                    rgnInt =  array._section_types[index_of_connection]
                    
                    
                    rgn_name = region_number_to_name_bidict.intToRegionName(int=rgnInt)
                    
                    if rgn_name is None:
                        rgn=None
                    else:
                        if not rgn_name in name_to_region_map:
                            name_to_region_map[rgn_name] = Region(rgn_name)
                        rgn = name_to_region_map[rgn_name]    
                        
                    newsection =  section.create_distal_section(region=rgn, x=x,y=y,z=z,r=r )
                    index_to_section_map[conn] = newsection
                    indices_to_visit.append( conn )
        
        from morphforge.morphology.core import MorphologyTree
        tree = MorphologyTree(name=array.name, dummysection=dummySection, region_number_to_name_bidict=region_number_to_name_bidict )
        
        
        # A sanity check:
        
        assert len(tree) == len(array), 'The tree and array are not the same size! %d vs %d'%(len(tree), len(array))
        return tree      
                
            
