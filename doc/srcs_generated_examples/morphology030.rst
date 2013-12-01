
.. _example_morphology030:

Example 3. Load  SWC data from a string directly into a MorphologyArray
=======================================================================


Load  SWC data from a string directly into a MorphologyArray.
We can load .swc from any file-like object, so we can use StringIO to load directly from strings.

Code
~~~~

.. code-block:: python

    
    
    
    
    
    
    
    
    
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

        ConfigOoptins {'BATCHRUN': None}
    ['BLUESPEC', 'BLUESPECDIR', 'CDPATH', 'COLORTERM', 'DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DISPLAY', 'EAGLEDIR', 'ECAD', 'ECAD_LICENSES', 'ECAD_LOCAL', 'EDITOR', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'HISTFILE', 'HISTSIZE', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'KRB5CCNAME', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LD_LIBRARY_PATH', 'LD_RUN_PATH', 'LESS', 'LM_LICENSE_FILE', 'LOGNAME', 'LSCOLORS', 'MAKEFLAGS', 'MAKELEVEL', 'MANDATORY_PATH', 'MFLAGS', 'MGLS_LICENSE_FILE', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PRINTER', 'PWD', 'PYTHONPATH', 'QUARTUS_64BIT', 'QUARTUS_BIT_TYPE', 'QUARTUS_ROOTDIR', 'SHELL', 'SHLVL', 'SOPC_KIT_NIOS2', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TEMP', 'TERM', 'TMP', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CACHE_HOME', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Morphology Vertices:
    [[ 1.  2.  3.  4.]
     [ 5.  6.  7.  8.]]
    Morphology Connectivity:
    [[1 0]]




