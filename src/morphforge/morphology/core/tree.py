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



docs = """Tree-based object-model of morphologies.

In the tree based representation, a morphology is considered as a set of
:py:class:`~.Section`. A :py:class:`~.Section` is an unbranching length
neurons, which can be connected to other sections at its end points. If it does
connect to other sections at the end points, then it shares the same position
and radius information at that point.



.. image:: /img_srcs/new_morphology_overview_simplecylinders_tree_simple.svg
    :align: center

For example, Figure 1 shows a morphology composed of 4 sections. Each end of
each frustra is specified as a point in 3D space and a radius:
:math:`(X,Y,Z);R`.  However, since positions and radii are shared, at join
points, only stores a reference to its parent (orange arrow), and its distal
coordinate (red dots).  Therefore


.. math::

    Section1^{distal}(x,y,z,r)=Section2^{proximal}(x,y,z,r) = (10,0,0,20)

    Section2^{distal}(x,y,z,r)=Section3^{proximal}(x,y,z,r) = (20,0,0,10)

    ...

Some care need to be taken around the start of the tree. In order for
`Section1` to have some length, We introduce a special Section, with no parent
(and hence no length), called the Dummy-Section, shown as a blue dot. This
section is just used for its position & radius coordinate; it does not
represent any volume or surface area.

The dummy section is always the root of the tree. Sections whose parents are
the Dummy-Section, are 'Root' sections. (shown in light green).  This means
that there can be many root nodes in a tree, for example:

.. image:: /img_srcs/new_morphology_overview_simplecylinders_tree_complex.svg
    :align: center


.. note::

    There is an assumption that the root nodes in the models are found made
    at the somata of cells. The terms 'Proxmial' and 'Distal' on Section
    objects refer to the ends closest and furthest away from the dummyroot
    section respectively.


.. note::

    This object model is heavily based on the .swc file format. DummyNode
    correspond to lines in the .swc format with a parent ID of -1.


To construct the morphology in the top figure; the code would look like:


.. code-block:: python

    askjdls
    asljf



.. todo::

    This is not the way morphologies are recommended to be built.
    It may be more convenient to use the 'DictionaryLoader'




Regions provide a way to group sections together, for example as 'axon',
'soma'.  Each Section in a morphology can optionally be assigned to a single
Region.  Regions are used by the :py:mod:`morphforge.simulation` layer for
specifying channel distributions over a morphology.

.. note::

    This way of specifying Regions is very similar to the 'type' field in the
    .swc file format.

Each Section can be assigned an 'ID-Tag'. This is simply a string that
can be used to refer to a particular section easily later. An IDTag can not be
repeated in a morphology.  For example, when constructing a morphology, we
might tag the main soma section, so that is it simple to add current clamps for
exampl in simulations.


.. todo::

    Reference some example.




.. todo::

    MorphLocations and MorphPaths

"""







import numpy
import numpy as np
import math
import itertools

from morphforge.core import SeqUtils
from morphforge.core import check_cstyle_varname

from morphforge.morphology.core.base import MorphologyBase
from morphforge.morphology.visitor import SectionListerDF
from morphologyconsistency import MorphologyConsistencyMgr




