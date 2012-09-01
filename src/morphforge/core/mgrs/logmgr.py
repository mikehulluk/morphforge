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

import logging
import os
import inspect


class LogMgrState(object):

    Ready = 'Ready'
    Configuring = 'Configuring'
    Uninitialised = 'Uninitalised'


class LogMgr(object):

    _initialised_state = LogMgrState.Uninitialised
    loggers = {}

    @classmethod
    def config(cls):
        from locmgr import LocMgr

        if cls._initialised_state == LogMgrState.Configuring:
            return
        if cls._initialised_state == LogMgrState.Ready:
            return

        cls._initialised_state = LogMgrState.Configuring

        logfilename = os.path.join(LocMgr.get_log_path(), 'log.html')
        logging.basicConfig(filename=logfilename, level=logging.INFO)

        cls._initialised_state = LogMgrState.Ready

        cls.info_from_logger('Logger Started OK')

    @classmethod
    def _pyfile_to_modulename(cls, filename):
        local_path = filename
        morphforge_lib = False
        if 'morphforge' in filename:
            local_path = 'morphforge' + filename.split('morphforge')[-1]
            morphforge_lib = True
        local_path = local_path.replace('.py', '')
        local_path = local_path.replace('/', '.')
        return (local_path, morphforge_lib)

    @classmethod
    def get_caller(cls):
        current_frame = inspect.currentframe()
        outer_frames = inspect.getouterframes(current_frame)
        out_frames_not_this_class = [frame for frame in outer_frames if not frame[1].endswith("logmgr.py")]

        prev_call_frame = out_frames_not_this_class[0]
        caller = cls._pyfile_to_modulename(prev_call_frame[1])
        return (caller, prev_call_frame[2])

    @classmethod
    def info_from_logger(cls, msg):
        package_name = 'morphforge.core.logmgr'
        if not package_name in cls.loggers:
            cls.loggers[package_name] = cls.create_logger(package_name)
        cls.loggers[package_name].info(msg)

    @classmethod
    def _is_logging_active_and_ready(cls):

        if cls._initialised_state == LogMgrState.Ready:
            from settingsmgr import SettingsMgr
            if not SettingsMgr.is_logging():
                return False
            return True
        elif cls._initialised_state == LogMgrState.Configuring:
            return False
        elif cls._initialised_state == LogMgrState.Uninitialised:
            cls.config()
            return True
        else:
            raise ValueError()

    @classmethod
    def info(cls, msg):
        if not cls._is_logging_active_and_ready():
            return
        cls.get_logger().info(msg)

    @classmethod
    def debug(cls, msg):
        if not cls._is_logging_active_and_ready():
            return
        cls.get_logger().debug(msg)

    @classmethod
    def warning(cls, msg):
        if not cls._is_logging_active_and_ready():
            return
        cls.get_logger().warning(msg)

    @classmethod
    def create_logger(cls, log_name):
        logger = logging.getLogger(log_name)
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        # create formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        # add formatter to handler
        handler.setFormatter(formatter)
        # add handler to logger
        logger.addHandler(handler)
        return logger

    @classmethod
    def get_logger(cls):

        # Find Who called us:
        call_mod = 'DISABLEDLOGGING'
        # (call_mod, isMorphforgeLib), lineNum = cls.get_caller()

        if not call_mod in cls.loggers:
            cls.loggers[call_mod] = cls.create_logger(call_mod)
        return cls.loggers[call_mod]


