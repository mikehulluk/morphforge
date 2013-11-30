
.. _example_morphology010:

Example 1. Creating morphologies from python dictionaries
=========================================================


Creating morphologies from python dictionaries.
In this example, we create 2 :py:class:`MorphologyTree` objects from python
dictionaries, and then demonstrate iterating over the sections

Code
~~~~

.. code-block:: python

    
    
    
    
    
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
        print " - Proximal:", section.p_x, section.p_y, section.p_z, section.p_r
        print " - Distal:  ", section.d_x, section.d_y, section.d_z, section.d_r
    
    








Output
~~~~~~

.. code-block:: bash

        ConfigOoptins {'BATCHRUN': None}
    ['BLUESPEC', 'BLUESPECDIR', 'CDPATH', 'COLORTERM', 'DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DISPLAY', 'EAGLEDIR', 'ECAD', 'ECAD_LICENSES', 'ECAD_LOCAL', 'EDITOR', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'HISTFILE', 'HISTSIZE', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'KRB5CCNAME', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LD_RUN_PATH', 'LESS', 'LM_LICENSE_FILE', 'LOGNAME', 'LSCOLORS', 'MAKEFLAGS', 'MAKELEVEL', 'MANDATORY_PATH', 'MFLAGS', 'MGLS_LICENSE_FILE', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PRINTER', 'PWD', 'PYTHONPATH', 'QUARTUS_64BIT', 'QUARTUS_BIT_TYPE', 'QUARTUS_ROOTDIR', 'SHELL', 'SHLVL', 'SOPC_KIT_NIOS2', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TEMP', 'TERM', 'TMP', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CACHE_HOME', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', '_', '_JAVA_AWT_WM_NONREPARENTING']
    M1:
    <SectionObject: [0.000000, 0.000000, 0.000000, r=10.000000] -> [20.000000, 0.000000, 0.000000, r=10.000000], Length: 20.00, Region:NoRegionGiven, >
    M2:
    Section:
     - Proximal: 0.0 0.0 0.0 10.0
     - Distal:   20.0 0.0 0.0 10.0
    Section:
     - Proximal: 20.0 0.0 0.0 10.0
     - Distal:   320.0 0.0 0.0 1.0




