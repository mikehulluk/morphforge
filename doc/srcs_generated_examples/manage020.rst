
22. Summarise the cells and channels that are registered to an environment
==========================================================================


Summarise the cells and channels that are registered to an environment

Code
~~~~

.. code-block:: python

    
    
    
    
    
    
    import mredoc
    from morphforge.stdimports import PluginMgr, CellLibrary, ChannelLibrary, MorphologyLibrary, PostSynapticTemplateLibrary
    import morphforgecontrib.stdimports as mfc
    from  modelling import *
    from modelling.sensory_pathway import *
    fname = '~/Desktop/morphforge_registered_templates.pdf'
    
    mredoc.Section('Summary',
        CellLibrary.summary_table(),
        ChannelLibrary.summary_table(),
        MorphologyLibrary.summary_table(),
        PostSynapticTemplateLibrary.summary_table(),
    
        ).to_pdf(fname)
    
    print 'Cell & Channel summary stored at: %s'%fname
    
    
    








Output
~~~~~~

.. code-block:: bash

        No handlers could be found for logger "neurounits"
    /home/mh735/.local/lib/python2.7/site-packages/setuptools-1.1.5-py2.7.egg/pkg_resources.py:979: UserWarning: /home/mh735/.python-eggs is writable by group/others and vulnerable to attack when used with get_resource_filename. Consider a more secure location (set with .set_extraction_path or the PYTHON_EGG_CACHE environment variable).
    Openning ScriptFlags
    /auto/homes/mh735/hw/NeuroUnits/ext_deps
    Loading StdLib file: /auto/homes/mh735/hw/NeuroUnits/src/neurounits/../stdlib/stdlib.eqn
    sqlite:////local/scratch/mh735/tmp/signalanalysis.sqlite
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> MHR-dIN-Inhib
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> MHR-dIN-Inhib
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> MHR-dIN-Inhib
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> MHR-dIN-Inhib
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> cIN-dIN-Inhib
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> cIN-dIN-Inhib
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> cIN-dIN-Inhib
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> cIN-dIN-Inhib
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> dIN-cIN-AMPA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> dIN-cIN-AMPA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> dIN-cIN-AMPA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> dIN-cIN-AMPA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> dIN-dIN-AMPA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> dIN-dIN-AMPA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> dIN-dIN-AMPA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> dIN-dIN-AMPA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> tIN-dIN-AMPA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> tIN-dIN-AMPA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> tIN-dIN-AMPA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> tIN-dIN-AMPA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-MgBlock
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synn/usr/bin/pdflatex
    mda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-MgBlock
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-MgBlock
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-MgBlock
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-MgBlock
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-MgBlock
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-MgBlock
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-SlowOpen
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-SlowOpen
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-SlowOpen
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-SlowOpen
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-SlowOpen
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-SlowOpen
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-SlowOpen
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> tIN-dIN-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> tIN-dIN-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> tIN-dIN-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> tIN-dIN-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> tIN-dIN-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> tIN-dIN-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> tIN-dIN-NMDA
    Tex File: /tmp/tmp_3175/mredoc/build/pdflatex//eqnset.tex
    Successfully written PDF to:  /home/mh735/Desktop/morphforge_registered_templates.pdf
    Cell & Channel summary stored at: ~/Desktop/morphforge_registered_templates.pdf




