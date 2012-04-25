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
#from morphforge.simulation.neuron.neuronsimulationsettings import NeuronSimulationSettings
from neurounits.importers.neuroml.core import parse_channelml_file,\
    MorphforgeNotImplementedException



def simulate_chls_on_neuron(chl_applicator_functor, simtype):
    # Create the environment:
    env = NeuronSimulationEnvironment()

    # Create the simulation:
    mySim = env.Simulation( tstop=unit("1500:ms"), cvode=False )

    # Create a cell:
    morphDict1 = {'root': {'length': 18.8, 'diam': 18.8, 'id':'soma'} }
    m1 = MorphologyTree.fromDictionary(morphDict1)
    myCell = mySim.createCell(name="Cell1%s"%simtype, morphology=m1)

    # Setup the HH-channels on the cell:
    chl = chl_applicator_functor(env, myCell, mySim)






    # Setup passive channels:
    ApplyPassiveEverywhereUniform(myCell, PassiveProperty.SpecificCapacitance, unit('1.0:uF/cm2') )




    # Get a location on the cell:
    somaLoc = myCell.getLocation("soma")

    # Create the stimulus and record the injected current:
    #cc = mySim.createCurrentClamp( name="Stim1", amp=unit("10:pA"), dur=unit("100:ms"), delay=unit("300:ms") * R.uniform(0.95,1.0), celllocation=somaLoc)
    offset = unit("50:ms") * R.uniform(0.70,1.3)
    cc = mySim.createVoltageClamp( name="Stim1",
                                   dur1=unit("200:ms")+offset, amp1=unit("-60:mV"),
                                   dur2=unit("500:ms"), amp2=unit("-22:mV"),
                                   dur3=unit("500:ms"), amp3=unit("-50:mV"),
                                   celllocation=somaLoc,
                                   )


    # Define what to record:
    mySim.record( myCell, what=StdRec.MembraneVoltage, name="SomaVoltage", location = somaLoc )
    mySim.record( cc, what=StdRec.Current, name="CurrentClamp" )




    # Run the simulation
    results = mySim.Run()




    return results










