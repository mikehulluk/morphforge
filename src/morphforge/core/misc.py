#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#  - Redistributions of source code must retain the above copyright notice,
#  this list of conditions and the following disclaimer.  - Redistributions in
#  binary form must reproduce the above copyright notice, this list of
#  conditions and the following disclaimer in the documentation and/or other
#  materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------
from mgrs import LocMgr

from os.path import exists as Exists
from os.path import join as Join
from subprocess import call

import hashlib
import string
import re 
import random
import os
import fnmatch

def find_files_recursively(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename



def StripCommentsAndBlankLines(text):
    new = []
    for l in text.split("\n"):
        n = l.find('#')
        if n != -1:
            l = l[:n]
        if l.strip():
            new.append(l.strip())
    return "\n".join(new)


def ExecCommandGetRetCode(cmd, args=None):
    args = args if args else []
    retcode = call(cmd + " " + " ".join(args), shell=True)
    return retcode
    
    

# TODO: Refactor the classes below into a class:
class FileWriter():
    Write = "Write"
    Append = "Append"
    def __init__(self, s, filename=None, filelocation=None, filesuffix=None, mode=Write):
        pass






def WriteToFile(s, filename=None, filedirectory=None, suffix=None):
    if not filename:
        filename = LocMgr.getTemporaryFilename( suffix=suffix, 
                                                filedirectory=filedirectory)

    with open(filename, "w") as f:
        f.write(s)

    return filename


def WriteStringToMD5SumName(s, filedirectory=None, suffix=""):
    filedirectory= filedirectory or LocMgr.getTmpPath()
    md5Str = getStringMD5Checksum(s)
    fullFileName = Join(filedirectory, md5Str + suffix)
    if Exists(fullFileName):
        if getFileMD5Checksum(fullFileName) != md5Str:  
            raise ValueError("File exists with invalid checksum")
        return fullFileName
    return WriteToFile(s, filename=fullFileName)



   
def getFileMD5Checksum(f):
    return getStringMD5Checksum(open(f).read())
    
def getStringMD5Checksum(s):
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()




def AppendToFile(s, filename):
    assert Exists(filename)
    f = open(filename, "a")
    f.write(s)
    f.close()
    return filename
    
    
    
    
def ReadFile(filename):
    f = open(filename)
    c = f.read()
    f.close()
    return c
    



    
def ExactlyOneNotNone(*args):
    notNone = [a for a in args if a != None]
    if len(notNone) != 1: raise ValueError("Not One Not None")
    return notNone[0]



    


def MergeDictionaries(dictionaries):
    res = {}
    for d in dictionaries:
        for (k, v) in d.iteritems():
            if k in res:  assert res[k] == v
            res[k] = v
    return res


def FilterExpectSingle(seq, filterFunc):
    filteredSeq = [ s for s in seq if filterFunc(s) ]
    if len(filteredSeq) == 0:  
        print seq
        raise ValueError("Unable to find any occurances")
    if len(filteredSeq) > 1:  
        raise ValueError("Found too many occurances")
    return filteredSeq[0]

def ExpectSingle(l):
    if len(l) != 1:
        if len(l)==0:
            print "ExpectSingle has none:", l
        else:
            print "ExpectSingle has multiple:", l 
        raise ValueError("")
    return l[0]
    


    
def Flatten(seq):
    res = []
    for item in seq:
        if (isinstance(item, (tuple, list))):
            res.extend(Flatten(item))
        else:
            res.append(item)
    return res





def FilterWithProb(lst,p):
    return [ l for l in lst if random.random() < p ] 








def CheckValidName(name):
    if not isinstance(name, basestring): 
        print name, name.__class__
        raise ValueError("Invalid Name - Not String!")
    validRegex = "^[a-zA-Z][_a-zA-Z0-9]*$"
    m = re.match(validRegex, name)
    if not m: raise  ValueError("Invalid Name: _%s_" % name)
    return name


def CleanName(name):
    newName = ""
    for c in name:
        if c in string.ascii_letters + string.digits:
            newName += c
    return newName

        
def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used."""
    from mgrs import LogMgr
    def newFunc(*args, **kwargs):
        LogMgr.warning("Call to deprecated function %s." % func.__name__)
        return func(*args, **kwargs)
    newFunc.__name__ = func.__name__
    newFunc.__doc__ = func.__doc__
    newFunc.__dict__.update(func.__dict__)
    return newFunc


def require(arg_name, *allowed_types):
    def make_wrapper(f):
        if hasattr(f, "wrapped_args"):
            wrapped_args = getattr(f, "wrapped_args")
        else:
            code = f.func_code
            wrapped_args = list(code.co_varnames[:code.co_argcount])

        try:
            arg_index = wrapped_args.index(arg_name)
        except ValueError:
            raise NameError, arg_name

        def wrapper(*args, **kwargs):
            if len(args) > arg_index:
                arg = args[arg_index]
                if not isinstance(arg, allowed_types):
                    type_list = " or ".join(str(allowed_type) for allowed_type in allowed_types)
                    raise TypeError, "Expected '%s' to be %s; was %s." % (arg_name, type_list, type(arg))
            else:
                if arg_name in kwargs:
                    arg = kwargs[arg_name]
                    if not isinstance(arg, allowed_types):
                        type_list = " or ".join(str(allowed_type) for allowed_type in allowed_types)
                        raise TypeError, "Expected '%s' to be %s; was %s." % (arg_name, type_list, type(arg))

            return f(*args, **kwargs)

        wrapper.wrapped_args = wrapped_args
        return wrapper

    return make_wrapper




def requiresubclass(arg_name, *allowed_types):
    def make_wrapper(f):
        if hasattr(f, "wrapped_args"):
            wrapped_args = getattr(f, "wrapped_args")
        else:
            code = f.func_code
            wrapped_args = list(code.co_varnames[:code.co_argcount])

        try:
            arg_index = wrapped_args.index(arg_name)
        except ValueError:
            raise NameError, arg_name

        def wrapper(*args, **kwargs):
            if len(args) > arg_index:
                arg = args[arg_index]
                if not (issubclass(arg.__class__, allowed_types) or isinstance(arg, allowed_types)):
                    type_list = " or ".join(str(allowed_type) for allowed_type in allowed_types)
                    raise TypeError, "Expected '%s' to be %s; was %s." % (arg_name, type_list, type(arg))
            else:
                if arg_name in kwargs:
                    arg = kwargs[arg_name]
                    if not (issubclass(arg.__class__, allowed_types) or isinstance(arg, allowed_types)):
                        type_list = " or ".join(str(allowed_type) for allowed_type in allowed_types)
                        raise TypeError, "Expected '%s' to be %s; was %s." % (arg_name, type_list, type(arg))

            return f(*args, **kwargs)

        wrapper.wrapped_args = wrapped_args
        return wrapper

    return make_wrapper



def CheckType(inst, cls):
    if not isinstance(inst, cls):
        print "INST:", inst
        print "CLASS:", cls
        
        raise  ValueError()













class memoized(object):
    """Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated.
    """
    def __init__(self, func):
        self.func = func
        self.cache = {}
    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            self.cache[args] = value = self.func(*args)
            return value
        except TypeError:
            print "Not Caching"
            # uncachable -- for instance, passing a list as an argument.
            # Better to not cache than to blow up entirely.
            return self.func(*args)
    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__









def isFloat(f):
    try:
        float(f)
        return True
    except:
        return False


def isInt(f):
    try:
        int(f)
        return True
    except:
        return False


def isIterable(f):
    try: 
        iter(f)
        return True
    except TypeError: 
        return False







import datetime

class TimerPredictor(object):
    defaultformatstring = "%A %d. %B %H:%M"

    def __init__(self, nJobsTotal):
        self.nJobsTotal = nJobsTotal
        self.tStart = datetime.datetime.now()
        self.formatstring = TimerPredictor.defaultformatstring


    def Str(self, nJobsComplete):
        tElapsed = datetime.datetime.now() - self.tStart
        tTotal = tElapsed / nJobsComplete * self.nJobsTotal  
        tFinish =  self.tStart + tTotal
        
        l1 = """Time Elapsed:     """ +str(tElapsed)
        l2 = """Percent Complete: %2.3f""" %( float(nJobsComplete)/float(self.nJobsTotal) * 100.0 )
        l3 = """Total Time:       """ + str(tTotal)
        l4 = """Finish Time:      """ + tFinish.strftime(self.formatstring)
        
        return "\n".join([l1,l2,l3,l4])
        
    
def maxWithUniqueCheck(collection, key):
    assert len(collection)
    if len(collection) ==1: return collection[0]
    sc = sorted(collection, key=key)
    assert key( sc[-1]) != key(sc[-2])
    return sc[-1]
