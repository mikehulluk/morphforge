
4. Converting between the morphology representations
====================================================


Converting between the morphology representations

Code
~~~~

.. code-block:: python

    
    
    
    
    
    
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

        Openning ScriptFlags
    Vertex Data
    [[ -1.61e+00   6.23e+00  -7.44e-02   1.56e+01]
     [ -9.08e+00   3.01e+01  -1.14e+00   4.70e+00]
     [ -1.08e+01   3.64e+01  -1.14e+00   4.28e+00]
     ..., 
     [ -1.61e+01  -1.85e+02   6.97e+00   1.68e+00]
     [ -1.70e+01  -1.84e+02   6.97e+00   1.68e+00]
     [ -1.97e+01  -1.88e+02   1.17e+01   1.35e+00]]
    Finished OK




