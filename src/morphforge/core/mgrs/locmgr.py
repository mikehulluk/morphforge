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


import os
import time
import socket
import random


from os.path import join as Join





class LocMgr(object):

    _locations = {}



    @classmethod
    def validate_exists(cls, cell_location):
        """ Helper function to ensure that returned path actually does exist"""
        if cell_location and not os.path.exists(cell_location):
            raise ValueError("Directory does not exist: %s"% cell_location)
        return cell_location

    @classmethod
    def ensure_dir_exists(cls, dir_location):
        """ Helper function that will make directories if they don't exist.

        Useful for temporary locations"""

        if dir_location and not os.path.exists(dir_location):
            from logmgr import LogMgr
            LogMgr.info("Creating FS Location - " + dir_location)
            if  not os.path.exists(dir_location): os.makedirs(dir_location)
        return cls.validate_exists(dir_location)


    @classmethod
    def get_root_path(cls):
        # Load it from the .rc file:
        if not "rootdir" in cls._locations:
            cls._locations["rootdir"] = os.path.abspath( os.path.join( os.path.dirname(__file__), "../../../" ) )
            cls.validate_exists(cls._locations["rootdir"])
        return cls.validate_exists(cls._locations["rootdir"])


    @classmethod
    def get_bin_path(cls):
        return cls.validate_exists(Join(cls.get_root_path(), "bin/"))

    @classmethod
    def get_log_path(cls):
        return cls.ensure_dir_exists(Join(cls.get_tmp_path(), "log/"))



    @classmethod
    def get_temporary_filename(cls, suffix="", filedirectory=None):


        rnd_string = "%f%d%s" % (time.time(), random.randint(0, 32000), socket.gethostname())
        from morphforge.core.misc import StrUtils
        fn = "tmp_%s%s" % (StrUtils.get_hash_md5(rnd_string), suffix)

        filedirectory = filedirectory if filedirectory else cls.get_tmp_path()
        return Join(filedirectory, fn)


    @classmethod
    def get_path_from_rcfile(cls, subsection, default):
        from rcmgr import RCMgr
        if not RCMgr.has_config():
            return default

        if not subsection in cls._locations:

            if RCMgr.has("Locations", subsection):
                cls._locations[subsection] = RCMgr.get("Locations", subsection)
            else:
                cls._locations[subsection] = default

        cls._locations[subsection] = cls._locations[subsection].replace("${PID}", "%d" % os.getpid())
        return cls.ensure_dir_exists(cls._locations[subsection])



    @classmethod
    def get_tmp_path(cls):
        try:
            loc = cls.get_path_from_rcfile("tmpdir", Join(cls.get_root_path(), "tmp"))
        except:
            loc = Join(cls.get_root_path(), "tmp")
        return cls.ensure_dir_exists(loc)




    @classmethod
    def get_default_mod_builddir(cls):
        loc = cls.get_path_from_rcfile("tmp_nrn_mod_builddir", Join(cls.get_tmp_path(), "modbuild_%d/"%os.getpid()) )
        return cls.ensure_dir_exists(loc)


    @classmethod
    def get_default_mod_outdir(cls):
        loc = cls.get_path_from_rcfile("tmp_nrn_mod_buildout", Join(cls.get_tmp_path(), "modout/"))
        return cls.ensure_dir_exists(loc)


    @classmethod
    def get_default_output_dir(cls):
        loc = Join( cls.get_root_path(), "output")
        return cls.ensure_dir_exists(loc)


    @classmethod
    def get_default_summary_output_dir(cls):
        loc = Join( cls.get_default_output_dir(), "summaries")
        return cls.ensure_dir_exists(loc)

    @classmethod
    def get_default_channel_summary_output_dir(cls):
        loc = Join( cls.get_default_summary_output_dir(), "channels" )
        return cls.ensure_dir_exists(loc)






    @classmethod
    def get_simulation_tmp_dir(cls):
        loc = cls.get_path_from_rcfile("tmp_simulationpicklesdir", Join(cls.get_tmp_path(), "simulationdir"))
        return cls.ensure_dir_exists(loc)



    @classmethod
    def get_simulation_results_tmp_dir(cls):
        loc = cls.get_path_from_rcfile("tmp_simulationpicklesdir", Join(cls.get_tmp_path(), "simulationresults"))
        return cls.ensure_dir_exists(loc)



    @classmethod
    def get_ply_parsetab_path(cls, subdir):
        dir_name = os.path.join( cls.get_tmp_path(), "parsetabs/")
        return cls.ensure_dir_exists( os.path.join( dir_name, subdir) )




    ## Test Data:
    ######################




    @classmethod
    def get_test_srcs_path(cls):
        return cls.validate_exists(Join(cls.get_root_path(), "morphforge_testdata"))

    @classmethod
    def get_test_mods_path(cls):
        return cls.validate_exists(Join(cls.get_test_srcs_path(), "mod_files"))