class Section(object):

    # Properties:
    d_x = property(lambda self: self._d_pos[0], None, doc="Distal x coordinate")
    d_y = property(lambda self: self._d_pos[1], None, doc="Distal y coordinate")
    d_z = property(lambda self: self._d_pos[2], None, doc="Distal z coordinate")
    d_r = property(lambda self: self._d_r, None, doc="Distal radius")

    p_x = property(lambda self: self.parent._d_pos[0], None, doc="Proximal x coordinate")
    p_y = property(lambda self: self.parent._d_pos[1], None, doc="Proximal y coordinate")
    p_z = property(lambda self: self.parent._d_pos[2], None, doc="Proximal z coordinate")
    p_r = property(lambda self: self.parent._d_r, None, doc="Proximal radius")

    region = property(lambda self: self._region, None, )
    idtag = property(lambda self: self._idTag, None)
    parent = property(lambda self: self._parent, None, )
    children = property(lambda self: self._children, None)



    def __init__(self, x, y, z, r, region, parent=None, idtag=None):
        """ Creation of the section.  """

        self._d_pos = numpy.array((float(x), float(y), float(z)))
        self._d_r = float(r)

        self._parent = parent
        self._children = []
        self._region = region
        self._idTag = idtag


        # Post Processing: tidy up loose ends:
        if region is not None:
            region.add_section(self)
        if not self.is_dummy_section():
            if not self in self.parent.children:
                self.parent.children.append(self)


    # Adding new sections:
    def create_distal_section(self, x, y, z, r, region, idtag=None):
        """Creates and returns a new Section object from its distal end.
        The parameters are the same as for the constructor.
        """
        return Section(parent=self, x=x, y=y, z=z, r=r, region=region, idtag=idtag)


    def is_a_root_section(self):
        if self.is_dummy_section():
            return False
        return self.parent.is_dummy_section() == True

    def is_dummy_section(self):
        return self.parent == None

    def is_leaf(self):
        return len( self.children ) == 0



    def get_npa3(self, position):
        assert 0 <= position <= 1
        return self.get_proximal_npa3() + self.get_proximal_to_distal_vector_npa3() * position

    def get_npa4(self, position):
        assert 0 <= position <= 1
        return self.get_proximal_npa4() + self.get_proximal_to_distal_vector_npa4() * position


    def get_distal_npa3(self):
        """Returns the 3 coordinates of the distal end of the section.  """
        return self._d_pos

    def get_distal_npa4(self):
        """Returns the 3 coordinates and the radius of the distal end of the
            section.  """
        return numpy.array((self.d_x, self.d_y, self.d_z, self.d_r))

    def get_proximal_npa3(self):
        """ Returns the 3 coordinates of the proximal end of the section.  """
        assert not self.is_dummy_section()
        return self.parent._d_pos

    def get_proximal_npa4(self):
        """Returns the 3 coordinates and the radius of the proximal end of the section.  """
        assert not self.is_dummy_section()
        return numpy.array((self.p_x, self.p_y, self.p_z, self.p_r))






    def __repr__(self):
        if self.is_dummy_section():
            return "DummySection"

        def EndSummary(e): return "[%f,%f,%f, r=%f]" % (e.d_x, e.d_y, e.d_z, e.d_r) if e else '<None>'
        end_string = "SectionObject: " + EndSummary(self.parent) + " -> " + EndSummary(self) + ", "
        rg_string = "Region:" + self.region.name +", " if self.region else ""
        id_string = "idtag:" + self.idtag + ", " if self.idtag else ""
        ln_string = "Length: %2.2f, " % self.get_length()
        return "<" +end_string + ln_string + rg_string + id_string +">"

    def get_proximal_to_distal_vector_npa3(self):
        """Returns the vector that joins the proximal end of the section to the distal end.  """
        return self.get_distal_npa3() - self.get_proximal_npa3()

    def get_proximal_to_distal_vector_npa4(self):
        """Returns the vector that joins the proximal end of the section to the distal end.  """
        return self.get_distal_npa4() - self.get_proximal_npa4()



    def get_length(self):
        assert not self.is_dummy_section(), "Getting Length of dummy section!"
        return numpy.linalg.norm( self.get_proximal_to_distal_vector_npa3() )


    def get_area(self,include_end_if_terminal=False):
        """ Returns the area of the section.  """
        #include_end_if_terminal=False
        # http://mathworld.wolfram.com/ConicalFrustum.html
        assert not self.is_dummy_section(), "Getting area of dummy section!"

        # We need to consider this; since there are 2 ends that might be
        # open
        #assert not include_end_if_terminal

        R = self.d_r
        r = self.p_r
        l = self.get_length()
        lateral_area =  math.pi * (R+r) * math.sqrt( (R-r)**2 + l**2 )

        if include_end_if_terminal and (self.is_leaf()  or self.is_a_root_section() ):
            A = lateral_area
            if self.is_leaf():
                A+= math.pi*R*R
            if self.is_a_root_section() and len(self._parent._children)==1:
                A+= math.pi*r*r
            return A

        else:
            return lateral_area


    def get_volume(self):
        """Returns the volume of the section."""
        assert not self.is_dummy_section(), "Getting volume of dummy section!"

        R = self.d_r
        r = self.p_r
        l = self.get_length()
        return (1.0/3.0) * math.pi * l * ( R*R + R*r + r*r)


    area = property(get_area)
    surface_area = property(get_area)
    volume = property(get_volume)


    # Deprecated:
    def get_vectorfrom_parent_np4(self):
        """ Deprecated: Returns the directional vector and the radious difference in the section.  """
        assert False, 'Deprecated'
        return self.get_distal_npa4() - self.get_proximal_npa4()















class Region(object):
    """
    Region is a collection of sections. It is used for annotating the sections
    (i.e. axon, soma, proximal dendrite, ...) and for collectively assigning
    the channels and membrane definitions to the sections.
    """


    def __str__(self):
        s = "<RegionObject: Name: %s, nSections: %d (ID:%s)>" % (self.name, len(self.sections), id(self) )
        return s
    def __init__(self, name):
        check_cstyle_varname(name)
        self.name = name
        self.sections = []
        self.morph = None


    def __iter__(self):
        return iter(self.sections)

    def __len__(self):
