# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
Support tools for text
"""


def col_fmt_helper(max_cols: int, current_col: int) -> tuple[int, str]:
    """
    tracks columns and issues newline and column reset
    when hit last column.
    """
    if current_col < max_cols:
        current_col += 1
        newline = ''
    else:
        current_col = 1
        newline = '\n'
    return current_col, newline
