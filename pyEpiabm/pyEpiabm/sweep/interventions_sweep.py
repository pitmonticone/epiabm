#
# Sweeps for taking care of the interventions
#

from pyEpiabm.core import Parameters, Person, Population
from pyEpiabm.intervention import CaseIsolation
from .abstract_sweep import AbstractSweep

class InterventionsSweep(AbstractSweep):
    """Class to sweep through all possible interventions. 
    Check if intervention should take place based on time (and/or threshold).
    Possible interventions:
    isolate_individual: Symptomatic case stays home.
    """

    def __init__(self):
        """Call in variables from the parameters file and set flags
        """
        self.interventions = []
        self.intervention_params = Parameters.instance().intervention_params  #{'case_isolation': [time_start, duration]}
        for intervention in self.intervention_params.keys():
            params = self.intervention_params[intervention]
            if intervention == 'case_isolation':
                self.interventions.append(CaseIsolation(*params, population=self._population))

    def __call__(self, time):
        """
        Perform interventions that should take place.

        Parameters
        ----------
        time : float
            Simulation time
        """
        for intervention in self.interventions:
            if intervention.is_active(time):
                intervention()
