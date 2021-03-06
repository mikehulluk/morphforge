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


from morphforge.core import LocMgr, Join

hostlistfilename = Join(LocMgr.get_bin_path(), "DellMachines.txt")
hostlistfile = open(hostlistfilename)

hosts = [l.strip() for l in hostlistfile.readlines() if not l.startswith("#") and l.strip() != ""]
hosts = []


print len(hosts)

print hosts
#assert False


import os
import re
import time
import sys

lifeline = re.compile(r"(\d) received")
report = ("No response", "Partial Response", "Alive")

print time.ctime()
alivehosts = []
for host in hosts:
    pingaling = os.popen("ping -q -c2 " + host, "r")
    print "Testing ", host,
    sys.stdout.flush()
    alive = False
    while 1:
        line = pingaling.readline()
        if not line: break
        igot = re.findall(lifeline, line)
        if igot:
            print report[int(igot[0])]
            res = int(igot[0])
            if res == 2:
                alivehosts.append(host)




print "Alive Hosts:", len(alivehosts)

print time.ctime()


opFile = open("ToLauch.sh", "w")
opFile.write("#! /bin/bash\n ")
#Launch up a job on each:
for host in alivehosts:
    opFile.write(" echo Starting Job on %s \n" % host.strip())
    opFile.write(" ssh -f %s 'nohup JC.sh &' \n" % host.strip())
    opFile.write(" sleep 5 \n")
opFile.close()
