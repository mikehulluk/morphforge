Simulation-Layer (Neuron-Specific)
==================================


Design-decisions
----------------
the Python interface to NEURON is used, but only minimally, and in a different process to the main script. After a Simulation is built, it is serialised and passed to a new process, where it is un-packed and imports the PyNeuron interface. The following functions are used:
   a) all the generated MODL libraries are loaded through calls to 'neuron.h.nrn_load_dll'
   b) the HOC file is loaded by a call to: 'neuron.h.load_file,'
   c) a callback object is registered to HOC, which is used to update the current/expected-time-to-finish on the screen
   d) simulation.run() is called
   d) the results are read from HOC to NEURON directly as numpy arrays.
These results are then serialised, and passed back to the calling process. This may seem convoluted, but the main reasons for doing this are:
    1) it simplifies running of multiple independent simulations from a single script, since it can be difficult (impossible?) to completely 'clear' the NEURON/PyNeuron workspace without launching a new process; 
    2) similarly, this also makes it easy/safe to run multiple simulations simultaneously, for example if there are multiple cores on a PC, by using the python 'multiprocessing' library. 
    2) it makes debugging easier, because the relevant HOC file is available to inspect by hand if there is a problem with a simulation; 
    3) by defering any interaction with the simulator until 'run' is called,  we open up the possibility of caching the output of long simulations - since the entire simulation setup is stored inside a Simulation object, we can check if a given simulation has already been run and transparently save ourselves from re-running long-run simulations.





Accessing HOC & MODL files
---------------------------

.. todo::

    Details about the HOC and MODL objects.


