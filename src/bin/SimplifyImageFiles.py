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
import sys
import glob



files = glob.glob(sys.argv[1])


ext_gen = None

intermediate_filename_tmpl = "mf_tmpF%03d%s"
op_file = "test1.avi"

os.system("rm mf_tmpF*")

for i, f in enumerate(sorted(files)):
    print i, f
    ext = os.path.splitext(f)[1]

    if ext_gen and ext != ext_gen:
        assert False, 'Inconsistent image file types! (%s, %s)'%(ext_gen, ext)
        ext_gen = ext


    new_name = intermediate_filename_tmpl%(i, ext)


    os.system('ln -s "%s" "%s" '%(f, new_name))

if os.path.exists(op_file):
    os.unlink(op_file)


vid_cmd = "ffmpeg -r 1 -i mf_tmpF%03d.png -vcodec mpeg4 -r 24 test1.avi"
os.system(vid_cmd)




#ffmpeg -i test_%d.jpg -vcodec mpeg4 test.avi
#
