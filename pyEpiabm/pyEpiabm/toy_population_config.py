import numpy as np
from .population import Population
from .household import Household


class ToyPopulation:
    """ Class that creates a toy population for use and returns in the simple
    python model.
    """
    def make_pop(self, population_size: int, cell_number: int,
                 microcell_per_cell: int, household_number: int,
                 if_households: bool = False):
        """Method that initializes a population class with a given population size,
        number of cells and number of microcells. A multinomial distribution is
        used to distribute the number of people into the different microcells.
        There is also an option to distribute people into households.

        : param pop_size: Total number of people in population.
        : type pop_size: int
        : param cell_number: Number of cell objects the population will be
          split in to.
        : type cell_number: int
        : param microcell_per_cell: Number of microcell objects per cell.
        : type microcell_per_cell: int
        : param household_number: Number of households per microcell.
        : type household_number: int
        : param if_households: decides whether to put people into households.
        : type if_households: bool

        : return new_pop: Population
        : rtype new_pop: `Population` class object
        """
        # Initialise a population class
        new_pop = Population()

        # Checks parameter type and stores as class objects
        if not (type(if_households) == bool):
            raise TypeError('Include household input needs to be boolean')
        self.pop_size = population_size
        self.total_number_microcells = cell_number*microcell_per_cell
        self.if_households = if_households
        self.household_number = household_number

        new_pop.add_cells(cell_number)
        # Sets up a probability array for the multinomial
        p = [1/self.total_number_microcells]*self.total_number_microcells
        # Distributes multinomially people into microcells
        cell_split = np.random.multinomial(population_size, p, size=1)[0]
        i = 0
        for cell in new_pop.cells:
            cell.add_microcells(microcell_per_cell)
            for microcell in cell.microcells:
                people_in_microcell = cell_split[i]
                microcell.add_people(people_in_microcell)
                i += 1

        # Splits people into households, either with a given number of
        # housholds per cell, or trivially (each person gets their own
        # household).
        if if_households:
            self.add_households(new_pop)
        else:
            self.no_households(new_pop)

        return new_pop

    def add_households(self, population: Population):
        """Method that groups people in microcell into households together.
        """
        # Initialises another multinomial distribution
        q = [1/self.household_number]*self.household_number
        for cell in population.cells:
            for microcell in cell.microcells:
                people_number = len(microcell.persons)
                household_split = np.random.multinomial(people_number, q,
                                                        size=1)[0]
                person_index = 0
                for j in range(self.household_number):
                    people_in_household = household_split[j]
                    new_household = Household()
                    for _ in range(people_in_household):
                        person = microcell.persons[person_index]
                        new_household.add_person(person)
                        person_index += 1

    def no_households(self, population: Population):
        """Method assigns each person to their own individual household.
        This means that household sweep will run trivially instead of
        throwing an error.
        """
        for cells in population.cells:
            for person in cells.persons:
                new_household = Household()
                new_household.add_person(person)
