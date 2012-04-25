# Chl Comparison New

from util import get_chl_info_dir
import shutil
import os
from os.path import join as Join
from Cheetah.Template import Template
html_output_dir = "/home/michael/Desktop/chl_comp"
from morphforge.core import LocMgr

import lxml.etree as etree

import pylab

from morphforge.stdimports import NeuronSimulationEnvironment,MorphologyTree, unit
from morphforge.stdimports import PassiveProperty, ApplyPassiveEverywhereUniform, StdRec
from morphforge.stdimports import  ApplyMechanismEverywhereUniform, pq

import random as R
from morphforge.simulation.core.segmentation.cellsegmenter import CellSegmenter_SingleSegment
import numpy as np

def simulate_chl_vclamp(chl, voltage_level):
    env = NeuronSimulationEnvironment()
    
    # Create the simulation:
    mySim = env.Simulation( tstop=unit("1500:ms") )
    
    # Create a cell:
    morphDict1 = {'root': {'length': 18.8, 'diam': 18.8, 'id':'soma'} }
    m1 = MorphologyTree.fromDictionary(morphDict1)
    myCell = mySim.createCell(morphology=m1, segmenter=CellSegmenter_SingleSegment() )
    
    # Setup the HH-channels on the cell:
    #chl = chl_applicator_functor(env, myCell, mySim)
    ApplyMechanismEverywhereUniform(myCell, chl )
    
    
    
    
    
    
    # Setup passive channels:
    ApplyPassiveEverywhereUniform(myCell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )
    
    
    
    
    # Get a location on the cell:
    somaLoc = myCell.getLocation("soma")
    
    # Create the stimulus and record the injected current:
    #cc = mySim.createCurrentClamp( name="Stim1", amp=unit("10:pA"), dur=unit("100:ms"), delay=unit("300:ms") * R.uniform(0.95,1.0), celllocation=somaLoc)
    
    cc = mySim.createVoltageClamp( name="Stim1",  
                                   dur1=unit("200:ms"), amp1=unit("-60:mV"), 
                                   #dur2=unit("500:ms")* R.uniform(0.95,1.0), amp2=voltage_level,
                                   dur2=unit("500:ms"), amp2=voltage_level,
                                   #dur3=unit("500:ms")* R.uniform(0.95,1.0), amp3=unit("-50:mV"),
                                   dur3=unit("500:ms"), amp3=unit("-50:mV"),
                                   celllocation=somaLoc, 
                                   )
    
    
    # Define what to record:
    mySim.record( myCell, what=StdRec.MembraneVoltage, name="SomaVoltage", location = somaLoc ) 
    mySim.record( cc, what=StdRec.Current, name="CurrentClamp" )
    
    
    
    
    # Run the simulation
    results = mySim.Run()
    
    
    
    
    return results



def simulate_chl_all(chl):
    #res = {}
    return [
        #simulate_chl_vclamp(chl, unit("-80:mV") ),
        #simulate_chl_vclamp(chl, unit("-50:mV") ),
        #simulate_chl_vclamp(chl, unit("-20:mV") ),
        #simulate_chl_vclamp(chl, unit("10:mV") ),
        simulate_chl_vclamp(chl, unit("40:mV") ),
        ]













class ComparisonResult(object):
    def __init__(self, xmlfile, op_file, same_chl="??", exception=None):
        self.xmlfile = xmlfile
        self.op_file = op_file
        self.same_chl = same_chl
        self.exception = exception
        self.output_image_files = []

    
    @property
    def model(self):
        return os.path.splitext(self.xmlfile)[0].split("/")[-2]

    @property
    def chl_type(self):
        return os.path.splitext(self.xmlfile)[0].split("/")[-1]


from xml.sax.saxutils import escape

#import xml

