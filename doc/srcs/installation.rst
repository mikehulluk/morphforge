Installation
==============

Overview
--------

.. note::

    Microsoft Windows is not supported; I have never tried it.
    But Ubuntu VirtualBox under Windows will!


.. warning::

    I have only tested morphforge on Python 2.7 on Ubuntu 11.10.
    It should work fine on other -nix, although it is hardwired 
    to expected certain paths in mod-file compilation, so there
    might be a problem runnning NEURON simulations on OSX. This
    is not insurmountable, I just haven't done it!
    

Package Dependancies
--------------------

morphforge is hosted on github, you will need `git <http://git-scm.com/>`_ to download it.

morphforge has the following hard dependancies:

 * numpy
 * matplotlib
 * `python-lex-yacc (python-ply) <http://www.dabeaz.com/ply/>`_
 * `quantities <https://github.com/python-quantities/python-quantities>`_
 * `cheetah <http://www.cheetahtemplate.org/>`_
 

And the following soft-dependancies 

 * scipy
 * Reportlab
 * NEURON (including the python bindings) (Note: NEURON needs the *readline* and *ncurses* development libraries)
    * `Manual Compilation Instructions <http://www.davison.webfactional.com/notes/installation-neuron-python/>`_
    * `Debian Package <http://neuralensemble.org/people/eilifmuller/>`_


If you want to build the documentation locally, you will need
 * `Sphinx <http://sphinx.pocoo.org/>`_
 * make 


Installing the packages on a debian-based system (Ubuntu)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


If you are using a debian based system, the following should 
install what you need.



.. code-block:: bash

    $ mkdir ~/hw
    $ cd hw  
    
    # Most dependancies satisfied by package manager:
    $ sudo apt-get install git ipython python-numpy python-scipy \
      python-matplotlib python-scipy python-ply python-cheetah \
      python-reportlab python-sphinx make libncurses5-dev \
      libreadline-dev python-pip
      
    # Install python-quantities
    # and check it installed OK:
    $ sudo pip install quantities
    $ python -c 'import quantities'
    $ # <No output displayed means everything is OK>
    
    

    


.. code-block:: bash


    # Install NEURON with Python bindings (thanks to Eilif Muller)
    # Download from here: http://neuralensemble.org/people/eilifmuller/
    # Install the deb package.
    $ python -c 'import neuron'
    NEURON -- Release 7.1 (359:7f113b76a94b) 2009-10-26
    Duke, Yale, and the BlueBrain Project -- Copyright 1984-2008
    See http://www.neuron.yale.edu/credits.html
    $ #<If you see the above banner, everything is good!>

.. code-block:: bash

    # Check all NEURON dependancies satisfied for building mod files:
    $ mkdir ~/mf_jnk   
    $ cd ~/mf_jnk
    $ cp /opt/nrn/share/nrn/examples/nrniv/netcon/ampa.mod .
    $ export PATH="$PATH:/opt/nrn/ARCH/bin"  # (where ARCH is your architecture.)
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
    $ git clone git://github.com/mikehulluk/morphforge.git
        
    # Add something like this to the end of your login script (eg ~/.bashrc):
    export PYTHONPATH="$PYTHONPATH:/home/michaeltest/hw/morphforge/src/"
    $ source ~/.bashrc

    # Try it out:
    $ cd ~
    $ python -c 'import morphforge'
    


Configuring .morphforgerc
-------------------------

morphforge needs to know the locations of various directories and tools 
for interacting with simulators. This is controlled through a config 
file in the home directory, :file:`~/.morphforgerc` , which is in the python 
`ConfigParser <http://docs.python.org/library/configparser.html>`_ syntax.

To get going, you should specify a temporary directory, and specify the
locations of various tools and locations for compiling mod-files. A 
sample :download:`.morphforgerc.sample </../etc/morphforgerc.sample>`,
you might need to edit the platform-architecture from **i686** to **x86_64**.
You can find the location of binaries using a commmand like:

.. code-block:: bash

    $ which nocmodl 
    /opt/nrn/x86_64/bin//nocmodl

In which case your ~/.morphforgerc file should look something like:

.. code-block:: bash

    $ cat ~/.morphforgerc
    [Locations]
    tmpdir= /home/michaeltest/mftmp/
    rootdir=/home/michaeltest/hw/morphforge/src/
    
    [Neuron]
    nrnprefix=/opt/nrn/
    nrnbin=%(nrnprefix)s/x86_64/bin

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

    $ cd ~/hw/morphforge/src/morphforgeexamples/singlecell_simulation/
    $ python singlecell_simulation010.py
    # < If everything is OK, the script should run and you should be 
    # presented with some graphs!


All examples can be found in this directory and can be checked that 
they are running using :program:`make`:

.. code-block:: bash

    $ cd ~/hw/morphforge/src/morphforgeexamples/
    $ make examples 
    
    

Running the Tests
-----------------

.. todo::

    Upload the tests to the repo and document how to run them.







