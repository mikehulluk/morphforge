
.. _example_morphology020:

Example 2. Loading from SWC and rendering with Matplotlib
=========================================================


Loading from SWC and rendering with Matplotlib.
This example shows loading in a morphology from an SWC file and then viewing it in matplotlib,
using Principle Component Analysis (PCA) to align the features of the morphology to the plot
window.

Code
~~~~

.. code-block:: python

    
    
    
    
    
    
    from morphforge.core import LocMgr, Join
    from morphforge.morphology.ui import MatPlotLibViewer
    from morphforge.morphology.core import MorphologyTree
    
    testSrcsPath = LocMgr().get_test_srcs_path()
    srcSWCFile = Join(testSrcsPath, "swc_files/28o_spindle20aFI.CNG.swc")
    
    m = MorphologyTree.fromSWC(src=open(srcSWCFile))
    MatPlotLibViewer(m, use_pca=False)
    MatPlotLibViewer(m, use_pca=True)
    
    




Figures
~~~~~~~~


.. figure:: /srcs_generated_examples/images/morphology020_out1.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/morphology020_out1.png>`


.. figure:: /srcs_generated_examples/images/morphology020_out2.png
    :width: 3in
    :figwidth: 4in

    Download :download:`Figure </srcs_generated_examples/images/morphology020_out2.png>`






Output
~~~~~~

.. code-block:: bash

        ['DBUS_SESSION_BUS_ADDRESS', 'DEFAULTS_PATH', 'DESKTOP_SESSION', 'DESKTOP_STARTUP_ID', 'DISPLAY', 'GDMSESSION', 'GNOME_KEYRING_CONTROL', 'GNOME_KEYRING_PID', 'GREP_COLOR', 'GREP_OPTIONS', 'GRIN_ARGS', 'GTK_MODULES', 'HOME', 'INFANDANGO_CONFIGFILE', 'INFANDANGO_ROOT', 'LANG', 'LANGUAGE', 'LC_CTYPE', 'LESS', 'LOGNAME', 'LSCOLORS', 'MANDATORY_PATH', 'MREORG_CONFIG', 'OLDPWD', 'PAGER', 'PATH', 'PWD', 'PYTHONPATH', 'SHELL', 'SHLVL', 'SSH_AGENT_PID', 'SSH_AUTH_SOCK', 'TERM', 'TEXTDOMAIN', 'TEXTDOMAINDIR', 'UBUNTU_MENUPROXY', 'USER', 'WINDOWID', 'XAUTHORITY', 'XDG_CONFIG_DIRS', 'XDG_DATA_DIRS', 'XDG_RUNTIME_DIR', 'XDG_SEAT_PATH', 'XDG_SESSION_COOKIE', 'XDG_SESSION_PATH', 'XTERM_LOCALE', 'XTERM_SHELL', 'XTERM_VERSION', '_', '_JAVA_AWT_WM_NONREPARENTING']
    [(18904.787115151994, array([ 0.17, -0.97,  0.15])), (560.28926277794278, array([-0.98, -0.18, -0.05])), (73.826665068840015, array([-0.08,  0.14,  0.99]))]




