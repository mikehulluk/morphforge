
Setting up and Running Morphforge
=================================

.. warning::

 *  As of April 2012; morphforge is **currently undergoing major API 
    changes**! Although the package is unlikely to change conceptually, 
    please be aware that class/method/parameter/package names
    will probably change from commit-to-commit, as the package is tidied!
    
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
    
    
.. note::

    Otherwise, enjoy morphforge! 
    Please contribute useful functions you have written, any example scripts, ideas for improving the documentation
    or general feedback about using it.
    
    Mike Hull, Edinburgh/Bristol, UK. (April 2012)
    
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



The ToolBox at a glance
---------------------------------
<<<<<<< HEAD
=======


.. toctree::
   :maxdepth: 1

   /srcs/packages/package_overview.rst
>>>>>>> d25b786a83994b945959dfd2b6ceeb9d0b08af89

To Delete
----------

.. toctree::
   :maxdepth: 1

    /srcs/packages/morphology.rst
    /srcs/packages/simulation.rst


To Delete What else is in the toolbox
----------------------------


. . toctree::
   :maxdepth: 2

   /srcs/packages/package_overview.rst


For more indepth API information, please see the :doc:`Morphforge Reference Guide </srcs/morphforge_developer>` 

Contact Information
--------------------
 
 * Email me: ?ike?ulluk@googlemail.com where ?s can be found at the top of the page!
 * Mailing list: http://groups.google.com/group/morphforge
 * GitHub: https://github.com/mikehulluk/morphforge

 







