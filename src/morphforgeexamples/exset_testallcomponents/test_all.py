
from morphforge.stdimports import *
from morphforgecontrib.stdimports import *





def test_channels():
    #for every type of channel, lets make a cell with channel and some leak:
    for key,chlfunctor in ChannelLibrary._channels.items():

        def my_new_cell(sim):
            cell = CellLibrary.create_cell(
                    sim=sim,
                    modelsrc=StandardModels.SingleCompartmentPassive,
                    input_resistance=300*units.MOhm)
            
            chl = chlfunctor(env=env)
            cell.apply_channel(chl)
            return cell
        CellLibrary.register(celltype='%s'%str(key), modelsrc='None', cell_functor=my_new_cell)
        




    cell_sucesses = []
    cell_failures = []
    for key, cellfunctor in sorted(CellLibrary._cells.items()):
        
        try:
            # Record everything that we can!
            env = NEURONEnvironment()
            sim = env.Simulation(tstop=400*units.ms)
            cell = CellLibrary.create_cell(sim=sim, modelsrc=key[0], celltype=key[1])
            for chl in cell.get_biophysics().get_all_channels_applied_to_cell():
                chl.record_all(sim=sim, cell_location=cell.soma)

            res = sim.run()    
            cell_sucesses.append( (key,res) )
            
        except Exception, e:
            print 'Error running:', key
            print e
            cell_failures.append( (key, str(e) ) )

    return cell_sucesses, cell_failures








chl_sucesses, chl_failures = test_channels()
import mredoc as mrd
res_doc = mrd.Section('Simulation Results',
            mrd.SectionNewPage("Channels",
                mrd.Section('Sucesses', mrd.Table(["Key"], [ c[0] for c in chl_sucesses] ) ),
                mrd.Section('Failures', mrd.Table(["Key", 'Msg'], [(c[0],str(c[1])) for c in chl_failures] ) ),

                mrd.Section('Sucess Details',
                    [ SimulationMRedoc.build(r[1]) for r in chl_sucesses ]
                    ),
            )
)

    
res_doc.to_html("output")

