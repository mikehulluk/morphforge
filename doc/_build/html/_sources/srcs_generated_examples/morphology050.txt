
5. Load morphologies from MorphML, and plot using MayaVI
========================================================


Load morphologies from MorphML, and plot using MayaVI

Code
~~~~

.. code-block:: python

    
    
    
    import morphforge.stdimports as mf
    import morphforgecontrib.morphology.importers.import_tree_morphml
    import pylab
    
    testSrcsPath = mf.LocMgr().get_test_srcs_path()
    srcMorphMLFile = mf.Join(testSrcsPath, "neuroml/morphml/CablesIncluded.xml")
    m = mf.MorphologyTree.fromMorphML(src=open(srcMorphMLFile) )
    #mf.MayaViRenderer(m).show_as_points_interpolated()
    
    
    
    # TODO - SPEAK TO PADRAIG:
    raise NotImplementedError()
    srcMorphMLFile = mf.Join(testSrcsPath, "neuroml/morphml/L23PyrFRB.morph.xml",)
    m = mf.MorphologyTree.fromMorphML(
            src=open(srcMorphMLFile),
            regions={
                'all':'Rgn1',
                'ModelViewParmSubset_1':'Rgn2',
                'ModelViewParmSubset_3':'Rgn2',
                'ModelViewParmSubset_8':'Rgn2',
                'OneSecGrp_SectionRef_1':'Rgn1',
            }
    )
    mf.MayaViRenderer(m).show_as_points_interpolated()
    
    
    
    
    








Output
~~~~~~

.. code-block:: bash

        




