#!/usr/bin/python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
 Tool for Arch PKGBUILD to ensure packages are rebuilt when some dependencies requirements
 trigger a rebuild.
 NB Uses makepkg to do the actual builds.

 Uses 2 new PKGBUILD variables to define rebuild triggers
 See README for more details

 gene C Oct 2022
"""
from lib import MkPkg

def main():
    """
    Build package if trigger dependencies have changed or as usual if package itself has changed.
    """
    mkpkg = MkPkg()
    mkpkg.build()

# -----------------------------------------------------
if __name__ == '__main__':
    main()
# -----------------------------------------------------
