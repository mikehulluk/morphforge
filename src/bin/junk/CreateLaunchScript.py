
from morphforge.core import LocMgr, Join

hostlistfilename = Join(LocMgr.getBinPath(), "DellMachines.txt")
hostlistfile = open(hostlistfilename) 

hosts = [ l.strip() for l in hostlistfile.readlines() if not l.startswith("#") and l.strip() != ""]
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