def testfile(xmlfile):
    #if xmlfile != "/home/michael/hw_to_come/morphforge/src/test_data/NeuroML/V1/example_simulations/MainenEtAl_PyramidalCell_NeuroML/K_ChannelML.xml":
    #    return

    #if xmlfile != "/home/michael/hw_to_come/morphforge/src/test_data/NeuroML/V1/example_simulations/CA1PyramidalCell_NeuroML/kap.xml":
    #   return

    #if xmlfile != "/home/michael/hw_to_come/morphforge/src/test_data/NeuroML/V1/example_simulations/CA1PyramidalCell_NeuroML/hd.xml":
    #        return 
    #if xmlfile != "/home/michael/hw_to_come/morphforge/src/test_data/NeuroML/V1/example_simulations/CA1PyramidalCell_NeuroML/na3.xml":
    #    return
    if xmlfile in [
                    #Contains parameters:
                    "/home/michael/hw_to_come/morphforge/src/test_data/NeuroML/V1/example_simulations/Thalamocortical_NeuroML/kc_fast.xml",
                    ]:
        return








    rec=False

    #  via the neurounits bridge:
    chl_neuro = NeuroML_Via_NeuroUnits_ChannelNEURON(xml_filename=xmlfile,  mechanism_id="Blhkjl")
    def applicator_neuro( env, cell, sim):
        ApplyMechanismEverywhereUniform(cell, chl_neuro )

        if rec:
            sim.addRecordable( chl_neuro.getRecordable( 'h', celllocation=cell.getLocation("soma"), nrn_unit=unit(""),  name="h") )
            sim.addRecordable( chl_neuro.getRecordable( 'h_inf', celllocation=cell.getLocation("soma"),   name="hinf") )
            sim.addRecordable( chl_neuro.getRecordable( 'h_tau', celllocation=cell.getLocation("soma"),   name="htau") )

            sim.addRecordable( chl_neuro.getRecordable( 'h_alpha', celllocation=cell.getLocation("soma"),  name="h_alpha") )
            sim.addRecordable( chl_neuro.getRecordable( 'h_beta', celllocation=cell.getLocation("soma"),   name="h_beta") )
            #sim.addRecordable( chl_neuro.getRecordable( 'm', celllocation=cell.getLocation("soma"), nrn_unit=unit(""),  name="m") )
            #sim.addRecordable( chl_neuro.getRecordable( 'm_inf', celllocation=cell.getLocation("soma"),   name="minf") )
            #sim.addRecordable( chl_neuro.getRecordable( 'm_tau', celllocation=cell.getLocation("soma"),   name="mtau") )

            #sim.addRecordable( chl_neuro.getRecordable( 'm_alpma', celllocation=cell.getLocation("soma"),  name="m_alpma") )
            #sim.addRecordable( chl_neuro.getRecordable( 'm_beta', celllocation=cell.getLocation("soma"),   name="m_beta") )

        return chl_neuro



    # via xsl transformation:
    xsl_file = "/home/michael/srcs/neuroml/CommandLineUtils/ChannelMLConverter/ChannelML_v1.8.1_NEURONmod.xsl"
    chl_xsl = NeuroML_Via_XSL_ChannelNEURON(xml_filename=xmlfile, xsl_filename=xsl_file,  mechanism_id="Blah")
    def applicator_xsl(env, cell, sim ):
        ApplyMechanismEverywhereUniform(cell, chl_xsl )

        if rec:
            sim.addRecordable( chl_xsl.getRecordable( 'h', celllocation=cell.getLocation("soma"), nrn_unit=unit(""),  name="h") )
            sim.addRecordable( chl_xsl.getRecordable( 'hinf', celllocation=cell.getLocation("soma"), nrn_unit=unit(""),  name="hinf") )
            sim.addRecordable( chl_xsl.getRecordable( 'htau', celllocation=cell.getLocation("soma"), nrn_unit=unit("ms"),  name="htau") )

            sim.addRecordable( chl_xsl.getRecordable( 'halpha', celllocation=cell.getLocation("soma"), nrn_unit=1/unit("ms"), name="h_alpha") )
            sim.addRecordable( chl_xsl.getRecordable( 'hbeta', celllocation=cell.getLocation("soma"), nrn_unit=1/unit("ms"),  name="h_beta") )

            #sim.addRecordable( chl_xsl.getRecordable( 'm', celllocation=cell.getLocation("soma"), nrn_unit=unit(""),  name="m") )
            #sim.addRecordable( chl_xsl.getRecordable( 'minf', celllocation=cell.getLocation("soma"), nrn_unit=unit(""),  name="minf") )
            #sim.addRecordable( chl_xsl.getRecordable( 'mtau', celllocation=cell.getLocation("soma"), nrn_unit=unit("ms"),  name="mtau") )

            #sim.addRecordable( chl_xsl.getRecordable( 'malpha', celllocation=cell.getLocation("soma"), nrn_unit=1/unit("ms"), name="m_alpha") )
            #sim.addRecordable( chl_xsl.getRecordable( 'mbeta', celllocation=cell.getLocation("soma"), nrn_unit=1/unit("ms"),  name="m_beta") )
        return chl_xsl






    import os
    os.system("cp %s /home/michael/mftmp/"%xmlfile)

    resA = simulate_chls_on_neuron( applicator_xsl, simtype="_XSL" )
    resB = simulate_chls_on_neuron( applicator_neuro,simtype="_NeuroUnit" )

    #TagViewer([resA,resB])
    #assert False



    if rec:
        print "Neurounit Names:", [ tr.name for tr in resA.getTraces() ]
        print "XSL Names:", [ tr.name for tr in resB.getTraces() ]


        import pylab
        f = pylab.figure()
        recs = ['h','hinf', 'htau','h_alpha','h_beta']
        rec_units = { 'h':"", 'hinf':"", 'h_alpha':1/unit('ms'), 'htau':'ms', 'h_beta':1/unit('ms')}
        for i,r in enumerate(recs):
            tr1 = resA.getTrace(r)
            tr2 = resB.getTrace(r)

            ax = f.add_subplot(len(recs),1, i+1)
            ax.plot( tr1._time.rescale('ms'), tr1._data.rescale(rec_units[r]).magnitude, 'b', label="XSL" )
            ax.plot( tr2._time.rescale('ms'), tr2._data.rescale(rec_units[r]).magnitude, 'g', label="NEUROUNITS" )
            ax.legend()
            ax.set_ylabel('Variable: %s'%r)




        trAlpha = resB.getTrace("h_alpha")
        trBeta = resB.getTrace("h_beta")
        pylab.figure()
        pylab.plot(trAlpha._time.rescale("ms"), trAlpha._data )
        pylab.figure()
        pylab.plot(trBeta._time.rescale("ms"), trBeta._data )



    print "XMLFILE:", xmlfile
    TagViewer( [resA,resB], timerange=(-10,1500)*pq.ms,show=False )
    #TagViewer( [resB], timerange=(-10,250)*pq.ms )

    #import pylab
    #pylab.show()







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

        print i, xmlfile

        try:
            testfile(xmlfile)
            ok.append(xmlfile)

        except MorphforgeNotImplementedException, e:
            fail1.append((xmlfile,e))
            #raise


        except NotImplementedError, e:
            fail2.append((xmlfile,e))
            raise

        except Exception, e:
            print xmlfile
            fail3.append( (xmlfile, e) )
            raise


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
for chl,e in fail1:
    print chl
    print "  ", e

print
print 'Failed from NeuroUnits not Supporting:'
for chl,e in fail2:
    print chl
    print "  ", e

print
print 'Failed generally:'
for chl,prob in fail3:

    print chl
    print "-",prob



import pylab
pylab.show()

