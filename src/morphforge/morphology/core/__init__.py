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

"""Object-models for morphology representations.  


Dual-Represention of  morphologies
-----------------------------------

In morphforge, as in many other tools, morphologies are represented as a tree of joined conical frustra (cylinders with different radii ends). 


.. figure:: /img_srcs/new_morphology_original.svg
    :align: center
    

Figure 1A shows a projection of an original neuron morphology,
In figure 1B, the morphology is approximated as a set of conical frustra. At every joining point of multiple frustra, the radii are the same.

There are 2 ways of considering these sets of frustra:
 * **TreeBased:** As a tree of *Sections*  (Figure 1C). 
 * **VertexBased:** As a set of vertices and a set of connections between them.

Underneath, these two representations contain the same information, but the different object model representations have strengths for different tasks.
In morphforge, they are represented as two different classes:  :py:class:`~.core.tree.MorphologyTree` and :py:class:`~.core.array.MorphologyArray`.

 * **TreeBased:** (:py:class:`~.core.tree.MorphologyTree` ) is arguably more intuitive to read. It is also what the :py:mod:`morphforge.simulation` layer handles.
 * **VertexBased:** (:py:class:`~.core.array.MorphologyArray` ) is more efficient in speed & memory size for large morphologies.


For more information about the representations, see the documentation for the submodules :py:mod:`~.core.tree` and :py:mod:`~.core.array`



Converting between representations
-----------------------------------


In general, you will only need to use one of the two representations, depending on what your are doing. However, :py:class:`~.core.tree.MorphologyTree`  and :py:class:`~.core.array.MorphologyArray`  objects can be converted to each type using the methods "to_array()" and "to_tree()". 


.. code-block:: python
 
 
   # Load a MorphArray object and convert 
   # it to MorphTree object
   morph_array = MorphArray.fromSWC(...)
   morph_tree = morph_array.to_array()
    
   # Vice-Versa
   morph_tree2 = MorphTree.fromSWC(...)
   morph_array = morph_tree2.to_array()
   
   # Trying to convert an object to its own
   # type returns the original object:
   morph_tree3 = morph_tree2.to_tree()
   assert morph_tree3 is morphtree2 
   
"""

 



from tree import MorphologyTree, Section, Region, MorphLocation, MorphPath
from array import MorphologyArray


__all__ = ['MorphologyTree','Section','Region','MorphLocation','MorphologyArray', 'MorphPath']
