#include "population.hpp"

#include <iostream>

namespace epiabm
{

    Population::Population() :
        m_cells()
    {}

    void Population::forEachCell(std::function<bool(Cell*)> callback)
    {
        for (size_t i = 0; i < m_cells.size(); i++)
        {
            if (!callback(&m_cells[i])) return;
        }
    }

    std::vector<Cell>& Population::cells() { return m_cells; }

    void Population::print()
    {
        std::cout << "Population with " << m_cells.size() << " Cells!" << std::endl;
    }

} // namespace epiabm
