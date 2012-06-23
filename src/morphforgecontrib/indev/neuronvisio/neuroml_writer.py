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




from xml.dom.minidom import Document

# Create the minidom document

"""
# Create the <wml> base element
wml = doc.createElement("wml")
doc.appendChild(wml)

# Create the main <card> element
maincard = doc.createElement("card")
maincard.setAttribute("id", "main")
wml.appendChild(maincard)

# Create a <p> element
paragraph1 = doc.createElement("p")
maincard.appendChild(paragraph1)

# Give the <p> elemenet some text
ptext = doc.createTextNode("This is a test!")
paragraph1.appendChild(ptext)

# Print our newly created XML
print doc.toprettyxml(indent="  ")
"""
import sys

class MorphMLWriter(object):

    @classmethod
    def writemany(cls, cells, filename=None):

        doc = Document()

        # MorphML Node:
        morphml_node = doc.createElement("morphml")
        doc.appendChild(morphml_node)


        # Cells Node:
        cells_node = doc.createElement('cells')
        morphml_node.appendChild(cells_node)


        # MorphML Node:
        cell_naming_data = {}
        for cell in cells:
            res = cls.writeone(cell=cell, cells_node=cells_node, doc=doc )
            cell_naming_data[cell] = res




        txt = doc.toprettyxml()
        txt = cls.hackAroundNamespace(txt)

        return txt, cell_naming_data

    @classmethod
    def hackAroundNamespace(cls, txt):

        return txt.replace("<morphml>", "<morphml >")

    @classmethod
    def writeone(cls, cell, cells_node, doc, id_base=0):



        cell_node = doc.createElement('cell')
        cell_node.setAttribute("name", "%s"%cell.name)
        cells_node.appendChild(cell_node)




        segments_node = doc.createElement('segments')
        cell_node.appendChild(segments_node)

        # Give a name to each segment:
        segnamedict = dict( [ (seg, "%s_seg_%d"%(cell.name, i)) for i,seg in enumerate( cell.get_segmenter() )] )
        segiddict = dict( [ (seg,  "%d"%(i+id_base)) for i,seg in enumerate( cell.get_segmenter() )] )

        for seg in cell.get_segmenter():


            # Create the segments node:
            seg_node = doc.createElement("segment")
            segments_node.appendChild(seg_node)

            # Set the ID:
            seg_node.setAttribute("id", segiddict[seg] )
            seg_node.setAttribute("name", segnamedict[seg] )

            #Set the parent ID:
            pSeg = seg.get_parent_segment()
            if pSeg:
                seg_node.setAttribute("parent", segiddict[pSeg] )


            # Add the proximal and distal objects:
            seg_node_proximal = doc.createElement("proximal")
            seg_node_proximal.setAttribute("x", "%f"% (seg.get_proximal_np4a()[0] ) )
            seg_node_proximal.setAttribute("y", "%f"% (seg.get_proximal_np4a()[1] ) )
            seg_node_proximal.setAttribute("z", "%f"% (seg.get_proximal_np4a()[2] ) )
            seg_node_proximal.setAttribute("diameter", "%f"% (seg.get_proximal_np4a()[3] *2.0 ) )
            seg_node.appendChild(seg_node_proximal)

            seg_node_distal = doc.createElement("distal")
            seg_node.appendChild(seg_node_distal)


            print seg

        return (segnamedict, segiddict)












        #assert False


