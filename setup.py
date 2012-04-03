
from distutils.core import setup

pkgs = [
'mhlibs',
'mhlibs.quantities_plot',
'mhlibs.scripttools',

'morphforge',
"morphforge/componentlibraries",
"morphforge/core",
"morphforge/core/mgrs",
"morphforge/core/quantities",
"morphforge/morphology",
"morphforge/morphology/builders",
"morphforge/morphology/core",
"morphforge/morphology/md5",
"morphforge/morphology/ui",
"morphforge/morphology/visitor",
"morphforge/morphology/util",
"morphforge/morphology/conversion",
"morphforge/morphology/errors",
"morphforge/morphology/importer",
"morphforge/morphology/exporter",
"morphforge/morphology/conventions",
"morphforge/morphology/mesh",
"morphforge/morphology/comparison",
"morphforge/simulation",
"morphforge/simulation/core",
"morphforge/simulation/core/biophysics",
"morphforge/simulation/core/networks",
"morphforge/simulation/core/result",
"morphforge/simulation/core/segmentation",
"morphforge/simulation/core/stimulation",
"morphforge/simulation/neuron",
"morphforge/simulation/neuron/biophysics",
"morphforge/simulation/neuron/hocmodbuilders",
"morphforge/simulation/neuron/objects",
"morphforge/simulation/neuron/simulationdatacontainers",
"morphforge/simulation/neuron/networks",
"morphforge/simulation/simulationmetadatabundle",
"morphforge/simulation/simulationmetadatabundle/builders",
"morphforge/simulation/simulationmetadatabundle/postsimulation",
"morphforge/simulation/shortcuts",
"morphforge/simulationanalysis",
"morphforge/simulationanalysis/summaries",
"morphforge/simulationanalysis/viewers",
"morphforge/stdimports",
"morphforge/constants",
"morphforge/traces",
"morphforge/traces/tags",
"morphforge/traces/std_methods",
"morphforge/traces/std_operators",
"morphforge/traces/tracetypes",
"morphforge/traces/io",
"morphforge/traces/tagviewer",
"morphforge/traces/generation",
"morphforge/traces/linkage",
]


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


	




