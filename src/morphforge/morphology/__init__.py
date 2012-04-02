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

"""
The morphology package provides an object model for representing neuronal morphologies, as well as tools for import, export, traversal, and rendering.


Blah 
######

In morphforge, morphologies are represented as a tree of joined cylinders. If we wanted to represent
the following morphology:

.. image:: /img_srcs/morphology_overview_bio.svg
    :align: center

Then we might break it up into a set of nodes and connections as follows:

.. image:: /img_srcs/morphology_overview.svg
    :align: center

In this scheme, each *node* has a position :math:`$(x,y,z)$`, and a radius denoted by the green line. 
Each node, except one, has a single parent.    



Hello
######

.. image:: /img_srcs/morphology_overview_simpledetails.svg
    :align: center



.. image:: /img_srcs/morphology_overview_simplecylinders.svg
    :align: center
 
 
 
This package provides the building blocks for defining a neuron's morphology.
It contains submodules for creating, manipulating, viewing, and storing
morphologies.


A neuron is approximated as a tree of cylinders, in which the two ends of the
cylinder can have different radii.  Each of these cylinder is a 'Section', and
can have 'Region's associated with it.  (Regions are useful for setting up
membrane properties later).  We can specify specific 'MorphLocation's on the
morphology, which are a 'Section' and distance along the section specified
between 0-1, as is done in NEURON.

Since the morphology is a tree, we often traverse it. Algorithms for this can
be accessed either directly through the 'parent' and 'children' attributes of
the Section objects, but since this is a common task, visitor classes can be
defined without defining explicit traversal code [see the visitor module]

Visualisation is provided through matplotlib and MayaVi in the ui module. """

from morphforge.morphology.core import MorphologyTree
from morphforge.morphology.core import MorphologyArray


# Ensure that the plugins get added dynamically:
import importer
import exporter



