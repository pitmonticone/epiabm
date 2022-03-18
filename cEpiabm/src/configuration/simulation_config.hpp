#ifndef EPIABM_CONFIGURATION_SIMULATION_CONFIGURATION_HPP
#define EPIABM_CONFIGURATION_SIMULATION_CONFIGURATION_HPP

#include "infection_config.hpp"

#include <memory>
#include <filesystem>

namespace epiabm
{

    class SimulationConfig
    {
    private:
    public:
        InfectionConfigPtr infectionConfig;

        unsigned short timestepsPerDay;

        SimulationConfig()
        {
            infectionConfig = std::make_shared<InfectionConfig>();
        }

    private:
    };

    typedef std::shared_ptr<SimulationConfig> SimulationConfigPtr;

} // epiabm

#endif // EPIABM_CONFIGURATION_SIMULATION_CONFIGURATION_HPP