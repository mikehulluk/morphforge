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

#from morphforge.morphology.core  import MorphPath
from morphforge.core import LocMgr
from morphforge.morphology.visitor import SectionIndexerDF
#from morphforge.simulation.neuron.objects.neuronrecordable import NEURONRecordableOnLocation
from random import randint, choice
import pylab

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

# from morphforge.management import PluginMgr

try:
    import mredoc as mrd
except ImportError:
    print 'Unable to import mredoc, you will be unable to produce pdf/html summaries'


class SummariserObject(object):

    @classmethod
    def build(cls, obj):
        raise NotImplementedError()


class SummariserLibrary(object):

    summarisers = {}

    @classmethod
    def register_summariser(cls, channel_baseclass, summariser_class):
        # Check it has a to_report_lab Method:
        # Todo: Replace this with 'hasattr'
        # assert 'to_report_lab' in summariser_class.__dict__

        # Add it to the dictionary of summarisers:
        cls.summarisers[channel_baseclass] = summariser_class

    @classmethod
    def get_summarisier(cls, obj):
        possible_summarisers = []
        for (ChlType, summarisier) in cls.summarisers.iteritems():
            if issubclass(type(obj), ChlType):
                possible_summarisers.append(summarisier)

        if len(possible_summarisers) == 0:
            return None
        if len(possible_summarisers) == 1:
            return possible_summarisers[0]
        else:
            assert False, 'I have to many options for summarising: ' \
                + str(obj)


class _DotSummaryUtils(object):

    @classmethod
    def save_dot(cls, graph, format, **kwargs):
        from morphforge.core import ObjectLabeller
        name = ObjectLabeller.get_next_unamed_object_name(type(graph))
        tmp_dir = LocMgr.get_tmp_path()
        fname = '%s/dotout_%s.%s' % (tmp_dir, name, format)
        graph.write_pdf(fname, **kwargs)
        return fname


