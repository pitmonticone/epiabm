#
# Infection due to contact within households
#

import random

from pyEpiabm.property import HouseholdInfection
from pyEpiabm.core import Person

from .abstract_sweep import AbstractSweep


class HouseholdSweep(AbstractSweep):
    """Class to run the intra-household infections
    as part of the sweep function. Takes an individual
    person as input and tests a infection event against each
    susceptible member of their household. The resulting
    exposed person is added to an infection queue.

    """
    def __call__(self, time: float):
        """Given a population structure, loops over infected members
        and considers whether they infected household members based
        on individual, and spatial infectiousness and susceptibility.

        Parameters
        ----------
        time : float
            Simulation time

        """
        # Double loop over the whole population, checking infectiousness
        # status, and whether they are absent from their household.
        for cell in self._population.cells:
            infectious_persons = filter(Person.is_infectious, cell.persons)
            for infector in infectious_persons:

                if infector.household is None:
                    raise AttributeError(f"{infector} is not part of a "
                                         + "household")

                # Loop over susceptible household members.
                for infectee in infector.household.susceptible_persons:

                    # Calculate "force of infection" parameter which will
                    # determine the likelihood of an infection event.
                    force_of_infection = HouseholdInfection.household_foi(
                        infector, infectee, time)

                    # Compare a uniform random number to the force of infection
                    # to see whether an infection event occurs in this timestep
                    # between the given persons.
                    r = random.uniform(0, 1)
                    if r < force_of_infection:
                        cell.enqueue_person(infectee)
