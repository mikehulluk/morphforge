from morphforge.morphology.util.morphlocator import MorphLocator
from morphforge.simulation.core.celllocation import CellLocation
import itertools
from morphforge.core.misc import SeqUtils

class CellLocator(object):
    """Provides the same functionality as MorphLocator, except that it operates on cells."""


    @classmethod
    def get_locations_at_distance_away_from_dummy(cls, cell, distance, section_predicate=None):

        morph_locs = MorphLocator.get_locations_at_distance_away_from_dummy(
                                        morphology=cell.morphology,
                                        distance=distance,
                                        section_predicate=section_predicate)
        return [ CellLocation(cell=cell, morphlocation=ml) for ml in morph_locs]


    @classmethod
    def get_locations_at_distances_away_from_dummy(cls, cell, distances, section_predicate=None):
        return list( itertools.chain( *[cls.get_locations_at_distance_away_from_dummy(cell=cell, distance=distance, section_predicate=section_predicate) for distance in distances]  ) )

    @classmethod
    def get_location_at_distance_away_from_dummy(cls, cell, distance, section_predicate=None):
        """Utility Function"""
        return SeqUtils.expect_single( cls.get_locations_at_distance_away_from_dummy(cell=cell, distance=distance, section_predicate=section_predicate) )
