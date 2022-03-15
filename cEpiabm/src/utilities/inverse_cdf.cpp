#include "inverse_cdf.hpp"

#include <random>

namespace epiabm
{

    InverseCDF::InverseCDF() {}

    void InverseCDF::setNegLog(double startValue)
    {
        m_values[InverseCDF::RES] = startValue;
        for (size_t i = 0; i < InverseCDF::RES; i++)
        {
            m_values[i] = -log(1 - static_cast<double>(i) / InverseCDF::RES);
        }
    }

    void InverseCDF::assignExponent()
    {
        for (size_t i = 0; i < InverseCDF::RES; i++)
        {
            m_values[i] = exp(-m_values[i]);
        }
    }

    void InverseCDF::assignExponent(double value)
    {
        for (size_t i = 0; i < InverseCDF::RES; i++)
        {
            m_values[i] = exp(value);
        }
    }

    unsigned short InverseCDF::choose(double mean, double timestepsPerDay)
    {
        double q;
        size_t i = static_cast<size_t>(floor(q = static_cast<double>(std::rand())/static_cast<double>(RAND_MAX)*static_cast<double>(InverseCDF::RES)));
        q -= static_cast<double>(i);

        double ti = -mean * log(q * m_values[i+1] + (1-q)*m_values[i]);
        return static_cast<unsigned short>(floor(0.5 + (ti * timestepsPerDay)));
    }

    std::array<double, InverseCDF::RES+1>& InverseCDF::getValues()
    {
        return m_values;
    }

    double& InverseCDF::operator[](size_t i)
    {
        return m_values[i];
    }


} // namespace epiabm
