// SPDX-FileCopyrightText: Copyright 2026 Rogier van Dalen
//
// SPDX-License-Identifier: Apache-2.0

/** \file
 * Code examples that the documentation can quote from.
 *
 * Both Sphinx and Doxygen can quote from this.
 * But this code can also be run as a test, to make sure that the examples
 * actually work.
 * The good thing about not using Google Test or such is that the documentation
 * does not rely on it.
 * On the other hand: the assert()s are not executed in optimised builds.
 * Oh well.
 */

#include <cassert>

#include "tooling_demo_cpp/add_two.hpp"

int main()
{
    // Example for inclusion in Sphinx documentation.

    // The tag in square brackets matches the one given in use_add_two.cpp, as
    // does the tag at the end.
    // This is used to clip the example from the code into the documentation.
    {
        // [start-sphinx-example]
        tooling_demo_cpp::AddTwo const add_two;
        int four = add_two(2);
        assert(four == 4);
        // [end-sphinx-example]
    }

    // Example for inclusion in Doxygen documentation with \snippet.
    // For Doxygen, the tag needs to be in exactly this format, with //! and the
    // square brackets. The tag inside the square brackets matches the second
    // argument to \snippet.
    {
        //! [doxygen-example]
        tooling_demo_cpp::AddTwo const add_two;
        int six = add_two(4);
        assert(six == 6);
        //! [doxygen-example]
    }


    return 0;
}
