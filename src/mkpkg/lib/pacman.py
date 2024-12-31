# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
 pacman query tools
"""
# pylint disable=R0912,R0915
import datetime
from .run_prog import run_prog

def pac_qi_key(result, key):
    """
    Extract value of key from pacman -Qi output
    """
    vers_str = None
    if not result:
        return vers_str
    for line in result.splitlines():
        if line.startswith(key):
            lsplit = line.split(':', 1)
            vers_str = lsplit[1].strip()
            break

    return vers_str

def pac_qi_install_date(result):
    """
    Extract install date from pacman -Qi output
        date time string format: Wed 06 Jul 2022 07:06:39 PM EDT
    """
    dtime = None
    if not result:
        return dtime

    key = 'Install Date'
    fmt = '%a %d %b %Y %I:%M:%S %p %Z'
    dt_str = pac_qi_key(result, key)
    if dt_str:
        dtime = datetime.datetime.strptime(dt_str, fmt)

    return dtime

def pacman_query(pacman_args):
    """
    Run pacman with proivded args and return result
    """
    pargs = ['/usr/bin/pacman'] + pacman_args
    [retc, output, _error] = run_prog(pargs)
    if retc == 0:
        return output
    return None
