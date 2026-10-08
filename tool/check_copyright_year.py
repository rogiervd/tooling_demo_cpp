#!/usr/bin/env python3

# SPDX-FileCopyrightText: Copyright 2026 Rogier van Dalen
#
# SPDX-License-Identifier: Apache-2.0

"""Checks that SPDX copyright notices include the current year.

For each file that has SPDX-FileCopyrightText lines with years in them, at
least one of those lines must include the current year. Files without such
lines (e.g. those covered by REUSE.toml) are skipped, and so are sections
between REUSE-IgnoreStart and REUSE-IgnoreEnd, as in REUSE.

With --fix, the year is added to a line. For example, if the current year is
2026:

- "2025" becomes "2025-2026" and "2023-2025" becomes "2023-2026", since 2025
  directly precedes 2026;
- "2024" becomes "2024, 2026", since there is a gap.

If a file has several copyright lines, the line that mentions the committer
(git config user.name) is fixed; if there is no such line, the file is only
reported.

The script tests itself every time it runs.
"""

import argparse
import datetime
import re
import subprocess
import sys
from pathlib import Path

# A copyright line, with only comment characters before the tag.
_COPYRIGHT_LINE = re.compile(r"^\W*SPDX-FileCopyrightText:")
# A list of years and year ranges, like "2020, 2023-2025".
_YEAR_LIST = re.compile(r"\d{4}(?:\s*-\s*\d{4})?(?:\s*,\s*\d{4}(?:\s*-\s*\d{4})?)*")
_YEAR_RANGE = re.compile(r"(\d{4})(?:\s*-\s*(\d{4}))?")
_IGNORE_START = "REUSE-IgnoreStart"
_IGNORE_END = "REUSE-IgnoreEnd"


def year_ranges(year_list: str) -> list[tuple[int, int]]:
    """Parses "2020, 2023-2025" into [(2020, 2020), (2023, 2025)]."""
    return [
        (int(first), int(last or first))
        for first, last in _YEAR_RANGE.findall(year_list)
    ]


def includes_year(year_list: str, year: int) -> bool:
    return any(first <= year <= last for first, last in year_ranges(year_list))


def add_year(year_list: str, year: int) -> str:
    """Adds year to a list of years.

    The year extends the last range or year if it directly follows it, and is
    appended after a comma otherwise.
    """
    if includes_year(year_list, year):
        return year_list
    last_range = list(_YEAR_RANGE.finditer(year_list))[-1]
    first, last = year_ranges(last_range.group(0))[0]
    if last == year - 1:
        return year_list[: last_range.start()] + f"{first}-{year}"
    return f"{year_list}, {year}"


def find_year_lists(lines: list[str]) -> list[tuple[int, re.Match]]:
    """Returns the lists of years in the copyright lines, with line indices."""
    year_lists = []
    ignoring = False
    for index, line in enumerate(lines):
        if _IGNORE_START in line:
            ignoring = True
        elif _IGNORE_END in line:
            ignoring = False
        elif not ignoring and _COPYRIGHT_LINE.match(line):
            match = _YEAR_LIST.search(line)
            if match:
                year_lists.append((index, match))
    return year_lists


def check_text(
    text: str, year: int, committer: str | None, fix: bool
) -> tuple[bool, str]:
    """Checks the copyright lines in text.

    Returns whether the text is fine as it is, and the text with the year added
    if fix is set and a line to fix was found.
    """
    lines = text.splitlines(keepends=True)
    year_lists = find_year_lists(lines)
    if not year_lists:
        return True, text
    if any(includes_year(match.group(0), year) for _, match in year_lists):
        return True, text
    if not fix:
        return False, text

    if len(year_lists) == 1:
        to_fix = year_lists[0]
    else:
        candidates = [
            (index, match)
            for index, match in year_lists
            if committer and committer in lines[index]
        ]
        if len(candidates) != 1:
            return False, text
        to_fix = candidates[0]

    index, match = to_fix
    line = lines[index]
    lines[index] = (
        line[: match.start()] + add_year(match.group(0), year) + line[match.end() :]
    )
    return False, "".join(lines)


# REUSE-IgnoreStart
# The test data contains SPDX tags, which are not this file's licensing
# information.


