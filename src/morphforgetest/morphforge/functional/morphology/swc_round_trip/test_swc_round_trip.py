#from morphforge.morphology.importer.morphologyimporter import MorphologyImporter
from io import StringIO
#from morphforge.morphology.exporter.morphologyexporter import MorphologyExporter

#import morphforge.morphology.exporter.export_tree_swc

from morphforge.core.misc import StrUtils, find_files_recursively

#import os
import numpy as np
from morphforge.morphology.core.morphologyarray import MorphologyArray
from morphforge.morphology.exporter.export_array_swc import ExportArray_SWC
ExportArray_SWC







class TestSWCRoundTrip(object):

    def test1(self):
        swcSrc = """
        1 0 1.0 2.0 3.0 4.0 -1
        2 0 5.0 6.0 7.0 8.0 1
        """

        swcOut = MorphologyArray.fromSWC(StringIO(swcSrc)).to_tree().toSWCStr()

        print "*", StrUtils.strip_comments_and_blank_lines(swcSrc), "*"
        print "*", StrUtils.strip_comments_and_blank_lines(swcOut), "*"
        assert StrUtils.strip_comments_and_blank_lines(swcSrc) == StrUtils.strip_comments_and_blank_lines(swcOut)


        m=MorphologyArray.fromSWC(StringIO(swcSrc))
        s = m.toSWC()
        print s



    def getNeuroMorphFilenames(self):
        f = "/home/michael/hw/morphforge/src/test_data/neuromorpho/"
        return list( find_files_recursively(f,"*.swc") )



    def testNeuroMorpho(self):



        for f in self.getNeuroMorphFilenames():

            m = MorphologyArray.fromSWC(open(f))

            print 'Loaded', f, "(%d Vertices)"%len(m)

            swcOut = m.toSWC()

            dtype= {'names':   ('id', 'type', 'x','y','z','r','pid'), 'formats': ('int32', 'int32', 'f4','f4','f4','f4','int32') }
            swcDataSrc = np.loadtxt(open(f),dtype=dtype )
            swcDataOut = np.loadtxt(StringIO(swcOut),dtype=dtype )

            eps = 0.01
            assert ( swcDataSrc['id'] == swcDataOut['id'] ).all()
            assert ( swcDataSrc['pid'] == swcDataOut['pid'] ).all()
            maxX = np.max( np.fabs( swcDataSrc['x'] - swcDataOut['x'] ) )
            maxY = np.max( np.fabs( swcDataSrc['y'] - swcDataOut['y'] ) )
            maxZ = np.max( np.fabs( swcDataSrc['z'] - swcDataOut['z'] ) )
            maxR = np.max( np.fabs( swcDataSrc['r'] - swcDataOut['r'] ) )
            maxEPS = np.max( (maxX,maxY,maxZ,maxR) )
            assert maxEPS < eps
            print ' -- Max EPS: %f'%maxEPS











if __name__ == "__main__":
    #TestSWCRoundTrip().test1()
    TestSWCRoundTrip().testNeuroMorpho()

