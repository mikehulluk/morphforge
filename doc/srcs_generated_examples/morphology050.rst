
.. _example_morphology050:

Example 5. Load morphologies from MorphML, and plot using MayaVI
================================================================


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
    
    
    
    ## TODO - SPEAK TO PADRAIG:
    #raise NotImplementedError()
    #srcMorphMLFile = mf.Join(testSrcsPath, "neuroml/morphml/L23PyrFRB.morph.xml",)
    #m = mf.MorphologyTree.fromMorphML(
    #        src=open(srcMorphMLFile),
    #        regions={
    #            'all':'Rgn1',
    #            'ModelViewParmSubset_1':'Rgn2',
    #            'ModelViewParmSubset_3':'Rgn2',
    #            'ModelViewParmSubset_8':'Rgn2',
    #            'OneSecGrp_SectionRef_1':'Rgn1',
    #        }
    #)
    #mf.MayaViRenderer(m).show_as_points_interpolated()
    
    
    
    
    








Output
~~~~~~

.. code-block:: bash

        No handlers could be found for logger "neurounits"
    /home/michael/hw_to_come/morphforge/src/morphforgecontrib/morphology/importers/import_tree_morphml.py:34: UserWarning: MorphML code in development
      warnings.warn('MorphML code in development')
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    CellName: CellWithCables
    Loaded Cable:  0 SomaSec
    Loaded Cable:  1 DendSec1
    Loaded Cable:  2 DendSec2
    Segment
    0 SomaSeg 0  (u'0', u'0', u'0', u'10') (u'10', u'0', u'0', u'10')
    Segment
    1 DendSeg1 1 0 (u'5', u'0', u'0', u'5') (u'5', u'10', u'0', u'5')
    Segment
    2 DendSeg2 1 1 (5.0, 10.0, 0.0, 5.0) (u'5', u'20', u'0', u'5')
    Segment
    3 DendSeg3 1 2 (5.0, 20.0, 0.0, 5.0) (u'5', u'30', u'0', u'5')
    Segment
    4 DendSeg4 2 0 (u'10', u'0', u'0', u'3') (u'10', u'0', u'10', u'3')
    Segment
    5 DendSeg5 2 4 (10.0, 0.0, 10.0, 3.0) (u'10', u'0', u'20', u'3')
    RegionNames: [u'soma_group', u'dendrite_group']




