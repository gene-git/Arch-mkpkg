# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
class MkPkg

Dervied from MkPkgBase which handles data.
ALl methods are with the subclass.

Uses makepkg to do actual bulds and ensures package gets
rebuilt whenever specific dependency conditions are met.
E.G. a package or file is more recent than the last build, or
a package has updated and now hits a version trigger
as specified in PKGBUILD array variable _mkpkg_depends.
"""
# pylint: disable=

from ._mkpkg_base import MkPkgBase

from .tools import print_summary
from .build import build
from .dep_vers import write_current_pkg_dep_vers
from .soname_deps import (write_soname_deps)
from .soname import (get_current_soname_info)


class MkPkg(MkPkgBase):
    """
    MkPkg class.

    Derived from base class which handles data.
    """
    def build(self):
        """
        Do build
            1) Regular build
            2) If up to date.
               check makedepends packages if newer than last build
        """
        build(self)
        if self.build_ok or self.refresh:
            #
            # Get any soname info and save package names and versions
            # of any depenencies (including sonames)
            #
            write_current_pkg_dep_vers(self)
            self.soname_info = get_current_soname_info('pkg')
            write_soname_deps(self)
        print_summary(self)
