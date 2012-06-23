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

import os.path as fs

import hashlib
import re
import random
import os
import fnmatch

from mgrs import LocMgr


def find_files_recursively(directory, pattern):
    for (root, dirs, files) in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename


class StrUtils(object):

    @classmethod
    def strip_comments_and_blank_lines(text):
        new = []
        for l in text.split('\n'):
            n = l.find('#')
            if n != -1:
                l = l[:n]
            if l.strip():
                new.append(l.strip())
        return '\n'.join(new)

    @classmethod
    def get_hash_md5(cls, s):
        m = hashlib.md5()
        m.update(s)
        return m.hexdigest()


class FileIO(object):

    @classmethod
    def append_to_file(cls, txt, filename):
        assert fs.exists(filename)
        with open(filename, 'a') as f:
            f.write(txt)
        return filename

    @classmethod
    def write_to_file(
        cls,
        txt,
        filename=None,
        filedirectory=None,
        suffix=None,
        ):

        if not filename:
            filename = LocMgr.get_temporary_filename(suffix=suffix,
                    filedirectory=filedirectory)
        with open(filename, 'w') as f:
            f.write(txt)
        return filename

    @classmethod
    def read_from_file(cls, filename):
        with open(filename) as f:
            c = f.read()
        return c

    @classmethod
    def get_hash_md5(cls, filename):
        StrUtils.get_hash_md5(FileIO.read_from_file(filename))


class SeqUtils(object):

    @classmethod
    def flatten(cls, seq):
        res = []
        for item in seq:
            if isinstance(item, (tuple, list)):
                res.extend(SeqUtils.flatten(item))
            else:
                res.append(item)
        return res

    @classmethod
    def expect_single(cls, l):
        if len(l) != 1:
            if len(l) == 0:
                print 'ExpectSingle has none:', l
            else:
                print 'ExpectSingle has multiple:', l
            raise ValueError('')
        return l[0]

    @classmethod
    def filter_expect_single(cls, seq, filter_func):
        filtered_seq = [s for s in seq if filter_func(s)]
        if len(filtered_seq) == 0:
            print seq
            raise ValueError('Unable to find any occurances')
        if len(filtered_seq) > 1:
            raise ValueError('Found too many occurances')
        return filtered_seq[0]

    @classmethod
    def filter_with_prob(cls, lst, p):
        return [l for l in lst if random.random() < p]

    @classmethod
    def max_with_unique_check(cls, collection, key):
        assert len(collection)
        if len(collection) == 1:
            return collection[0]
        sc = sorted(collection, key=key)
        assert key(sc[-1]) != key(sc[-2])
        return sc[-1]


def is_iterable(f):
    try:
        iter(f)
        return True
    except TypeError:
        return False


def merge_dictionaries(dictionaries):
    res = {}
    for d in dictionaries:
        for (k, v) in d.iteritems():
            if k in res:
                assert res[k] == v
            res[k] = v
    return res


def check_cstyle_varname(name):
    if not isinstance(name, basestring):
        print name, name.__class__
        raise ValueError('Invalid Name - Not String!')
    valid_regex = '^[a-zA-Z][_a-zA-Z0-9]*$'
    m = re.match(valid_regex, name)
    if not m:
        raise ValueError('Invalid Name: _%s_' % name)
    return name


# Deprecated:
# =========================

def is_float(f):

    # We are getting rid of the only function calling this './morphforge/src/morphforge/core/quantities/fromcore.py'

    try:
        float(f)
        return True
    except:
        return False


def is_int(f):

    # We are getting rid of the only function calling this './morphforge/src/morphforge/core/quantities/fromcore.py'

    try:
        int(f)
        return True
    except:
        return False


