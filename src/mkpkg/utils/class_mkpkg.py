"""
class MkPkg

Wrapper around makepkg to ensure package gets rebuilt whenever a package from makedepends list
is newer than the last time package was built
"""
# pylint: disable=R0902
import os
from .class_msg import GcMsg
from .tools import argv_parser
from .tools import print_summary
from .build import build
from .dep_vers import write_current_pkg_dep_vers

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

        self.depends = None
        self.depends_vers = None
        self.dep_vers_last = None
        self.dep_vers_now = None
        self.dep_vers_opers = ['>', '>=', '<']
        self.depends_files = None

        # options
        self.verb = False              # don't show normal makepkg output
        self.force = False              # run makepkg even if not necessary

        self.argv = argv_parser(self)   # passed down to makepkg

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
        if self.build_ok:
            # save package names and versions of any depenencies
            write_current_pkg_dep_vers(self)
        print_summary(self)
