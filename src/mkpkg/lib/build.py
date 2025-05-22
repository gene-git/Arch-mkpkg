# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
build()

- does all the work.
  Ensure package gets rebuilt whenever needed.
"""
# pylint: disable=too-many-branches, too-many-statements, too-many-locals
from typing import (Any)

from ._mkpkg_base import MkPkgBase
from .check_deps import check_deps
from .pkgbuild import bump_pkgrel
from .pkgbuild import set_pkgrel
from .pkgbuild import get_pkgbld_data
from .tools import check_package_exists
from .build_makepkg import build_w_makepkg
from .dep_vers import get_pkg_dep_vers_now
from .soname_deps import read_soname_deps
from .soname_rebuild import soname_rebuild_needed


def _pkg_or_soname_rebuild(pkg_vers_changed: bool, soname_build: bool,
                           mkpkg: MkPkgBase) -> bool:
    """
    Package changed or soname

    - pkgver changed or soname needs rebuild (pkgver_updated)
      - reset pkgrel and rebuild
    Returns True rebuild required.
    """
    msg = mkpkg.msg
    needs_build = False

    if not (pkg_vers_changed or soname_build):
        return False

    result = mkpkg.result
    name = mkpkg.pkgname
    ver = mkpkg.pkgver
    ver_updated = mkpkg.pkgver_updated
    rel = mkpkg.pkgrel

    info = f'{ver} -> {ver_updated}'

    msg(f'Package vers changed : {name} ({info})\n', fg='cyan')

    if soname_build:
        msg('Soname requires rebuild\n')

    result.append(('changed', 'package', f'{info}'))

    if pkg_vers_changed:
        rel = "1"
    else:
        rel = bump_pkgrel(rel)

    mkpkg.pkgrel_updated = rel

    msg(f'Resetting pkgrel and rebuilding : {rel}\n', fg='cyan')
    if set_pkgrel(mkpkg, rel):
        needs_build = True
    else:
        msg('Failed to reset pkgrel\n', fg='red')
        result.append(('error', 'pkgbuild', f'write new pkgrel {rel}'))

    return needs_build


def _dep_rebuild(pkg_file_info: dict[str, Any], mkpkg: MkPkgBase) -> bool:
    """
    Package itself is up to date - now deal with make dependencies.

    - pgver unchanged
      - pkg_file found
        - pfile matches vers
        - pfile matches pkrel
          check for newer deps - if so bump rel and rebuild
        - pfile rel not same
          rebuild (no rel bump as no package. deps not relevant as we building
      - pkg_file not found
        - rebuild (no rel bump as no package. deps not relevant as we building

    Returns True rebuild required.
    """
    msg = mkpkg.msg
    name = mkpkg.pkgname

    needs_build = False

    msg(f'Package vers un-changed: {name}\n', fg='cyan')

    pkg_file_found = pkg_file_info['found']

    if not pkg_file_found:
        msg('Pkg file not found\n', fg='cyan')
        mkpkg.result.append(('changed', 'no-package', 'packge missing'))
        return True

    pkg_file_exact_match = pkg_file_info['exact_match']
    pkg_file_prel = pkg_file_info['prel']

    rel = mkpkg.pkgrel
    verb = mkpkg.verb
    result = mkpkg.result

    #
    # pkg file has vers but release doesn't match
    #
    if not pkg_file_exact_match:
        rel_info = f'{pkg_file_prel} vs {rel}'
        txt = f'Pkg file version matches but not release ({rel_info})\n'
        msg(txt, fg='cyan')
        result.append(('changed', 'no-package', f'rel {rel_info}: '))
        return True

    #
    # pkg file vers and release match
    #
    if verb:
        msg('Checking make deps\n', fg='cyan')

    (okay, deps_newer) = check_deps(mkpkg)

    if okay and deps_newer:
        result.append(('changed', 'deps', 'deps updated'))
        msg('Trigger Deps have changed will rebuild\n', ind=1)

        rel_updated = bump_pkgrel(rel)
        mkpkg.pkgrel_updated = rel_updated
        msg(f'Updating pkgrel : {rel} -> {rel_updated}\n', ind=1)
        if set_pkgrel(mkpkg, rel_updated):
            needs_build = True
        else:
            txt = f'writing new pkgrel {rel_updated}'
            result.append(('error', 'pkgbuild', txt))
            msg('Failed to update pkgrel\n', fg='red')
            return False
    else:
        if verb:
            msg('No new trigger dependencies)\n', ind=1)
        result.append(('up2date', 'all', 'current'))

    return needs_build


def _build_if_needed(pkg_changed: bool,
                     soname_build: bool,
                     pkg_file_info: dict[str, Any],
                     mkpkg: MkPkgBase) -> bool:
    """
    Checks if build is needed.

    a) Package changed or soname requires build

    b) Dependencies changed or package file not found

    """
    msg = mkpkg.msg
    result = mkpkg.result
    ran_build = False

    #
    # Check package and soname
    #
    needs_build = _pkg_or_soname_rebuild(pkg_changed, soname_build, mkpkg)

    if not needs_build:
        needs_build = _dep_rebuild(pkg_file_info, mkpkg)

    if mkpkg.force and not needs_build:
        needs_build = True
        msg('Force active : Running build\n', ind=1)
        pkgrel = bump_pkgrel(mkpkg.pkgrel)

        mkpkg.pkgrel_updated = pkgrel
        result.append(('changed', 'force', 'rebuild forced'))

        msg(f'Updating pkgrel : {mkpkg.pkgrel} -> {pkgrel}\n', ind=1)
        if not set_pkgrel(mkpkg, pkgrel):
            msg('Failed to update pkgrel\n', fg='red')
            txt = f'writing new pkgrel {pkgrel}'
            result.append(('error', 'pkgbuild', txt))

    if needs_build:
        msg('Building package\n', ind=1)
        mkpkg.build_ok = build_w_makepkg(mkpkg)
        ran_build = True
        if not mkpkg.build_ok:
            msg('Build failed\n', ind=1, fg='red')
    else:
        msg('Nothing to do\n', ind=1)

    return ran_build


def build(mkpkg: MkPkgBase):
    """
    Do build
        1) Regular build
        2) If up to date -
           check all depends packages for being newer than last build
        3) check all depends_vers for greater version than last build
    """
    #
    # Extract info from pkgbui;d
    #
    okay = get_pkgbld_data(mkpkg)
    if not okay:
        mkpkg.result.append(('error', 'pkgbuild', 'getting data'))
        return

    #
    # read the last soname data (if exists)
    #
    read_soname_deps(mkpkg)
    soname_build = soname_rebuild_needed(mkpkg)

    #
    # handle case where prev build was incomplete
    #   look for package matching vers-rel (exact_match) or latest release vers
    #
    pkg_file_info = check_package_exists(mkpkg)

    pkg_vers_changed = False
    if mkpkg.pkgver_updated and mkpkg.pkgver_updated != mkpkg.pkgver:
        pkg_vers_changed = True

    #
    # For all mkpkg deps get the current versions
    # save into mkpkg.dep_vers>now
    #
    get_pkg_dep_vers_now(mkpkg)

    #
    # build if needed
    #
    ran_build = _build_if_needed(pkg_vers_changed, soname_build,
                                 pkg_file_info, mkpkg)

    #
    # summarize result (for easy parsing)
    #
    if ran_build:
        if mkpkg.build_ok:
            mkpkg.result.append(('sucess', 'build', 'makepkg succeeded'))
        else:
            mkpkg.result.append(('error', 'build', 'makepkg failed'))
