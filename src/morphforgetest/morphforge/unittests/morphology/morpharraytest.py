from morphforge.morphology.core.morphologyarray import MorphologyArray

from morphforge.morphology.core.morphologytree import MorphologyTree
from morphforge.morphology.ui.mayavirenderer import MayaViRenderer
from morphforge.morphology.ui.matplotlibviewer import MatPlotLibViewer
from morphforge.morphology.importer.morphologyimporter import MorphologyImporter
from morphforge.morphology.exporter.morphologyexporter import MorphologyExporter
from morphforge.morphology.comparison.comparearrays import MorphArrayComparison
from morphforge.morphology.builders.morphologyloader import MorphologyLoader






m = MorphologyImporter.fromSWCFile( filename="/home/michael/workspace/morphforge/src/test_data/swc_srcs/28o_spindle20aFI.CNG.swc", astype=MorphologyTree)


MorphologyExporter.toSWCFile( morphology = m, filename="/home/michael/Desktop/test1.swc" )

m2 = MorphologyImporter.fromSWCFile( filename="/home/michael/Desktop/test1.swc", astype=MorphologyTree )



#m2 = MorphologyLoader.fromSWC( src=open("/home/michael/workspace/morphforge/src/test_data/swc_srcs/28o_spindle20aFI.CNG.swc") )







are_same =  MorphArrayComparison.are_same(m,m2 )
print are_same

#m = MorphologyLoader2.loadSWCFile( filename="/home/michael/workspace/morphforge/src/test_data/swc_srcs/05b_pyramidal9aACC.CNG_short.swc", astype=MorphologyTree)

#MayaViRenderer(morph=m, ).showSimpleCylinders().show()
#MorphologyLoader2.loadSWCFile( astype=MorphologyArray)
MatPlotLibViewer(m)

import pylab
pylab.show()