local_tmpl = """
<html>
<body>
<H1>Comparison for $data.xmlfile </H1>

#if $data.exception:
    <pre>
$data.exception_long
</pre>
#end if

<h2>Images</H2>
#for im in $data.output_image_files:
<a href="${im}.pdf"> <img src="${im}.png" width="300" /></a>
#end for

<H2>Source XML</H2>
<pre>$src_xml</pre>

<H2>Output Eqnset (NeuroUnits)</H2>
#try
<pre> $data.chl_neurounits.eqnset.src_text </pre>
#except
Error reading src_txt
#end try


#try
<a href="$data.chl_neurounits_pdf"> PDF of chl </a>
#except
Can't find chl pdf
#end try 

<H2>Output ModFile (NeuroUnits)</H2>
#try
<pre> $data.chl_neurounits.nmodl_txt </pre>
#except
Error reading modl txt
#end try



<H2>Output ModFile (XSL)</H2>
#try
<pre> $data.chl_xsl.modtxt </pre>
#except
Error reading modl txt
#end try



<H2> Neurounit HOC </H2>
#try
#for filename in $data.chl_neurounit_hoc:
<a href="$filename">Hoc </a>
#end for
#except
No Hoc
#end try
<H2> XSL HOC </H2>
#try
#for filename in $data.chl_xsl_hoc:
<a href="$filename">Hoc</a>
#end for
#except
No Hoc
#end try


</body>
</html>

"""


def write_local_page(data):
    x = etree.parse(data.xmlfile)
    xml_pretty = escape ( etree.tostring(x, pretty_print = True) )

    context = { 'data':data,
                'src_xml':xml_pretty,
              }

    with open(data.op_file,"w") as f:
        f.write( Template(local_tmpl, context).respond() )


from morphforgecontrib.simulation.membranemechanisms.neuroml_via_neurounits.neuroml_via_neurounits_neuron import NeuroML_Via_NeuroUnits_ChannelNEURON
from morphforgecontrib.simulation.membranemechanisms.neuroml_via_xsl.neuroml_via_xsl_neuron import NeuroML_Via_XSL_ChannelNEURON
from mhlibs.quantities_plot import QuantitiesFigure



def compareNeuroMLChl( xmlFile ):
    model, chl_type = os.path.splitext(xmlFile)[0].split("/")[-2:]
    print model, chl_type

    op_dir = LocMgr.EnsureMakeDirs(Join(html_output_dir, model, chl_type) )
    op_html = Join(op_dir, "index.html")
    c = ComparisonResult( xmlfile=xmlFile, op_file = op_html, same_chl=True, exception=None)

    try:

        # Make the NeuroUnits channel:
        chl_neuro = NeuroML_Via_NeuroUnits_ChannelNEURON(xml_filename=xmlFile,  mechanism_id="Blhkjl")
        c.chl_neurounits = chl_neuro
        
        from neurounits.tools.writepdf import WriteToPDF
        op_pdf_file = Join(op_dir, 'Op1.pdf')
        #WriteToPDF(eqnset = chl_neuro.eqnset, filename = op_pdf_file)
        c.chl_neurounits_pdf = op_pdf_file
    
        
        # Make the NeuroML channel:
        xsl_file = "/home/michael/srcs/neuroml/CommandLineUtils/ChannelMLConverter/ChannelML_v1.8.1_NEURONmod.xsl"
        chl_xsl = NeuroML_Via_XSL_ChannelNEURON(xml_filename=xmlFile, xsl_filename=xsl_file,  mechanism_id="Blah")
        c.chl_xsl = chl_xsl
        c.chl_xsl_hoc = []


        chl_neuro_res = simulate_chl_all(chl_neuro)
        chl_xsl_res = simulate_chl_all(chl_xsl)
        c.chl_neurounit_hoc = []


        for i,(rN,rX) in enumerate( zip(chl_neuro_res, chl_xsl_res)):

            c.chl_neurounit_hoc.append( rN.hocfilename  )
            c.chl_xsl_hoc.append( rX.hocfilename  )

            tN = rN.getTrace("CurrentClamp").convert_to_fixed(dt=unit("1.01:ms"))
            tX = rX.getTrace("CurrentClamp").convert_to_fixed(dt=unit("1.01:ms"))

            # Compare current traces:
            tN._data[ np.fabs( tN._time.rescale("ms").magnitude - 0) <0.05] *=0
            tX._data[ np.fabs( tX._time.rescale("ms").magnitude - 0) <0.05] *=0
            tN._data[ np.fabs( tN._time.rescale("ms").magnitude - 200) <0.05] *=0
            tX._data[ np.fabs( tX._time.rescale("ms").magnitude - 200) <0.05] *=0
            tN._data[ np.fabs( tN._time.rescale("ms").magnitude - 700) <0.05] *=0
            tX._data[ np.fabs( tX._time.rescale("ms").magnitude - 700) <0.05] *=0
            print "TR1"
            f = QuantitiesFigure()
            ax1 = f.add_subplot(4,1,1)
            ax2 = f.add_subplot(4,1,2)
            ax3 = f.add_subplot(4,1,3)
            ax4 = f.add_subplot(4,1,4)
            ax1.plotTrace(tN, color='b')
            ax1.plotTrace(tX, color='g', linewidth=20, alpha=0.2)
            ax2.plotTrace(tN.window((200,250)*pq.ms), color='b')
            ax2.plotTrace(tX.window((200,250)*pq.ms), color='g', linewidth=20, alpha=0.2)

            num = (tN-tX)
            denom = (tN+tX)
            diff = num/denom
            ax3.plotTrace(diff, color='r')
            
            ax4.plotTrace(rN.getTrace('SomaVoltage'), color='m')
            ax4.plotTrace(rX.getTrace('SomaVoltage'), color='m', linewidth=20, alpha=0.2)
             
            if num.max()[1] > unit("0.1:pA"):
                c.same_chl = False

            out_im = Join( op_dir, "out_im%03d"%i)
            pylab.savefig(out_im+".png")
            pylab.savefig(out_im+".pdf")
            c.output_image_files.append(out_im)
            pylab.close()
        
        c.finished_ok=True


        

    except Exception,e:
        print 'Exception caught:', e
        import traceback
        import StringIO
        s = StringIO.StringIO()
        traceback.print_exc(file=s)
        c.exception_long=s.getvalue()
        c.exception="%s (%s)"%(str(e), str(type(e)))
        c.same_chl = False
        c.finished_ok=False
        raise
    write_local_page(c)

    return c












