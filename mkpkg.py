#!/usr/bin/python
"""
 Wrapper for makepkg which rebuilds package when packages listed in makedepends are newer than
 previous build.

 First we try regular build - if its up to date then bump the pkg_rel and rebuild.

 Should this be builtin to makepkg?

 Call this in place of makepkg

 Should we keep all the build info in file or in PKGBUILD itself?
   - for now we keep in separate file where each line has
     package build_date

 All arguments are passed through to /usr/bin/makepkg

 gene 2022
"""

#import pdb
from utils import MkPkg

def main():
    """
    Wrapper over makepkg to handle makedepends dependencies.
    If any of the makedepends packages have been updated since last build
    bump pkg_ver and rebuild. New builds have their pkrel set to "1"
    """
    #pdb.set_trace()

    mkpkg = MkPkg()
    mkpkg.build()

# -----------------------------------------------------
if __name__ == '__main__':
    main()
# -----------------------------------------------------
