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



"""
DocumentLayout:


Root:
    /Simulation Overview
        /Overview Diagram
        /Input Summary
        /KeyTraces

    /Details:
        /Entire Population1

        /Cells:
            /Population1
                /Cell1,Cell2
            /Population2
                /Cell1,Cell2
        /Chemical Synapses:
            All Details: (By type)
            By-Presynaptic
            By-Post Synaptic
        /Gap Junctions
            All Details

        /Stimulations
            /Current Clamps
            /Voltage Clamps

        /Channel Dynamics
        /Synaptic Dynamics

    /Platform Information



"""

from morphforge.simulation.base import Simulation

try:
    import mredoc as mrd
except ImportError:
    print 'Unable to import mredoc, you will be unable to produce pdf/html summaries'


class MembraneMechanismSummariserLibrary(object):
    pass

class SimulationMRedoc(object):

    @classmethod
    def build(self, obj):
        return SimulationMRedoc(obj).mredoc

    def __init__(self, obj):
        assert isinstance(obj, Simulation)
        self.sim = obj
        self.mredoc = self.build_simulation()

        pass

    def save_dot(self, graph, **kwargs):
        from morphforge.core import ObjectLabeller
        name = ObjectLabeller.get_next_unamed_object_name(type(graph))
        fname = '/tmp/dotout_%s.pdf' % name
        graph.write_pdf(fname, **kwargs)
        return fname

    # Todo:
    def build_simulationresult(self, sim):
        pass


    def build_simulation(self):
        return mrd.Section('Simulation Summary',
                mrd.TableOfContents(),
         #       self.build_simulation_overview(),
                self.build_simulation_details(),
               )


    def build_simulation_overview(self,):
        #return
        return mrd.Section("Overview",
                self.build_population_overview(),
               )

    def build_simulation_details(self,):
        return mrd.Section("Details",
                self.build_population_details()
               )


    # The details of the simulation:
    def build_population_overview(self,):

        t = mrd.VerticalColTable(
                "Population | Size | Type """,
                [(pop.pop_name, len(pop), ",".join(pop.cell_types))  for pop in self.sim.neuron_populations]
               )
        t2 = mrd.VerticalColTable(
                "Population | Size | Type """,
                [(pop.synapse_pop_name, len(pop), ",".join(pop.synapse_types))  for pop in self.sim.synapse_populations]
               )

        return mrd.Section("Population Overview",
                           t,t2,
                           self.build_population_overview_dot(),
                           #self.build_population_complete_dot()
                          )



    def build_population_overview_dot(self,):
        import pydot
        graph = pydot.Dot('graphname', graph_type='digraph')

        kwargs = {'fontsize':'6'}

        pops = {}
        for p in self.sim.neuron_populations:
            n = pydot.Node(p.pop_name, shape='square', color='lightblue', style='filled', **kwargs)
            pops[p] = n
            graph.add_node(n)

        for (i, synpop) in enumerate(self.sim.synapse_populations):
            pre_pop = synpop.presynaptic_population
            post_pop = synpop.postsynaptic_population

            if not pre_pop:
                pre_n = pydot.Node(name='SpikeTimes%d'%i, shape='point', color='lightsalmon',style='filled',**kwargs)
                graph.add_node(pre_n)
            else:
                pre_n = pops[pre_pop]

            post_n = pops[post_pop]

            syn_name = "%s\\n(%s)"%(synpop.synapse_pop_name, len(synpop))
            e = pydot.Edge(pre_n, post_n,label=syn_name, color='red', **kwargs)
            graph.add_edge(e)


        fname = self.save_dot(graph)
        return mrd.Figure(mrd.Image(fname))



    def build_population_complete_dot(self,):
        import pydot
        graph = pydot.Dot('graphname', graph_type='digraph', size='7,7', ratio='fill')

        kwargs = {'fontsize':'10'}

        pops = {}
        for p in self.sim.ss_cells:
            n = pydot.Node(p.name, shape='square', color='lightblue', style='filled', **kwargs)
            pops[p] = n
            graph.add_node(n)

        for (i, s) in enumerate(self.sim.ss_synapses):
            pre_cell = s.get_presynaptic_cell()
            post_cell = s.get_postsynaptic_cell()

            if not pre_cell:
                pre_n = pydot.Node(name='SpikeTimes%d' % i, shape='point', color='lightsalmon',style='filled',**kwargs)
                graph.add_node(pre_n)
            else:
                pre_n = pops[pre_cell]
            post_n = pops[post_cell]

            syn_name = '%s' % (s.name)
            e = pydot.Edge(pre_n, post_n,label=syn_name, color='red', **kwargs)
            graph.add_edge(e)

        fname = self.save_dot(graph, prog='circo')
        return mrd.Figure(mrd.Image(fname))




    def _build_population_cell_table(self, population):

        t = mrd.VerticalColTable('Cell|Cell Type|SA(um2)|nseg|Regions(SA(um2):nseg)|Pre/Post-SynChem|GJ|Chls',
                [(cell.name,
                  cell.cell_type_str,
                  "%.0f"%(cell.morphology.surface_area),
                  "%d"%cell.segmenter.get_num_segment_total(),
                  " ".join(["%s(%d:%d)"%(rgn.name,rgn.surface_area, cell.segmenter.get_num_segment_region(rgn)) for rgn in cell.morphology.regions]),
                  "%d %d"%(len(cell.presynaptic_connections),len(cell.postsynaptic_connections)),
                  "%d"%len(cell.electrical_connections),
                  " ".join(cell.biophysics.get_mechanism_ids()),
                 ) for cell in population])

        return t

    def build_population_details(self):
        return mrd.Section('Population Details:',
                *[ self._build_population_details(pop) for pop in self.sim.neuron_populations]
       )

    def _build_population_details(self, pop):
        return mrd.Section('Population: %s'%pop.pop_name,
                self._build_population_cell_table(pop),
                *[ self.build_neuron_details(nrn) for nrn in pop ]
       )




    def build_neuron_details(self, neuron):
        t = mrd.VerticalColTable('Section|SA|Region|nseg|Channels', [], caption='%s:Morphology'%neuron.name)
        t1 = mrd.VerticalColTable('Mechanism|Targetter|Applicator', [], caption='%s:Channels'%neuron.name)
        t2 = mrd.VerticalColTable('Type|Distance From Soma', [], caption='%s:Presynaptic Connections'%neuron.name)
        t3 = mrd.VerticalColTable('Type|Distance From Soma', [], caption='%s:Postsynaptic Connections'%neuron.name)
        t4 = mrd.VerticalColTable('Type|Distance From Soma', [], caption='%s:Gap Junctions'%neuron.name)

        return mrd.SectionNewPage('Neuron:%s'%neuron.name,
                "Blah blha",
                t,t1,t2,t3,t4,
               )


