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

import cPickle as pickle
from morphforge.core.misc import StrUtils
#from morphforge.core import ObjectLabeller


class NEURONChl_Base(object):

    def __init__(self, **kwargs):
        super(NEURONChl_Base, self).__init__(**kwargs)
        self.mm_neuronNumber = None 
        self.cachedNeuronSuffix = None

    def get_neuron_suffix(self):

        # Cache the result: (We shouldn't have to do this, but there is a bug
        # with EqnSetChlNeuron::getModFileChangeble(), which is not returning the same thing
        # on each call for some reason.
        if self.cachedNeuronSuffix is None:
            # We take the hash off the parameters that will change the mod-file.
            # This means we don't duplicate millions of mod-files
            mod_file_changeables = self.get_mod_file_changeables()
            mod_file_changeables[None] = str(type(mod_file_changeables).__str__), str(self.__class__.__name__)

            md5 = StrUtils.get_hash_md5(pickle.dumps(sorted(tuple(mod_file_changeables.iteritems()))))
            self.cachedNeuronSuffix = 'MIKETMP%sChl' % md5

        return self.cachedNeuronSuffix


    def get_mod_file_changeables(self):
        raise NotImplementedError()







