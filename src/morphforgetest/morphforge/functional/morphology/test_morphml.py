

import os
from morphforge.morphology.builders.morphologyloader import MorphologyLoader
import unittest




class TestMorphMLLoading(unittest.TestCase):
    
    dir = "/home/michael/hw/morphforge/src/test_data/NeuroML/V1/morphml_samples/"




    def testAllSampleFilesLoadable(self):
        filenames = [
             ("CablesIncluded.xml", {} ),  
             ("L23PyrFRB.morph.xml",  { 'dendrite_group': 'dendrite', 'soma_group':'soma' } ),
             ("Simple.morph.xml", {} ),
             ("SimpleNeuroML.xml", {} ),
             ]


        for f,regions in filenames:
            full = os.path.join( TestMorphMLLoading.dir, f)
            m6 = MorphologyLoader.fromMorphML(open(full), regions=regions) 
        




    def assertListAlmostEqual(self, l1, l2):
        assert len(l1) == len(l2)
        for i1,i2 in zip(l1,l2):
            self.assertAlmostEqual(i1, i2)
    
    def testCablesIncluded(self):
        #print 'Testing MorphML'
        full = os.path.join(TestMorphMLLoading.dir, "CablesIncluded.xml" )
        m = MorphologyLoader.fromMorphML(open(full))
         
        # The morphology has 6 segments and 2 regions:
        self.assertEqual(len(m), 6)
        self.assertEqual(len(m.getRegions()),2)
        self.assertEqual(set([ r.name for r in m.getRegions()] ),set(['somagroup', 'dendritegroup'] ) ) 
        
        
        s = list( m )
        self.assertTrue(  s[0].is_a_root_section() )
        self.assertFalse( s[1].is_a_root_section() )
        self.assertFalse( s[2].is_a_root_section() )
        self.assertFalse( s[3].is_a_root_section() )
        self.assertFalse( s[4].is_a_root_section() )
        self.assertFalse( s[5].is_a_root_section() )
        
        # Sections::
        # SECTION ID=0        
        self.assertListAlmostEqual( 
                              [s[0].p_x, s[0].p_y, s[0].p_z, s[0].p_r],
                              [ 0.0, 0.0, 0.0, 5.0 ] )
        self.assertListAlmostEqual( 
                              [s[0].d_x, s[0].d_y, s[0].d_z, s[0].d_r],
                              [ 10.0, 0.0, 0.0, 5.0 ] )
        self.assertEqual( m.getRegion('somagroup'), s[0].region )
        self.assertEqual( s[0].idTag, 'SomaSeg' )
        root =  s[0]
        
        
        # SECTION ID=1
        s1 = m.getSection(idTag = 'DendSeg1')
        self.assertEqual( s1.parent, root )
        self.assertEqual( m.getRegion('dendritegroup'), s1.region )
        self.assertListAlmostEqual( 
                              [s1.d_x, s1.d_y, s1.d_z, s1.d_r],
                              [ 5.0, 10.0, 0.0, 2.5 ] )
        
        # SECTION ID=2
        s2 = m.getSection(idTag = 'DendSeg2')
        self.assertEqual( s2.parent, s1 )
        self.assertEqual( m.getRegion('dendritegroup'), s2.region )
        self.assertListAlmostEqual( 
                              [s2.d_x, s2.d_y, s2.d_z, s2.d_r],
                              [ 5.0, 20.0, 0.0, 2.5 ] )
        
        
        # SECTION ID=3
        s3 = m.getSection(idTag = 'DendSeg3')
        self.assertEqual( s3.parent, s2 )
        self.assertEqual( m.getRegion('dendritegroup'), s3.region )
        self.assertListAlmostEqual( 
                              [s3.d_x, s3.d_y, s3.d_z, s3.d_r],
                              [ 5.0, 30.0, 0.0, 2.5 ] )
        
        
        # SECTION ID=4
        s4 = m.getSection(idTag = 'DendSeg4')
        self.assertEqual( s4.parent, root )
        self.assertEqual( m.getRegion('dendritegroup'), s4.region )
        self.assertListAlmostEqual( 
                              [s4.d_x, s4.d_y, s4.d_z, s4.d_r],
                              [ 10.0, 0.0, 10.0, 1.5 ] )
        
        # SECTION ID=5
        s5 = m.getSection(idTag = 'DendSeg5')
        self.assertEqual( s5.parent, s4 )
        self.assertEqual( m.getRegion('dendritegroup'), s5.region )
        self.assertListAlmostEqual( 
                              [s5.d_x, s5.d_y, s5.d_z, s5.d_r],
                              [ 10.0, 0.0, 20.0, 1.5 ] )
        
       
        
        