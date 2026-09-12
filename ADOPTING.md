# Adopting this framework for a real project

The point of this repository is as a framework for new or existing projects.
This framework is fairly opinionated:

* It uses Bazel. This makes builds as hermetic and reproducible as reasonable. (CMake, the obvious alternative, is a mess.)
* It uses Sphinx for documentation, with Doxygen to gather the API documentation from C++ files.
* It uses GitHub Actions for CI. This seems easy and well integrated with GitHub.
* It automatically formats C++, yaml, and Starlark files with `pre-commit`.
* It uses linting with clang-tidy for C++ code.
* It uses automated testing. (Maybe not controversial.)
* Automated tests can run under Address Aanitiser, Undefined Behavior Sanitizer, and Valgrind. And these do run in CI.
* There is an automated coverage check which, through Coveralls.io, should show up in pull requests.

# Structure of this framework

* `include/tooling_demo_cpp` contains the headers that a user of this library should use.
* `test/tooling_demo_cpp` contains the tests of the library.
* `documentation` contains the documentation for the library.
* `.github/workflows` contains the GitHub Actions specifications.

# How to adopt this framework

* Do not clone this framework; that makes little sense.
  Future improvements should probably be carried across as patches.
* Copy
`.bazelrc`,
`.bazelversion`,
`MODULE.bazel`,
and the `BUILD.bazel` files in various directories.
* Copy `README.md`, put project-specific information at the top, and edit.
* Add a license, possibly by copying
`LICENSE`.
* Rename
`include/tooling_demo_cpp`
and `test/tooling_demo_cpp` to have the name of the actual project.
* To run unit tests on GitHub Actions, copy `.github/workflows/test.yml`.


### Sphinx and Doxygen
* Copy `./documentation`.
* Edit `conf.py`, and of course the actual documentation.
* To run documentation generation on GitHub Actions, copy
`.github/workflows/documentation.yml`.


### GitHub Actions

### Automatic formatting
* Copy
`.pre-commit-config.yaml`,
`.clang-format`,
and `.yamllint.yaml`.
* To run formatting on GitHub Actions, copy `.github/workflows/pre-commit.yml`
* If you apply this framework to a pre-existing library which is not formatted correctly, then
  * Make a separate commit for just reformatting.
  * add the full SHA-1 hash of the reformatting commit to `.git-blame-ignore-revs` and check it in.
  * `git blame` (and the blame on GitHub) should now be unpolluted.

### Linting
* Copy
`.clang-tidy`.
* To run linting on GitHub Actions, copy
`.github/workflows/lint.yml`.


### Running with sanitisers
* To run tests with sanitisers on GitHub Actions, copy
`.github/workflows/sanitizers.yml`.
* To run tests with Valgrind on GitHub Actions, copy
`.github/workflows/valgrind.yml`
* A lot of the details of how to call helpers are specified in `.bazelrc`.

### Test coverage
To run coverage on GitHub Actions,
* Copy `.github/workflows/coverage.yml`.
* Get this repo set up on coveralls.io.
* Add the Coveralls user to the repo on GitHub.
