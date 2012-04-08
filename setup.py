
from distutils.core import setup


import os
import itertools
import glob

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    print
    print """This setup.py is not complete, it is only here"""
    print """so that the docs can be built on read-the-docs."""
    print """Please see the morphforge documentation for more"""
    print """information"""
    print     
    assert False 


    
locs = [
        "srcs/morphforge/__init__.py",
        "srcs/morphforge/*/__init__.py",
        "srcs/morphforge/*/*/__init__.py",
        "srcs/morphforge/*/*/*/__init__.py",
        "srcs/morphforge/*/*/*/*/__init__.py",
        ]
glob_pkgs =itertools.chain( *[glob.glob(loc) for loc in locs] ) 
glob_pkgs = [ l.replace("srcs/","").replace("__init__.py","") for l in glob_pkgs] 

pkgs = [
'mhlibs',
'mhlibs.quantities_plot',
'mhlibs.scripttools',
] + glob_pkgs



setup(
    name="morphforge",
    version="0.1dev",
    packages=pkgs,
    package_dir = {'': 'src/'},

    author = "Mike Hull",	
    author_email = "mikehulluk@googlemail.com",
    maintainer	="Mike Hull",
    maintainer_email = "mikehulluk@googlemail.com",
    url	="https://github.com/mikehulluk/morphforge",
    description = "A high-level python library for simulating small networks of multicompartmental nuerons",
    long_description = open("README.txt").read(),
    download_url = "https://github.com/mikehulluk/morphforge",
    license="BSD 2-Clause",

    )


	




