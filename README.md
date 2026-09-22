# C++ tooling demo

This is a demo of how to set up tooling for C++ with Bazel.
It has a module "tooling_demo_cpp" in the `include/tooling_demo_cpp` directory, and tests in `test`.

## Use this library with Bazel

This section explains how this repo could be used if it provided useful functionality.

1. Make your project depend on `@tooling_demo_cpp//:tooling_demo_cpp`, or, since the name of the module and the target are the same, `@tooling_demo_cpp`.

2. Use the Bazel module registry at `github.com/rogiervd/...` by adding to your `.bazelrc`

        build --registry file:///.../bzlmod-registry

3. Add to your `MODULE.bazel`

        bazel_dep(name = "tooling_demo_cpp", version = "x.y.z")

### A note about Bazel files

In the Bazel files there are a lot of comments that explain simple things that anyone who understands Bazel should know.
This is on purpose.
Understanding Bazel is not a prerequisite for working with this code.

## Testing and developing


### Unit testing

```
bazel test //test/...
```

In CI, this is run for multiple configurations.
For an optimised buid, add `-c opt`.


### Formatting

Pull requests should adhere to formatting rules, enforced by `clang-format` for C++ files, and `buildifier` (currently version 7.1.1) for Bazel files.

Check formatting of C++ code and Bazel code:

```
clang-format --dry-run -Werror `find . -name '*.?pp'`
buildifier -mode=check -lint=warn -r .
```

Apply formatting rules:

```
clang-format -i `find . -name '*.?pp'`
buildifier -mode=fix -lint=fix -r .
```

Other formatting is done with `pre-commit`.
```
pip install pre-commit
pre-commit run -a
```

To run the pre-commit checks before every commit:
```
pre-commit install
```

### Static checks

Linting:

First, generate the `compile_commands.json` file.
`clang-tidy -p .` tells clang-tidy to use `compile_commands.json`.

```
bazel run @hedron_compile_commands//:refresh_all
clang-tidy -p . --config-file=.clang-tidy --exclude-header-filter='external/.*' `find . -name '*.?pp'`
```

On MacOS, you may have a clang-tidy installed that is incompatible with the clang used by the compiler. To point it to the correct headers,
```
clang-tidy -p . --config-file=.clang-tidy --exclude-header-filter='external/.*' \
  --extra-arg="--sysroot=$(xcrun --sdk macosx --show-sdk-path)" \
  `find . -name '*.cpp'`
```


### Coverage

```
bazel coverage //test/...
```

[![Code coverage](https://coveralls.io/repos/github/rogiervd/tooling_demo_cpp/badge.svg?branch=main)](https://coveralls.io/github/rogiervd/tooling_demo_cpp?branch=main)


## Building documentation

```
bazel run //documentation:requirements.update
bazel build //documentation:documentation
```

To serve the documentation from a webserver on `localhost`:

```
bazel run //documentation:documentation.serve
```
