#
# Mirocell Class
#
from .person import Person
from .place import Place
import typing


class Microcell:
    """Class representing a Microcell (Group of people and places).
    Collection of :class:`Person` s

    :param cell: An instance of :class:`Cell`
    :type cell: Cell
    """
    def __init__(self, cell):
        """Constructor Method.

        :param cell: Microcell's parent :class:`Cell` instance.
        :type cell: Cell
        """
        self.persons = []
        self.places = []
        self.cell = cell

    def __repr__(self):
        """String representation of Microcell.

        :return: String representation of Microcell
        :rtype: str
        """
        return f"Microcell with {len(self.persons)} people"

    def add_people(self, n):
        """Adds n default :class:`Person` to Microcell.

        :param n: Number of default :class:`Person` s to add
        :type n: int
        """
        for i in range(n):
            p = Person(self)
            self.cell.persons.append(p)
            self.persons.append(p)

    def add_place(self, n, loc: typing.Tuple[float, float],
                  place_type):
        """Adds n default :class:`Place` to Microcell.

        :param n: Number of default :class:`Place` s to add
        :type n: int
        """
        for i in range(n):
            p = Place(loc, place_type, self.cell, self)
            self.cell.places.append(p)
            self.places.append(p)
