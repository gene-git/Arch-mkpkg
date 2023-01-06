#!/usr/bin/python
# SPDX-License-Identifier: MIT
# Copyright (c) 2022,2023 Gene C
"""
 Tool for Arch PKGBUILD to ensure packages are rebuilt when some dependencies requirements
 trigger a rebuild.
 NB Uses makepkg for actual builds.

 Uses 2 new PKGBUILD variables to define rebuild triggers
 See README for more details

 gene Oct 2022
"""

#import pdb
from lib import MkPkg

def main():
    """
    Build package if trigger dependencies have changed or as usual if package itself has changed.
    """
    #pdb.set_trace()

    mkpkg = MkPkg()
    mkpkg.build()

# -----------------------------------------------------
if __name__ == '__main__':
    main()
# -----------------------------------------------------
