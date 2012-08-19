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

import re
from os.path import join as Join

from morphforge.core import LocMgr, LogMgr
from morphforge.core.misc import StrUtils


class ModFile(object):

    @classmethod
    def extract_nrn_suffix_from_text(cls, txt):

        r = re.compile(
            r""".* ^[^:]* SUFFIX \s* (?P<suffix>[a-zA-Z0-9_]+) (\s+:.*)? $ .*""",
            re.VERBOSE | re.MULTILINE | re.DOTALL)
        m = r.match(txt)
        assert m, "Can't extract suffix from mod-file"
        nrnsuffix = m.groupdict()['suffix']
        return nrnsuffix

    def __init__(
        self,
        modtxt,
        name=None,
        additional_compile_flags='',
        additional_link_flags='',
        additional_ld_library_path='',
        ):
        
        # if no name is provided:
        if name == None:
            name = ModFile.extract_nrn_suffix_from_text(modtxt)

        self.name = name
        self.modtxt = modtxt

        self.additional_compile_flags = additional_compile_flags
        self.additional_link_flags = additional_link_flags
        self.additional_ld_library_path = additional_ld_library_path

    def ensure_built(self):
        LogMgr.info('Ensuring Modfile is built')
        from modfilecompiler import ModFileCompiler
        ModFileCompiler().build_modfile(self)

    def get_md5_hash(self):
        return StrUtils.get_hash_md5(self.modtxt)

    def get_built_filename_short(self, ensure_built=True):
        if ensure_built:
            self.ensure_built()
        return 'mod_' + self.get_md5_hash() + '.so'

    def get_built_filename_full(self, ensure_built=True):
        if ensure_built:
            self.ensure_built()
        return Join(LocMgr.get_default_mod_outdir(),
                    self.get_built_filename_short(ensure_built=ensure_built))


