#ifndef COMPUTE_ADD_TWO_HPP
#define COMPUTE_ADD_TWO_HPP

#include <boost/rational.hpp>

namespace compute {

class AddTwo
{
public:
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
