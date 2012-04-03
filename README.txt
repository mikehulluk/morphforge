
morphforge is a high level, simulator independent, Python library for building
simulations of small populations of multi-compartmental neurons, in which
membrane voltage is calculated from the sum of individual ionic currents
flowing across a membrane. It was built as part of Mike Hull’s Ph.D thesis;
investigating the role of electrical coupling in small populations of
interneurons in Xenopus laevis tadpoles.


The use-case of the API is to allows the user to quickly construct simulations
of small populations of neurons and synaptic connections, with particular focus
on:

 * allowing simulation specification, with visualisation and analysis in a 
   minimal, clean, human readable language;
 * reduction of complex simulation tool chains to a single python script;
 * promoting reproducible research through automatic self-documentation;
 * encourage the re-use of components such like morphologies, neurons and 
   channels such so that specific and stochastic variation in parameters is 
   simple;
 * transparent handling of different units;
 * allowing the use of established formats, (e.g. NEURON nmodl files), but 
   also simplify the definition and sharing of new channel types easily, 
   including the possibility to support other libraries and standards easily 
   (e.g. PyNN, 9ML, NeuroML, CSA)
   
Morphforge is not a simulator; it is a high layer interface to simulators
(currently NEURON), providing a set of high-level primitives for specifying
morphologies, channel distributions, synapses, in python. It was designed to
remove a lot of tedious code currently needed to specify such simulations and
what to record from them and provides an API to make visualising results
simpler.


For more information, please visit the documentation: morphforge.rtfd.org