class SimulationMRedoc(object):

    @classmethod
    def build(cls, obj, result=None):
        sim_redoc = SimulationMRedoc(obj).mredoc

        if result is None:
            return sim_redoc

        else:
            return mrd.Section('Simulation Results:', 
                    mrd.Image(result.fig.fig, auto_adjust=False),
                    sim_redoc,
                    )



    def __init__(self, obj):

        assert isinstance(obj, Simulation)
        self.sim = obj
        self.mredoc = self.build_simulation()

    # Todo:
    def build_simulationresult(self, sim):
        pass

    def build_simulation(self):

        from morphforge.management import PluginMgr
        return mrd.Section('Simulation Summary: %s'%self.sim._sim_desc_str(),
                mrd.TableOfContents(),
                self.build_simulation_overview(),
                self.build_simulation_details(),
                #PluginMgr.summarise_all(),
               )


    def build_simulation_overview(self):
        return mrd.SectionNewPage('Overview',
                                  self.build_population_overview(),
                                  self.build_population_complete_dot(),
                                  self.build_singlecell_overview())

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

        table = mrd.VerticalColTable(
                "Population | Size | Type """,
                [(pop.pop_name, len(pop), ",".join(pop.cell_types))  for pop in self.sim.neuron_populations]
               )
        table2 = mrd.VerticalColTable(
                "Population | Size | Type """,
                [(pop.synapse_pop_name, len(pop), ",".join(pop.synapse_types))  for pop in self.sim.synapse_populations]
               )

        return mrd.Section("Population Overview",
                           table, table2,
                           #self.build_population_overview_dot(),
                           self.build_population_complete_dot()
                          )




    def build_population_complete_dot(self):
        return DOTWriter(self.sim).build_population_complete_dot()













    @classmethod
    def _build_population_cell_table(cls, population):
        return cls._build_cell_table(cell_list=population)

    @classmethod
    def _build_cell_table(cls, cell_list):

        table = mrd.VerticalColTable('Name|Type|SA(um2)|\#sections/segments|Regions(SA(um2):nseg)|\#Pre/Post-Synapse|\#GapJunctions|Chls',
                [(cell.name,
                  cell.cell_type_str,
                  "%.0f" % (cell.morphology.surface_area),
                  "%d:%d" % (len(cell.morphology), cell.segmenter.get_num_segment_total()),
                  " ".join(["%s(%d:%d)" % (rgn.name, rgn.surface_area, cell.segmenter.get_num_segment_region(rgn)) for rgn in cell.morphology.regions]),
                  "%d %d" % (len(cell.presynaptic_connections), len(cell.postsynaptic_connections)),
                  "%d" % len(cell.electrical_connections),
                  " ".join([chl.name for chl in cell.biophysics.get_all_channels_applied_to_cell()]),
                 ) for cell in cell_list])

        return table

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

        return mrd.HierachyScope(self._build_singlecell_overview_cells(),
                                 self._build_singlecell_overview_iclamps(),
                                 self._build_singlecell_overview_vclamps())

    def _build_singlecell_overview_cells(self):
        return mrd.Section('Individual Cells',
                           self._build_cell_table(cell_list=self.sim.cells))

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
                           self._build_singlecell_overview_stimtable(stims=self.sim.current_clamps))

    def _build_singlecell_overview_vclamps(self):
        return mrd.Section('Voltage Clamps',
                           self._build_singlecell_overview_stimtable(stims=self.sim.voltage_clamps))

    def build_singlecell_details(self):
        sub_sections = [self.build_neuron_details(nrn) for nrn in
                        self.sim.cells]
        return mrd.Section('Single Cell Details', *sub_sections)


    def _build_details_channel(self, chl):

        sumcls = SummariserLibrary.get_summarisier(chl)
        if not sumcls:
            return mrd.Section('Summary of channel: %s' % chl.name,
                    mrd.Paragraph('<Summariser Missing for type: %s>' % type(chl))
                )

        return mrd.SectionNewPage('Summary of channel: %s' % chl.name,
                           sumcls.build(chl))

    def build_details_channels(self):
        channels = sorted( self.sim.get_all_channels(), key=lambda i: i.name)
        return mrd.SectionNewPage('Channels',
                *[ self._build_details_channel(chl) for chl in channels]
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
                    '%.1f/%.1f' % (sec.p_r * 2., sec.d_r * 2.)
                    ) for sec in morph],
                caption='%s:Morphology (Sections)' % nrn.name)

        region_table = mrd.VerticalColTable(
                'Region|Surface Area|\#Sections',
                [(rgn.name, rgn.surface_area, len(rgn)) for rgn in nrn.morphology.regions],
                caption='%s:Morphology (Regions)' % nrn.name
                )


        from morphforge.morphology.ui import MatPlotLibViewer
        fig = MatPlotLibViewer(nrn.morphology, fig_kwargs={'figsize':(7, 7)}).fig


        return mrd.HierachyScope(section_table, region_table, mrd.Image(fig), 'tada')




    def _create_neuron_details_2b_pta(self, nrn):
        passives = nrn.biophysics.get_applied_passives()
        return mrd.VerticalColTable(
                'PassiveProp|Priority|Targetter|Value', 
                [  (pta.passiveproperty,
                    pta.targetter.get_priority(),
                    pta.targetter.get_description(),
                    str(pta.value),
                    ) for pta in passives], 
                caption='%s:Passive Properties' % nrn.name)


    def _create_neuron_details_2_mta(self, nrn):
        channels = nrn.biophysics.get_applied_mtas()
        return mrd.VerticalColTable(
                'Mechanism|Priority|Targetter|Applicator', 
                [ ( '%s ' % (mta.channel.name, ),
                    mta.targetter.get_priority(),
                    mta.targetter.get_description(),
                    mta.applicator.get_description(),
                    ) for mta in channels], 
                caption='%s:Channels' % nrn.name)

    def _create_neuron_details_3a_presynapses(self, nrn):
        return mrd.VerticalColTable('Type|Distance From Soma', [],
                                    caption='%s:Presynaptic Connections'
                                     % nrn.name)

    def _create_neuron_details_3b_postsynapses(self, nrn):
        return mrd.VerticalColTable('Type|Distance From Soma', [],
                                    caption='%s:Postsynaptic Connections'
                                     % nrn.name)

    def _create_neuron_details_3c_gapjunctions(self, nrn):
        return mrd.VerticalColTable('Type|Distance From Soma', [],
                                    caption='%s:Gap Junctions'
                                    % nrn.name)

    def _create_neuron_details_4_stimulation(self, nrn):
        return mrd.VerticalColTable('Type|Distance From Soma', [],
                                    caption='%s:Stimulation' % nrn.name)

    def build_neuron_details(self, neuron):

        return mrd.SectionNewPage(
            'Neuron:%s' % neuron.name,
            self._create_neuron_details_1_morphology(neuron),
            self._create_neuron_details_2b_pta(neuron),
            self._create_neuron_details_2_mta(neuron),
            self._create_neuron_details_3a_presynapses(neuron),
            self._create_neuron_details_3b_postsynapses(neuron),
            self._create_neuron_details_3c_gapjunctions(neuron),
            self._create_neuron_details_4_stimulation(neuron),
            )


    # -------------------------------




