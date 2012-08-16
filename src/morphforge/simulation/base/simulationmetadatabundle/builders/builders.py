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


from morphforge.core import FileIO, LocMgr, Join
from morphforge.core.misc import StrUtils


import cPickle

from morphforge.simulation.base.simulationmetadatabundle import SimMetaDataBundle

import morphforge




class MetaDataBundleBuilder(object):

    """ Creates a bundle that:
        -- Writes Simulation to disk.
        -- Pickles Result after simulation
    """

    simsuffix = '.neuronsim.pickle'
    ressuffix = '.neuronsim.results.pickle'


    @classmethod
    def build_std_pickler(cls, sim):

        from morphforge.simulation.base.simulationmetadatabundle.postsimulation import PostSimulationActionPickleSimulation

        reslocation = LocMgr.get_simulation_results_tmp_dir()


        b = MetaDataBundleBuilder.prepare_sim_bundle(sim)
        # Save the random number seed
        b.random_seed = morphforge.core.mfrandom.MFRandom._seed
        md5sum = b.get_sim_md5sum()
        resfilename = Join(reslocation, 
                           '%s/' % md5sum[:2],
                           md5sum + cls.ressuffix)

        # Save the results to pickle file:
        b.add_postprocessing_action(PostSimulationActionPickleSimulation(resfilename))

        return (b, resfilename)


    @classmethod
    def prepare_sim_bundle(cls, sim):

        simstring = cPickle.dumps(sim)
        simmd5sum = StrUtils.get_hash_md5(simstring)

        simlocation = LocMgr.ensure_dir_exists(LocMgr.get_simulation_tmp_dir() + simmd5sum[0:2])
        simfilename = Join(simlocation, simmd5sum + cls.simsuffix)

        FileIO.write_to_file(txt=simstring, filename=simfilename)

        b = SimMetaDataBundle(sim)
        return b