root_html_tmpl = """
<HTML>
    <BODY>
    <H1>Sucesses</H1>
<table>
    <tr>
        <th> Model </th>
        <th> Chl </th>
        <th> Finished OK </th>
        <th> Outcome </th>
        <th> Exception </th>
    </tr>

#for $res in $data:
#if $res.finished_ok
    <tr>
        <td><a href="$res.op_file">$res.model</a></td>
        <td><a href="$res.op_file">$res.chl_type</a></td>
        <td>$res.finished_ok</td>
        <td>$res.same_chl</td>
        <td>$res.exception</td>
    </tr>
#end if
#end for
</table>



    <H1>Failures</H1>
<table>
    <tr>
        <th> Model </th>
        <th> Chl </th>
        <th> Finished OK </th>
        <th> Outcome </th>
        <th> Exception </th>
    </tr>

#for $res in $data:
#if not $res.finished_ok
    <tr>
        <td><a href="$res.op_file">$res.model</a></td>
        <td><a href="$res.op_file">$res.chl_type</a></td>
        <td>$res.finished_ok</td>
        <td>$res.same_chl</td>
        <td>$res.exception</td>
    </tr>
#end if
#end for
</table>
    </BODY>
</HTML>
"""





def main():

    # Clear out the old directory:
    if os.path.exists(html_output_dir):
        shutil.rmtree(html_output_dir)
    LocMgr.EnsureMakeDirs(html_output_dir)

    root_html = Join(html_output_dir,"index.html")

    data = []
    for xmlfile in get_chl_info_dir():

        #if xmlfile != "/home/michael/hw_to_come/morphforge/src/test_data/NeuroML/V1/example_simulations/GranCellLayer_NeuroML/Golgi_NaF_CML.xml":
        #        continue


        #if xmlfile != "/home/michael/hw_to_come/morphforge/src/test_data/NeuroML/V1/example_simulations/MainenEtAl_PyramidalCell_NeuroML/K_ChannelML.xml":
        #        continue 
        #if xmlfile != "/home/michael/hw_to_come/morphforge/src/test_data/NeuroML/V1/example_simulations/CA1PyramidalCell_NeuroML/kdr.xml":
        #    continue

        # Compare:
        data.append( compareNeuroMLChl(xmlfile) )

        # Re-update the html:
        with open(root_html,"w") as f:
            f.write( Template(root_html_tmpl, {'data': data}).respond())

        #break



main()