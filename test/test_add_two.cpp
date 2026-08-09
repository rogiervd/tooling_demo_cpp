#include "compute/add_two.hpp"

// Ignore warnings caused by Google Test macros.
// NOLINTBEGIN(misc-use-internal-linkage,
// bugprone-throwing-static-initialization, cert-err58-cpp,
// cppcoreguidelines-owning-memory, modernize-use-scoped-lock)

#include <gtest/gtest.h>

TEST(AddTwo, Fifty)
{
    const compute::AddTwo add_two;
    EXPECT_EQ(add_two(50), 52);
}

// NOLINTEND(misc-use-internal-linkage, bugprone-throwing-static-initialization,
// cert-err58-cpp, cppcoreguidelines-owning-memory)
