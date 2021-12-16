#include "dataclasses/person.hpp"
#include "dataclasses/cell.hpp"

#include "../catch/catch.hpp"

using namespace epiabm;

TEST_CASE("dataclasses/person: test initialize person", "[Person]")
{
    Person subject = Person(0,5, 10);
    REQUIRE(subject.cellPos() == 5);
    REQUIRE(subject.microcellPos() == 10);
    REQUIRE(subject.microcell() == 0);
    REQUIRE_NOTHROW(subject.params());
    REQUIRE(subject.status() == InfectionStatus::Susceptible);
}

TEST_CASE("dataclasses/person: test status", "[Person]")
{
    Cell cell = Cell(0);
    cell.microcells().push_back(Microcell(0));
    cell.microcells()[0].people().push_back(0);
    cell.people().push_back(Person(0,0,0));
    Person& subject = cell.people()[0];
    REQUIRE(subject.status() == InfectionStatus::Susceptible);
    
    auto test = [&](InfectionStatus status)
    {
        subject.updateStatus(&cell, status, 0);
        REQUIRE(subject.status() == status);
    };
    test(InfectionStatus::Susceptible);
    test(InfectionStatus::Dead);
    test(InfectionStatus::Exposed);
    test(InfectionStatus::InfectGP);
    test(InfectionStatus::Recovered);
}

TEST_CASE("dataclasses/person: test setHousehold", "[Person]")
{
    Person subject = Person(0,0,0);
    size_t hh = static_cast<size_t>((std::rand() % 500) * 2);
    REQUIRE(subject.setHousehold(hh));
    REQUIRE(subject.setHousehold(
        static_cast<size_t>((std::rand()%500) * 2 + 1)) == false);
    REQUIRE(subject.household() == hh);
}
