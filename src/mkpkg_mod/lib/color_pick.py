# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present Gene C <arch@sapience.com>
"""
color_pick:

Given a list of color names and an name which
can be partial name find the match.

e.g. given ['black', 'blue', 'brown']
 black would be matched by bla
 blue                   by blu
 etc.
 bl would not be a unique match.
    in this case we return the first match in list.
We want to avoid errors.
"""


def _get_matches(cnt: int, num_max: int, color: str,
                 color_list: list[str]) -> list[str]:
    """
    Return all matches of first 'cnt' chars
    """
    if color in color_list:
        return [color]

    sub_list = []
    for avail in color_list:
        if len(avail) >= cnt and color[0:cnt] == avail[0:cnt]:
            sub_list.append(avail)

    if len(sub_list) > 1 and cnt <= num_max:
        sub_list = _get_matches(cnt + 1, num_max, color, sub_list)

    return sub_list


def color_pick(color: str, color_list: list[str]):
    """
    Find matching color given full or partial name
    """
    if not color:
        return ''

    num_max = len(color)
    matches = _get_matches(1, num_max, color, color_list)
    if matches:
        return matches[0]
    return ''
