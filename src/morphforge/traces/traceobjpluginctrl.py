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

import operator

from morphforge.core.quantities import unit
from morphforge.traces.tracetypes import TraceFixedDT


class TraceOperatorCtrl(object):

    trace_operators_all = {}
    trace_operators_active = {}
    trace_operators = [operator.__add__, operator.__sub__,
                       operator.__div__, operator.__mul__]

    @classmethod
    def add_trace_operator(cls, operator_type, lhs_type, rhs_type, operator_func, flag='default', set_as_default=False):
        assert operator_type in cls.trace_operators

        key = (operator_type, lhs_type, rhs_type)

        # Add to the list of all:
        if not key in cls.trace_operators_all:
            cls.trace_operators_all[key] = {}

        # Check the flag is not already active:
        assert not flag in cls.trace_operators_all[key], 'Duplicate key/flag %s %s:' % (flag, key)
        cls.trace_operators_all[key][flag] = operator_func

        # Set as default if there is no current default, or flag is default:
        if not key in cls.trace_operators_active or flag == 'default' or set_as_default:
            cls.trace_operators_active[key] = operator_func, flag

    @classmethod
    def add_trace_operator_symmetrical(cls, operator_type, lrhs_type, operator_func, flag='default', set_as_default=False):
        cls.add_trace_operator(operator_type=operator_type,
                              lhs_type=lrhs_type,
                              rhs_type=lrhs_type,
                              operator_func=operator_func,
                              flag=flag,
                              set_as_default=set_as_default)







    @classmethod
    def operate(cls, operator_type, lhs, rhs, use_flag=None, **kwargs):
        #toc = TraceOperatorCtrl
        key = (operator_type, type(lhs), type(rhs))

        # Use the active operation:
        if not use_flag:
            assert key in cls.trace_operators_active, 'Trace Operation not defined for: %s' % str(key)
            opfunctor = cls.trace_operators_active[key][0]

        # Use a custom operation:
        else:
            assert key in cls.trace_operators_all
            assert use_flag in cls.trace_operators_all[key]
            opfunctor = cls.trace_operators_all[key][use_flag]

        return opfunctor(lhs=lhs, rhs=rhs, **kwargs)






def _prepend_conversion_to_fixed_trace_to_function(func, fixed_trace_dt):
    from morphforge.traces import TraceConverter

    def wrapped_func(self, *args, **kwargs):
        tr_new = TraceConverter.rebase_to_fixed_dt(self, dt=fixed_trace_dt)
        return func(tr_new, *args, **kwargs)

    return wrapped_func


class TraceMethodCtrl(object):

    registered_methods = {}

    # A list of method names that can be used for anytrace
    # if a specific method is not available for a type of trace
    fallback_to_fixedtrace_methods = {}

    default_fallback_resolution = unit('0.1:ms')

    @classmethod
    def register(cls, trace_cls, method_name, method_functor, can_fallback_to_fixed_trace=False, fallback_resolution=None):
        # print 'Registering method', trace_cls, method_name
        key = (trace_cls, method_name)
        assert not key in cls.registered_methods
        cls.registered_methods[key] = method_functor

        # Can we fallback to fixed_dt traces to use this operation
        if can_fallback_to_fixed_trace:
            fallback_resolution = fallback_resolution or cls.default_fallback_resolution
            assert trace_cls == TraceFixedDT
            cls.fallback_to_fixedtrace_methods[method_name] = fallback_resolution

    @classmethod
    def has_method(cls, trace_cls, method_name):
        if (trace_cls, method_name) in cls.registered_methods:
            return True
        if method_name in cls.fallback_to_fixedtrace_methods:
            return True
        return False

    @classmethod
    def get_method(cls, trace_cls, method_name):
        key = (trace_cls, method_name)
        if key in cls.registered_methods:
            return cls.registered_methods[key]
        # Fallback to FixedDT
        if method_name in cls.fallback_to_fixedtrace_methods:
            method = cls.registered_methods[(TraceFixedDT, method_name)]
            dt = cls.fallback_to_fixedtrace_methods[method_name]
            return _prepend_conversion_to_fixed_trace_to_function(method, fixed_trace_dt=dt)

        # Error!
        assert False







def copy_trace_attrs(tr_old, tr_new, name=None, comment=None, tags=None, add_tags=None):
    # NewName:
    if name is not None:
        if name.startswith('+'):
            new_name = tr_old.name + name[1:]
        elif name.endswith('+'):
            new_name = name[:-1] + tr_old.name
        else:
            new_name = name
    else:
        new_name = tr_old.name

    # NewComment:
    if comment is not None:
        if comment.startswith('+'):
            new_comment = tr_old.comment + comment[1:]
        elif comment.endswith('+'):
            new_comment = comment[:-1] + tr_old.comment
        else:
            new_comment = comment
    else:
        new_comment = tr_old.comment

    if tags:
        assert not add_tags
        new_tags = tags
    else:
        new_tags = tr_old.tags + ((add_tags if add_tags else []))

    tr_new.name = new_name
    tr_new.comment = new_comment
    tr_new.tags = new_tags

    return tr_new




def clone_trace(tr, data=None, time=None, name=None, comment=None, tags=None, add_tags=None):

    new_data = (data if data is not None else tr._data)
    new_time = (time if time is not None else tr._time)

    # Create a new trace
    tr_new = type(tr)(time=new_time, data=new_data)
    return copy_trace_attrs(tr,tr_new, name=name, comment=comment, tags=tags, add_tags=add_tags)


