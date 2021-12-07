import unittest
import pyEpiabm as pe
from queue import Queue
from unittest import mock


class TestPlaceSweep(unittest.TestCase):
    """Test the 'PlaceSweep' class.
    """

    @classmethod
    def setUpClass(cls) -> None:
        ''' Initialises a population with one infected person. Sets up a
        single household containing this person.
        '''
        cls.pop = pe.Population()
        cls.pop.add_cells(1)
        cls.cell = cls.pop.cells[0]
        cls.pop.cells[0].add_microcells(1)
        cls.microcell = cls.cell.microcells[0]
        cls.pop.cells[0].microcells[0].add_people(1)
        cls.person = cls.pop.cells[0].microcells[0].persons[0]
        cls.person.infection_status = pe.InfectionStatus.InfectMild
        cls.microcell.add_place(1, (1, 1), pe.PlaceType.Hotel)
        cls.place = cls.cell.places[0]
        cls.place.add_person(cls.person)
        pe.Parameters.instance().time_steps_per_day = 1

    @mock.patch('pyEpiabm.CovidsimHelpers.calc_house_susc')
    @mock.patch('pyEpiabm.CovidsimHelpers.calc_house_inf')
    def test__call__(self, mock_inf, mock_susc):
        '''
        Test whether the household sweep function correctly
        adds persons to the queue.
        '''
        mock_inf.return_value = 10
        mock_susc.return_value = 10
        subject = pe.PlaceSweep()
        time = 1

        # Assert a population with one infected will not change the queue
        subject(time, self.pop)
        assert(self.cell.person_queue.empty())

        # Change person's status to recovered
        self.person.infection_status = pe.InfectionStatus.Recovered
        subject(time, self.pop)
        assert(self.cell.person_queue.empty())

        # Add one susceptible to the population, with the mocked infectiousness
        # ensuring they are added to the infected queue.
        self.person.infection_status = pe.InfectionStatus.InfectMild
        test_queue = Queue()
        new_person = pe.Person(self.microcell)
        self.place.persons.append(new_person)
        self.pop.cells[0].persons.append(new_person)

        test_queue.put(new_person)
        subject(time, self.pop)
        self.assertEqual(self.cell.person_queue.qsize(), 1)

        # Change the additional person to recovered, and assert the queue
        # is empty.
        new_person.infection_status = pe.InfectionStatus.Recovered
        self.cell.persons.append(new_person)
        self.cell.person_queue = Queue()
        subject(time, self.pop)
        assert(self.cell.person_queue.empty())


if __name__ == '__main__':
    unittest.main()
