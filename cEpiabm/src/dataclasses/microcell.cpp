
#include "cell.hpp"
#include "microcell.hpp"

namespace epiabm
{

    Microcell::Microcell(size_t cellPos) :
        m_people(),
        m_places(),
        m_households(),
        m_cellPos(cellPos),
        m_compartmentCounter()
    {}

    Microcell::Microcell(const Microcell& other) :
        m_people(other.m_people),
        m_places(other.m_places),
        m_households(other.m_households),
        m_cellPos(other.m_cellPos)
    {}

    Microcell::Microcell(Microcell&& other) :
        m_people(std::move(other.m_people)),
        m_places(std::move(other.m_places)),
        m_households(std::move(other.m_households)),
        m_cellPos(std::move(other.m_cellPos))
    {}

    size_t Microcell::cellPos() const { return m_cellPos; }

    void Microcell::forEachPerson(Cell& cell, std::function<bool(Person*)> callback)
    {
        for (size_t i = 0; i < m_people.size(); i++)
        {
            if (!callback(&cell.m_people[m_people[i]])) return;
        }
    }

    void Microcell::forEachPlace(std::function<bool(Place*)> callback)
    {
        for (size_t i = 0; i < m_places.size(); i++)
        {
            if (!callback(m_places[i].get())) return;
        }
    }

    Person& Microcell::getPerson(Cell& cell, size_t i)
    {
        return cell.m_people[m_people[i]];
    }

    std::vector<size_t>& Microcell::people() { return m_people; }
    std::vector<PlacePtr>& Microcell::places() { return m_places; }
    std::vector<HouseholdPtr>& Microcell::households() { return m_households; }

    void Microcell::initialize(Cell* cell)
    {
        m_compartmentCounter.initialize(cell, m_people);
    }

    void Microcell::personStatusChange(Person* person, InfectionStatus newStatus, unsigned short /*timestep*/)
    {
        m_compartmentCounter.notify(person->status(), newStatus);
    }

} // namespace epiabm
