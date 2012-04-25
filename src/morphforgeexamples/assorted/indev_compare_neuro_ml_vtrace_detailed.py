


from morphforgecontrib.simulation.membranemechanisms.neuroml_via_xsl.neuroml_via_xsl_neuron import NeuroML_Via_XSL_ChannelNEURON
import glob

#from morphforge.core import Join
#from morphforgecontrib.indev.neuroml.core import parse_channelml_file,\
#    MorphforgeNotImplementedException
#from morphforge.simulation.neuron.neuronsimulationenvironment import NeuronSimulationEnvironment
#from morphforge.morphology.core.tree import MorphologyTree
#from morphforge.simulation.shortcuts import ApplyMechanismEverywhereUniform,\
#    ApplyPassiveEverywhereUniform
#from morphforge.simulation.core.biophysics.passiveproperties import PassiveProperty
#from morphforge.core.quantities.fromcore import unit





from morphforge.stdimports import *

import random as R
from morphforgecontrib.simulation.membranemechanisms.neuroml_via_neurounits.neuroml_via_neurounits_neuron import NeuroML_Via_NeuroUnits_ChannelNEURON
from morphforge.simulation.neuron.neuronsimulationsettings import NeuronSimulationSettings
from neurounits.importers.neuroml.core import parse_channelml_file,\
    MorphforgeNotImplementedException
from morphforge.simulation.core.segmentation.cellsegmenter import CellSegmenter_SingleSegment
#from morphforgecontrib.mhdev.junk import NEURONHACKRevVoltageSetter



def simulate_chls_on_neuron(chl_applicator_functor, voltage_level, simtype, ):
    # Create the environment:
    env = NeuronSimulationEnvironment()
    
    # Create the simulation:
    mySim = env.Simulation( tstop=unit("1500:ms") )
    
    # Create a cell:
    morphDict1 = {'root': {'length': 18.8, 'diam': 18.8, 'id':'soma'} }
    m1 = MorphologyTree.fromDictionary(morphDict1)
    myCell = mySim.createCell(name="Cell1%s"%simtype, morphology=m1, segmenter=CellSegmenter_SingleSegment() )
    
    # Setup the HH-channels on the cell:
    chl = chl_applicator_functor(env, myCell, mySim)
    
    
    
    
    
    
    # Setup passive channels:
    ApplyPassiveEverywhereUniform(myCell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )
    
    
    
    
    # Get a location on the cell:
    somaLoc = myCell.getLocation("soma")
    
    # Create the stimulus and record the injected current:
    #cc = mySim.createCurrentClamp( name="Stim1", amp=unit("10:pA"), dur=unit("100:ms"), delay=unit("300:ms") * R.uniform(0.95,1.0), celllocation=somaLoc)
    
    cc = mySim.createVoltageClamp( name="Stim1",  
                                   dur1=unit("200:ms"), amp1=unit("-60:mV"), 
                                   dur2=unit("500:ms")* R.uniform(0.95,1.0), amp2=voltage_level,
                                   dur3=unit("500:ms")* R.uniform(0.95,1.0), amp3=unit("-50:mV"),
                                   celllocation=somaLoc, 
                                   )
    
    
    # Define what to record:
    mySim.record( myCell, what=StdRec.MembraneVoltage, name="SomaVoltage", location = somaLoc ) 
    mySim.record( cc, what=StdRec.Current, name="CurrentClamp" )
    
    
    
    
    # Run the simulation
    results = mySim.Run()
    
    
    
    
    return results



class SimMode:
    XSL="XSL"
    NeuroUnit="NeuroUnit"


