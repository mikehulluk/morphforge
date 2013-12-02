



from morphforgecontrib.stdimports import SynapticTriggerAtTimes
from morphforgecontrib.stdimports import SynapticTriggerByVoltageThreshold


from morphforgecontrib.simulation.synapse_templates.neurounit import *
from morphforgecontrib.simulation.synapse_templates.exponential_form.expsyn.core import *
from morphforgecontrib.simulation.synapse_templates.exponential_form.exp2syn.core import *
from morphforgecontrib.simulation.synapse_templates.exponential_form.exp2synnmda.core import *


from morphforge.stdimports import *
#from morphforgecontrib.simulation.channels.simulatorbuiltin.sim_builtin_core import BuiltinChannel
from morphforgecontrib.data_library.stdmodels import StandardModels


def simulate_chls_on_neuron():


    # Create the environment:
    env = NEURONEnvironment()
    sim = env.Simulation()

    # Create a cell:
    cell1 = CellLibrary.create_cell(celltype=None, modelsrc=StandardModels.HH52, sim=sim)
    cell2 = CellLibrary.create_cell(celltype=None, modelsrc=StandardModels.HH52, sim=sim)


    exp2template = env.PostSynapticMechTemplate(
        PostSynapticMech_Exp2SynNMDA_Base,
        template_name='expsyn2tmpl',
        tau_open = 5 * units.ms, tau_close=20*units.ms, e_rev=0 * units.mV, popening=1.0, peak_conductance = qty("1:nS"),  vdep=False,
        )



    syn = sim.create_synapse(
            trigger = env.SynapticTrigger(
                                     SynapticTriggerAtTimes,
                                     time_list =   (100,105,110,112,115, 115,115) * units.ms ,
                                     ),
            postsynaptic_mech = exp2template.instantiate(cell_location = cell1.soma, ),
           )

    syn = sim.create_synapse(
            trigger = env.SynapticTrigger(
                                     SynapticTriggerByVoltageThreshold,
                                     cell_location=cell1.soma,
                                     voltage_threshold=qty("0:mV"),
                                     delay=qty('1:ms'),
                                     ),
            postsynaptic_mech = exp2template.instantiate(cell_location = cell2.soma, ),
           )




    # Define what to record:
    sim.record(what=StandardTags.Voltage, name="SomaVoltage1", cell_location = cell1.soma)
    sim.record(what=StandardTags.Voltage, name="SomaVoltage2", cell_location = cell2.soma)


    # run the simulation
    results = sim.run()
    return results


results = simulate_chls_on_neuron()
SimulationMRedoc.build( results ).to_pdf(__file__ + '.pdf')

TagViewer(results, timerange=(95, 200)*units.ms, show=True)