def _self_test() -> None:
    assert add_year("2024", 2026) == "2024, 2026"
    assert add_year("2025", 2026) == "2025-2026"
    assert add_year("2023-2025", 2026) == "2023-2026"
    assert add_year("2023 - 2025", 2026) == "2023-2026"
    assert add_year("2020-2023", 2026) == "2020-2023, 2026"
    assert add_year("2020, 2025", 2026) == "2020, 2025-2026"
    assert add_year("2020, 2023-2025", 2026) == "2020, 2023-2026"
    assert add_year("2020, 2024", 2026) == "2020, 2024, 2026"
    assert add_year("2024-2026", 2026) == "2024-2026"

    assert includes_year("2026", 2026)
    assert includes_year("2020-2027", 2026)
    assert includes_year("2020, 2026", 2026)
    assert not includes_year("2020-2025", 2026)
    assert not includes_year("2020, 2027", 2026)

    # No copyright line.
    assert check_text("int x;\n", 2026, None, True) == (True, "int x;\n")

    # The current year is there.
    text = "// SPDX-FileCopyrightText: Copyright 2024-2026 Rogier van Dalen\n"
    assert check_text(text, 2026, None, True) == (True, text)

    # The current year is missing.
    text = "# SPDX-FileCopyrightText: Copyright 2024 Rogier van Dalen\n"
    assert check_text(text, 2026, None, False) == (False, text)
    assert check_text(text, 2026, None, True) == (
        False,
        text.replace("2024", "2024, 2026"),
    )

    # Fixing keeps the rest of the line and the line endings.
    text = (
        "// SPDX-FileCopyrightText: Copyright 2025 Rogier van Dalen\r\n"
        "//\r\n"
        "// SPDX-License-Identifier: Apache-2.0\r\n"
    )
    assert check_text(text, 2026, None, True) == (
        False,
        text.replace("2025", "2025-2026"),
    )

    # Markdown and reStructuredText headers.
    text = "<!--\nSPDX-FileCopyrightText: Copyright 2024 Rogier van Dalen\n-->\n"
    assert check_text(text, 2026, None, True)[1] == text.replace(
        "2024", "2024, 2026"
    )
    text = ".. SPDX-FileCopyrightText: Copyright 2025 Rogier van Dalen\n"
    assert check_text(text, 2026, None, True)[1] == text.replace(
        "2025", "2025-2026"
    )

    # One line with the current year is enough.
    text = (
        "# SPDX-FileCopyrightText: 2020 Someone Else\n"
        "# SPDX-FileCopyrightText: 2026 Rogier van Dalen\n"
    )
    assert check_text(text, 2026, None, False) == (True, text)

    # With several lines, the committer's line is fixed.
    text = (
        "# SPDX-FileCopyrightText: 2020 Someone Else\n"
        "# SPDX-FileCopyrightText: 2025 Rogier van Dalen\n"
    )
    assert check_text(text, 2026, "Rogier van Dalen", True) == (
        False,
        text.replace("2025 Rogier", "2025-2026 Rogier"),
    )
    # If there is no line for the committer, nothing is fixed.
    assert check_text(text, 2026, "Another Person", True) == (False, text)

    # The tag in the middle of a line, or in a REUSE.toml annotation, is not
    # a copyright line.
    text = 'TAG = "SPDX-FileCopyrightText: 2020"\n'
    assert check_text(text, 2026, None, True) == (True, text)
    text = 'SPDX-FileCopyrightText = "NONE"\n'
    assert check_text(text, 2026, None, True) == (True, text)

    # Ignored sections are skipped.
    text = (
        "# SPDX-FileCopyrightText: 2026 Rogier van Dalen\n"
        "# REUSE-IgnoreStart\n"
        "# SPDX-FileCopyrightText: 2020 Someone Else\n"
        "# REUSE-IgnoreEnd\n"
    )
    assert [index for index, _ in find_year_lists(text.splitlines())] == [0]


# REUSE-IgnoreEnd


def committer_name() -> str | None:
    try:
        return (
            subprocess.run(
                ["git", "config", "user.name"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            or None
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def main() -> int:
    _self_test()

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", help="files to check")
    parser.add_argument(
        "--fix", action="store_true", help="add the current year where it is missing"
    )
    args = parser.parse_args()

    year = datetime.date.today().year
    committer = committer_name() if args.fix else None
    ok = True
    for name in args.files:
        path = Path(name)
        try:
            with path.open(encoding="utf-8", newline="") as file:
                text = file.read()
        except (UnicodeDecodeError, IsADirectoryError):
            continue
        file_ok, new_text = check_text(text, year, committer, args.fix)
        if file_ok:
            continue
        ok = False
        if new_text != text:
            with path.open("w", encoding="utf-8", newline="") as file:
                file.write(new_text)
            print(f"{name}: added {year} to the copyright notice")
        else:
            print(f"{name}: no SPDX-FileCopyrightText line includes {year}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
