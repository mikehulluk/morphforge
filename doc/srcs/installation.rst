Installation
==============

Overview
--------


.. warning::

    I have only tested morphforge on Python 2.7 on Ubuntu 11.10.
    It should work fine on other -nix, although it is hardwired 
    to expected certain paths in mod-file compilation, so there
    might be a problem runnning NEURON simulations on OSX. This
    is not insurmountable, I just haven't done it!
    

Package Dependancies
--------------------

morphforge has the following hard dependancies:
 * numpy
 * scipy
 * matplotlib
 * Python-PLY
 * quantities
 * Cheetah
 * Reportlab (currently hard dep, will be made soft dependancy) 
 * To use the NEURON backend, you will need NEURON compiled with python. (This also requires libreadline-dev and libncurses5-dev )
 * To build the documentatation, you will need Sphinx and make



If you are using a debian based system, the following should 
install what you need:


.. code-block:: bash


    # Most dependancies satisfied by package manager:
    $ sudo apt-get install git ipython python-numpy python-scipy python-matplotlib python-scipy python-ply
     python-cheetah python-reportlab python-sphinx make

    

    # Python-Quantities (by Darren Dale):
    # (See https://github.com/python-quantities/python-quantities)
    # Install to ~/opt/
    $ mkdir ~/opt
    $ mkdir ~/srcs
    $ cd ~/srcs/
    $ git clone https://github.com/python-quantities/python-quantities.git
    $ cd python-quantities/
    $ python setup.py install --prefix=~/opt/
    
    # Add something like this to the end of your login script (eg ~/.bashrc):
    # export PYTHONPATH="$PYTHONPATH:/home/michaeltest/opt/lib/python2.7/site-packages/"
    $ source ~/.bashrc 
    
    #Check it imports correctly:
    $ cd ~
    $ ipython
    # typing 'import quantities' should return sucessfully
    
    
    # NEURON with Python bindings (Eilif Muller)
    # Download from here: http://neuralensemble.org/people/eilifmuller/
    # Install the deb package.
    
    #TODO: Test compile a mod-file!! 
    # There is some dependancy that can be a bit tricky to track down, because 
    # the error is cryptic. I think it is 
    # libreadline-dev and one other!
    
    

Cloning the Repository 
----------------------

In the following code, the user is 'michaeltest', and we are going to 
install morphforge into a directory '/home/michaeltest/hw/morphforge'


.. code-block:: bash

    $ mkdir ~/hw
    $ cd hw  
    
    # Clone the repo:
    $ git clone git@github.com:mikehulluk/morphforge.git
    
    # Add something like this to the end of your login script (eg ~/.bashrc):
    $ export PYTHONPATH="$PYTHONPATH:/home/michaeltest/hw/morphforge/src/"
    $ source ~/.bashrc

    # Try it out:
    $ ipython
    # Trying the command: "import morphforge" will raise the exception:
    >>> Exception: The resource file: /home/michaeltest/.morphforgerc does not exist!
    


Configuring .morphforgerc
-------------------------


Running the Examples
--------------------


Running the Tests
-----------------



