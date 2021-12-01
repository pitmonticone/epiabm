#
# Person Class
#
from .infection_status import InfectionStatus

class Person:
    """Class to represent each person in a population.

    :param microcell: An instance of an :class:`Microcell`.
    :type microcell: Microcell
    """

    def __init__(self, microcell,
                 age = 0, susceptibility = 0, infectiveness = 0):
        """Constructor Method.

        :param microcell: Person's parent :class:`Microcell` instance.
        :type microcell: Microcell
        """
        self.age = age
        self.susceptibility = susceptibility
        self.infectiveness = infectiveness
        self.microcell = microcell
        self.infection_status = InfectionStatus.Susceptible

    def __repr__(self):
        """String Representation of Person.

        :return: String representation of person
        :rtype: str
        """
        return f"Person, Age = {self.age}"
