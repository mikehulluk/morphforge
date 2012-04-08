from morphforge.morphology.util.morphlocator import MorphLocator
from morphforge.simulation.core.celllocation import CellLocation
import itertools
from morphforge.core.misc import ExpectSingle

class CellLocator(object):
    """Provides the same functionality as MorphLocator, except that it operates on cells."""
    
    
    @classmethod
    def getLocationsAtDistanceAwayFromDummy(cls, cell, distance, section_predicate=None):
         
        morph_locs = MorphLocator.getLocationsAtDistanceAwayFromDummy(
                                        morphology=cell.morphology, 
                                        distance=distance, 
                                        section_predicate=section_predicate)
        return [ CellLocation(cell=cell, morphlocation=ml) for ml in morph_locs]
        
        
    @classmethod
    def getLocationsAtDistancesAwayFromDummy(cls, cell, distances, section_predicate=None):
        return list( itertools.chain( *[cls.getLocationsAtDistanceAwayFromDummy(cell=cell, distance=distance, section_predicate=section_predicate) for distance in distances]  ) )
        
    @classmethod
    def getLocationAtDistanceAwayFromDummy(cls, cell, distance, section_predicate=None):
        """Utility Function"""
        return ExpectSingle( cls.getLocationsAtDistanceAwayFromDummy(cell=cell, distance=distance, section_predicate=section_predicate) )
