
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

import mredoc

class PostSynapticTemplateLibrary(object):

    _postsynaptic_template_functor_info = dict()
    _sim_instances = dict()


    @classmethod
    def register_template_specialisation( cls,
                  modelsrc, synapsetype,
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
            templ_type, kwargs = cls._postsynaptic_template_functors
            cls._sim_instances[key] = sim.environment.PostSynapticMechTemplate(templ_type, **kwargs)
        return cls._sim_instances[key]



    #@classmethod
    #def register_psm_template(cls, modelsrc, synapsetype, psm_template_functor):
    #    key = (modelsrc, synapsetype)
    #    assert not key in cls._morphology_functors
    #    cls._postsynaptic_template_functors[key] = psm_template_functor

    #@classmethod
    #def get_postsynaptic_template_functor(cls, synapsetype, modelsrc=None):
    #    return cls._postsynaptic_template_functors[(modelsrc, synapsetype)]

    #@classmethod
    #def get_postsynaptic_template(cls, synapsetype, modelsrc=None, **kwargs):
    #    functor = cls._postsynaptic_template_functors[(modelsrc, synapsetype)]
    #    return functor(**kwargs)

    #@classmethod
    #def summary_table(cls, ):
    #    summary_data = []
    #    for ((modelsrc,synapsetype), functor) in sorted(cls._postsynaptic_template_functors.iteritems()):
    #        summary_data.append( ( modelsrc, synapsetype ))
    #    summary_table = mredoc.VerticalColTable( ('Model','Synapse-Type'), summary_data)
    #    return mredoc.Section('Synapse Library Summary', summary_table )

