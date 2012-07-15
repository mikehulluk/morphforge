
4. Converting between the morphology representations
====================================================


Converting between the morphology representations

Code
~~~~

.. code-block:: python

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
	
	
	
	
	
	from morphforge.core import LocMgr, Join
	from morphforge.morphology.core import MorphologyTree
	
	
	testSrcsPath = LocMgr().get_test_srcs_path()
	srcSWCFile = Join(testSrcsPath, "swc_files/28o_spindle20aFI.CNG.swc")
	
	mTree = MorphologyTree.fromSWC(src=open(srcSWCFile))
	mArray = mTree.to_array()
	
	print 'Vertex Data'
	print mArray._vertices
	
	
	# Convert back
	mTree2 = mArray.to_tree()
	
	# Round-trip: check that the SWC outputs are the same:
	assert mTree.toSWCStr() == mTree2.toSWCStr()
	print 'Finished OK'
	
	
	
	
	








Output
~~~~~~

.. code-block:: bash

    	Vertex Data
	[[ -1.61e+00   6.23e+00  -7.44e-02   1.56e+01]
	 [ -9.08e+00   3.01e+01  -1.14e+00   4.70e+00]
	 [ -1.08e+01   3.64e+01  -1.14e+00   4.28e+00]
	 ..., 
	 [ -1.61e+01  -1.85e+02   6.97e+00   1.68e+00]
	 [ -1.70e+01  -1.84e+02   6.97e+00   1.68e+00]
	 [ -1.97e+01  -1.88e+02   1.17e+01   1.35e+00]]
	Finished OK
	




