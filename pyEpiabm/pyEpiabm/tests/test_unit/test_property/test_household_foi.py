import unittest
from unittest.mock import patch

import pyEpiabm as pe
from pyEpiabm.property import HouseholdInfection
from pyEpiabm.tests.test_unit.parameter_config_tests import TestPyEpiabm


class TestHouseholdInfection(TestPyEpiabm):
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
        super(TestHouseholdInfection, cls).setUpClass()  # Sets up parameters
        cls.cell = pe.Cell()
        cls.microcell = pe.Microcell(cls.cell)
        cls.infector = pe.Person(cls.microcell)
        cls.infector.infectiousness = 1.0
        cls.infector.date_vaccinated = 0
        cls.infectee = pe.Person(cls.microcell)
        cls.infectee.date_vaccinated = 0
        cls.infectee.is_vaccinated = True
        cls.infector.is_vaccinated = True
        cls.time = 1

    def test_house_inf(self):
        result = HouseholdInfection.household_inf(self.infector, self.time)
        self.assertEqual(result, 1)
        self.assertIsInstance(result, float)

    def test_house_susc(self):
        result = HouseholdInfection.household_susc(self.infector,
                                                   self.infectee,
                                                   self.time)
        self.assertEqual(result, 1.0)
        self.assertIsInstance(result, float)

    def test_house_inf_force(self):
        result = HouseholdInfection.household_foi(self.infector,
                                                  self.infectee,
                                                  self.time)
                    
        self.assertEqual(result, 0.05)
        # expected value based on infectiousness(1) * susceptibiliy (1) *
        # vaccine infectiouness drop (0.5) * household transmission (0.1)
        self.assertIsInstance(result, float)

    @patch('pyEpiabm.property.HouseholdInfection.household_susc')
    @patch('pyEpiabm.property.HouseholdInfection.household_inf')
    @patch('pyEpiabm.core.Parameters.instance')
    def test_carehome_scaling(self, mock_params, mock_inf, mock_susc):
        mock_inf.return_value = 1
        mock_susc.return_value = 1
        mock_params.return_value.carehome_params\
            = {'carehome_resident_household_scaling': 2}
        mock_params.return_value.household_transmission = 1
        mock_params.return_value.false_positive_rate = 0
        mock_params.return_value.intervention_params\
            = {"vaccine_params": {'vacc_inf_drop': 0,
                                  'time_to_efficacy': 0}}
        self.infector.care_home_resident = True
        self.infectee.care_home_resident = False
        result = HouseholdInfection.household_foi(self.infector,
                                                  self.infectee,
                                                  self.time)
        self.assertEqual(result, 2)

        self.infector.care_home_resident = False
        self.infectee.care_home_resident = True
        result = HouseholdInfection.household_foi(self.infector,
                                                  self.infectee,
                                                  self.time)
        self.assertEqual(result, 2)

        self.infector.care_home_resident = True
        self.infectee.care_home_resident = True
        result = HouseholdInfection.household_foi(self.infector,
                                                  self.infectee,
                                                  self.time)
        self.assertEqual(result, 4)

        self.assertEqual(mock_inf.call_count, 3)
        self.assertEqual(mock_susc.call_count, 3)


if __name__ == '__main__':
    unittest.main()
