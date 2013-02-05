#!/usr/bin/python
# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  - Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------

import itertools
import string
from morphforge.simulation.base.core.cell import Cell
from morphforgecontrib.tags import StdTagFunctors
from morphforge.core.objectnumberer import ObjectLabeller
from morphforge.core.misc import is_iterable


class NeuronPopulation(object):

    def __init__(
        self,
        sim,
        neuron_functor,
        n,
        pop_name=None,
        name_tmpl_str=None,
        user_tags=None,
        ):

        user_tags = user_tags or []
        if pop_name:
            user_tags.extend(pop_name.split('_'))

        if pop_name is None:
            pop_name = ObjectLabeller.get_next_unamed_object_name(NeuronPopulation, prefix='NrnPop', num_fmt_string='%d')

        self.pop_name = pop_name

        if name_tmpl_str is None:
            name_tmpl_str = '%s_$i' % self.pop_name

        name_tmpl = string.Template(name_tmpl_str)
        self.sim = sim

        # Create the neurons:
        self._nrns = []
        for i in range(n):
            cell_name = name_tmpl.substitute({'i': i})


            cell_tags = user_tags + ['Index%d' % i]
            n = neuron_functor(sim=sim, name=cell_name,
                               cell_tags=cell_tags)
            n.population = self
            self._nrns.append(n)


        self._cell_to_index_lut = self._build_cell_to_index_lut()

    def __len__(self):
        return len(self._nrns)

    def __getitem__(self, i):
        return self._nrns[i]

    def __iter__(self):
        return iter(self._nrns)

    @property
    def cell_types(self):
        return set(['<Unknown>'])

    def record(
        self,
        cell,
        location_func=None,
        what=None,
        user_tags=None,
        user_tag_functors=None,
        **kwargs
        ):

        # Indexable by index of cell reference
        if isinstance(cell, int):
            cell = self[cell]
        assert cell in self._nrns

        what = what or Cell.Recordables.MembraneVoltage
        user_tags = user_tags or []
        user_tag_functors = user_tag_functors \
            or StdTagFunctors.get_record_functors_neuron()
        location_func = location_func or (lambda cell: cell.soma)
        cell_location = location_func(cell)

        kw_utf = {'cell_location': cell_location,
                  'neuron_population': self, 'neuron': cell}

        functor_tags = list(itertools.chain(*[utf(**kw_utf) for utf in
                            user_tag_functors]))
        r = self.sim.record(cell, cell_location=location_func(cell),
                            what=what, user_tags=user_tags
                            + functor_tags, **kwargs)
        return r

    def record_all(self, **kwargs):
        assert False, "Method renamed to 'record_from_all"
        return [self.record(cell, **kwargs) for cell in self._nrns]

    def record_from_all(self, **kwargs):
        return [self.record(cell, **kwargs) for cell in self._nrns]

    def for_each(self, func):
        return [func(cell=nrn) for nrn in self._nrns]

    def _build_cell_to_index_lut(self):
        return dict([ (cell,index) for (index,cell) in enumerate(self._nrns)])

    def index(self, cell):
        return self._cell_to_index_lut[cell]


class SynapsePopulation(object):

    """A synapse population is a container for a set of synapses. It does not do anything special,
    except add methods that make it easier to handle the synapse population"""

    def __init__(
        self,
        sim,
        synapses,
        synapse_pop_name=None,
        user_tags=None,
        ):

        # Some functions return lists of synapses; so we
        # reduce the input down to a flat list:
        self.synapses = []
        for s in synapses:
            if s is None:
                continue
            elif is_iterable(s):
                self.synapses.extend(s)
            else:
                #print 'Not Iterable:', s
                self.synapses.append(s)

        for s in self.synapses:
            #print s, type(s)
            assert s.population is None
            s.population = self

        self.sim = sim
        self.synapse_pop_name=synapse_pop_name if synapse_pop_name is not None else ObjectLabeller.get_next_unamed_object_name(SynapsePopulation, prefix="SynPop")

        user_tags = user_tags or []

    @property
    def synapse_types(self):
        return set(['UnknownType'])

    def record(self, synapse,  what, user_tags=None, user_tag_functors=None, **kwargs):
        if isinstance(synapse, int):
            synapse = self[synapse]
        assert synapse in self.synapses

        user_tags = user_tags or []
        user_tag_functors = user_tag_functors \
            or StdTagFunctors.get_record_functors_synapse()

        kw_utf = {'synapse': synapse, 'synapse_population': self}
        functor_tags = list(itertools.chain(*[utf(**kw_utf) for utf in
                            user_tag_functors]))
        return self.sim.record(synapse, what=what, user_tags=user_tags
                               + functor_tags, **kwargs)

    def record_all(self, **kwargs):
        assert False, "method renamed to 'record_from_all'"
        return [self.record(syn, **kwargs) for syn in self.synapses]

    def record_from_all(self, **kwargs):
        return [self.record(syn, **kwargs) for syn in self.synapses]

    def __len__(self):
        return len(self.synapses)

    def __getitem__(self, i):
        return self.synapses[i]

    def __iter__(self):
        return iter(self.synapses)

    def where_presynaptic(self, cell=None):
        return [syn for syn in self.synapses
                if syn.get_presynaptic_cell() == cell]

    def where_postsynaptic(self, cell=None):
        return [syn for syn in self.synapses
                if syn.get_postsynaptic_cell() == cell]

    def get_where_presynaptic(self, cell=None):
        assert False
        return SynapsePopulation(sim=self.sim,
                                 synapse_pop_name=self.synapse_pop_name,
                                 synapses=[syn for syn in self.synapses
                                 if syn.get_presynaptic_cell() == cell])

    def get_where_postsynaptic(self, cell=None):
        assert False
        return SynapsePopulation(sim=self.sim,
                                 synapse_pop_name=self.synapse_pop_name,
                                 synapses=[syn for syn in self.synapses
                                 if syn.get_postsynaptic_cell()
                                 == cell])

    @property
    def presynaptic_population(self):
        pre_pops = set([])
        for syn in self.synapses:
            pre = syn.get_presynaptic_cell()
            if pre and pre.population:
                pre_pops.add(pre.population)
        if not pre_pops:
            return None
        else:
            assert len(pre_pops) == 1
            return list(pre_pops)[0]

    @property
    def postsynaptic_population(self):
        post_pops = set([])
        for syn in self.synapses:
            post = syn.get_postsynaptic_cell()
            if post and post.population:
                post_pops.add(post.population)
        if not post_pops:
            return None
        else:
            assert len(post_pops) == 1
            return list(post_pops)[0]

    @property
    def presynaptic_times(self):
        assert False


