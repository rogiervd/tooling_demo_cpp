// SPDX-FileCopyrightText: Copyright 2026 Rogier van Dalen
//
// SPDX-License-Identifier: Apache-2.0

#include "tooling_demo_cpp/add_two.hpp"

#include <boost/rational.hpp>

namespace tooling_demo_cpp {

int AddTwo::operator()(int value) const
{
    int const numerator = 10;
    int const denominator = 5;
    boost::rational<int> const fraction(numerator, denominator);
    return value + fraction.numerator();
}

}  // namespace tooling_demo_cpp
