#!/usr/bin/python
# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  - Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------





from morphforgecontrib.simulation.channels.neuroml_via_xsl.neuroml_via_xsl_neuron import NeuroML_Via_XSL_ChannelNEURON
import glob





from morphforge.stdimports import *

import random as R
from morphforgecontrib.simulation.channels.neuroml_via_neurounits.neuroml_via_neurounits_neuron import NeuroML_Via_NeuroUnits_ChannelNEURON




from morphforge.simulation.base.segmentation.cellsegmenter import CellSegmenter_SingleSegment
from mhlibs.test_data.neuroml import NeuroMLDataLibrary
from neurounits.importers.neuroml.errors import NeuroUnitsImportNeuroMLNotImplementedException




def simulate_chls_on_neuron(chl_applicator_functor, voltage_level, simtype):
    # Create the environment:
    env = NEURONEnvironment()

    # Create the simulation:
    sim = env.Simulation(tstop=qty("1500:ms"))

    # Create a cell:
    morphDict1 = {'root': {'length': 18.8, 'diam': 18.8, 'id':'soma'} }
    m1 = MorphologyTree.fromDictionary(morphDict1)
    cell = sim.create_cell(name="Cell1%s" % simtype, morphology=m1, segmenter=CellSegmenter_SingleSegment())

    # Setup the HH-channels on the cell:
    chl = chl_applicator_functor(env, cell, sim)






    # Setup passive channels:
    cell.set_passive( PassiveProperty.SpecificCapacitance, qty('1.0:uF/cm2'))




    # Create the stimulus and record the injected current:
    #cc = sim.create_currentclamp(name="Stim1", amp=qty("10:pA"), dur=qty("100:ms"), delay=qty("300:ms") * R.uniform(0.95, 1.0), cell_location=cell.soma)

    cc = sim.create_voltageclamp(name="Stim1",
                                   dur1=qty("200:ms"), amp1=qty("-60:mV"),
                                   dur2=qty("500:ms")* R.uniform(0.95, 1.0), amp2=voltage_level,
                                   dur3=qty("500:ms")* R.uniform(0.95, 1.0), amp3=qty("-50:mV"),
                                   cell_location=cell.soma,
                                  )


    # Define what to record:
    sim.record(cell, what=StandardTags.Voltage, name="SomaVoltage", cell_location = cell.soma)
    sim.record(cc, what=StandardTags.Current, name="CurrentClamp")




    # run the simulation
    results = sim.run()




    return results



class SimMode:
    XSL="XSL"
    NeuroUnit="NeuroUnit"


def testfile(xmlfile):

    if xmlfile != "/home/michael/hw_to_come/mf_test_data/test_data/NeuroML/V1/example_simulations/GranCellLayer_NeuroML/Golgi_NaF_CML.xml":
        return




    f = QuantitiesFigure()


    variables = ["CurrentClamp", 'SomaVoltage', 'h', 'hinf', 'htau', 'g']
    ax = []
    for i in range(len(variables)):
        t = [f.add_subplot(len(variables), 2, i*2+1), f.add_subplot(len(variables), 2, i*2+2)]
        ax.append(t)




    colors = 'rgbcmykrgbcmyk'
    view_min, view_max = [None]*len(variables), [None]*len(variables)







    #v_levels = [-80, -40, -20, 20]
    v_levels = [-80, -40, -20, 20]
    min_max_window = (600, 650)*units.ms
    for i, v in enumerate(v_levels):
        #if i> 2:
        #    continue
        res = testfile_voltage(xmlfile, qty("%d:mV"%v))

        for j, v in enumerate(variables):
            print 'Var', v
            trXSL = res[SimMode.XSL].get_trace(v)
            trNUnits = res[SimMode.NeuroUnit].get_trace(v)

            trXSLMin = trXSL.window(min_max_window).mean()
            if not view_min[j] or view_min[j] > trXSLMin:
                view_min[j] = trXSLMin
            if not view_max[j] or view_max[j] < trXSLMin:
                view_max[j] = trXSLMin
            trNUMin = trNUnits.window(min_max_window).mean()
            if not view_min[j] or view_min[j] > trNUMin:
                view_min[j] = trNUMin
            if not view_max[j] or view_max[j] < trNUMin:
                view_max[j] = trNUMin

            l = ax[j][0].plotTrace(trXSL, color=colors[i])
            ax[j][0].plotTrace(trNUnits, color=l[0].get_color(), linewidth=10 , alpha=0.2)

            l = ax[j][1].plotTrace(trXSL, color=colors[i])
            ax[j][1].plotTrace(trNUnits, color=l[0].get_color(), linewidth=10 , alpha=0.2)


    for j in range(len(variables)):
        rRange = view_max[j] - view_min[j]
        ax[j][0].set_ylim((view_min[j]-0.1*rRange, view_max[j]+0.1*rRange))
        ax[j][1].set_ylim((view_min[j]-0.1*rRange, view_max[j]+0.1*rRange))

        #ax[j][0].set_xlim((190, 250) * units.ms)
        #ax[j][1].set_xlim((100, 700) * units.ms )


    root_dir = "/home/michael/Desktop/fOut/"

    LocMgr.ensure_dir_exists(root_dir)
    fName = root_dir + "_".join(xmlfile.split("/")[-3:])
    import pylab
    pylab.savefig(fName + ".svg" )
    print fName
    #assert False




