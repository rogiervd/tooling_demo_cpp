#ifndef TOOLING_DEMO_CPP_ADD_TWO_HPP
#define TOOLING_DEMO_CPP_ADD_TWO_HPP

namespace tooling_demo_cpp {

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
    int operator()(int value) const;
};


}  // namespace tooling_demo_cpp

#endif  // TOOLING_DEMO_CPP_ADD_TWO_HPP
