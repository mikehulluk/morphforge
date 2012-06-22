import unittest
import StringIO
import tempfile
from morphforge.morphology.builders.morphologyloader import MorphologyLoader


class TestSWC(unittest.TestCase):

    swcSample = """
         1         1       1591.43         53.87         20.48        0.15        -1
         2         1       1590.78         50.61         20.48        5.80         1
         3         1       1591.43         46.99         20.48        5.16         2
         4         1       1592.74         43.50         20.48        5.16         3
         5         1       1593.39         41.12         20.48        2.02         4
         6        16       1593.39         40.50         20.48        0.64         5
         7        16       1595.35         39.01         20.48        1.43         6
    """



    def testBasicLoad(self):
        
        f = StringIO.StringIO(TestSWC.swcSample)
        m = MorphologyLoader.fromSWC(src=f, morphname=None, regionNames=None)
        print m
        
        self.assertEqual( len(m), 6 )
        self.assertEqual( len(m.get_regions() ), 2 )
        
        root = m.get_root_section()
        self.assertAlmostEqual( root.p_x,  1591.43 )
        self.assertAlmostEqual( root.p_y,  53.87   )
        self.assertAlmostEqual( root.p_z,  20.48   )
        self.assertAlmostEqual( root.p_r,  0.15    )
        
        self.assertAlmostEqual( root.d_x,  1590.78 )
        self.assertAlmostEqual( root.d_y,  50.61   )
        self.assertAlmostEqual( root.d_z,  20.48   )
        self.assertAlmostEqual( root.d_r,  5.80    )
        
        
        
