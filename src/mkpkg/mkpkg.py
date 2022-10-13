#!/usr/bin/python
"""
 Arch tool to ensure packages are rebuilt when some dependencies are newer than the last build
 Uses makepkg for actual rebuilds.

 Uses 2 new PKGBUILD variables to define rebuild triggers

 See README for more details

 gene Oct 2022
"""

#import pdb
from utils import MkPkg

def main():
    """
    Build package if trigger dependencies have changed or as usual if package itself has changed.
        mkpkg_newer - if any package listed was installed since the last build
        mkpkg_vers  - version constraints. Uses semantic versioning.
                      Can trigger on any version, major, major.minor or major.minor.patch
    Uses regular makepkg to do the actual build
    """
    #pdb.set_trace()

    mkpkg = MkPkg()
    mkpkg.build()

# -----------------------------------------------------
if __name__ == '__main__':
    main()
# -----------------------------------------------------
