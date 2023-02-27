#
# Case isolation Class
#

import random

from pyEpiabm.intervention import AbstractIntervention


class CaseIsolation(AbstractIntervention):
    """Case isolation intervention
    Isolate symptomatic individual based on the isolation_probability
    and stop isolating isolated individuals after their isolation period.
    """

    def __init__(
        self,
        isolation_duration,
        isolation_probability,
        isolation_delay,
        population,
        **kwargs
    ):
        self.isolation_duration = isolation_duration
        self.isolation_delay = isolation_delay
        self.isolation_probability = isolation_probability

        super(CaseIsolation, self).__init__(population=population, **kwargs)

    def __call__(self, time):
        for cell in self._population.cells:
            for person in cell.persons:
                if person.isolation_start_time is not None:
                    if time > person.isolation_start_time + self.\
                              isolation_duration:
                        # Stop isolating people after their isolation period
                        person.isolation_start_time = None
                else:
                    if person.is_symptomatic():
                        r = random.random()
                        # Require symptomatic individuals to self-isolate
                        # with given probability
                        if r < self.isolation_probability:
                            person.isolation_start_time = time + self.\
                                                          isolation_delay

    def __turn_off__(self, time: float):
        for cell in self._population.cells:
            for person in cell.persons:
                if person.isolation_start_time is not None:
                    person.isolation_start_time = None