from matplotlib.ticker import MaxNLocator




def build_connectivity_graph(synapse_pop, size=0.75):

    prepop = synapse_pop.presynaptic_population
    #if prepop:
    #    prepop_lut = prepop.build_cell_to_index_lut()

    postpop = synapse_pop.postsynaptic_population
    #postpop_lut = postpop.build_cell_to_index_lut()

    connectivity = list()
    for syn in synapse_pop:

        if prepop:
            pre_index = syn.get_presynaptic_cell().index_in_pop
        else:
            pre_index = 0

        post_index = syn.get_postsynaptic_cell().index_in_pop
        connectivity.append((pre_index, post_index))

    prepop_len = (len(prepop) if prepop else 1) 
    postpop_len = len(postpop)
    max_len = max( (prepop_len, postpop_len) )

    import pylab
    figsize_raw =(size * (float(prepop_len)/max_len),size*(float(postpop_len)/max_len))
    figsize = figsize_raw #figsize_raw[0]+0.75, figsize_raw[1]+0.75
    print figsize



    fig = pylab.figure(figsize=figsize, dpi=400 )
    #ax = fig.add_subplot(1,1,1, aspect='equal') 
    ax = fig.add_axes([0,0,1,1], aspect='equal') 
    xpts,ypts = zip(*connectivity)
    ax.scatter(xpts,ypts, marker='s', s=7, edgecolors='none')
    #ax.axis('equal')
    ax.set_xlim(-0.5, prepop_len-0.5 )
    ax.set_ylim(-0.5, postpop_len-0.5 )
    ax.xaxis.set_major_locator(MaxNLocator(min(prepop_len,3)))
    ax.yaxis.set_major_locator(MaxNLocator(min(postpop_len,3)))
    ax.axes.get_xaxis().set_ticklabels([])
    ax.axes.get_yaxis().set_ticklabels([])
    #pylab.suptitle('Connectivity: %d synapses'%len(synapse_pop))
    #pylab.show()
    return fig











