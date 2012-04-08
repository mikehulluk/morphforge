from morphforge.simulation.core.biophysics.membranemechanism import MembraneMechanism


class BuiltinChannel(MembraneMechanism):
    def __init__(self,sim_chl_name, mechanism_id=None):
        MembraneMechanism.__init__(self, mechanism_id=mechanism_id)
        self.sim_chl_name = sim_chl_name
