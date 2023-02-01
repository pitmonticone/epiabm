#
# Sweeps for taking care of the interventions
#

from pyEpiabm.core import Parameters
from pyEpiabm.intervention import CaseIsolation
from pyEpiabm.intervention import PlaceClosure
from pyEpiabm.intervention import HouseholdQuarantine
from .abstract_sweep import AbstractSweep


class InterventionSweep(AbstractSweep):
    """Class to sweep through all possible interventions.
    Check if intervention should take place based on time (and/or threshold).

    Possible interventions:

            * `case_isolation`: Symptomatic case stays home.
            * `household quarantine`: Household quarantine if member
                                      is symptomatic
    """

    def __init__(self):
        """Call in variables from the parameters file and set flags.
        """
        self.interventions = []
        self.intervention_params = Parameters.instance().intervention_params

    def bind_population(self, population):
        self._population = population
        for intervention in self.intervention_params.keys():
            params = self.intervention_params[intervention]
            if intervention == 'case_isolation':
                self.interventions.append(CaseIsolation(
                    start_time=params['time_start'],
                    policy_duration=params['policy_duration'],
                    case_threshold=params['case_threshold'],
                    isolation_delay=params['isolation_delay'],
                    isolation_duration=params['isolation_duration'],
                    isolation_probability=params['isolation_probability'],
                    isolation_effectiveness=params['isolation_effectiveness'],
                    isolation_house_effectiveness=params['isolation_house_'
                                                         'effectiveness'],
                    population=self._population
                ))
            elif intervention == 'place_closure':
                self.interventions.append(PlaceClosure(
                    start_time=params['time_start'],
                    policy_duration=params['policy_duration'],
                    case_threshold=params['case_threshold'],
                    closure_delay=params['closure_delay'],
                    closure_duration=params['closure_duration'],
                    closure_household_infectiousness=params
                    ['closure_household_infectiousness'],
                    closure_spatial_params=params['closure_spatial_params'],
                    icu_microcell_threshold=params['icu_microcell_threshold'],
                    case_microcell_threshold=params['case_microcell_'
                                                    'threshold'],
                    population=self._population
                ))
            elif intervention == 'household_quarantine':
                self.interventions.append(HouseholdQuarantine(
                    start_time=params['time_start'],
                    policy_duration=params['policy_duration'],
                    case_threshold=params['case_threshold'],
                    quarantine_delay=params['quarantine_delay'],
                    quarantine_duration=params['quarantine_duration'],
                    quarantine_house_compliant=params['quarantine_house_'
                                                      'compliant'],
                    quarantine_individual_compliant=params['quarantine_'
                                                           'individual_'
                                                           'compliant'],
                    quarantine_house_effectiveness=params['quarantine_'
                                                          'house_'
                                                          'effectiveness'],
                    quarantine_spatial_effectiveness=params['quarantine_'
                                                            'spatial_'
                                                            'effectiveness'],
                    quarantine_place_effectiveness=params['quarantine_'
                                                          'place_'
                                                          'effectiveness'],
                    population=self._population
                ))

    def __call__(self, time):
        """
        Perform interventions that should take place.

        Parameters
        ----------
        time : float
            Simulation time
        """
        for intervention in self.interventions:
            # TODO:
            # - Include an alternative way of case-count.
            #   Idealy this will be a global parameter that we can plot
            # - Include condition on ICU
            #   Intervention will be activated based on time and cases now.
            #   We would like to implement a threshold based on ICU numbers.
            num_cases = 0
            for cell in self._population.cells:
                for person in cell.persons:
                    if person.is_infectious():
                        num_cases += 1
            if intervention.is_active(time, num_cases):
                intervention(time)
