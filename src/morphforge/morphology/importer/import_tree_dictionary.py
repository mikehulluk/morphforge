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




from morphforge.morphology.importer.morphologyimporter import MorphologyImporter
from morphforge.core.misc import merge_dictionaries, SeqUtils, check_cstyle_varname
from morphforge.morphology.core import Region
from morphforge.morphology.core import Section
import math
from morphforge.morphology.core import MorphologyTree


class DictionaryLoader(object):
    @classmethod
    def load(cls,  morph_dict, name=None, metadata=None):
        """ Load a morphology from a recursive dictionary such as:
        {'root': {'length': 20, 'diam': 20, 'sections':
            [
                {'absangle': 120, 'length': 40, 'diam': 5, 'region': 'dendrite'},
                {'absangle': 240, 'length': 40, 'diam': 5, 'sections':
                    [
                        {'region': 'dendrite', 'diam': 5, 'relangle': 240, 'length': 40}
                    ], 'region': 'dendrite'},
                {'absangle': 5, 'length': 500, 'diam': 0.29999999999999999, 'region': 'axon'}],
            'region': 'soma'}}

            If addRootSection is true, then we make the root section, by adding in a fake section:

        """


        if not morph_dict or not morph_dict.has_key("root"): raise ValueError()
        valid_keywords = ["length", "diam", "id", "sections", "region", 'regions', "relangle", "absangle", "xyz"]
        required_keywords = ["diam"]



        # Does the root has a length variable? if it does, then lets add an intermediate node and remove it.
        root_node = morph_dict["root"]
        if root_node.has_key('length'):
          # Lets assume it extends backwards on the X-axis. This isn't great, but will work, although
          # visualisations are likely to look a bit screwy:

          assert not root_node.has_key('xyz')

          #print root_node


          #del root_node['length']
          new_root_node =  {'region': 'soma', 'diam': root_node['diam'], 'xyz':(0.0,0.0,0.0), 'sections': [root_node]}

          #print new_root_node

          root_node = new_root_node

          #assert False

          #section_dict[None] = Section(x=0.0, y=0.0, z=0.0, r=root_yaml_sect['diam'] / 2.0, region=None, parent=None)







        #First flatten the recursion, by copy
        #the dictionary and adding a parent tag:
        yaml_section_dict = {} # id to paramDict
        def recursivelyAddSectionToList(sectionNode, sectionNodeParentID, sectionDictInt):
            for k in sectionNode.keys():
                if not k in valid_keywords: raise ValueError("Invalid Keyword: " + k)
            for rK in required_keywords:
                if not rK in sectionNode.keys(): raise ValueError("Required Key: %s not found." % rK)

            children = sectionNode.get("sections", [])
            if sectionNode.has_key("sections"): del sectionNode["sections"]
            section_id = len(sectionDictInt)
            sectionDictInt[section_id] = merge_dictionaries([{"parent": sectionNodeParentID}, sectionNode])
            for c in children:  recursivelyAddSectionToList(c, section_id, sectionDictInt)

        #root_node = morph_dict["root"]

        recursivelyAddSectionToList(root_node, None, yaml_section_dict)


        #We now have a dictionary similar to:
        """ 0 {'length': 20, 'diam': 20, 'region': 'soma', 'parent': None}
            1 {'absangle': 120, 'length': 40, 'diam': 5, 'region': 'dendrite', 'parent': 0}
            2 {'absangle': 240, 'length': 40, 'diam': 5, 'region': 'dendrite', 'parent': 0}
            3 {'length': 40, 'region': 'dendrite', 'diam': 5, 'relangle': 240, 'parent': 2}
            4 {'absangle': 5, 'length': 500, 'diam': 0.29999999999999999, 'region': 'axon', 'parent': 0}
        """

        #Map a lack of region to region:"NoRegionGiven"
        for yml in yaml_section_dict.values():
            if not ("region" in yml or "regions" in yml):
                yml["region"] = "NoRegionGiven"

        region_names1 = [ yml["region"] for yml in yaml_section_dict.values() if yml.has_key("region") ]
        region_names2 = SeqUtils.flatten([ yml["regions"] for yml in yaml_section_dict.values() if yml.has_key("regions") ])

        region_names = list(set( region_names1 + region_names2) )
        region_dict = dict([ (n, Region(n)) for n in region_names])
        section_angles_dict = {}
        section_id_tags = []




        # We create a 'dummy' root node, and then the real root node.
        # This will be at index '0'

        # Do we need to create a dummy node explicity? This depends on whether the root node has a length:
        section_dict = {}
        root_yaml_sect = yaml_section_dict[0]


        if 'length' in root_yaml_sect.keys():
            assert False
            #section_dict[None] = Section(x=0.0, y=0.0, z=0.0, r=root_yaml_sect['diam'] / 2.0, region=None, parent=None)
        else:
            pass
            #section_dict[None] = Section(x=0.0, y=0.0, z=0.0, r=root_yaml_sect['diam'] / 2.0, region=None, parent=None)
            #assert False




        xyz = root_yaml_sect['xyz']
        section_dict[0] = Section(x=xyz[0], y=xyz[1], z=xyz[2], r=root_yaml_sect['diam'] / 2.0, region=None, parent=None)

        # Add the remaining nodes:
        for yamlID, yamlSect in yaml_section_dict.iteritems():

            if yamlSect['parent'] == None:
                continue

            #print yamlID, yamlSect

            parent_section = section_dict[ yamlSect["parent"] ]

            #Region:
            rg_names1 = [ yamlSect["region"] ] if yamlSect.has_key("region") else []
            rg_names2 = yamlSect["regions"] if yamlSect.has_key("regions") else []
            rgs = [ region_dict[rgName] for rgName in rg_names1 + rg_names2   ]
            # Since December 2010 each section is only allowed to have one
            # region.
            assert len(rgs) <= 1

            #Diameter & length:
            if not yamlSect.has_key("diam") or not (yamlSect["diam"] > 0): raise ValueError("indvalid radius")
            rad = yamlSect["diam"] / 2.0





            # End Point:
            def getYamlLength(yamlSect):
                if not yamlSect.has_key("length"): raise ValueError("No Length given")
                length = yamlSect["length"]
                if not length > 0: raise ValueError("Invalid Length")
                return length

            #We only specify end points by using angles or by xyz cooridinates:
            if int(yamlSect.has_key("absangle")) + int(yamlSect.has_key("relangle")) + int(yamlSect.has_key("xyz")) >= 2:
                raise ValueError("Too many ways for specifying endpoint")

            if yamlSect.has_key("xyz"):
                if not parent_section: angle = 0
                xyz = yamlSect["xyz"]


            elif yamlSect.has_key("absangle"):
                length = getYamlLength(yamlSect)
                angle = yamlSect["absangle"]
                xyz = (parent_section.d_x + length * math.cos(math.radians(angle)), parent_section.d_y + length * math.sin(math.radians(angle)), 0.0)

            elif yamlSect.has_key("relangle"):
                length = getYamlLength(yamlSect)
                angle = section_angles_dict[parent_section] + yamlSect["relangle"]
                xyz = (parent_section.d_x + length * math.cos(math.radians(angle)), parent_section.d_y + length * math.sin(math.radians(angle)), 0.0)

            else: # Default to 'abs'-angle to 0
                length = getYamlLength(yamlSect)
                angle = 0
                xyz = (parent_section.d_x + length * math.cos(math.radians(angle)), parent_section.d_y + length * math.sin(math.radians(angle)), 0.0)



            #Possible ID's:
            section_id_tag = yamlSect["id"] if yamlSect.has_key("id") else None
            if section_id_tag:
                check_cstyle_varname(section_id_tag)
            if section_id_tag in section_id_tags:
                raise ValueError("Duplicate Section ID: %s" % section_id_tag)
            if section_id_tag:  section_id_tags.append(section_id_tag)


            # Create the new section:
            if parent_section:
                new_section = parent_section.create_distal_section(x=xyz[0], y=xyz[1], z=xyz[2], r=rad, region=rgs[0], idtag=section_id_tag)
            else:
                new_section = Section(x=xyz[0], y=xyz[1], z=xyz[2], r=rad, region=None, idtag=section_id_tag)
                section_dict[None] = new_section




            # Calculate the angle of the current section:
            if parent_section:
                joining_vec = new_section.get_distal_npa3() - parent_section.get_distal_npa3()
                angle = math.radians(math.atan2(joining_vec[1], joining_vec[0]))
            section_angles_dict[new_section] = angle


            #Save the section:
            section_dict[yamlID] = new_section


        ## TODO: THIS IS A HACK! Ensure the dummy node has no attached regions:
        #section_dict[None].regions = []
        assert section_dict[0].region == None

        if section_dict[0].children == []: raise ValueError("No segments found")
        c = MorphologyTree(name=name, dummysection=section_dict[0], metadata=metadata)
        if len(c) < 1: raise ValueError
        return c



MorphologyImporter.register("fromDictionary", DictionaryLoader.load, allow_override=False, as_type=MorphologyTree)
