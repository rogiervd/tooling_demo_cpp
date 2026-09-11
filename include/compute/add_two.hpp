#ifndef COMPUTE_ADD_TWO_HPP
#define COMPUTE_ADD_TWO_HPP

#include <boost/rational.hpp>

namespace compute {

/**
 * @brief A functor that adds two to an integer value.
 */
class AddTwo
{
public:
    /**
     * @brief Adds two to the given integer value.
     * @param value The integer value to which two will be added.
     * @return The result of adding two to the input value.
     */
    int operator()(int value) const
    {
        const int numerator = 10;
        const int denominator = 5;
        const boost::rational<int> fraction(numerator, denominator);
        return value + fraction.numerator();
    }
};


}  // namespace compute

#endif  // COMPUTE_ADD_TWO_HPP
