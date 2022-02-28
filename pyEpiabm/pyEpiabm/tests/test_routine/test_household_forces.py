import unittest

import pyEpiabm as pe
from pyEpiabm.routine import HouseholdInfection


class TestHouseholdInfection(unittest.TestCase):
    """Test the 'HouseholdInfection' class, which contains the
    infectiousness and susceptibility calculations that
    determine whether infection events occur within households.
    Each function should return a number greater than 0.
    """
    @classmethod
    def setUpClass(cls) -> None:
        """Intialise a population with one infector and one
        infectee, both in the same place and household.
        """
        cls.cell = pe.Cell()
        cls.microcell = pe.Microcell(cls.cell)
        cls.infector = pe.Person(cls.microcell)
        cls.infectee = pe.Person(cls.microcell)
        cls.timestep = 1

    def test_house_inf(self):
        result = HouseholdInfection.household_inf(self.infector, self.timestep)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    def test_house_susc(self):
        result = HouseholdInfection.household_susc(self.infector,
                                                   self.infectee,
                                                   self.timestep)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    def test_house_inf_force(self):
        result = HouseholdInfection.household_foi(self.infector,
                                                  self.infectee,
                                                  self.timestep)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)


if __name__ == '__main__':
    unittest.main()