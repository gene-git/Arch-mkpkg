# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
pacman query tools
"""
from datetime import datetime

from .run_prog_local import run_prog


def pac_qi_key(result: str, key: str) -> str:
    """
    Extract value of key from pacman -Qi output
    """
    vers_str = ''
    if not result:
        return vers_str

    for line in result.splitlines():
        if line.startswith(key):
            lsplit = line.split(':', 1)
            vers_str = lsplit[1].strip()
            break

    return vers_str


def pac_qi_install_date(result: str) -> datetime | None:
    """
    Extract install date from pacman -Qi output.
    date time string format: Wed 06 Jul 2022 07:06:39 PM EDT
    """
    dtime = None
    if not result:
        return dtime

    key = 'Install Date'
    fmt = '%a %d %b %Y %I:%M:%S %p %Z'
    dt_str = pac_qi_key(result, key)
    if dt_str:
        dtime = datetime.strptime(dt_str, fmt)

    return dtime


def pacman_query(pacman_args: list[str]) -> str:
    """
    Run pacman with proivded args and return result
    """
    pargs = ['/usr/bin/pacman'] + pacman_args
    (retc, output, _error) = run_prog(pargs)
    if retc == 0:
        return output
    return ''
