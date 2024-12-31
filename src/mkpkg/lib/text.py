# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
Support tools for text
    text_fmt_helper() - tracks columns and issues newline and column reset when hit last column
"""

def col_fmt_helper(max_cols, current_col):
    """
    tracks columns and issues newline and column reset when hit last column
    """
    if current_col < max_cols:
        current_col += 1
        newline = ''
    else:
        current_col = 1
        newline = '\n'
    return current_col, newline

def str_iter(txt):
    """
    Iterator which works for either single str or list of strings
    Convenience so caller can loop whether string or list
    Used for log/msg which allow either.
    """
    if isinstance(txt, str) :
        yield txt
    else:
        try:
            # use iter() to force exception on non-iterable
            yield from iter(txt)
        except TypeError:
            yield txt