class Connectors(object):

    @classmethod
    def all_to_all(
        cls,
        sim,
        presynaptic_population,
        postsynaptic_population,
        connect_functor,
        synapse_pop_name=None,
        ):


        pre_post_it = itertools.product(presynaptic_population,
                postsynaptic_population)
        synapses = [connect_functor(sim=sim, presynaptic=pre,
                    postsynaptic=post) for (pre, post) in pre_post_it
                    if pre != post]
        return SynapsePopulation(sim=sim, synapses=synapses,
                                 synapse_pop_name=synapse_pop_name)

    @classmethod
    def times_to_all(
        cls,
        sim,
        syncronous_times,
        postsynaptic_population,
        connect_functor,
        synapse_pop_name=None,
        ):
        synapses = [connect_functor(sim=sim, postsynaptic=post,
                    times=syncronous_times) for post in
                    postsynaptic_population]
        return SynapsePopulation(sim=sim, synapses=synapses,
                                 synapse_pop_name=synapse_pop_name)


    @classmethod
    def all_to_all_template(
        cls,
        sim,
        presynaptic_population,
        postsynaptic_population,
        post_synaptic_template,
        pconnection=1.0,
        synapse_pop_name=None,

        presynaptic_location_functor=None,
        postsynaptic_location_functor=None,
        presynaptic_kwargs=None,
        postsynaptic_kwargs=None,
        ):

        #TODO: presynaptic_location_functor, postsynaptic_location_functor are not handled properly!
        assert presynaptic_location_functor == None
        assert postsynaptic_location_functor == None

        if presynaptic_kwargs is None:
            presynaptic_kwargs = {}
        if postsynaptic_kwargs is None:
            postsynaptic_kwargs = {}


        env = sim.environment

        import numpy as np
        from morphforgecontrib.stdimports import *

        # Lets build a connectivity matrix:
        npre = len(presynaptic_population)
        npost = len(postsynaptic_population)

        connectivity = np.random.rand(npre, npost) < pconnection

        needs_presynaptic = np.any(connectivity, axis=1)
        needs_postsynaptic = np.any(connectivity, axis=0)

        # OK, so lets make the presynaptic objects:
        presynaptic_objects = {}
        for i in range(npre):
            if needs_presynaptic[i]:
                pre_cell = presynaptic_population[i]
                pre_cell_loc = presynaptic_location_functor(pre_cell) if presynaptic_location_functor else pre_cell.soma
                presynaptic_objects[i] = env.SynapticTrigger( SynapticTriggerByVoltageThreshold, cell_location=pre_cell_loc,**presynaptic_kwargs )

        # And lets make the post-synaptic objects:
        postsynaptic_objects = {}
        for i in range(npost):
            if needs_postsynaptic[i]:
                post_cell = postsynaptic_population[i]
                post_cell_loc = postsynaptic_location_functor(post_cell) if postsynaptic_location_functor else post_cell.soma
                postsynaptic_objects[i] = post_synaptic_template.instantiate(cell_location=post_cell_loc, **postsynaptic_kwargs)


        # And let connect them up, according to our connectivty matrix:
        synapses = []
        for (pre_index,post_index), are_connected in np.ndenumerate(connectivity):
            if not are_connected or pre_index==post_index:
                continue

            # Connecting:
            syn = sim.create_synapse( trigger = presynaptic_objects[pre_index], postsynaptic_mech=postsynaptic_objects[post_index] )
            synapses.append(syn)

        return SynapsePopulation(sim=sim, synapses=synapses,
                                 synapse_pop_name=synapse_pop_name)
















        #assert False

        #pre_post_it = itertools.product(presynaptic_population, postsynaptic_population)
        #synapses = [connect_functor(sim=sim, presynaptic=pre, postsynaptic=post) for (pre, post) in pre_post_it if pre != post]
        #return SynapsePopulation(sim=sim, synapses=synapses, synapse_pop_name=synapse_pop_name)
