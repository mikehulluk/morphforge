
.. _example_morphology040:

Example 4. Converting between the morphology representations
============================================================


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

        ConfigOoptins {'BATCHRUN': None}
    ['BLUESPEC', 'BLUESPECDIR', 'CDPATH', 'COLORTERM', 'DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DISPLAY', 'EAGLEDIR', 'ECAD', 'ECAD_LICENSES', 'ECAD_LOCAL', 'EDITOR', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'HISTFILE', 'HISTSIZE', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'KRB5CCNAME', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LD_RUN_PATH', 'LESS', 'LM_LICENSE_FILE', 'LOGNAME', 'LSCOLORS', 'MAKEFLAGS', 'MAKELEVEL', 'MANDATORY_PATH', 'MFLAGS', 'MGLS_LICENSE_FILE', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PRINTER', 'PWD', 'PYTHONPATH', 'QUARTUS_64BIT', 'QUARTUS_BIT_TYPE', 'QUARTUS_ROOTDIR', 'SHELL', 'SHLVL', 'SOPC_KIT_NIOS2', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TEMP', 'TERM', 'TMP', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CACHE_HOME', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Vertex Data
    [[ -1.61e+00   6.23e+00  -7.44e-02   1.56e+01]
     [ -9.08e+00   3.01e+01  -1.14e+00   4.70e+00]
     [ -1.08e+01   3.64e+01  -1.14e+00   4.28e+00]
     ..., 
     [ -1.61e+01  -1.85e+02   6.97e+00   1.68e+00]
     [ -1.70e+01  -1.84e+02   6.97e+00   1.68e+00]
     [ -1.97e+01  -1.88e+02   1.17e+01   1.35e+00]]
    Finished OK




