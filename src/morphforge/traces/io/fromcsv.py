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

import json
import re

import numpy as np

from morphforge.units import unit
from morphforge.traces.tracetypes import TraceVariableDT, TraceFixedDT


class InvalidNeuroCSVFile(RuntimeError):

    pass


def parse_json_helpful(s):

    S = s.replace("'", '"')
    try:
        return json.loads(S)
    except:
        raise


class NeuroCSVHeaderData(object):

    def __init__(self, headerlines):
        self.column_data = {}
        self.file_data = None
        self.load_hints = None
        self.events = []
        self.ignored_lines = []

        # Parse the header:
        self.parse(headerlines)

        self.summarise()

    def summarise(self):
        print self.file_data
        for col_key in sorted(self.column_data):
            print 'Column: ', col_key, self.column_data[col_key]
        print 'LoadHints', self.load_hints
        print 'Ignored Lines:', self.ignored_lines

    def parse(self, headerlines):
        actions = {'@': self.parse_at, 
                   '!': self.parse_exclaim}
        for line in headerlines:
            line = line.strip()
            if not line:
                continue
            action = actions.get(line[0], None)
            if action:
                action(line[1:].strip())
            else:
                self.ignored_lines.append(line)

    @classmethod
    def parse_at(cls, line):
        print 'Parsing Event:', line
        print line
        raise NotImplementedError()


    def parse_exclaim(self, line):

        # Either the first Character is a { or something of the form 'COLUMN1' or 'LOADHINT'
        if line[0] == '{':
            self.file_data = parse_json_helpful(line)
        else:
            exclaim_line_regex = re.compile(r"""\s* (LOADHINT|COLUMN)(\d*) \s* : \s* (.*)""", re.VERBOSE)
            match_obj = exclaim_line_regex.match(line)
            if not match_obj:
                raise InvalidNeuroCSVFile('Could not parse line: %s' % line)

            # Load 'COLUMN' info:
            if match_obj.group(1) == 'COLUMN':
                col_num = int(match_obj.group(2))
                if col_num in self.column_data:
                    raise InvalidNeuroCSVFile('Repeated Column Description Found: %d' % col_num)
                self.column_data[col_num] = parse_json_helpful(match_obj.group(3))

            # Load 'LOADHINT' info
            else:
                if self.load_hints is not None:
                    raise InvalidNeuroCSVFile('Repeated LOADHINT Description Found')
                self.load_hints = parse_json_helpful(match_obj.group(3))


class NeuroCSVParser(object):

    @classmethod
    def parse(cls, filename):
        # Read the Header
        header_lines = cls.extract_header(filename)
        header_lines = cls.resolve_header_backslashes(header_lines)
        header = NeuroCSVHeaderData(header_lines)

        # Body Data:
        data_array = cls.readbodydata(filename)

        # Build the traces:
        trs = cls.build_traces(header_info=header,
                               data_array=data_array)
        return trs

    @classmethod
    def extract_header(cls, filename):
        """ Reads just the header out of a file"""

        header = []
        with open(filename, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if not line.startswith('#'):
                    return header
                else:
                    header.append(line[1:])

    @classmethod
    def resolve_header_backslashes(cls, header_data):
        new_header_data = []
        current_line = ''
        for line in header_data:
            # Drop the leading '#':
            current_line += line.strip()

            if line.endswith('\\'):
                # Strip the '\' and replace it with a space
                current_line = current_line[:-1] + ' '
            else:
                new_header_data.append(current_line)
                current_line = ''

        # Check no trailing backslash:
        assert current_line == ''
        return new_header_data

    @classmethod
    def readbodydata(cls, filename):
        print filename
        data = np.loadtxt(fname=filename, comments='#')
        return data

    @classmethod
    def build_traces(cls, header_info, data_array):
        n_cols = data_array.shape[1]

        # Get the time column:
        time_data_raw = data_array[:, 0]
        time_unit = unit(str(header_info.column_data[0]['unit']))
        time_data = time_data_raw * time_unit

        # Do we build as fixed or variable array:
        trace_builder = (TraceFixedDT if TraceFixedDT.is_array_fixed_dt(time_data) else TraceVariableDT)

        trcs = []
        for i in range(1, n_cols):
            d_i = data_array[:, i]
            column_metadict = header_info.column_data[i]
            dataUnit = unit(str(column_metadict.get('unit', '')))
            data_label = str(column_metadict.get('label', 'Column%d' % i))
            data_tags = str(column_metadict.get('tags', '')).split(',')
            d = d_i * dataUnit

            tr = trace_builder(time_data, d, name=data_label, tags=data_tags)
            trcs.append(tr)
        return trcs


