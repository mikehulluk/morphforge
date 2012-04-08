
1. Creating morphologies from python dictionaries
=================================================



Creating morphologies from python dictionaries.
In this example, we create 2 :py:class:`MorphologyTree` objects from python 
dictionaries, and then demonstrate iterating over the sections


Code
~~~~

.. code-block:: python

	
	
	"""Creating morphologies from python dictionaries.
	In this example, we create 2 :py:class:`MorphologyTree` objects from python 
	dictionaries, and then demonstrate iterating over the sections"""
	 
	from morphforge.morphology import MorphologyTree
	
	# Build a morphology consisting of a single-section:
	morphDict1 = {'root': {'length': 20, 'diam': 20} }
	m1 = MorphologyTree.fromDictionary(morphDict1, name="SimpleMorphology1")
	print "M1:"
	for section in m1:
	    print section
	
	
	# Build a morphology consisting of a 2 compartments: 
	morphDict2 = {'root': {'length': 20, 'diam': 20, 'sections': [{'length': 300, 'diam': 2}]  } }
	m2 = MorphologyTree.fromDictionary(morphDict2, name="SimpleMorphology2")
	print "M2:"
	for section in m2:
	    print "Section:"
	    print " - Proximal:",section.p_x,section.p_y, section.p_z, section.p_r
	    print " - Distal:  ",section.d_x,section.d_y, section.d_z, section.d_r
	
	


Output
~~~~~~

.. code-block:: bash

    	Setting Random Seed: 57533
	M1:
	<SectionObject: [0.000000,0.000000,0.000000, r=10.000000] -> [20.000000,0.000000,0.000000, r=10.000000], Length: 20.00, Region:NoRegionGiven, >
	M2:
	Section:
	 - Proximal: 0.0 0.0 0.0 10.0
	 - Distal:   20.0 0.0 0.0 10.0
	Section:
	 - Proximal: 20.0 0.0 0.0 10.0
	 - Distal:   320.0 0.0 0.0 1.0
	