def testfile(xmlfile):
    
    if xmlfile != "/home/michael/hw_to_come/morphforge/src/test_data/NeuroML/V1/example_simulations/MainenEtAl_PyramidalCell_NeuroML/K_ChannelML.xml":
        return 
    
    
    print xmlfile
    #return

    
    
    f = QuantitiesFigure()
    
    
    vars = ["CurrentClamp",'SomaVoltage','ninf','I','g']
    ax = []
    for i in range( len(vars)):
        t = [f.add_subplot(len(vars),2,i*2+1),f.add_subplot(len(vars),2,i*2+2)] 
        ax.append( t )
    


    
    colors = 'rgbcmykrgbcmyk'
    view_min,view_max = [None]*len(vars), [None]*len(vars)
    
    
    
    
    
    
    
    #v_levels = [-80, -40,-20,20]
    v_levels = [-80,-40, -20, 20]
    for i,v in enumerate(v_levels):
        #if i> 2:
        #    continue
        res = testfile_voltage(xmlfile, unit("%d:mV"%v) )
        
        for j,v in enumerate(vars):
            print 'Var', v
            trXSL = res[SimMode.XSL].getTrace(v)
            trNUnits = res[SimMode.NeuroUnit].getTrace(v)
            
            trXSLMin = trXSL.window( (600,650)*pq.ms).mean()
            if not view_min[j] or view_min[j] > trXSLMin:
                view_min[j] = trXSLMin
            if not view_max[j] or view_max[j] < trXSLMin:
                view_max[j] = trXSLMin
            trNUMin = trNUnits.window( (600,650)*pq.ms).mean()
            if not view_min[j] or view_min[j] > trNUMin:
                view_min[j] = trNUMin
            if not view_max[j] or view_max[j] < trNUMin:
                view_max[j] = trNUMin
            
            l = ax[j][0].plotTrace(trXSL, color=colors[i])
            ax[j][0].plotTrace(trNUnits, color=l[0].get_color(), linewidth=10 , alpha=0.2)
            
            l = ax[j][1].plotTrace(trXSL, color=colors[i])
            ax[j][1].plotTrace(trNUnits, color=l[0].get_color(), linewidth=10 , alpha=0.2)
            
    
    for j in range(len(vars)):
        rRange = view_max[j] - view_min[j]
        ax[j][0].set_ylim( (view_min[j]-0.1*rRange, view_max[j]+0.1*rRange ) )
        ax[j][1].set_ylim( (view_min[j]-0.1*rRange, view_max[j]+0.1*rRange ) )
        
        ax[j][0].set_xlim( (190,250) * pq.ms )
        ax[j][1].set_xlim( (100,700) * pq.ms  )
        
    
    root_dir = "/home/michael/Desktop/fOut/"
    
    LocMgr.EnsureMakeDirs(root_dir)
    fName = root_dir + "_".join( xmlfile.split("/")[-3:] )
    import pylab
    pylab.savefig( fName + ".svg"  )
    print fName
    #assert False
    





    


def testfile_voltage(xmlfile, voltage):
    
    #  via the neurounits bridge:
    chl_neuro = NeuroML_Via_NeuroUnits_ChannelNEURON(xml_filename=xmlfile,  mechanism_id="Blhkjl")
    def applicator_neuro( env, cell, sim): 
        
        ApplyMechanismEverywhereUniform(cell, chl_neuro )
        sim.addRecordable( chl_neuro.getRecordable( 'n_inf', celllocation=cell.getLocation("soma"), nrn_unit=unit(""),  name="ninf") )
        sim.addRecordable( chl_neuro.getRecordable( 'I', celllocation=cell.getLocation("soma"), nrn_unit=unit(""),  name="I") )
        sim.addRecordable( chl_neuro.getRecordable( 'g', celllocation=cell.getLocation("soma"), nrn_unit=unit(""),  name="g") )
        return chl_neuro
    
    # via xsl transformation: 
    xsl_file = "/home/michael/srcs/neuroml/CommandLineUtils/ChannelMLConverter/ChannelML_v1.8.1_NEURONmod.xsl"
    chl_xsl = NeuroML_Via_XSL_ChannelNEURON(xml_filename=xmlfile, xsl_filename=xsl_file,  mechanism_id="Blah")
    def applicator_xsl(env, cell, sim ): 
        
        ApplyMechanismEverywhereUniform(cell, chl_xsl )
        sim.addRecordable( chl_xsl.getRecordable( 'ninf', celllocation=cell.getLocation("soma"), nrn_unit=unit(""),  name="ninf") )
        sim.addRecordable( chl_xsl.getRecordable( 'ik', celllocation=cell.getLocation("soma"), nrn_unit=unit("mA/cm2"),  name="I") )
        sim.addRecordable( chl_xsl.getRecordable( 'gion', celllocation=cell.getLocation("soma"), nrn_unit=unit("S/cm2"),  name="g") )
        #sim.simulation_objects.append( NEURONHACKRevVoltageSetter(cell=cell, ion="ek", value=unit("-90:mV")) )
        return chl_xsl
    
    

    import os
    os.system("cp %s /home/michael/mftmp/"%xmlfile)
    
    resA = simulate_chls_on_neuron( applicator_xsl, voltage_level=voltage, simtype="_XSL" )
    resB = simulate_chls_on_neuron( applicator_neuro,voltage_level=voltage, simtype="_NeuroUnit" )
    

    return {
            SimMode.XSL:resA, 
            SimMode.NeuroUnit:resB, 
            }
    









