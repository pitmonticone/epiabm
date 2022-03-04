import unittest
import pyEpiabm as pe
from pyEpiabm.property.infection_status import InfectionStatus

from pyEpiabm.utility import StateTransitionMatrix
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal


class TestStateTransitionMatrix(unittest.TestCase):
    """Test the 'StateTransitionMatrix' class.
    """
    def test_build_initial_matrix(self):
        """Tests the build_state_transition_matrix method by asserting if it is
        equal to the initial matrix expected.
        """
        matrix_object = StateTransitionMatrix()
        matrix = matrix_object.build_state_transition_matrix()
        labels = [status.name for status in InfectionStatus]
        zero_filled_dataframe = pd.DataFrame(np.zeros((10, 10)),
                                             columns=labels, index=labels)
        assert_frame_equal(matrix, zero_filled_dataframe)

    def test_fill_state_transition_matrix(self):
        """Tests the fill_state_transition_matrix method and asserts that each row
        sums to 1 (ie that the transition probabilities for each current
        infection status sum to 1).
        """
        matrix_object = StateTransitionMatrix()
        matrix = matrix_object.build_state_transition_matrix()
        filled_matrix = matrix_object.fill_state_transition_matrix(matrix)
        filled_matrix['sum'] = filled_matrix.sum(axis=1)
        for i in filled_matrix['sum']:
            self.assertAlmostEqual(i, 1)

    def test_update_probability(self):

        # Test method updates probability as expected
        back_up_matrix = \
            pe.Parameters.instance().state_transition_matrix.copy()
        matrix_object = StateTransitionMatrix()
        row_status = InfectionStatus.Susceptible
        column_status = InfectionStatus.Exposed
        new_probability = 0.5
        matrix_object.update_probability(row_status,
                                         column_status, new_probability)
        self.assertEqual(0.5,
                         pe.Parameters.instance().
                         state_transition_matrix.loc['Susceptible', 'Exposed'])

        pe.Parameters.instance().state_transition_matrix = back_up_matrix

        # Test error for incorrect columns is raised
        with self.assertRaises(ValueError):
            row = ''
            column = ''
            matrix_object.update_probability(row, column, 0.5)

        # Test error for incorrect probability is raised
        with self.assertRaises(ValueError):
            row = InfectionStatus.Susceptible
            column = InfectionStatus.Susceptible
            matrix_object.update_probability(row, column, 10.0)


if __name__ == '__main__':
    unittest.main()
