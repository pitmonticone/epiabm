#
# Case isolation Class
#

import random

from pyEpiabm.intervention import AbstractIntervention


class CaseIsolation(AbstractIntervention):
    """Case isolation intervention.
    Isolate symptomatic individual based on the isolation_probability
    and stop isolating isolated individuals after their isolation period
    or after the end of the policy.
    Detailed description of the implementation can be found in github wiki:
    https://github.com/SABS-R3-Epidemiology/epiabm/wiki/Interventions.
    """

    def __init__(
        self,
        isolation_duration,
        isolation_probability,
        isolation_delay,
        criterion,
        population,
        **kwargs
    ):
        self.isolation_duration = isolation_duration
        self.isolation_delay = isolation_delay
        self.isolation_probability = isolation_probability
        self.criterion = criterion

        super(CaseIsolation, self).__init__(population=population, **kwargs)

    def __call__(self, time):
        for cell in self._population.cells:
            for person in cell.persons:
                if (hasattr(person, 'isolation_start_time')) and (
                        person.isolation_start_time is not None):
                    if time > person.isolation_start_time + self.\
                              isolation_duration:
                        # Stop isolating people after their isolation period
                        person.isolation_start_time = None
                else:
                    if self.person_selection_method(person):
                        r = random.random()
                        # Require symptomatic individuals to self-isolate
                        # with given probability
                        if r < self.isolation_probability:
                            person.isolation_start_time = time + self.\
                                                          isolation_delay
                            if person.date_positive is not None:
                                self._population.test_isolate_count = [0, 0]
                                if person.is_symptomatic():
                                    self._population.test_isolate_count[0] += 1
                                else:
                                    self._population.test_isolate_count[1] += 1

    def person_selection_method(self, person):
        if self.criterion == 0:
            return person.is_symptomatic()
        else:
            if person.date_positive is not None:
                return True

    def turn_off(self):
        for cell in self._population.cells:
            for person in cell.persons:
                if (hasattr(person, 'isolation_start_time')) and (
                        person.isolation_start_time is not None):
                    person.isolation_start_time = None
