# SPDX-License-Identifier: MIT
# Copyright (c) 2022,2023 Gene C
"""
class MkPkg

Wrapper around makepkg to ensure package gets rebuilt whenever specific dependency
conditions are met. E.G. a package or file is more recent than the last build, or
a package has updated and now hits a version trigger as specified in PKGBUILD
array variable _mkpkg_depends.
"""
# pylint: disable=R0902
import os
from .class_msg import GcMsg
from .class_config import MkpkgConf
#from .tools import argv_parser
from .tools import print_summary
from .build import build
from .dep_vers import write_current_pkg_dep_vers
from .soname import write_current_pkg_dep_soname
from .soname import pkginfo_soname_dep_info

class MkPkg:
    """ MkPkg wrapper class """
    def __init__(self):

        self.pkgbuild = None
        self.pkgname = None
        self.pkgrel = None
        self.pkgrel_updated = None
        self.pkgver = None
        self.pkgver_updated = None
        self.pkgver_makepkg = None
        self.epoch = None

        self.depends = None
        self.depends_vers = None
        self.dep_vers_last = None
        self.dep_vers_now = None
        self.dep_vers_opers = ['>', '>=', '<']
        self.depends_files = None

        # options
        self.conf = MkpkgConf()
        self.verb = self.conf.verb              # don't show normal makepkg output
        self.force = self.conf.force            # run makepkg even if not necessary
        self.refresh = self.conf.refresh        # refresh .mkpkg_dep_soname .mkpkg_dep_vers
        self.soname_build = self.conf.soname_build
        self.argv = self.conf.makepkg_args      # passed down to makepkg
        self.use_makedepends = self.conf.use_makedepends  # deprecated

        self.soname_info = {}

        self.cwd = os.getcwd()
        self.mymsg = GcMsg()

        self.build_ok = None            # makepkg exit code
        self.status = None              # error, success, up2date
        self.result = []                # list of : [what, where, comment]

    def __getattr__(self,name):
        return None

    def msg(self, txt, **kwargs):
        """ display output message """
        self.mymsg.msg(txt, **kwargs)

    def build(self):
        """
        Do build
            1) Regular build
            2) If up to date - check all makedepends packages for being newer than last build
        """
        build(self)
        if self.build_ok or self.refresh:
            #
            # Get any soname info and save package names and versions
            # of any depenencies (including sonames)
            #
            write_current_pkg_dep_vers(self)
            self.soname_info = pkginfo_soname_dep_info(self)
            write_current_pkg_dep_soname(self)
        print_summary(self)
