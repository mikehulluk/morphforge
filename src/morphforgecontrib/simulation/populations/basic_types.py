#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------
import itertools
import string
from morphforge.simulation.core.cell import Cell
from morphforgecontrib.tags import StdTagFunctors
from morphforge.core.objectnumberer import ObjectLabeller
from morphforge.core.misc import is_iterable

class NeuronPopulation(object):


    def __init__(self, sim, neuron_functor, n, pop_name=None, name_tmpl_str=None, user_tags = None):

        user_tags = user_tags or []
        if pop_name:
            user_tags.extend( pop_name.split("_") )


        self.pop_name = pop_name if pop_name is not None else ObjectLabeller.getNextUnamedObjectName(NeuronPopulation, prefix="NrnPop",num_fmt_string="%d" )

        if  name_tmpl_str is None:
            name_tmpl_str = "%s_$i"%self.pop_name

        name_tmpl = string.Template(name_tmpl_str)
        self.sim = sim

        #Create the neurons:
        self.nrns = []
        for i in range(n):
            cell_name = name_tmpl.substitute({'i':i})
            #print cell_name
            #assert False
            cell_tags = user_tags + ['Index%d'%i]
            n = neuron_functor(sim=sim, name=cell_name, cell_tags=cell_tags )
            n.population = self
            self.nrns.append(n)


    def __len__(self):
        return len( self.nrns )

    def __getitem__(self, i):
        return self.nrns[i]

    def __iter__(self):
        return iter(self.nrns)


    @property
    def cell_types(self):
        return set( ["<Unknown>"] )



    def record(self, cell, location_func=None, what=None, user_tags=None, user_tag_functors=None, **kwargs  ):

        # Indexable by index of cell reference
        if isinstance(cell, int):
            cell = self[cell]
        assert cell in self.nrns


        what = what or Cell.Recordables.MembraneVoltage
        user_tags = user_tags or []
        user_tag_functors = user_tag_functors or  StdTagFunctors.getRecordFunctorsNeuron()
        location_func = location_func or ( lambda cell: cell.getLocation("soma") )
        location=location_func(cell)

        kw_utf = { 'celllocation':location,'neuron_population':self,'neuron':cell}

        functor_tags = list( itertools.chain( *[utf( **kw_utf ) for utf in user_tag_functors] ) )
        r = self.sim.record( cell, location=location_func(cell), what=what, user_tags=user_tags + functor_tags, **kwargs)
        return r


    def record_all(self, **kwargs):
        assert False, "Method renamed to 'record_from_all"
        return [self.record(cell,**kwargs) for cell in self.nrns ]

    def record_from_all(self, **kwargs):
        return [self.record(cell,**kwargs) for cell in self.nrns ]

    def for_each(self, func ):
        return [ func(cell=nrn ) for nrn in self.nrns ]





class SynapsePopulation(object):
    """A synapse population is a container for a set of synapses. It does not do anything special,
    except add methods that make it easier to handle the synapse population"""

    def __init__(self, sim,  synapses,synapse_pop_name=None, user_tags=None):

        # Some functions return lists of synapses; so we
        # reduce the input down to a flat list:
        self.synapses = []
        for s in synapses:
            if s is None:
                continue
            elif is_iterable(s):
                self.synapses.extend(s)
            else:
                print 'Not Iterable:',s
                self.synapses.append(s)


        for s in self.synapses:
            print s, type(s)
            assert s.population is None
            s.population = self

        self.sim = sim
        self.synapse_pop_name=synapse_pop_name if synapse_pop_name is not None else ObjectLabeller.getNextUnamedObjectName(SynapsePopulation, prefix="SynPop")

        user_tags = user_tags or []


    @property
    def synapse_types(self):
        return set(['UnknownType'])

    def record(self, synapse,  what, user_tags=None,user_tag_functors=None, **kwargs):
        if isinstance(synapse, int):
            synapse = self[synapse]
        assert synapse in self.synapses


        user_tags = user_tags or []
        user_tag_functors = user_tag_functors or StdTagFunctors.getRecordFunctorsSynapse()

        kw_utf = { 'synapse':synapse,'synapse_population':self }
        functor_tags = list( itertools.chain( *[utf( **kw_utf ) for utf in user_tag_functors] ) )
        return self.sim.record( synapse,  what=what, user_tags=user_tags + functor_tags, **kwargs)



    def record_all(self, **kwargs):
        assert False, "method renamed to 'record_from_all'"
        return [ self.record( syn, **kwargs) for syn in self.synapses]

    def record_from_all(self, **kwargs):
        return [ self.record( syn, **kwargs) for syn in self.synapses]

    def __len__(self):
        return len( self.synapses )

    def __getitem__(self, i):
        return self.synapses[i]

    def __iter__(self):
        return iter(self.synapses)


    def where_presynaptic(self, cell=None):
        return [ syn for syn in self.synapses if syn.getPreSynapticCell()==cell ]

    def where_postsynaptic(self, cell=None):
        return [ syn for syn in self.synapses if syn.getPostSynapticCell()==cell ]



    def get_where_presynaptic(self, cell=None):
        assert False
        return SynapsePopulation( sim=self.sim, synapse_pop_name=self.synapse_pop_name, synapses = [ syn for syn in self.synapses if syn.getPreSynapticCell()==cell ] )

    def get_where_postsynaptic(self, cell=None):
        assert False
        return SynapsePopulation( sim=self.sim, synapse_pop_name=self.synapse_pop_name, synapses = [ syn for syn in self.synapses if syn.getPostSynapticCell()==cell ] )


    @property
    def presynaptic_population(self,):
        pre_pops = set([])
        for syn in self.synapses:
            pre = syn.getPreSynapticCell()
            if pre and pre.population:
                pre_pops.add(pre.population)
        if not pre_pops:
            return None
        else:
            assert len(pre_pops)==1
            return list(pre_pops)[0]
        



    @property
    def postsynaptic_population(self,):
        post_pops = set([])
        for syn in self.synapses:
            post = syn.getPostSynapticCell()
            if post and post.population:
                post_pops.add(post.population)
        if not post_pops:
            return None
        else:
            assert len(post_pops)==1
            return list(post_pops)[0]




class Connectors(object):
    @classmethod
    def AllToAll(cls, sim, presynaptic_population, postsynaptic_population, connect_functor, synapse_pop_name=None ):
        pre_post_it = itertools.product( presynaptic_population, postsynaptic_population )
        synapses = [ connect_functor(sim=sim,  presynaptic=pre, postsynaptic=post) for (pre,post) in pre_post_it if (pre != post) ]
        return SynapsePopulation(sim=sim, synapses=synapses,  synapse_pop_name=synapse_pop_name)


    @classmethod
    def TimesToAll(cls, sim, syncronous_times, postsynaptic_population, connect_functor, synapse_pop_name=None ):
        synapses = [ connect_functor(sim=sim, postsynaptic=post, times=syncronous_times) for post in postsynaptic_population]
        return SynapsePopulation(sim=sim, synapses=synapses, synapse_pop_name=synapse_pop_name)


