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

"""
A collection of utility functions.
Often these are not the most efficient implementations, especially when
dealing with large files, but for most files morphforge has to deal with,
they work fine and make code more readable.

"""

import os.path as fs

import hashlib
import re
import random
import os
import fnmatch

from morphforge.core.mgrs import LocMgr


def find_files_recursively(directory, pattern):
    """ Recursive 'glob' for files.

    This function walks over a directory looking for filenames matching a
    certain pattern"""

    for (root, dirs, files) in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename


class StrUtils(object):

    """ A collection of string utility functions"""

    @classmethod
    def strip_comments_and_blank_lines(cls, text, cmt_sym='#'):
        """ Removes comments and blank lines from block of text
        """

        new = []
        for line in text.split('\n'):
            idx = line.find(cmt_sym)
            if idx != -1:
                line = line[:idx]
            if line.strip():
                new.append(line.strip())
        return '\n'.join(new)

    @classmethod
    def get_hash_md5(cls, s):
        """ Returns the md5 digest hash of a string"""

        m = hashlib.md5()
        m.update(s)
        return m.hexdigest()


class FileIO(object):

    """ A collection of file utility functions"""

    @classmethod
    def append_to_file(cls, txt, filename, file_expected=True):
        """ Appends text to an existing file.

        By default the file is expected to already exist, otherwise an IOError
        exception be thrown. This can be overridden with the file_expected
        parameter. Returns `filename`"""

        if file_expected and not fs.exists(filename):
            raise IOError("Can't append to non-existant file: %s"
                          % filename)
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
        """ Writes text to a file
        This function will overwrite an existing file. If no filename is given,
        a filename will be invented, using LocMgr.get_temporary_filename().
        The name of the file written to will be returned.
        """

        if not filename:
            filename = LocMgr.get_temporary_filename(suffix=suffix,
                    filedirectory=filedirectory)
        with open(filename, 'w') as f:
            f.write(txt)
        return filename

    @classmethod
    def read_from_file(cls, filename):
        """ Reads text from a file"""

        with open(filename) as f:
            c = f.read()
        return c

    @classmethod
    def get_hash_md5(cls, filename):
        """ Returns the md5 checksum of a file.

        This function should not be used for large files, since it loads
        the entire file into memory.
        """

        return StrUtils.get_hash_md5(FileIO.read_from_file(filename))


class SeqUtils(object):

    """ A collection of utility functions for working with sequences"""

    @classmethod
    def flatten(cls, seq, flatten_types=(tuple, list)):
        """ 'Flattens' a sequence recursively.

        The objects types to flatten are specified by the flatten_types
        parameter, which must by a tuple of classes. By default it flattens
        lists and tuples.
        """

        res = []
        for item in seq:
            if isinstance(item, flatten_types):
                new_items = SeqUtils.flatten(
                                item, 
                                flatten_types=flatten_types)
                res.extend(new_items)
            else:
                res.append(item)
        return res

    @classmethod
    def expect_single(cls, l):
        """ Expects a sequence containing a single object and returns it.

        If 0 or more than 1 objects are found, it raises an error.
        """

        if len(l) != 1:
            if len(l) == 0:
                print 'ExpectSingle has none:', l
            else:
                print 'ExpectSingle has multiple:', l
            raise ValueError('')
        return l[0]

    @classmethod
    def filter_expect_single(cls, seq, filter_func):
        """ Filters a sequence according to the predicate filter_func, then
        expects a single item to remain, which it returns.  If 0 or more than
        1 objects are found, it raises an error.
        """

        filtered_seq = [s for s in seq if filter_func(s)]
        if len(filtered_seq) == 0:
            print seq
            raise ValueError('Unable to find any occurances')
        if len(filtered_seq) > 1:
            raise ValueError('Found too many occurances')
        return filtered_seq[0]

    @classmethod
    def filter_with_prob(cls, lst, p):
        """ Returns a copy of the sequence, in which each item in the original
        has a fixed probability of being in the new sequence.
        """

        return [l for l in lst if random.random() < p]

    @classmethod
    def max_with_unique_check(cls, collection, key):
        """ Return the maximum from a sequence, based on a key, but verify
        that there is a unique maximum.

        This is designed to be used when the
        key generates integers."""

        assert len(collection)
        if len(collection) == 1:
            return collection[0]
        sc = sorted(collection, key=key)
        assert key(sc[-1]) != key(sc[-2])
        return sc[-1]


def is_iterable(f):
    """ Returns True if an object can be iterated over by using iter(obj)
    """

    try:
        iter(f)
        return True
    except TypeError:
        return False


def merge_dictionaries(dictionaries):
    """ Merge a sequence of dictionaries safely.

    This function merges dictionaries together, but ensures that there are
    not same keys which point to different values. That is,
    merge_dictionaries({'alpha':True}, {'alpha':True}) is OK, but
    merge_dictionaries({'alpha':True}, {'alpha':False}) will raise an
    exception
    """

    res = {}
    for d in dictionaries:
        for (k, v) in d.iteritems():
            if k in res:
                assert res[k] == v
            res[k] = v
    return res


def check_cstyle_varname(name):
    """ Check a string conforms to a C-style variable name.
    """

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
    """Deprecated"""

    # We are getting rid of the only function calling this './morphforge/src/morphforge/core/quantities/fromcore.py'
    try:
        float(f)
        return True
    except:
        return False


def is_int(f):
    """Deprecated"""

    # We are getting rid of the only function calling this './morphforge/src/morphforge/core/quantities/fromcore.py'
    try:
        int(f)
        return True
    except:
        return False


