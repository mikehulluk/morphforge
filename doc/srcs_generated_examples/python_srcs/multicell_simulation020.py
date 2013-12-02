





import morphforge.stdimports as mf
import morphforgecontrib.stdimports as mfc
from morphforge.stdimports import units as U

# The simulation:
env = mf.NEURONEnvironment()
sim = env.Simulation(cvode=True)
cell1 = sim.create_cell(area=5000 * U.um2, initial_voltage=0*U.mV, name='Cell1')
lk_chl1 = env.Channel(mfc.StdChlLeak,
                conductance=0.66  * U.mS/U.cm2,
                reversalpotential=0*U.mV )

cell1.apply_channel(lk_chl1)
cell1.set_passive(mf.PassiveProperty.SpecificCapacitance, (1e-3) * U.uF / U.cm2)


cell2 = sim.create_cell(area=20000 * U.um2, initial_voltage=0*U.mV, name='Cell2')
lk_chl2 = env.Channel(mfc.StdChlLeak,
                conductance=0.01* U.mS/U.cm2,
                reversalpotential=0*U.mV
                )

cell2.apply_channel(lk_chl2)
cell2.set_passive(mf.PassiveProperty.SpecificCapacitance, (1e-3) * U.uF / U.cm2)

gj = sim.create_gapjunction(
    celllocation1 = cell1.soma,
    celllocation2 = cell2.soma,
    resistance = 100 * mf.units.MOhm
    )

cc = sim.create_currentclamp(cell_location=cell1.soma,
                        amp=200 * U.pA,
                        delay=100*U.ms,
                        dur=250*U.ms)



sim.record(cell1, what=mf.StandardTags.Voltage)
sim.record(cell2, what=mf.StandardTags.Voltage)
sim.record(cc, what=mf.StandardTags.Current)

res = sim.run()

# Create an output .pdf
mf.SimulationMRedoc.build( sim ).to_pdf(__file__ + '.pdf')

mf.TagViewer(res)


