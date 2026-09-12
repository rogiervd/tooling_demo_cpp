#include "tooling_demo_cpp/add_two.hpp"

#include <boost/rational.hpp>

namespace tooling_demo_cpp {

int AddTwo::operator()(int value) const
{
    const int numerator = 10;
    const int denominator = 5;
    const boost::rational<int> fraction(numerator, denominator);
    return value + fraction.numerator();
}

}  // namespace tooling_demo_cpp
