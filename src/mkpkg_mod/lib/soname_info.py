# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present Gene C <arch@sapience.com>
"""
Soname info data.
"""
from dataclasses import (dataclass, field, asdict)


@dataclass(kw_only=True)
class SonameInfo:
    """
    State of soname lib
     - soname is just the soname path (/usr/lib/libfoo.so.1)
     - soname_vers is it's associated version   (1)
     - path is the actual library being used    (/usrlib.foo.so.1.1.0)
     - path_vers is its version                 (1.1.0)
     - avail list of all available versions     (1, 1.1.0, 1.2.0, ...)
    """
    soname: str = ''
    vers: str = ''
    path: str = ''
    path_vers: str = ''
    mtime: int = -1
    avail: list[str] = field(default_factory=list)
    class_vers: int = 1

    def asdict(self) -> dict[str, str | int | list[str]]:
        """
        Convert self to dictionary
        """
        return asdict(self)
