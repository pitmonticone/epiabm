#ifndef _COVIDSIM_FACTORY_HPP
#define _COVIDSIM_FACTORY_HPP

#include "dataclasses/population.hpp"
#include "dataclasses/cell.hpp"
#include "dataclasses/microcell.hpp"
#include "dataclasses/place.hpp"
#include "dataclasses/person.hpp"

#include <iostream>

namespace seir
{

    class Factory
    {
    private:
    public:
        PopulationPtr makePopulation();
        void addCell(PopulationPtr population);
        void addMicrocell(CellPtr cell);
        void addPerson(MicrocellPtr microcell);

        void addCells(PopulationPtr population, int n);
        void addMicrocells(CellPtr cell, int n);
        void addPeople(MicrocellPtr microcell, int n);

        void print() { std::cout << "Hello World!" << std::endl; }
        
    private:
    };

} // namespace seir

#endif // _COVIDSIM_FACTORY_HPP
