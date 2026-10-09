<!--
SPDX-FileCopyrightText: Copyright 2026 Rogier van Dalen

SPDX-License-Identifier: CC-BY-4.0
-->

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
* Choose a license (currently, for code, the Apache license), put it in `./LICENSE` (for GitHub) as well as `./LICENSES/` (for the license checks) and make sure files have SPDX headers.
* Rename
`include/tooling_demo_cpp`
and `test/tooling_demo_cpp` to have the name of the actual project.
* To run unit tests on GitHub Actions, copy `.github/workflows/test{,-optimised}.yml`.

### Publishing a new release
* Copy `.github/workflows/release.yml` and `tool/release.py`.

### Publishing the Bazel module in rogiervd's registry
Any time there is a release, put in a PR to add this release of the Bazel module to the registry:
* Copy `.bcr/presubmit.yml`, `.bcr/metadata.template.json`, `.github/workflows/publish-to-bazel-registry.yml`; copy and edit `.bcr/metadata.template.json`.
* Then create a personal access token (PAT):
  * Go to https://github.com/settings/tokens -> Generate new token -> Generate new token (classic, not the fine-grained kind: `publish-to-bcr`'s README notes fine-grained tokens can't open PRs against public repos yet).
  * Name it something like `bazel-registry-publish-<module_repo>`.
  * Pick an expiration (you'll need to regenerate and update the secret when it lapses).
  * Check these two scopes: `repo` and `workflow`.
  * Click "Generate token" and copy the value (GitHub only shows it once).
  * Add it as a secret on the module repo (not the registry repo), since that's where `publish-to-bcr.yml` reads it from:
    ```
    gh secret set BCR_PUBLISH_TOKEN --repo rogiervd/<module_repo>
    ```

### Documentation building

The documentation uses Sphinx and Doxygen.

* Copy the bottom half of `MODULE.bazel`, for configuring the Python toolchain.
* Copy `./documentation`.
* Edit `conf.py`, `BUILD.bazel`, and of course the actual documentation.
* To run documentation generation on GitHub Actions, copy
`.github/workflows/documentation.yml`.

#### Updating the Python packages automatically
`documentation/requirements.txt` pins the versions of the Python packages.
To upgrade them by hand, run
`bazel run //documentation:requirements.run -- --upgrade`.
(`bazel run //documentation:requirements.update` does not upgrade packages that are already pinned.)

To have GitHub Actions do this on the first day of every odd month and open a pull request with the result:
* Copy `.github/workflows/update-requirements.yml`.
* On GitHub, go to the repository's Settings -> Actions -> General, and under "Workflow permissions" check "Allow GitHub Actions to create and approve pull requests".
  Without this, the workflow fails when it tries to open the pull request.
  (If this is greyed out, it needs to be allowed for the organisation first.)
* Optionally, make CI run on these pull requests.
  Pull requests that a workflow opens with the default `GITHUB_TOKEN` do not trigger other workflows, so the tests and the documentation build would not run on them.
  To fix this, create a personal access token (PAT):
  * Go to https://github.com/settings/personal-access-tokens -> Generate new token (the fine-grained kind).
  * Name it something like `update-requirements-<repo>`.
  * Pick an expiration (you'll need to regenerate and update the secret when it lapses).
  * Under "Repository access", select only this repository.
  * Under "Permissions", give "Read and write" access to "Contents" and "Pull requests".
  * Click "Generate token" and copy the value (GitHub only shows it once).
  * Add it as a secret on the repo:
    ```
    gh secret set REQUIREMENTS_UPDATE_TOKEN --repo <owner>/<repo>
    ```
  If the secret is not set, the workflow falls back to `GITHUB_TOKEN`.
* To test the workflow without waiting, start it by hand from the repository's Actions tab ("Update Python requirements" -> "Run workflow").


### GitHub Actions

### Automatic formatting
* Copy
`.pre-commit-config.yaml`,
`.clang-format`,
and `.yamllint.yaml`.
* To run formatting on GitHub Actions, copy `.github/workflows/pre-commit.yml`
* If you apply this framework to a pre-existing library which is not formatted correctly, then
  * Make a separate commit for just reformatting.
  * add the full SHA-1 hash (`git rev-parse HEAD`) of the reformatting commit to `.git-blame-ignore-revs` and check this file in.
  * Locally, say `git config blame.ignoreRevsFile .git-blame-ignore-revs`.
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

### .gitignore
* Copy `.gitignore` to make Git ignore `bazel-*` symlinks in the root directory.

### Files specific to Visual Studio Code
You may or may not want to check these into your repo.
* `.vscode/settings.json` tells VS code to ignore `bazel-*` symlinks when searching.
* `.vscode/c_cpp_properties.json` instructs IntelliSense to work from `compile_commands.json`, which can be generated with the Bazel invocation given in `README.md`.
