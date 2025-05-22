# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
Package dependency support tools for MkPkg class
    -
"""
# pylint: disable=too-many-locals
import os
import glob
from datetime import datetime

from ._mkpkg_base import MkPkgBase
from .tools import pkg_version
from .tools import primary_pkgname
from .dep_vers import get_depends_times
from .dep_vers import get_depends_versions
from .dep_vers import get_file_depends_times


def _most_recent_package_date(mkpkg: MkPkgBase) -> datetime | None:
    """
    Find modified time of package.

    We just pick first (we assume .zst)
    Since we know we're using zstd compression.
    """
    pname = primary_pkgname(mkpkg)
    full_vers = pkg_version(mkpkg)

    # package must be there as called after a first build
    dtime = None
    pkg_pattern = f'{pname}-{full_vers}-*.pkg.tar.zst'
    flist = glob.glob(pkg_pattern)
    for pkgfile in flist:
        mod_time = os.path.getmtime(pkgfile)
        pkg_dtime = datetime.fromtimestamp(mod_time)
        if dtime:
            dtime = max(dtime, pkg_dtime)
        else:
            dtime = pkg_dtime
    return dtime


def check_deps(mkpkg: MkPkgBase) -> tuple[bool, bool]:
    """
    Check depenencies.

    check if any of triggre deps dep has changed since last build
      - any package listed in mkpkg.depends
      - any package listed in mkpkg.depends_vers with greater
        listed version than last build
      - any file listed in mkpkg.depends_files

    get_pkgbld_data() to read PKGBUILD must be called prior
    to calling this func.

    Returns:
        (okay: bool, deps_newer: bool)
    """
    msg = mkpkg.msg

    #
    # if no deps then nothing to do
    #
    if not (mkpkg.depends or mkpkg.depends_files or mkpkg.depends_vers):
        return (False, False)

    #
    # make sure we have pulled PKGBUILD info
    #
    if not mkpkg.pkgname:
        msg('error: Missing pkgbuild data\n', fg='red', ind=1)
        return (False, False)

    #
    # current package datetime
    #
    pkg_date = _most_recent_package_date(mkpkg)
    if not pkg_date:
        #
        # missing package - maybe interuppted build.
        #  - treat same as deps newer
        #
        return (True, True)

    #
    # get list of datetime for each makedep package
    #
    okay = True
    deps_newer = False

    these_deps_times = get_depends_times(mkpkg.depends)
    for (pkg, dtime) in these_deps_times:
        if not dtime:
            msg(f'Dependency not installed {pkg}\n', ind=1)
            okay = False
        elif dtime > pkg_date:
            deps_newer = True
            msg(f'Dependency newer: {pkg}\n', ind=1)
            # dont break so can record all deps

    these_deps_times = get_file_depends_times(mkpkg.cwd, mkpkg.depends_files)
    for file, dtime in these_deps_times:
        if not dtime:
            msg(f'File not found {file}\n', ind=1)
            okay = False
        elif dtime > pkg_date:
            deps_newer = True
            msg(f'File dependency newer: {file}\n', ind=1)
            # dont break so can record all deps

    these_deps_vers = get_depends_versions(mkpkg, mkpkg.depends_vers)
    for this_one in these_deps_vers:
        (pkg, oper, vers_trigger, pvers, lvers, trigger) = this_one
        if trigger:
            deps_newer = True
            txt = f'{pkg} {oper} {vers_trigger}: {pvers} {oper} {lvers}'
            msg(f'Version trigger: {txt}\n', ind=1)

    return (okay, deps_newer)