v_invest = "h"




def testfile_voltage(xmlfile, voltage):

    #  via the neurounits bridge:
    chl_neuro = NeuroML_Via_NeuroUnits_ChannelNEURON(xml_filename=xmlfile,  )
    def applicator_neuro(env, cell, sim):

        cell.apply_channel( chl_neuro)
        sim.record(chl_neuro, what= 'h', cell_location=cell.soma,   name="h")
        sim.record(chl_neuro,  what='h_inf', cell_location=cell.soma,   name="hinf")
        sim.record(chl_neuro, what = 'h_tau', cell_location=cell.soma,   name="htau")
        sim.record(chl_neuro, what= 'g', cell_location=cell.soma,  name="g")
        return chl_neuro

    # via xsl transformation:
    xsl_file = "/home/michael/srcs/neuroml/CommandLineUtils/ChannelMLConverter/ChannelML_v1.8.1_NEURONmod.xsl"
    chl_xsl = NeuroML_Via_XSL_ChannelNEURON(xml_filename=xmlfile, xsl_filename=xsl_file,  )
    def applicator_xsl(env, cell, sim):

        cell.apply_channel( chl_xsl)
        sim.record(chl_xsl,  what='h', cell_location=cell.soma, nrn_unit=qty(""),  name="h")
        sim.record(chl_xsl ,  what='hinf', cell_location=cell.soma, nrn_unit=qty(""),  name="hinf")
        sim.record(chl_xsl,  what='htau', cell_location=cell.soma, nrn_unit=qty("ms"),  name="htau")
        sim.record(chl_xsl, what='gion', cell_location=cell.soma, nrn_unit=qty("S/cm2"),  name="g")
        return chl_xsl

    import os
    os.system("cp %s /home/michael/mftmp/"%xmlfile)

    resA = simulate_chls_on_neuron(applicator_xsl, voltage_level=voltage, simtype="_XSL")
    resB = simulate_chls_on_neuron(applicator_neuro, voltage_level=voltage, simtype="_NeuroUnit")


    return {
            SimMode.XSL:resA,
            SimMode.NeuroUnit:resB,
            }





i=0

ok = []
fail1 = []
fail2 = []
fail3 = []





for xmlfile in NeuroMLDataLibrary.get_channelMLV1FilesWithSingleChannel():



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


        except NeuroUnitsImportNeuroMLNotImplementedException:
            fail1.append(xmlfile)


        except NotImplementedError:
            fail2.append(xmlfile)


        except Exception, e:
            print xmlfile
            fail3.append((xmlfile, e))
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
for chl, prob in fail3:

    print chl
    print "-", prob




















