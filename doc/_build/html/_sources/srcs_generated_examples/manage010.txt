
21. Summarise the various plugins of the environment
====================================================


Summarise the various plugins of the environment

Code
~~~~

.. code-block:: python

    
    
    
    
    
    
    from morphforge.stdimports import PluginMgr
    import morphforgecontrib.stdimports as mfc
    
    fname = '~/Desktop/morphforge_config.pdf'
    summary = PluginMgr.summarise_all()
    summary.to_pdf(fname)
    print 'morphforge environment summary stored at: %s'%fname
    
    
    








Output
~~~~~~

.. code-block:: bash

        No handlers could be found for logger "neurounits"
    /usr/bin/pdflatex
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    Remove paragraph? (no)
    Remove paragraph? (no)
    Tex File: /tmp/tmp_3175/mredoc/build/pdflatex//eqnset.tex
    Successfully written PDF to:  /home/mh735/Desktop/morphforge_config.pdf
    morphforge environment summary stored at: ~/Desktop/morphforge_config.pdf




