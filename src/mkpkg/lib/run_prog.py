# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
Support tools for MkPkg class
    run external program
"""
# pylint: disable=too-many-arguments,too-many-positional-arguments

import subprocess
from subprocess import SubprocessError


def run_prog(pargs: list[str],
             input_str: str = '',
             stdout: int = subprocess.PIPE,
             stderr: int = subprocess.PIPE) -> tuple[int, str, str]:
    """
    Run a program
    """
    if not pargs:
        return (0, '', 'Missing pargs')

    bstring = b''
    if input_str:
        bstring = bytearray(input_str, 'utf-8')

    try:
        ret = subprocess.run(pargs, input=bstring, stdout=stdout,
                             stderr=stderr, check=False)

    except (FileNotFoundError, SubprocessError) as err:
        return (-1, '', str(err))

    retc = ret.returncode
    output = ''
    errors = ''

    if ret.stdout:
        output = str(ret.stdout, 'utf-8', errors='ignore')

    if ret.stderr:
        errors = str(ret.stderr, 'utf-8', errors='ignore')

    return (retc, output, errors)
