# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
 Package dependency support tools for MkPkg class
    - split_deps_vers_list()
        splits depends list into 2 lists:
        mkpkg.depends       - package names with no version requirement
        mkpkg.depends_vers  - packages with version requirements
"""
# pylint: disable=
from ._mkpkg_base import MkPkgBase
from .dep_vers import read_last_dep_vers


def _split_pkg_vers_constraint(mkpkg: MkPkgBase, item: str
                               ) -> tuple[str, str, str]:
    """
    Takes a string in form 'pkgname oper vers'
    where oper is one of the opers list

    Returns (pkgname, oper,  vers)
     opers can be: '>', '>=' or '<'
     < for downgrades: pkg<last
    """
    pkg = ''
    oper = ''
    vers_trigger = ''
    msg = mkpkg.msg

    #
    # add white space
    #
    xitem = item.replace('>', ' > ')
    xitem = xitem.replace('<', ' < ')
    xitem = xitem.replace('< =', '<= ')
    xitem = xitem.replace('> =', '>= ')

    splitem: list[str] = xitem.split()
    num_items = len(splitem)
    err_txt = f'_mkpkg_depends item should be "X" or "X>Y" etc. Got: {item}'

    if num_items == 1:
        pkg = splitem[0]

    elif num_items == 2:
        # incomplete either a) (pkg oper) or (pkg vers)
        # we can return orig or first piece as it makes no sense
        # we return orig
        pkg = item.strip()
        msg(f'Error: {err_txt}', fg='warn')

    elif num_items == 3:
        pkg = splitem[0]
        oper = splitem[1]
        vers_trigger = splitem[2]

    else:
        # ug - also makes no sense
        pkg = item.strip()
        msg(f'Error: {err_txt}', fg='warn')

    return (pkg, oper, vers_trigger)


def split_deps_vers_list(mkpkg: MkPkgBase):
    """
    Splits the mkpkg.depends list into 2 lists:
        mkpkg.depends       - package names with no version requirement
        mkpkg.depends_vers  - packages with version requirements
    """
    if not mkpkg.depends:
        return

    dep_names: list[str] = []
    dep_vers: list[tuple[str, str, str]] = []

    for item in mkpkg.depends:
        (pkg, oper, vers_trigger) = _split_pkg_vers_constraint(mkpkg, item)
        if oper:
            this = (pkg, oper, vers_trigger)
            dep_vers.append(this)
        else:
            pkg = item.strip()
            dep_names.append(pkg)

    mkpkg.depends_vers = dep_vers
    mkpkg.depends = dep_names

    if mkpkg.depends_vers:
        mkpkg.dep_vers_last = read_last_dep_vers(mkpkg)
