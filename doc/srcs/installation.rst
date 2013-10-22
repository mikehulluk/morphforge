Installation
==============

Overview
--------


.. note::

    morphforge uses Python version 2.8, not 3.X


.. note::

    Microsoft Windows is not supported; I have never tried it.
    But Ubuntu VirtualBox under Windows will!


.. warning::

    I have only tested morphforge on Python 2.7 on Ubuntu.
    It should work fine on other -nix, although it is hardwired 
    to expected certain paths in mod-file compilation, so there
    might be a problem running NEURON simulations on OSX. This
    is not insurmountable, I just haven't done it!



.. warning::

    The packages morphforge, neurounits, mredoc and mreorg contain potential security holes.
    All these packages write intermediate files to temporary locations, which are then used
    by other tools. It might be possible to edit these files to cause the execution of arbitrary
    code and therefore **these tools should only be used in trusted environments**.

    

Package Dependancies
--------------------


morphforge is hosted on github, you will need `git <http://git-scm.com/>`_ to download it. morphforge has the following hard dependencies on:

 * numpy
 * matplotlib
 * `python-lex-yacc (python-ply) <http://www.dabeaz.com/ply/>`_
 * `quantities <https://github.com/python-quantities/python-quantities>`_
 * `cheetah <http://www.cheetahtemplate.org/>`_
 * `NeuroUnits <http://neurounit.readthedocs.org/>`_ (Neurounits is a library for working with quantities and equations involving units, which builds on the quantities package)

And the following soft-dependancies 

 * scipy
 * Reportlab
 * NEURON (including the python bindings) (Note: NEURON needs the *readline* and *ncurses* development libraries)
    * `Manual Compilation Instructions <http://www.davison.webfactional.com/notes/installation-neuron-python/>`_
    * `Debian Package <http://neuralensemble.org/people/eilifmuller/>`_
 * MayaVI
 * `mreorg <http://mreorg.readthedocs.org/en/latest/>`_
 * `mredoc <http://mredoc.readthedocs.org/en/latest/>`_
 * Latex

If you want to build the documentation locally, you will need
 * `Sphinx <http://sphinx.pocoo.org/>`_
 * make 




Installing the packages on a debian-based system (Ubuntu)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


If you are using a debian based system, the following should 
install what you need.





.. code-block:: bash
  
    # Most dependancies satisfied by package manager:
    $ sudo apt-get install git ipython python-numpy python-scipy \
      python-matplotlib python-scipy python-ply python-cheetah \
      python-reportlab python-sphinx make libncurses5-dev \
      libreadline-dev python-setuptools python-mako python-lxml
     
    $ Lets install all packages locally, to ~/.local/
    $ mkdir -p /home/mh/.local//lib/python2.7/site-packages/
    $ echo export PYTHONPATH="$PYTHONPATH:~/.local//lib/python2.7/site-packages/" >> ~/.bashrc
    $ source ~/.bashrc
 
    # Install neurounits, (which will automatically install 'quantities')
    $ easy_install --prefix=~/.local/ neurounits=v0.1
    $ ipython -c 'import neurounits'
    $ # <No output displayed means everything is OK>



Optionally, install mreorg and mredoc. Briefly, mreorg allows you to
automatically save figures created with matplotlib to files and to suppress the
display of GUI windows, which is important for running batches of scripts and
for running the example files with make. mredoc is a library for build html and
pdf files from equations, figures, text and tables from within python. Neither
of these libraries are essential for morphforge to run.



.. code-block:: bash

    # It might be best to install django (mreorg dependancy)
    # through the package manager:
    $ sudo apt-get install texlive-full python-django python-django-dajax

    # Install mreorg and mredoc using easy install
    $ easy_install --prefix=~/.local/ mreorg==0.1.1 mredoc==0.1

    # Test out mreorg:
    $ ipython -c 'import mreorg'
    $ #< Should throw an error - mreorg expects an environmental variable to be set: >
    $ export MREORG_CONFIG=''; ipython -c 'import mreorg'
    $ # <No output displayed means everything is OK>

    # Test out mredoc by creating a simple doc:
    $ ipython
    >>> import mredoc
    >>> doc = mredoc.Section('Test Document',mredoc.Section('Equations', r"""$x=\frac{-b\pm\sqrt{b^2-4ac}}{2a}$""" ))
    >>> doc.to_html("~/mredoc_test_out/")
    >>> doc.to_pdf("~/mredoc_test.pdf")
    >>> quit
    $ chromium-browser ~/mredoc_test_out/index.html
    $ evince ~/mredoc_test.pdf



Install NEURON and python bindings:
    
.. code-block:: bash

    # Install NEURON with Python bindings (thanks to Eilif Muller)
    # Download from here: http://neuralensemble.org/people/eilifmuller/
    # Install the deb package.
    $ ipython -c 'import neuron'
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    $ #<If you see the above banner, everything is good!>

    # And lets add the binaries to the PATH. ARCH is your architecture,
    # (probably 'x86_64' or 'i686')
    $ echo export PATH="$PATH:/opt/nrn/ARCH/bin" >> ~/.bashrc
    $ source ~/.bashrc

