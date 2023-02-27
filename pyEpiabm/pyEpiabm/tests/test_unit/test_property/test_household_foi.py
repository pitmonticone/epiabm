import unittest

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
        cls.time = 1
        cls._population = pe.Population()
        cls._population.add_cells(1)
        cls._population.cells[0].add_microcells(1)
        cls._population.cells[0].microcells[0].add_people(2)
        for person in cls._population.cells[0].microcells[0].persons:
            person.infectiousness = 1.0
        cls.infector = cls._population.cells[0].microcells[0].persons[0]
        cls.infectee = cls._population.cells[0].microcells[0].persons[1]

    def test_house_inf(self):
        result = HouseholdInfection.household_inf(self.infector, self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    def test_house_susc(self):
        result = HouseholdInfection.household_susc(
            self.infector, self.infectee, self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    def test_house_inf_force(self):
        result = HouseholdInfection.household_foi(
            self.infector, self.infectee, self.time)
        self.assertTrue(result > 0)
        self.assertIsInstance(result, float)

    def test_house_case_isolation(self):
        # Not isolating (isolation_start_time = None)
        result = HouseholdInfection.household_foi(
            self.infector, self.infectee, self.time)

        # Case isolate
        isolation_house_effectiveness = \
            pe.Parameters.instance().intervention_params[
                'case_isolation']['isolation_house_effectiveness']
        self.infector.isolation_start_time = 1
        result_isolating = HouseholdInfection.household_foi(self.infector,
                                                            self.infectee,
                                                            self.time)
        self.assertEqual(result*isolation_house_effectiveness,
                         result_isolating)

    def test_house_place_closure(self):
        # No place closure (closure_start_time = None)
        result = HouseholdInfection.household_inf(
            self.infector, self.time)

        # Place closure
        closure_household_infectiousness = \
            pe.Parameters.instance().intervention_params[
                'place_closure']['closure_household_infectiousness']
        self.infector.microcell.closure_start_time = 1
        result_closure = HouseholdInfection.household_inf(
            self.infector, self.time)
        self.assertEqual(result*closure_household_infectiousness,
                         result_closure)

    def test_house_household_quarantine(self):
        # Not in quarantine (quarantine_start_time = None)
        result = HouseholdInfection.household_foi(
            self.infector, self.infectee, self.time)

        # Household quarantine
        quarantine_house_effectiveness = \
            pe.Parameters.instance().intervention_params[
                'household_quarantine']['quarantine_house_effectiveness']
        self.infector.quarantine_start_time = 1
        result_isolating = HouseholdInfection.household_foi(self.infector,
                                                            self.infectee,
                                                            self.time)
        self.assertEqual(result*quarantine_house_effectiveness,
                         result_isolating)

    def test_house_social_distancing(self):
        # Not in social distancing (distancing_start_time = None)
        result = HouseholdInfection.household_susc(
            self.infector, self.infectee, self.time)

        # Normal social distancing
        self.infector.microcell.distancing_start_time = 1
        self.infector.distancing_enhanced = False
        distancing_house_susc = pe.Parameters.instance().\
            intervention_params['social_distancing'][
                'distancing_house_susc']
        result_distancing = HouseholdInfection.household_susc(
            self.infector, self.infectee, self.time)
        self.assertEqual(result*distancing_house_susc,
                         result_distancing)

        # Enhanced social distancing
        self.infector.distancing_enhanced = True
        distancing_house_enhanced_susc = pe.Parameters.instance().\
            intervention_params['social_distancing'][
                'distancing_house_enhanced_susc']
        result_distancing_enhanced = HouseholdInfection.household_susc(
            self.infector, self.infectee, self.time)
        self.assertEqual(result*distancing_house_enhanced_susc,
                         result_distancing_enhanced)


if __name__ == '__main__':
    unittest.main()