#        assert False
        return len(self.sections)

    def add_section(self, section):
        """Adding a section to the region."""

        if section in self.sections:
            raise ValueError("Section already in Region.sections")

        self.sections.append(section)


    def set_morphology(self, morph):

        if not morph:
            raise ValueError()
        if self.morph:
            raise ValueError()
        self.morph = morph

    @property
    def surface_area(self):
        return sum( s.surface_area for s in self)





class MorphLocation(object):
    """A MorphLocations represents a cell_location (more accurately a disk) on a
    morphology. It is specied by a Section, and the proportion of the distance
    along it, sectionpos. Sectionpos is a float from 0.0 (most proximal) to 1.0
    (most distal) (like NEURON).
    """

    # Read-only's:
    @property
    def section(self):
        return self._section
    @property
    def sectionpos(self):
        return self._sectionpos


    def __init__(self, section, sectionpos, position_info=None):
        self._section = section
        self._sectionpos = sectionpos
        assert 0.0 <= sectionpos <= 1.0


    def get_3d_position(self,):
        """Returns the 3D position of the morphology cell_location"""
        local_vector = self.sectionpos * self.section.get_proximal_to_distal_vector_npa3()
        return self.section.get_proximal_npa3() + local_vector










class MorphologyTree(MorphologyBase):

    def to_tree(self):
        return self

    def to_array(self, **kwargs):
        from morphforge.morphology.conversion import MorphologyConverter
        return MorphologyConverter.tree_to_array(self,**kwargs)








    def __init__(self, name=None, dummysection=None, metadata=None, region_number_to_name_bidict=None):
        MorphologyBase.__init__(self, region_number_to_name_bidict=region_number_to_name_bidict, name=name, metadata=metadata)

        self._regions = None
        self._dummysection = None

        if dummysection:
            self.set_dummy_section(dummysection)

        self.ensure_consistency(requiretreeset=False)



    def __str__(self):
        s = "MorphologyTree Object: Name: %s, nSections: %d, Regions:[%s], idTags:[%s]" % (self.name,
                                                                       len(self),
                                                                       ",".join([rgn.name for rgn in self.get_regions()]),
                                                                       ",".join(self.get_idtags())
                                                                       )
        return s


    # It is not nessesary to define the dummy node when we call __init__,
    # but we need to check it is set before being requested.
    def is_dummy_section_set(self):
        """ Returns whether a tree has been assigned to this morphology"""
        return self._dummysection != None


    def set_dummy_section(self, dummysection):
        """ Set the tree node for the morphology. You can only do this to a morphology
        which has not had its tree assigned yet. The root-object of the tree is a 'dummysection',
        but this is **not** the same as a root node.
        """
        assert not self.is_dummy_section_set(), "Setting of MorphologyTree Twice"
        assert isinstance(dummysection, Section), "Setting the tree with something that is not a Section object"
        assert dummysection.is_dummy_section(), "Dummysection is not a dummy section!"

        assert MorphologyConsistencyMgr.get_checker(self).disable()
        self._dummysection = dummysection
        for r in self.get_regions():
            r.set_morphology(self)
        assert MorphologyConsistencyMgr.get_checker(self).enable()

        assert self.ensure_consistency(), "Morphology is not consistent"





    def _every_section(self):
        """Includes dummy section"""
        return itertools.chain( *[[self.get_dummy_section()], self  ] )


    # Iteration over morphologies:

    def __iter__(self):
        """ Iteration over each of the sections."""

        assert self.ensure_consistency(), "Morphology is not consistent"

        #TODO: replace this with a iterator method on one of the sections in the tree. I
        # need to think about this. it might be the dummysection. This will be cleaner.
        return iter(SectionListerDF(self)())

    def __len__(self):
        """Returns the numbers of sections in the morphology """
        assert self.ensure_consistency()

        # TODO: as per iter
        return len(SectionListerDF(self)())





    def get_dummy_section(self):
        assert self.ensure_consistency(), "MorphologyTree not consistent"
        return self._dummysection

    def get_root_section(self):
        assert False, 'Deprecated'
        assert self.ensure_consistency(), "MorphologyTree not consistent"
        return self._dummysection.children[0]

    def get_root_sections(self):
        return self._dummysection.children



    def get_regions(self):
        """ Returns a list of unique regions in the morphology
        """
        assert self.ensure_consistency()

        if self._regions is None:
            all_regions = [ section.region for section in self]
            self._regions = list(set(all_regions))
            self._regions.sort(key=lambda r:r.name)
            if self._regions.__contains__(None):
                self._regions.remove(None)
        return self._regions

    @property
    def regions(self):
        return self.get_regions()

    def get_region_names(self):
        return [ r.name for r in self.get_regions()]

    def get_region(self, name):
        """ Returns a Region object relevant to this tree, given a filename"""
        assert self.ensure_consistency()

        return SeqUtils.filter_expect_single(self.get_regions(), lambda r: r.name == name)

    def get_section(self, idtag):
        """ Returns a Section object with a given id"""
        assert self.ensure_consistency()
        return SeqUtils.filter_expect_single(self, lambda s: s.idtag == idtag)

    def get_idtags(self):
        return [ section.idtag for section in self if section.idtag]




    def ensure_consistency(self, requiretreeset=True):
        """
        This method is used to check the consistency of the tree. In production code, all calls to this should be optimised out using
        -O optimisation to python.
        This requests a check from MorphologyConsistencyMgr. We do this to avoid storing additional attributes in the MorphologyTree
        Object, which could cause upset for calculating md5sums or pickling.
        """
        if requiretreeset:
            assert self.is_dummy_section_set()


        MorphologyConsistencyMgr.check_morphology(self)
        return True



    @property
    def surface_area(self):
        return sum( s.surface_area for s in self)
















