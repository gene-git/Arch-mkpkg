# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
Package dependency support tools for MkPkg class check_deps()

 - read_last_dep_vers
   read list of packages / versions
 - write_current_pkg_dep_vers
   write list of packages / versions
 - get_pkg_dep_vers_now
   retrieve current package versions
 - get_depends_times()
   list of packages and times  [(pkg, time),...]
 - get_file_depends_times
   list of files and times from file depends list
 -
"""
import os
from datetime import datetime

from ._mkpkg_base import MkPkgBase
from .file_tools import open_file
from .pacman import pacman_query
from .pacman import pac_qi_key
from .pacman import pac_qi_install_date
from .version_compare import check_version_trigger


def write_current_pkg_dep_vers(mkpkg: MkPkgBase):
    """
    Writes list of dependeny packages and versions as of last build.

    File written: .mkpkg_dep_vers
    Each item take form:
      - package_name version
    """
    data = ''
    if mkpkg.dep_vers_now:
        for (pkg, vers) in mkpkg.dep_vers_now.items():
            data += f'{pkg} {vers}\n'

        fname = '.mkpkg_dep_vers'
        pname = os.path.join(mkpkg.cwd, fname)
        fobj = open_file(pname, 'w')
        if fobj:
            fobj.write(data)
            fobj.close()
        else:
            mkpkg.msg(f'Failed save pkg dep versions into {pname}\n')


def read_last_dep_vers(mkpkg: MkPkgBase) -> dict[str, str]:
    """
    Read list of dependeny packages and versions as of last build
        package_name version

    File read: .mkpkg_dep_vers
    """
    fname = '.mkpkg_dep_vers'
    pname = os.path.join(mkpkg.cwd, fname)
    dep_vers_last: dict[str, str] = {}
    data = None
    if os.path.exists(pname):
        fobj = open_file(pname, 'r')
        if fobj:
            data = fobj.readlines()

    if data:
        for row in data:
            [pkg, vers] = row.split()
            pkg = pkg.strip()
            vers = vers.strip()
            dep_vers_last[pkg] = vers
    return dep_vers_last


def get_pkg_dep_vers_now(mkpkg: MkPkgBase):
    """
    For each package in depends and depends_vers
    lookup current version using pacman -Qi.

    depends = [p1, p2, ...]
    depends_vers = [item, item2, ...]
    item = (pkgname, oper, vers_trigger)

    Save in dictionary mkpkg.dep_vers_now
    """
    mkpkg.dep_vers_now = {}
    pkg_list: list[str] = []
    if mkpkg.depends_vers:
        for (pkg, _oper, _vers_trigger) in mkpkg.depends_vers:
            pkg_list.append(pkg)

    if mkpkg.depends:
        for pkg in mkpkg.depends:
            pkg_list.append(pkg)

    for pkg in pkg_list:
        output = pacman_query(['-Qi', pkg])
        pkg_vers = pac_qi_key(output, 'Version')
        mkpkg.dep_vers_now[pkg] = pkg_vers


def get_depends_times(pkglist: list[str]
                      ) -> list[tuple[str, datetime | None]]:
    """
    For each package in 'pkglist' lookup the install date using pacman
    pkglist is a list of package names

    return list of (pkgname, date)
    handle case of pkg not installed - it's date is set to None
    """
    dep_datetimes: list[tuple[str, datetime | None]] = []
    if pkglist:
        for pkg in pkglist:
            output = pacman_query(['-Qi', pkg])
            dtime = pac_qi_install_date(output)
            this_one = (pkg, dtime)
            dep_datetimes.append(this_one)

    return dep_datetimes


def get_file_depends_times(cwd, flist) -> list[tuple[str, datetime | None]]:
    """
    for each file in flist, get its last modified time
    non-existent files ignored - not an error
    """
    dep_file_dates = []
    if flist:
        for file in flist:
            path = os.path.join(cwd, file)
            if os.path.exists(path):
                mod_time = os.path.getmtime(path)
                dtime = datetime.fromtimestamp(mod_time)
            else:
                dtime = None
            this_one = (file, dtime)
            dep_file_dates.append(this_one)

    return dep_file_dates


def _get_pkg_dep_vers_last(mkpkg: MkPkgBase, pkg: str) -> str:
    """
    Get the package version used in last build.
    Retrieved from the saved file of package dependencies which
    is stored in mkpkg.dep_vers_last  dictionary
    """
    vers = ''
    if mkpkg.dep_vers_last and pkg in mkpkg.dep_vers_last:
        vers = mkpkg.dep_vers_last[pkg]
    return vers


def get_depends_versions(mkpkg: MkPkgBase,
                         depends_vers: list[tuple[str, str, str]]
                         ) -> list[tuple[str, str, str, str, str, bool]]:
    """
    1) For each package in depends_vers lookup the current version using pacman
        depends_vers = [item, item2, ...]
        item = (pkgname, oper, vers_trigger)

    2) Find the the saved version used in last build for each package
        if found return list of [pkgname, date]
        handle case of package not installed - set it's date None
    """
    dep_vers_now = mkpkg.dep_vers_now
    dep_vers: list[tuple[str, str, str, str, str, bool]] = []

    if not depends_vers:
        return dep_vers

    for (pkg, oper, vers_trigger) in depends_vers:

        pkg_vers = dep_vers_now[pkg]
        last_vers = _get_pkg_dep_vers_last(mkpkg, pkg)

        info = check_version_trigger(mkpkg.msg, oper, vers_trigger,
                                     pkg_vers, last_vers)
        (trigger, pvers_comp, lvers_comp) = info

        this_one = (pkg, oper, vers_trigger, pvers_comp, lvers_comp, trigger)
        dep_vers.append(this_one)

    return dep_vers
