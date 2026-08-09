#include "compute/add_two.hpp"

// Ignore warnings caused by Boost.Test macros.
// NOLINTBEGIN(misc-use-internal-linkage, readability-identifier-length, cppcoreguidelines-avoid-do-while, cppcoreguidelines-pro-type-vararg, hicpp-vararg)

// This define is needed once per executable (which here is every cpp file).
#define BOOST_TEST_MODULE test_add_two_2
#include <boost/test/unit_test.hpp>

BOOST_AUTO_TEST_CASE(AddTwo)
{
    const compute::AddTwo add_two;
    BOOST_TEST(add_two(70) == 72);
}

// NOLINTEND(misc-use-internal-linkage, readability-identifier-length, cppcoreguidelines-avoid-do-while, cppcoreguidelines-pro-type-vararg, hicpp-vararg)

