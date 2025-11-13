# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
Base class used by MkPkg.

Manage all data to ensure package gets rebuilt
whenever specific dependency conditions are met.
E.G. a package or file is more recent than the last build, or
a package has updated and now hits a version trigger
as specified in PKGBUILD array variable _mkpkg_depends.
"""
# pylint: disable=too-many-instance-attributes, too-few-public-methods
import os

from .class_msg import Msg
from .class_config import MkpkgConf
from .soname_info import SonameInfo


class MkPkgBase:
    """
    MkPkg base class.

    Manages the data / attributes.
    """
    def __init__(self):

        self.pkgbuild: list[str] = []   # content of PKGBUILD
        self.pkgbase: str = ''
        self.pkgname: str = ''
        self.pkgnames: list[str] = []
        self.pkgrel: str = ''
        self.pkgrel_updated: str = ''
        self.pkgver: str = ''
        self.pkgver_updated: str = ''
        self.pkgver_makepkg: str = ''
        self.epoch: str = ''

        #
        # depends_vers list of (pkg, op, trigger)
        # e.g. ('pkg-name', '>=', '22.0')
        #
        self.depends: list[str] = []
        self.depends_vers: list[tuple[str, str, str]] = []
        self.dep_vers_last: dict[str, str] = {}
        self.dep_vers_now: dict[str, str] = {}
        self.dep_vers_opers: list[str] = ['>', '>=', '<']
        self.depends_files: list[str] = []

        #
        # Current version of a package dependency comes from pacman -Q
        # However, if that package is not installed then need alternate
        # way to to get the current version.
        #
        # e.g. pigeonhole can be built against the dovecot source repo
        #
        # For this case we can provide a list of programs to run that returns
        # the package version. It takes one argument which is the package name
        # The default is to run pacman -Qi and extract "Version"
        #
        # List of dependency package names and program to run
        # AN associative array variable in PKGBUILD
        # declare -A _dep_vers_prog
        # _dep_vers_prog["pkg-name"] = "prog-returns-version"
        #
        self.dep_vers_prog: dict[str, str] = {}

        #
        # options
        #  - force just forces a rebuild
        #  - refresh updates .mkpkg_dep_soname .mkpkg_dep_vers
        self.conf = MkpkgConf()
        self.verb = self.conf.verb
        self.force = self.conf.force
        self.refresh = self.conf.refresh

        # soname_build ~ 'never', 'newer', <compare-how>
        #  These compare using greater than: 'major' or 'minor' or 'last' etc
        self.soname_comp = self.conf.soname_comp
        self.soname_info: dict[str, SonameInfo] = {}

        self.argv = self.conf.makepkg_args      # passed down to makepkg

        self.cwd = os.getcwd()
        theme = 'dark'
        self.mymsg = Msg(theme=theme)

        #
        # build_ok: makepkg exit code
        # status: error, success or up2date
        # result:  (what, where, comment)
        #
        self.build_ok: bool = False     # makepkg exit code
        self.status: str = ''           # error, success, up2date
        self.result: list[tuple[str, str, str]] = []

    def msg(self, txt: str, **kwargs):
        """ display output message """
        self.mymsg.msg(txt, **kwargs)
