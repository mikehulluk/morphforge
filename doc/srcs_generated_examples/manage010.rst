
.. _example_manage010:

Example 24. Summarise the various plugins of the environment
============================================================


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
    ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    Remove paragraph? (no)
    Tex File: /home/michael/.mredoc/build/pdflatex/eqnset.tex
    Successfully written PDF to:  /home/michael/Desktop/morphforge_config.pdf
    morphforge environment summary stored at: ~/Desktop/morphforge_config.pdf




