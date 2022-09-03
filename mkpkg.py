#!/usr/bin/python
"""
 Wrapper for makepkg which rebuilds package when packages listed in makedepends are newer than
 previous build.

 See README for more details

 gene Sep 2022
"""

#import pdb
from utils import MkPkg

def main():
    """
    Wrapper over makepkg to handle makedepends dependencies.
    Does a regular makepkg build but additionally rebuilds
    should any makedepend be more recent than the package.
    """
    #pdb.set_trace()

    mkpkg = MkPkg()
    mkpkg.build()

# -----------------------------------------------------
if __name__ == '__main__':
    main()
# -----------------------------------------------------
