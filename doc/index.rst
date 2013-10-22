

Overview
---------

morphforge is a high level, simulator independent, Python library for building simulations of small populations of multi-compartmental neurons, in which membrane voltage is calculated from the sum of individual ionic currents flowing across a membrane. 
It was built as part of `Mike Hull's <http://www.anc.ed.ac.uk/dtc/index.php?option=com_people&func=showall&userid=359>`_ Ph.D thesis; investigating the role of electrical coupling in small populations of interneurons in Xenopus laevis tadpoles.



The use-case of the API is to allows the user to quickly construct simulations of small populations of neurons and synaptic connections, with particular focus on:  

  1. allowing simulation specification, with visualisation and analysis in a minimal, clean, **human readable language**; 
  2. reduction of complex simulation tool chains to a **single python script**; 
  3. promoting reproducible research through **automatic self-documentation**; 
  4. encourage the **re-use of components** such like morphologies, neurons and channels such so that specific and stochastic variation in parameters is simple; 
  5. transparent handling of different **units**; 
  6. allowing the use of established formats, (e.g. NEURON nmodl files), but also simplify the definition and sharing of new channel types easily, including the possibility to support other libraries and standards easily (e.g. PyNN, 9ML, NeuroML, CSA) 


Morphforge is not a simulator; it is a high layer interface to simulators (currently NEURON), providing a set of high-level primitives for specifying morphologies, channel distributions, synapses, in python.  It was designed to remove a lot of tedious code currently needed to specify such simulations and what to record from them and provides an API to make visualising results simpler.



Example Use-Case
-----------------
Consider the following example:

	“I would like to build a network, of 30 neurons. Each soma should be 20(± 3) µm diameter, and axons are 1000µm long with have a hillock of radius 5um for the first 10µm, then tapers into a axon of radius 0.3µm which. I will use a single compartment for the soma, divide the hillock into compartments of length 1um, and the axon into 100 compartments. We will use the sodium and potassium voltage-gated channels as specified by the equations and parameters in paper X, but we want to use 3 times the density of sodium channels on the axon hillock.
	
	The neurons should be connected by gap junctions, distributed according to algorithm X, with resistances of 1GOhm ± 500MOhm. The neurons also self-excite other neurons in the population with AMPA  synapses, with a probability of connections between any pair of neurons of 20%. I would like to stimulate this network with NMDA synaptic input to ~50% of the neurons at fixed times, as well as different levels of step current injections to cell 12, and measure plot graphs of the ionic currents flowing across the membrane of cells 2, 12, and any cells that spike, as well as the membrane voltage of all the neurons. I want to compare against with the case when the gap junctions have been blocked.”

The morphforge allows the specification of this complete simulation and visualisation of the results in a single python scripts of less than 100?? lines, only requiring a single command to run. It is designed to make it possible to specify connection algorithms, morphologies, channel descriptions and simulation parameters as high-level objects, such that they can be reused in across other simulations, without the need to copy and paste code. Units are handled transparently, reports of the simulation setup can be automatically generated, and a clean separation between of simulation and visualisation is achieved through a mechanism of *tagging* in the framework. The library is built on standard Python libraries, (Numpy, matplotlib), making it easy to integrate with other libraries.

The framework is under active development, with a NEURON backend, currently supporting everything in the above example.		











Setting up and Running Morphforge
=================================

.. warning::

 *  As of Autumn 2013; morphforge is **currently undergoing major API 
    changes**! Although the package is unlikely to change conceptually, 
    please be aware that class/method/parameter/package names
    will probably change from commit-to-commit, as the packages are tidied!
    
 *  This package is provided as-is and should currently be considered *alpha*
    quality! **YOU HAVE BEEN WARNED: THIS IS NEW SOFTWARE -THERE MAY BE BUGS!** I hope there are
    relatively few, but it is a large piece of code; which I have developed
    informally alongside my Ph.D.  Please contribute any tests you write to
    improve the testsuite!

 *  morphforge needs to read and write lots of files to interact with
    simulators; so **there is a lot of code which deletes files/directories from
    the filesystem!** There is always the danger that a path gets mis-set
    somewhere in the code and the **wrong thing might be deleted** by mistake. I
    have never had a problem with this  (I have been running this package on my
    computer for the last 2 years with absolutely no problems), but it is a
    still possiblity, especially under different operating systems.

.. warning::

    **Until lots of people have tested it on different platforms, I recommend
    running *morphforge* within a sandboxed environment; such as a VirtualBox,
    in case there are any issues that cause files to be delete unexpectedly!**
    
.. warning::

    **Morphforge and related packages may not be secure!**. morphforge uses lots of code-generation,
    and reloads files from filesystem, which could be a vector for a malicious attack depending on where temporary files are stored.. ** only use morphforge in 'safe' environments. If in doubt, use a sandbox! **
    
.. note::

    Otherwise, enjoy morphforge! 
    Please contribute useful functions you have written, any example scripts, ideas for improving the documentation
    or general feedback about using it.
    
    Mike Hull, Edinburgh/Bristol/Cambridge, UK. (October 2013)
    
    P.S. I have started a googlegroup for morphforge at http://groups.google.com/group/morphforge. Sign up for 
    latest development news!
    



Installing Morphforge
----------------------

.. toctree::
   :maxdepth: 2

   /srcs/installation.rst


Examples
--------


.. toctree::
   :maxdepth: 2

   /srcs/examples/examples.rst


Users Guide
-------------



.. toctree::
   :maxdepth: 2
   :hidden:
    
   /index_api_new.rst

For more indepth API information, please see the :doc:`Morphforge Users Guide</index_api_new>` 


Contact Information
--------------------
 
 * Email me: ?ike?ulluk@googlemail.com where ?s can be found at the top of the page!
 * Mailing list: http://groups.google.com/group/morphforge
 * GitHub: https://github.com/mikehulluk/morphforge

 





