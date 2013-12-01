
.. _example_manage020:

Example 25. Summarise the cells and channels that are registered to an environment
==================================================================================


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
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-MgBlock
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core.PostSynapticMech_Exp2SynNMDA_Base'> dIN-dIN-Background-NMDA-MgBlock
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
    <class 'morphforgecontrib.simulation./usr/bin/pdflatex
    synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> tIN-dIN-AMPA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> tIN-dIN-AMPA
    <class 'morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core.PostSynapticMech_Exp2Syn_Base'> tIN-dIN-AMPA
    Tex File: /home/michael/.mredoc/build/pdflatex/eqnset.tex
    Successfully written PDF to:  /home/michael/Desktop/morphforge_registered_templates.pdf
    Cell & Channel summary stored at: ~/Desktop/morphforge_registered_templates.pdf




