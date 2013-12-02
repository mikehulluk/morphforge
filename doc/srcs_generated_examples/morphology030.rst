
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

        ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Morphology Vertices:
    [[ 1.  2.  3.  4.]
     [ 5.  6.  7.  8.]]
    Morphology Connectivity:
    [[1 0]]




