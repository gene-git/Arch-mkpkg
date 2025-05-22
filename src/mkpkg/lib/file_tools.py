# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
Support tools for MkPkg class
"""
# pylint: disable=
from typing import IO


def open_file(pathname: str, mode: str) -> IO | None:
    """
    Open file / handle errors.
    Returns IO file object if successfuke otherwise None
    """
    # pylint: disable=unspecified-encoding,consider-using-with
    try:
        fobj = open(pathname, mode)
    except OSError as err:
        print(f'Error opening file {pathname}: {err}')
        fobj = None
    return fobj