class DOTWriter(object):
    def __init__(self, sim):
        self.sim = sim

    def build_population_complete_dot(self):
        fig_count = 0
        fig_out = '/tmp/dotimages/'
        import pydot
        graph = pydot.Dot('graphname', graph_type='digraph', size='7,7' , ratio='compress', compound='true', splines='true',sep='0.3' )

        size = '0.55'
        fontsize = '6'
        kwargs_general = {
            'fontsize': fontsize,
            'fixedsize': 'True',
            'width': size,
            'height': size,
            'fontname':'Helvetica'
            }


        cell_size='0.15'
        kwargs_cell = { 'shape':'circle', 'fillcolor':'#80b3ffff', 'color':'#0066ffff', 'style':'filled', 'penwidth':'1', 'width':cell_size, 'height':cell_size }
        kwargs_cc = {'shape':'circle', 'style':'filled', 'width':'0.05', }


        kwargs_pop = {'style':'filled', 'color':'lightgrey','nodesep':'100' }
        kwargs_synpop = {'shape':'none', 'fixedsize':'false'  }
        kwargs_synpop_img = {'shape':'square', 'labelloc':'b',   'scale':'false','fixedsize': 'true',}
        kwargs_synpop_edge = {'penwidth':'3', 'color':'green', 'minlen':'50' } 


        # Map Simulation objects into dot objects:
        obj2nodedict = {}
        subgraphs = []

        # Populations become subgraphs:
        for population in self.sim.neuron_populations:
            n = pydot.Cluster(population.pop_name, label=population.pop_name, **dict(kwargs_general.items() +  kwargs_pop.items() ))
            subgraphs.append(n)
            obj2nodedict[population] = n


        # Cells into Nodes
        for cell in self.sim.cells:
            n = pydot.Node(
                cell.name,
                label=cell.name if cell.population is None else '<%d>' % cell.index_in_pop,
                **dict(kwargs_general.items()+ kwargs_cell.items())
                )
            obj2nodedict[cell] = n

            if cell.population:
                obj2nodedict[cell.population].add_node(n)
            else:
                graph.add_node(n)



        for sg in subgraphs:
            graph.add_subgraph(sg)
        del subgraphs



        # Synapse Populations are turned into a node, with edges from pre and
        # to the post synaptic population:
        for synpopindex, synpop in enumerate(self.sim.synapse_populations):

            synpopcluster = pydot.Cluster('SynpopCluster'+synpop.synapse_pop_name)

            # Create the connectivity graph:
            connectivity_graph_figure = build_connectivity_graph(synpop)
            fname = fig_out + '/synpop%d.png' % synpopindex
            pylab.savefig(fname, transparent=True, dpi=400,bb_inches='tight')


            n = pydot.Node(synpop.synapse_pop_name+'im',label='', image=fname, **dict(kwargs_general.items() + kwargs_synpop_img.items()))
            synpopcluster.add_node(n)


            label=''
            label+= synpop.synapse_pop_name
            len_prepop = len(synpop.presynaptic_population) if synpop.presynaptic_population else 1
            pc_conn = 100. * len(synpop) / (len_prepop * len(synpop.postsynaptic_population))
            #print pc_conn
            #pc_conn=50.
            #label+= '\\nType: %s'% (synpop.type)
            label+= '\\nSynapses: %d (%d%%)'% (len(synpop),pc_conn )
            #label= synpop.synapse_pop_name
            n = pydot.Node(synpop.synapse_pop_name+'cap',label='"%s"'%label,  **dict(kwargs_general.items() + kwargs_synpop.items()))
            synpopcluster.add_node(n)


            obj2nodedict[synpop] = synpopcluster
            graph.add_subgraph(synpopcluster)

            # Connect to pre- and post- synaptic pops:
            post_pop = synpop.postsynaptic_population
            e = pydot.Edge(synpopcluster.get_name(), obj2nodedict[post_pop].get_name(), **dict(kwargs_general.items() + kwargs_synpop_edge.items() ))
            graph.add_edge(e)

            pre_pop = synpop.presynaptic_population
            if pre_pop is not None:
                e = pydot.Edge( obj2nodedict[pre_pop].get_name(), synpopcluster.get_name(), **dict(kwargs_general.items() + kwargs_synpop_edge.items() ))
                graph.add_edge(e)
            else:
                print 'NONE'





        for (i, synapse) in enumerate(self.sim.synapses):
            if synapse.population:
                continue
            pre_cell = synapse.get_presynaptic_cell()
            post_cell = synapse.get_postsynaptic_cell()

            if not pre_cell:
                pre_n = pydot.Node(name='SpikeTimes%d' % i,
                                   shape='point', color='lightsalmon',
                                   style='filled', **kwargs_general)
                graph.add_node(pre_n)
            else:
                pre_n = obj2nodedict[pre_cell]
            post_n = obj2nodedict[post_cell]

            syn_name = '%s' % synapse.name
            e = pydot.Edge(pre_n, post_n, label=syn_name, color='red',
                           **kwargs_general)
            graph.add_edge(e)





        stims = {}
        # Simulations:
        for cclamp in self.sim.current_clamps:
            label = '"IClamp: %s\\n %s"' % (cclamp.name,
                    cclamp.location_summary_dot_str)  
            n = pydot.Node(
                cclamp.name,
                label=label,
                **dict(kwargs_general.items()+ kwargs_cc.items())
                )
            stims[cclamp] = n
            graph.add_node(n)

            # Make the edge:
            cell_node = obj2nodedict[cclamp.cell]
            e = pydot.Edge(n, cell_node, label='', color='red')  # **kwargs)
            graph.add_edge(e)

        ## Records:
        #records = {}
        #for record in self.sim.recordables:
        #    name = record.name
        #    # label = '"Record: %s\\n %s"' % (name, record.location_summary_dot_str )
        #    label = '"Record: %s\\n"' % name  # , record.location_summary_dot_str )
        #    n = pydot.Node(
        #        name,
        #        shape='circle',
        #        style='filled',
        #        width='0.05',
        #        fixedsize='True',
        #        label=label,
        #        fontsize=fontsize,
        #        )
        #    records[record] = n
        #    graph.add_node(n)

        #    # Make the edge:
        #    if isinstance(record, NEURONRecordableOnLocation):
        #        post_node = obj2nodedict[record.cell_location.cell]
        #        e = pydot.Edge(n, post_node, label='', color='green')
        #        graph.add_edge(e)

        #    # cell_node = obj2nodedict[record.cell_location.cell]






        graph.write_raw('example_cluster2.dot')

        # Put the stimulations on:

        #fname = _DotSummaryUtils.save_dot(graph, prog='dot')
        fname = _DotSummaryUtils.save_dot(graph, format='pdf', prog='fdp')
        #fname = _DotSummaryUtils.save_dot(graph, prog='osage')
        #fname = _DotSummaryUtils.save_dot(graph, prog='neato')
        return mrd.Section(
                'Diagram Overview',
                mrd.Figure(mrd.Image(fname))
                )
