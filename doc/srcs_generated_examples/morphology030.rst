
3. Load  SWC data from a string directly into a MorphologyArray
===============================================================


Load  SWC data from a string directly into a MorphologyArray.
We can load .swc from any file-like object, so we can use StringIO to load directly from strings.

Code
~~~~

.. code-block:: python

	
	
	
	
	
	
	
	#from morphforge.core.misc import StripCommentsAndBlankLines
	from morphforge.morphology.core import MorphologyArray
	from StringIO import StringIO
	
	swcSrc = """
	1 0 1.0 2.0 3.0 4.0 -1
	2 0 5.0 6.0 7.0 8.0 1
	"""
	
	m = MorphologyArray.fromSWC(StringIO(swcSrc))
	
	print 'Morphology Vertices:'
	print m._vertices
	
	print 'Morphology Connectivity:'
	print m._connectivity
	
	
	








Output
~~~~~~

.. code-block:: bash

    	Morphology Vertices:
	[[ 1.  2.  3.  4.]
	 [ 5.  6.  7.  8.]]
	Morphology Connectivity:
	[[1 0]]
	




