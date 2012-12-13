 
from morphforgecontrib.simulation.populations import PopAnalSpiking
from morphforge.traces.tags import TagSelector


class AllSpikeFinderPostProcessor(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, result):
        spikes = PopAnalSpiking.evset_first_spike( res=result, **self.kwargs) 
        result.add_evset(spikes)


class FirstSpikeFinderPostProcessor(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, result):
        spikes = PopAnalSpiking.evset_all_spikes( res=result, **self.kwargs) 
        result.add_evset(spikes)

class AddEventSetPostProcessor(object):
    def __init__(self, evset):
        self.evset = evset

    def __call__(self, result):
        result.add_evset(self.evset)

