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





import glob
from os.path import join as Join




class NeuroMLDataLibrary(object):

    @classmethod
    def get_channelMLV1Files(cls):

        subdirs = [
            "CA1PyramidalCell_NeuroML",
            "GranCellLayer_NeuroML",
            "GranuleCell_NeuroML",
            "MainenEtAl_PyramidalCell_NeuroML",
            "SolinasEtAl_GolgiCell_NeuroML",
            "Thalamocortical_NeuroML",
            "VervaekeEtAl-GolgiCellNetwork_NeuroML",
       ]

        simSrcDir = "/home/michael/hw_to_come/mf_test_data/test_data/NeuroML/V1/example_simulations/"
        #simSrcDir = "/home/michael/hw_to_come/morphforge/src/test_data/NeuroML/V1/example_simulations/"

        files = []
        for subdir in subdirs:
            files.extend( glob.glob(Join(simSrcDir, subdir) + '/*.xml'))
        #print files
        #assert False
        return files


    @classmethod
    def _fileContainsSingleChannel(cls, filename):
        from neurounits.importers.neuroml import ChannelMLReader
        from neurounits.importers.neuroml import NeuroMLFileContainsNoChannels, NeuroMLFileContainsMultipleChannels

        try:
            ChannelMLReader.LoadChlRaw(filename)
            return True
        except NeuroMLFileContainsNoChannels:
            return False
        except NeuroMLFileContainsMultipleChannels:
            return False
        except:
            raise


    @classmethod
    def get_channelMLV1FilesWithSingleChannel(cls,):
        return [f for f in cls.get_channelMLV1Files() if cls._fileContainsSingleChannel(f)]

