from morphforge.componentlibraries.channellibrary import ChannelLibrary
from morphforge.core.quantities.fromcore import unit
from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmleak import MM_LeakChannel
from morphforgecontrib.simulation.membranemechanisms.hh_style.core.mmalphabeta import MM_AlphaBetaChannel
from morphforgecontrib.data_library.stdmodels import StandardModels



def get_sample_lk(env):
    lkChannels = env.MembraneMechanism(
                         MM_LeakChannel,
                         name="LkChl",
                         conductance=unit("0.3:mS/cm2"),
                         reversalpotential=unit("-54.3:mV"),
                         mechanism_id = 'HULL12_DIN_LK_ID'
                        )
    return lkChannels


def get_sample_na(env):
    naStateVars = { "m": {
                          "alpha":[-4.00,-0.10,-1.00,40.00,-10.00],
                          "beta": [ 4.00, 0.00, 0.00,65.00, 18.00]},
                        "h": {
                            "alpha":[0.07,0.00,0.00,65.00,20.00] ,
                            "beta": [1.00,0.00,1.00,35.00,-10.00]}
                      }

    naChannels = env.MembraneMechanism(
                            MM_AlphaBetaChannel,
                            name="NaChl", ion="na",
                            equation="m*m*m*h",
                            conductance=unit("120:mS/cm2"),
                            reversalpotential=unit("50:mV"),
                            statevars=naStateVars,
                            mechanism_id="HH_NA_CURRENT"
                            )
    return naChannels


def get_sample_k(env):
    kStateVars = { "n": { "alpha":[-0.55,-0.01,-1.0,55.0,-10.0],
                          "beta": [0.125,0,0,65,80]},
                       }
    kChannels = env.MembraneMechanism(
                            MM_AlphaBetaChannel,
                            name="KChl", ion="k",
                            equation="n*n*n*n",
                            conductance=unit("36:mS/cm2"),
                            reversalpotential=unit("-77:mV"),
                            statevars=kStateVars,
                            mechanism_id="HH_K_CURRENT"
                            )
    return kChannels




ChannelLibrary.register_channel(modelsrc=StandardModels.HH52,  channeltype="Na", chl_functor=get_sample_na)
ChannelLibrary.register_channel(modelsrc=StandardModels.HH52,  channeltype="K",  chl_functor=get_sample_k)
ChannelLibrary.register_channel(modelsrc=StandardModels.HH52,  channeltype="Lk", chl_functor=get_sample_lk)


