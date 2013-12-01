
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

import types


class PostSynapticTemplateLibrary(object):

    _postsynaptic_template_functor_info = dict()
    _sim_instances = dict()


    @classmethod
    def register_template_specialisation( cls,
                  modelsrc,
                  synapsetype,
                  template_type,
                  **kwargs
                  ):
        key = (modelsrc, synapsetype)
        assert not key in cls._postsynaptic_template_functor_info
        cls._postsynaptic_template_functor_info[key] = (template_type, kwargs)

    @classmethod
    def get_template(cls, sim, modelsrc, synapsetype):
        key = (sim, modelsrc, synapsetype)
        if not key in cls._sim_instances:
            templ_type, kwargs = cls._postsynaptic_template_functor_info[(modelsrc, synapsetype)]
            cls._sim_instances[key] = sim.environment.PostSynapticMechTemplate(templ_type, **kwargs)
        return cls._sim_instances[key]


    @classmethod
    def instantiate(cls, sim, modelsrc, synapsetype, **kwargs):
        tmpl = cls.get_template(sim=sim, modelsrc=modelsrc, synapsetype=synapsetype)
        return tmpl.instantiate(**kwargs)


    @classmethod
    def _dummy_instantiate(cls, modelsrc, synapsetype):
        from morphforge.stdimports import NEURONEnvironment
        sim = NEURONEnvironment().Simulation()
        cell = sim.create_cell(area=1000)
        postsyn = cls.instantiate(sim=sim, modelsrc=modelsrc, synapsetype=synapsetype, cell_location=cell.soma)
        return postsyn




    @classmethod
    def summary_table(cls):
        import mredoc as mrd
        modelsrcs = sorted( set([ modelsrc for (modelsrc, synapsetype) in cls._postsynaptic_template_functor_info.keys() ]) )

        # We are going to make one table per synapse_type per modelsrc:
        sects = []
        for modelsrc in modelsrcs:

            model_data = [ (template_type,synapsetype) for ((_modelsrc,synapsetype), (template_type,_kwargs)) in cls._postsynaptic_template_functor_info.iteritems()  if _modelsrc==modelsrc]
            tmpl_types = sorted(set( [ tt for (tt,st) in model_data] ))
            tmpl_types = [ (tt, sorted([st2 for (tt2,st2) in model_data if tt==tt2])) for tt in tmpl_types]
            tmpl_types = [ (tt,sts) for (tt, sts) in tmpl_types if sts]

            subsect=[]
            for template_type, synapsetypes in tmpl_types:

                var_names = template_type.get_variables()
                cols = ['Name'] + var_names
                row_data = []
                for synapsetype in synapsetypes:
                    syn = cls._dummy_instantiate(modelsrc=modelsrc, synapsetype=synapsetype)
                    syn_vars_dict = syn.get_resolved_parameters()

                    for k,v in syn_vars_dict.iteritems():
                        if isinstance(v, (float, types.BooleanType )):
                            continue
                        print template_type, synapsetype

                        syn_vars_dict[k] = v.rescale(template_type.get_preferred_unit(k))


                    row_data.append( [synapsetype] + [str(syn_vars_dict[varname]) for varname in var_names] )

                tbl = mrd.VerticalColTable(cols, row_data)
                subsect.append( mrd.Section('Type: %s' %(template_type.__name__), tbl) )

            sects.append( mrd.Section('ModelSrc: %s' %(modelsrc), *subsect) )

        return  mrd.Section('PostSynaptic Templates', *sects)
        #'return sect

