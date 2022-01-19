#
# Calculate household force of infection based on Covidsim code
#

from pyEpiabm.core import Person


class HouseholdForces:
    """Class to calculate the infectiousness and susceptibility
    parameters for the force of infection parameter, within households.
    """
    @staticmethod
    def household_inf(infector: Person, timestep: int):
        """Calculate the infectiveness of a household.

        :param infector: Infector
        :type infector: Person
        :param timestep: Current simulation timestep
        :type timestep: int
        :return: Infectiveness parameter of household
        :rtype: float
        """
        return 0.1

    @staticmethod
    def household_susc(infector: Person, infectee: Person, timestep: int):
        """Calculate the susceptibility of a household.

        :param infector: Infector
        :type infector: Person
        :param infectee: Infectee
        :type infectee: Person
        :param timestep: Current simulation timestep
        :type timestep: int
        :return: Susceptibility parameter of household
        :rtype: float
        """
        return 0.1

    @staticmethod
    def household_inf_force(infector: Person, infectee: Person, timestep: int):
        """Calculate the force of infector parameter of a household,
        for a particular infector and infectee.

        :param infector: Infector
        :type infector: Person
        :param infectee: Infectee
        :type infectee: Person
        :param timestep: Current simulation timestep
        :type timestep: int
        :return: Force of infection parameter of household
        :rtype: float
        """
        infectiousness = HouseholdForces.household_inf(infector, timestep)
        susceptibility = HouseholdForces.household_susc(infector, infectee,
                                                        timestep)
        return (infectiousness * susceptibility)
