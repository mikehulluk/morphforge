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

class MM_Neuron_Base(object):


    MM_count = 0

    @classmethod
    def get_next_neuron_number(cls):
        x = MM_Neuron_Base.MM_count
        MM_Neuron_Base.MM_count += 1
        return x

    def __init__(self):
        self.mm_neuronNumber = MM_Neuron_Base.get_next_neuron_number()
        self.cachedNeuronSuffix = None

    def get_neuron_suffix(self):

        # Cache the result: (We shouldn't have to do this, but there is a bug
        # with EqnSetChlNeuron::getModFileChangeble(), which is not returning the same thing
        # on each call for some reason.
        if self.cachedNeuronSuffix is None:
            # We take the hash off the parameters that will change the mod-file.
            # This means we don't duplicate millions of mod-files
            # print 'At get_neuron_suffix'
            mod_file_changeables = self.get_mod_file_changeables()
            mod_file_changeables[None] = str( type(mod_file_changeables).__str__ )
            #md5 = getStringMD5Checksum ( pickle.dumps(mod_file_changeables ) )
            md5 = StrUtils.get_hash_md5( pickle.dumps(mod_file_changeables ) )
            self.cachedNeuronSuffix = 'MIKETMP%sChl'%md5
            #return 'MIKETMP%sChl'%md5

        return self.cachedNeuronSuffix

