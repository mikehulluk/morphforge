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




class ObjectLabeller(object):
    """ Provides names for internal use for annoymous objects

    Often, we need to automatically generate names for objects. For example,
    a user might not nessesarily provide names for all cells in simulations,
    but the simulator will expect variable names to refer to them. This class
    provides methods to create new names of objects, based on thier type.
    """

    objectcount = {}

    @classmethod
    def _get_and_increment_count_for_object(cls, obj):
        newcnt = cls.objectcount.get(obj, 0) + 1
        cls.objectcount[obj] = newcnt
        return newcnt

    @classmethod
    def get_next_unamed_object_name(
        cls,
        obj_type,
        prefix=None,
        num_fmt_string=None,
       ):
        """ Returns the next 'anonymous' name for an object of 'obj_type'.
        """
        if num_fmt_string is None:
            num_fmt_string = '%04d'
        if prefix is None:
            prefix = 'Unamed' + str(obj_type.__name__)
        return prefix + num_fmt_string \
            % ObjectLabeller._get_and_increment_count_for_object(obj_type)


