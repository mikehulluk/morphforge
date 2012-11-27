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



class AbstCellSegmenter(object):

    def __init__(self, cell=None, **kwargs):
        super(AbstCellSegmenter,self).__init__(**kwargs)
        assert cell is None, 'CellSegmenters no longer contain references to cells, to allow for sharing'
        #self.cell = cell

    #def connect_to_cell(self, cell):
    #    assert self.cell is None
    #    self.cell = cell

    def get_num_segments(self, section):
        raise NotImplementedError()

    def get_num_segment_total(self, cell):
        return sum([self.get_num_segments(section) for section in cell.morphology])

    def get_num_segment_region(self, region):
        return sum([self.get_num_segments(section) for section in region])


class CellSegmenterStd(AbstCellSegmenter):

    def __init__(self, **kwargs):
        super(CellSegmenterStd, self).__init__(**kwargs)

    def get_num_segments(self, section):
        return self._get_n_segments(section)

    def _get_n_segments(self, section):
        raise NotImplementedError()



class CellSegmenter_MaxCompartmentLength(CellSegmenterStd):

    def __init__(self, max_segment_length=5, **kwargs):
        super(CellSegmenter_MaxCompartmentLength, self).__init__(**kwargs)
        self.max_segment_length = max_segment_length

    def _get_n_segments(self, section):
        return int(section.get_length() / self.max_segment_length) + 1


class CellSegmenter_SingleSegment(CellSegmenterStd):

    def _get_n_segments(self, section):
        return 1


class CellSegmenter_MaxLengthByID(CellSegmenterStd):

    def __init__(self, section_id_segment_maxsizes=None, default_segment_length=5, **kwargs):
        self.default_segment_length = default_segment_length
        self.section_id_segment_sizes = section_id_segment_maxsizes if section_id_segment_maxsizes is not None else {}

        super(CellSegmenter_MaxLengthByID, self).__init__(**kwargs)

    def _get_n_segments(self, section):
        max_size = self.section_id_segment_sizes.get(section.idtag, self.default_segment_length)
        return int(section.get_length() / max_size) + 1
