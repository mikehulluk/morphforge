#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.  All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------
from morphforge.core import LocMgr, FileIO
from morphforge.core.misc import SeqUtils
import pickle


class SimulationResult(object):

    """ traces is a list of trace Objects"""
    def __init__(self, traces, simulation):
        self.traces = traces
        self.simulation = simulation
        self.t_start = None
        self.t_stop = None

    def set_simulation_time(self, t_start, t_stop):
        self.t_start = t_start
        self.t_stop = t_stop

    def get_trace(self, name):
        return SeqUtils.filter_expect_single(self.traces, lambda s: s.name == name)


    def get_traces(self,):
        return self.traces


    # Loading & Saving:
    def save_to_file(self, filename):
        resString = pickle.dumps(self)
        return FileIO.write_to_file(resString, filename=filename, filedirectory=LocMgr.get_simulation_tmp_dir())

    @classmethod
    def load_from_file(cls, filename):
        return pickle.load(open(filename))

