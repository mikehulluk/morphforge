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


from morphforge.morphology.core  import MorphPath
from morphforge.morphology.visitor import SectionIndexerDF
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
    def build(cls, obj):
        return SimulationMRedoc(obj).mredoc

    def __init__(self, obj):
        assert isinstance(obj, Simulation)
        self.sim = obj
        self.mredoc = self.build_simulation()


    @classmethod
    def save_dot(cls, graph, **kwargs):
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
                self.build_simulation_overview(),
                self.build_simulation_details(),
               )


    def build_simulation_overview(self):
        return mrd.SectionNewPage("Overview",
               self.build_population_overview(),
               self.build_singlecell_overview(),
               )

    def build_simulation_details(self):
        return mrd.SectionNewPage("Details",
               self.build_singlecell_details(),
               self.build_population_details(),
                self.build_details_channels(),
               )







    # Overview in terms of populations
    # -------------------------------------

    # The details of the simulation:
    def build_population_overview(self):

        if not self.sim.neuron_populations:
            return None

        t = mrd.VerticalColTable(
                "Population | Size | Type """,
                [(pop.pop_name, len(pop), ",".join(pop.cell_types))  for pop in self.sim.neuron_populations]
               )
        t2 = mrd.VerticalColTable(
                "Population | Size | Type """,
                [(pop.synapse_pop_name, len(pop), ",".join(pop.synapse_types))  for pop in self.sim.synapse_populations]
               )

        return mrd.Section("Population Overview",
                           t, t2,
                           self.build_population_overview_dot(),
                           self.build_population_complete_dot()
                          )



    def build_population_overview_dot(self):


        import pydot
        graph = pydot.Dot('graphname', graph_type='digraph')

        kwargs = {'fontsize': '6'}

        pops = {}
        for p in self.sim.neuron_populations:
            n = pydot.Node(p.pop_name, shape='square', color='lightblue'
                           , style='filled', **kwargs)
            pops[p] = n
            graph.add_node(n)

        for (i, synpop) in enumerate(self.sim.synapse_populations):
            pre_pop = synpop.presynaptic_population
            post_pop = synpop.postsynaptic_population

            if not pre_pop:
                pre_n = pydot.Node(name='SpikeTimes%d' % i, shape='point', color='lightsalmon', style='filled', **kwargs)
                graph.add_node(pre_n)
            else:
                pre_n = pops[pre_pop]

            post_n = pops[post_pop]

            syn_name = "%s\\n(%s)" % (synpop.synapse_pop_name, len(synpop))
            e = pydot.Edge(pre_n, post_n, label=syn_name, color='red', **kwargs)
            graph.add_edge(e)

        fname = self.save_dot(graph)
        return mrd.Figure(mrd.Image(fname))



    def build_population_complete_dot(self):
        import pydot
        graph = pydot.Dot('graphname', graph_type='digraph', size='7,7'
                          , ratio='fill')

        kwargs = {'fontsize': '10'}

        pops = {}
        for p in self.sim.ss_cells:
            n = pydot.Node(p.name, shape='square', color='lightblue',
                           style='filled', **kwargs)
            pops[p] = n
            graph.add_node(n)

        for (i, s) in enumerate(self.sim.ss_synapses):
            pre_cell = s.get_presynaptic_cell()
            post_cell = s.get_postsynaptic_cell()

            if not pre_cell:
                pre_n = pydot.Node(name='SpikeTimes%d' % i,
                                   shape='point', color='lightsalmon',
                                   style='filled', **kwargs)
                graph.add_node(pre_n)
            else:
                pre_n = pops[pre_cell]
            post_n = pops[post_cell]

            syn_name = '%s' % s.name
            e = pydot.Edge(pre_n, post_n, label=syn_name, color='red',
                           **kwargs)
            graph.add_edge(e)

        fname = self.save_dot(graph, prog='circo')
        return mrd.Figure(mrd.Image(fname))












    @classmethod
    def _build_population_cell_table(cls, population):
        return cls._build_cell_table(cell_list=population)

    @classmethod
    def _build_cell_table(cls, cell_list):

        t = mrd.VerticalColTable('Name|Type|SA(um2)|\#sections/segments|Regions(SA(um2):nseg)|\#Pre/Post-Synapse|\#GapJunctions|Chls',
                [(cell.name,
                  cell.cell_type_str,
                  "%.0f" % (cell.morphology.surface_area),
                  "%d:%d" % (len(cell.morphology), cell.segmenter.get_num_segment_total()),
                  " ".join(["%s(%d:%d)" % (rgn.name, rgn.surface_area, cell.segmenter.get_num_segment_region(rgn)) for rgn in cell.morphology.regions]),
                  "%d %d" % (len(cell.presynaptic_connections), len(cell.postsynaptic_connections)),
                  "%d" % len(cell.electrical_connections),
                  " ".join(cell.biophysics.get_mechanism_ids()),
                 ) for cell in cell_list])

        return t

    def build_population_details(self):
        return mrd.Section('Population Details:',
                *[self._build_population_details(pop) for pop in self.sim.neuron_populations]
       )

    def _build_population_details(self, pop):
        return mrd.Section('Population: %s' % pop.pop_name,
                self._build_population_cell_table(pop),
                *[self.build_neuron_details(nrn) for nrn in pop]
       )

    # --------------------------------------------------------




    # Single Cell Overview:
    # --------------------------------------------------------
    # The details of the simulation:
    def build_singlecell_overview(self):
        if self.sim.are_all_cells_in_pops:
            return None

        return mrd.HierachyScope(
                self._build_singlecell_overview_cells(),
                self._build_singlecell_overview_iclamps(),
                self._build_singlecell_overview_vclamps(),
                )

    def _build_singlecell_overview_cells(self):
        return mrd.Section(
                'Individual Cells',
                self._build_cell_table(cell_list=self.sim.ss_cells),
                )


    # Stim Tables:
    def _build_singlecell_overview_stimtable(self, stims):
        data = [(stim.name, 
                 stim.location_summary_str,
                 stim.get_summary_description(),
                 ) for stim in stims]
        tbl = mrd.VerticalColTable('Name|Location|Description', data)
        return tbl

    def _build_singlecell_overview_iclamps(self):
        return mrd.Section('Current Clamps', 
                self._build_singlecell_overview_stimtable(stims=self.sim.ss_current_clamps)
                )

    def _build_singlecell_overview_vclamps(self):
        return mrd.Section('Voltage Clamps', 
                self._build_singlecell_overview_stimtable(stims=self.sim.ss_voltage_clamps)
                )



    def build_singlecell_details(self):
        sub_sections = [self.build_neuron_details(nrn) for nrn in self.sim.cells]
        return mrd.Section('Single Cell Details', *sub_sections)


    # --------------------------------------------------------


    def _build_details_channel(self, mech):
        return mrd.Section('Channel: %s' % mech.name,
                    mrd.Paragraph('boom')
                    )

    def build_details_channels(self):
        mechs = sorted( self.sim.get_mechanisms_in_simulation(), key=lambda i: i.name)
        return mrd.SectionNewPage('Channels',
                *[ self._build_details_channel(mech) for mech in mechs]
                )

















    # Individual Neuron details:
    # -------------------------------

    def _create_neuron_details_1_morphology(self, nrn):
        morph = nrn.morphology
        section_indexer = SectionIndexerDF(morph)
        section_table = mrd.VerticalColTable(
                'ID|Tags|Lateral Surface Area (um2)|Region|nseg|L|diam (prox/dist)',
                [(  section_indexer[sec],
                    sec.idtag,
                    '%.0f' % sec.area,
                    (sec.region.name if sec.region else ''),
                    nrn.cell_segmenter.get_num_segments(sec),
                    sec.length,
                    '%.1f/%.1f' % (sec.p_r*2., sec.d_r*2.)
                    ) for sec in morph],
                caption='%s:Morphology (Sections)' % nrn.name)

        region_table = mrd.VerticalColTable(
                'Region|Surface Area|\#Segments',
                [(rgn.name, rgn.surface_area, len(rgn)) for rgn in nrn.morphology.regions],
                caption='%s:Morphology (Regions)' % nrn.name
                )


        from morphforge.morphology.ui import MatPlotLibViewer
        fig = MatPlotLibViewer(nrn.morphology, fig_kwargs={'figsize':(7,7)} ).fig


        return mrd.HierachyScope(section_table, region_table, mrd.Image(fig), 'tada')

    def _create_neuron_details_2_mta(self, nrn):
        mechs = nrn.biophysics.get_applied_mtas()
        return mrd.VerticalColTable(
                'Mechanism|Priority|Targetter|Applicator', 
                [ ( '%s (%s)' % (mta.mechanism.name, mta.mechanism.get_mechanism_id()),
                    mta.targetter.get_priority(),
                    mta.targetter.get_description(),
                    mta.applicator.get_description(),
                    ) for mta in mechs], 
                caption='%s:Channels' % nrn.name)

    def _create_neuron_details_3a_presynapses(self, nrn):
        return mrd.VerticalColTable('Type|Distance From Soma', [], caption='%s:Presynaptic Connections' % nrn.name)
    def _create_neuron_details_3b_postsynapses(self, nrn):
        return mrd.VerticalColTable('Type|Distance From Soma', [], caption='%s:Postsynaptic Connections' % nrn.name)

    def _create_neuron_details_3c_gapjunctions(self, nrn):
        return mrd.VerticalColTable('Type|Distance From Soma', [], caption='%s:Gap Junctions' % nrn.name)
    def _create_neuron_details_4_stimulation(self, nrn):
        return mrd.VerticalColTable('Type|Distance From Soma', [], caption='%s:Stimulation' % nrn.name)




    def build_neuron_details(self, neuron):

        return mrd.SectionNewPage('Neuron:%s' % neuron.name,
                self._create_neuron_details_1_morphology(neuron),
                self._create_neuron_details_2_mta(neuron),
                self._create_neuron_details_3a_presynapses(neuron),
                self._create_neuron_details_3b_postsynapses(neuron),
                self._create_neuron_details_3c_gapjunctions(neuron),
                self._create_neuron_details_4_stimulation(neuron),
               )


    # -------------------------------