class MorphPath(object):

    DirDistal = 'DirDistal'
    DirProximal = 'DirProximal'


    # Find the paths back to the dummy_section()::
    @classmethod
    def get_sections_to_root(cls,sect):
        sects = set([])
        current_sect = sect.parent
        while not current_sect.is_dummy_section():
            sects.add(current_sect)
            current_sect = current_sect.parent
        return sects


    def __init__(self, morphloc1, morphloc2):

        # Check they are on the same morphology!
        s1 = morphloc1.section
        s2 = morphloc2.section
        while not s1.is_dummy_section(): s1 = s1.parent
        while not s2.is_dummy_section(): s2 = s2.parent
        assert s1 is s2



        # Remap dummy sections to being proximal on the
        #first child section, to reduce special case handling:
        if morphloc1.section.is_dummy_section():
            morphloc1 = MorphLocation( morphloc1.section.children[0], 0.0)
        if morphloc2.section.is_dummy_section():
            morphloc2 = MorphLocation( morphloc2.section.children[0], 0.0)




        self.morphloc1 = morphloc1
        self.morphloc2 = morphloc2

        # TO SET:
        self.morphloc1_dir = None
        self.morphloc2_dir = None
        self._connecting_sections = []


        if morphloc1.section == morphloc2.section:

            # Points in the same section:
            self._connecting_sections = []
            if morphloc1.sectionpos < morphloc2.sectionpos:
                self.morphloc1_dir, self.morphloc2_dir =  self.DirDistal, self.DirProximal
            else:
                self.morphloc1_dir, self.morphloc2_dir =  self.DirProximal, self.DirDistal

        else:

            s1_sects = MorphPath.get_sections_to_root(morphloc1.section)
            s2_sects = MorphPath.get_sections_to_root(morphloc2.section)


            # Is one a direct parent of the other?
            if morphloc1.section in s2_sects:
                self._connecting_sections = set.symmetric_difference( s1_sects,s2_sects)
                self.morphloc1_dir, self.morphloc2_dir =  self.DirDistal, self.DirProximal
            elif morphloc2.section in s1_sects:
                self._connecting_sections = set.symmetric_difference( s1_sects,s2_sects)
                self.morphloc1_dir, self.morphloc2_dir =  self.DirProximal, self.DirDistal

            else:
                assert False


            # Remove the original sections,  from the list of
            # connecting sections:
            self._connecting_sections.discard( morphloc1.section)
            self._connecting_sections.discard( morphloc2.section)




        assert not self.morphloc1.section in self._connecting_sections
        assert not self.morphloc2.section in self._connecting_sections


    def get_length(self):

        #Handle the special case of both being on the same section:
        if self.morphloc1.section == self.morphloc2.section:
            return self.morphloc1.section.get_length() * np.fabs( self.morphloc1.sectionpos - self.morphloc2.sectionpos )


        def s_len(loc, dir):
            if dir == MorphPath.DirDistal:
                return (1.0-loc.sectionpos) * loc.section.get_length()
            elif dir == MorphPath.DirProximal:
                return loc.sectionpos * loc.section.get_length()
            else:
                assert False

        s1_length =  s_len(self.morphloc1, self.morphloc1_dir )
        s2_length =  s_len(self.morphloc2, self.morphloc2_dir )
        connecting_section_lengths = [ s.get_length() for s in self._connecting_sections]
        l = s1_length + s2_length + sum(connecting_section_lengths)
        return l


    #def isSectionInPath(self, section):
    #    return section in self._connecting_sections

    #def isSectionOnEndpoint(self, section):
    #    return section in ( self.morphloc1.section, self.morphloc2.section )