subdirs = [
    "CA1PyramidalCell_NeuroML",
    "GranCellLayer_NeuroML",
    "GranuleCell_NeuroML",
    "MainenEtAl_PyramidalCell_NeuroML",
    "SolinasEtAl_GolgiCell_NeuroML",
    "Thalamocortical_NeuroML",
    "VervaekeEtAl-GolgiCellNetwork_NeuroML",
]

simSrcDir = "/home/michael/hw_to_come/morphforge/src/test_data/NeuroML/V1/example_simulations/"


chls = {}



i=0

ok = []
fail1 = []
fail2 = []
fail3 = []


for subdir in subdirs:
    
    xmlFiles = glob.glob( Join(simSrcDir, subdir) + '/*.xml')
    
    for xmlfile in xmlFiles:
        
        
        new_chls = parse_channelml_file(xmlfile)
        if len(new_chls) == 0:
            continue
        
        
        i = i +1
        
        #if i < 70:
        #    continue
        
        
        
        #print i, xmlfile
        if xmlfile in [
                       # has a suffix: pas, which neuron chokes on:
                       "/home/michael/hw/morphforge/src/test_data/NeuroML/V1/example_simulations/CA1PyramidalCell_NeuroML/pas.xml",
                       "/home/michael/hw/morphforge/src/test_data/NeuroML/V1/example_simulations/Thalamocortical_NeuroML/pas.xml",
                       # Choked on build for some reason:
                       "/home/michael/hw/morphforge/src/test_data/NeuroML/V1/example_simulations/SolinasEtAl_GolgiCell_NeuroML/KAHP_CML.xml",
                       "/home/michael/hw/morphforge/src/test_data/NeuroML/V1/example_simulations/VervaekeEtAl-GolgiCellNetwork_NeuroML/KAHP_CML.xml",
                       
                       "/home/michael/hw/morphforge/src/test_data/NeuroML/V1/example_simulations/CA1PyramidalCell_NeuroML/na3.xml",
                       
                       "/home/michael/hw/morphforge/src/test_data/NeuroML/V1/example_simulations/Thalamocortical_NeuroML/ar.xml",
            
                        # Funny alpha term that I don't get:
                       "/home/michael/hw/morphforge/src/test_data/NeuroML/V1/example_simulations/Thalamocortical_NeuroML/kc_fast.xml",
                       "/home/michael/hw/morphforge/src/test_data/NeuroML/V1/example_simulations/Thalamocortical_NeuroML/kc.xml",
                       
                       ]:
            continue
        
        
        
        try:
            testfile(xmlfile)
            ok.append(xmlfile)
            
        
        except MorphforgeNotImplementedException:
            fail1.append(xmlfile)
            
    
        except NotImplementedError:
            fail2.append(xmlfile)
            
        
        except Exception, e:
            print xmlfile
            fail3.append( (xmlfile, e) )
            raise
    

import pylab
pylab.show()
    


print "done"


print 'OKs:', len(ok)
print 'Fails: (1):', len(fail1)
print 'Fails: (2)', len(fail2)
print 'Fails: (3)', len(fail3)



print 'OKs:'
for chl in ok:
    print chl

print
print 'Failed from MF Not Supporting:'
for chl in fail1:
    print chl

print
print 'Failed from NeuroUnits not Supporting:'
for chl in fail2:
    print chl

print
print 'Failed generally:'
for chl,prob in fail3:
    
    print chl
    print "-",prob

        
        








