#
# Place Class
#
from .person import Person
import typing
from .place_type import PlaceType


class Place:
    """Creates a place class which represents spaces such
    as cafes, restaurants and hotel where people may come
    into contact with others outside their household.
    """
    def __init__(self, loc: typing.Tuple[float, float],
                 place_type: PlaceType, cell, microcell):
        """Constructor method.

        :param loc: (x,y) coordinates of the place.
        :type loc: tuple
        :param place_type: categorises the place.
        :type place_type: 'PlaceType' enum
        :param cell: An instance of :class:`Cell`
        :type cell: Cell
        :param microcell: An instance of :class:`Microcell`
        :type microcell: Microcell
        """
        self._location = loc
        self.persons = []
        self.place_type = place_type
        self.max_capacity = 50
        self.susceptibility = 0
        self.infectiveness = 0

        self.cell = cell
        self.microcell = microcell
        if not (self.microcell.cell == self.cell):
            raise KeyError("Microcell is not contained in cell")

    def set_max_cap(self, max_capacity: int):
        """Sets the maximum capacity of a place.

        :param max_capacity: maximum number of people
            allowed inplace.
        :type max_capacity: int
        """
        self.max_capacity = max_capacity

    def set_infectiveness(self, infectiveness: float):
        """Sets a baseline infectiveness for the place.

        :param infectiveness: baseline infectiveness.
        :type infectiveness: float
        """
        self.infectiveness = infectiveness

    def set_susceptibility(self, susceptibility: float):
        """Sets a baseline susceptibility for the place.

        :param susceptibility: baseline susceptibility.
        :type susceptibility: float
        """
        self.susceptibility = susceptibility

    def add_person(self, person: Person):
        """Add people into the place.

        :param person: person to add.
        :type person: Person
        """
        self.persons.append(person)

    def remove_person(self, person: Person):
        """Remove people from place.

        :param person: Person to remove from place.
        :type person: Person
        """
        if person not in self.persons:
            raise KeyError("Person not found in this place")
        else:
            self.persons.remove(person)

    def empty_place(self):
        """Remove all people from place. For example
        a restaurant or park might regularly change
        all occupants each timestep.
        """
        while len(self.persons) > 0:
            self.remove_person(self.persons[0])