.. code-block:: bash

    # Check all NEURON dependancies satisfied for building mod files:
    $ mkdir ~/mf_jnk   
    $ cd ~/mf_jnk
    $ cp /opt/nrn/share/nrn/examples/nrniv/netcon/ampa.mod .
    
    $ nrnivmodl
    <.... lots of output...>
    Successfully created x86_64/special
    $ #<Great, NEURON can build .modfiles!>
   


Cloning the Repository 
----------------------

In the following code, the user is :file:`michaeltest`, and we are going to 
install morphforge into a directory :file:`/home/michaeltest/hw/morphforge`


.. code-block:: bash

    $ mkdir ~/hw
    $ cd hw  
    
    # Clone the repo:
    $ git clone git://github.com/mikehulluk/morphforge.git v0.2
        
    # Lets add this to the PYTHONPATH (eg ~/.bashrc):
    $ echo export PYTHONPATH="$PYTHONPATH:~/hw/morphforge/src/" >> ~/.bashrc

    # And also, lets set the flags for mreorg to automatically save all images:
    $ echo export MREORG_CONFIG="SAVEALL" >> ~/.bashrc
    $ source ~/.bashrc

    # Try it out:
    $ cd ~
    $ python -c 'import morphforge'
    


Configuring .morphforgerc
-------------------------

morphforge needs to know the locations of various directories and tools 
for interacting with simulators. This is controlled through a configuration 
file in the home directory, :file:`~/.morphforgerc` , which is in the python 
`ConfigParser <http://docs.python.org/library/configparser.html>`_ syntax.

To get going, you should specify a temporary directory, and specify the
locations of various tools and locations for compiling mod-files. A 
sample :download:`.morphforgerc.sample </../etc/morphforgerc.sample>`,
you might need to edit the platform-architecture from **i686** to **x86_64**.
You can find the location of binaries using a command like:

.. code-block:: bash

    $ which nocmodl 
    /opt/nrn/x86_64/bin//nocmodl

In which case your ~/.morphforgerc file should look something like:

.. code-block:: bash

    $ cat ~/.morphforgerc
    [Locations]
    tmpdir= /home/michaeltest/mftmp/
    
    [Neuron]
    nrnprefix=/opt/nrn/
    nrnbin=%(nrnprefix)s/x86_64/bin
    rootdir=/home/michaeltest/hw/morphforge/src/

    modlunitpath=%(nrnbin)s/modlunit
    nocmodlpath=%(nrnbin)s/nocmodl
    libtoolpath=%(nrnprefix)s/share/nrn/libtool
    compileIncludes=%(nrnprefix)s/include/nrn:%(nrnprefix)s/x86_64/lib
    nrnLinkDirs=%(nrnprefix)s/x86_64/lib:%(nrnprefix)s/x86_64/lib
    rpath=%(nrnprefix)s/x86_64/libs
    rndAloneLinkStatement=%(nrnprefix)s/x86_64/lib/libnrniv.la

    additional_link_libraries=%(rootdir)s/morphforgecontrib/simulation/neuron_gsl/cpp/libgslwrapper
    ld_library_path_suffix=%(rootdir)s/morphforgecontrib/simulation/neuron_gsl/cpp/
 
More information about .~/morphforgerc configuration can be found :doc:`here </srcs/morphforgerc>`


.. warning::
    
    morphforge will overwrite files in the directory specified by 
    :file:`tmpdir` without asking. Make sure there is nothing important
    in there!
        


Running the Examples
--------------------


If everything is set up correctly, you should now be able to run your first example:

.. code-block:: bash
    $ cd ~/hw/morphforge/src/morphforgeexamples/exset2_singlecell_simulations/
    $ python singlecell_simulation010.py
    # < If everything is OK, the script should run and you should be 
    # presented with some graphs!


All examples can be found in this directory and can be checked that 
they are running using :program:`make`:

.. code-block:: bash

    $ cd ~/hw/morphforge/src/morphforgeexamples/
    $ make examples

This will run all the examples, and the figures will be found in the _output/<script-name> folders within each directory.
    
    

Running the Tests
-----------------

Morphforge has been tested with the Simulator-TestData repository. `<https://github.com/mikehulluk/simulator-test-data>`_

To run the tests:

.. code-block:: bash

    # Install python-glob2 (allows recusrive globbing in python)
    $ easy_install --prefix=~/.local/ glob2 

    # Clone the repository:
    $ cd ~/hw
    $ git clone git@github.com:mikehulluk/simulator-test-data.git
    $ cd simulator-test-data

    # Download waf:
    # (as per: http://docs.waf.googlecode.com/git/book_16/single.html#_download_and_installation )
    $ wget http://waf.googlecode.com/files/waf-1.6.11 && mv waf-1.6.11 waf && chmod +x waf

    # Configure waf
    ./waf configure

    # Run the simulations
    # By default, the repository will run all the simulations it finds with all the simulators. (May take a long time)
    ./waf generate
    
    # (This can be reduced by setting the following environmental variables:
    export STD_SIMS='morphforge;NEURON';
    export STD_SCENS='022; 5??; 62[12]'; # (Using regular expression syntax)
    export STD_SHORT='TRUE';
    ./waf generate


    # Once the simulations have run, the results can be summarised with:
    ./waf compare

    # which will create summary documents of the tests that have been run in
    # ./test_results/
    $ chromium-browser ./test_results/index.html






