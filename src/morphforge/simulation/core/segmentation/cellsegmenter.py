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
from morphforge.simulation.core.segmentation.segment import CellSegment



class AbstCellSegmenter(object):

    def __init__(self, cell=None):
        self.cell = cell

    def connect_to_cell(self, cell):
        raise NotImplementedError()


    def get_num_segments(self, section):
        raise NotImplementedError()

    def get_segments(self, section):
        raise NotImplementedError()

    def __iter__(self):
        for section in self.cell.morphology:
            for seg in self.get_segments(section):
                yield seg

    def get_num_segment_total(self):
        return sum( [ self.get_num_segments(section) for section in self.cell.morphology] )

    def get_num_segment_region(self, region):
        return sum( [ self.get_num_segments(section) for section in region] )




class CellSegmenterStd(AbstCellSegmenter):

    def __init__(self, cell=None, ):
        AbstCellSegmenter.__init__(self, cell)
        self._cellSegments = None

        if self.cell:
            self.connect_to_cell(cell)


    def connect_to_cell(self, cell):
        assert not self.cell
        self.cell = cell


    def get_num_segments(self, section):
        return self._get_n_segments(section)

    def get_segments(self, section):
        assert False, 'What is using the cell segment objects??'
        return self.cellSegments[section]


    def _get_n_segments(self, section):
        raise NotImplementedError()



    @property
    def cellSegments(self):
        assert False, 'To remove, as off Jun-2012'
        if self._cellSegments is None:
            self._cellSegments = {}

            # Segment the cell:
            for section in self.cell.morphology:
                nSegs = self._get_n_segments(section)
                self._cellSegments[section] = [ CellSegment(cell=self.cell, section=section, nsegments=nSegs, segmentno=i, segmenter=self) for i in range(0, nSegs) ]
        return self._cellSegments







class CellSegmenter_MaxCompartmentLength(CellSegmenterStd):

    def __init__(self, cell=None, maxSegmentLength=5):
        CellSegmenterStd.__init__(self, cell)
        self.maxSegmentLength = maxSegmentLength

    def _get_n_segments(self, section):
        return int( section.get_length() / self.maxSegmentLength ) + 1



class CellSegmenter_SingleSegment(CellSegmenterStd):

    def _get_n_segments(self, section):
        return 1




class CellSegmenter_MaxLengthByID(CellSegmenterStd):

    def __init__(self, cell=None, section_id_segment_maxsizes=None, defaultSegmentLength=5):
        self.defaultSegmentLength = defaultSegmentLength
        self.section_id_segment_sizes =section_id_segment_maxsizes if section_id_segment_maxsizes is not None else {}

        CellSegmenterStd.__init__(self, cell)

    def _get_n_segments(self, section):
        max_size = self.section_id_segment_sizes.get(section.idTag, self.defaultSegmentLength )
        return  int(section.get_length() / max_size )  +1
