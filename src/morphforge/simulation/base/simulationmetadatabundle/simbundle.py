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

import os
import cPickle

from morphforge.core import FileIO
from morphforge.core import LocMgr
from morphforge.core.misc import StrUtils


# This class is a work around for the circular loop caused by not being
# able to store the md5 hash of an object within that object:

class SimMetaDataBundleBase(object):

    def __init__(self, sim):
        super(SimMetaDataBundleBase, self).__init__()
        self.sim = sim
        self.simmd5sum = StrUtils.get_hash_md5(cPickle.dumps(sim))
        self.postsimulationactions = []

    def add_postprocessing_action(self, action):
        self.postsimulationactions.append(action)

    def do_postprocessing_actions(self):
        assert self.get_simulation().result
        for action in self.postsimulationactions:
            action(self.get_simulation().result, self)

    @classmethod
    def load_from_file(cls, filename):
        bundle = cPickle.load(open(filename))
        return bundle

    def get_sim_md5sum(self):
        return self.simmd5sum


class SimMetaDataBundle(SimMetaDataBundleBase):

    def __init__(self, sim):
        super(SimMetaDataBundle, self).__init__(sim=sim)
        self.metadata = {}

    def get_simulation(self):
        return self.sim

    def _write_to_file(self, bundlefilename=None):
        bundleloc = LocMgr.get_simulation_tmp_dir()
        bundlesuffix = '.bundle'

        if bundlefilename is None:
            bundle_dir = bundleloc + '/' + self.get_sim_md5sum()[0:2]
            bundle_dir = LocMgr.ensure_dir_exists(bundle_dir)
            bundle_fname = self.get_sim_md5sum() + bundlesuffix
            bundlefilename = os.path.join(bundle_dir, bundle_fname)

        FileIO.write_to_file(txt=cPickle.dumps(self),
                             filename=bundlefilename)
        # print 'bundlefilename', bundlefilename
        return bundlefilename

    def write_to_file_and_get_exec_string(self,
            bundlefilename=None,
            simulation_binary_file='SimulateBundle.py'):

        bundle_fname = self._write_to_file(
                        bundlefilename=bundlefilename)
        bundle_exec_bin = os.path.join(
                               LocMgr.get_bin_path(),
                               simulation_binary_file)
        sim_cmd = '%s %s' % (bundle_exec_bin, bundle_fname)
        return (bundle_fname, sim_cmd)


