# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present Gene C <arch@sapience.com>
"""
Support tools for MkPkg class
"""
# pylint: disable=
import os
import glob

from ._mkpkg_base import MkPkgBase


def primary_pkgname(mkpkg: MkPkgBase) -> str:
    """
    return the pkgname string
    """
    pkgname = mkpkg.pkgname
    if isinstance(pkgname, list):
        pname = pkgname[0]
    else:
        pname = pkgname

    return pname


def pkg_version_release(mkpkg: MkPkgBase) -> tuple[str, str, str]:
    """
    Returns version and release number
    """
    pvers = mkpkg.pkgver
    if mkpkg.pkgver_updated:
        pvers = mkpkg.pkgver_updated

    prel = mkpkg.pkgrel
    if mkpkg.pkgrel_updated:
        prel = mkpkg.pkgrel_updated

    epoch = ''
    if mkpkg.epoch:
        epoch = mkpkg.epoch

    return (epoch, pvers, prel)


def pkg_version(mkpkg: MkPkgBase) -> str:
    """
    construct latest package version/release string
    """
    (epoch, pvers, prel) = pkg_version_release(mkpkg)
    if epoch:
        full_vers = f'{epoch}:{pvers}-{prel}'
    else:
        full_vers = f'{pvers}-{prel}'
    return full_vers


def _pkg_fname_vers_rel(fname: str) -> tuple[str, str]:
    """
    parse package file and extract version and release
    """
    pvers = ''
    prel = ''
    if fname:
        fsplit = fname.split('-')
        pvers = fsplit[1]
        prel = fsplit[2]
    return (pvers, prel)


def check_package_exists(mkpkg: MkPkgBase) -> dict[str, str | bool]:
    """
    Used when PKGBUILD has not pkgver() update function.
    Check that current pkgver/rel has corresponding package
     - Check for [epoch:]vers-rel
     - If not find latest vers.

    If the package is a split package, then we check that all
    packages exist. That way if first package succeeded but
    other packages failed, we will trigger a rebuild.

    For simplicity we report back a single "packge file info".
    For split pckage, we take the "worst" of any of the packages.
    e.g. if one package is missing we report that. This way
    we wont miss a needed rebuild.
    """
    (epoch, pvers, prel) = pkg_version_release(mkpkg)

    found: bool = True
    exact_match: bool = True

    for pname in mkpkg.pkgnames:
        (found_p, exact_p, pvers_p, prel_p) = (
                _one_package_exists(pname, epoch, pvers, prel)
                )
        found &= found_p
        exact_match &= exact_p

        if not found_p:
            # Stop looking - we need to rebuild
            # Keep the failing package vers and release
            pvers = pvers_p
            prel = prel_p
            break

    pkg_file_info: dict[str, str | bool] = {
            'found': found,
            'exact_match': exact_match,
            'pvers': pvers,
            'prel': prel,
            }
    return pkg_file_info


def _one_package_exists(pname: str, epoch: str, pvers: str, prel: str
                        ) -> tuple[bool, bool, str, str]:
    """
    Used when PKGBUILD has not pkgver() update function.
    Check that current pkgver/rel has corresponding package
     - Check for [epoch:]vers-rel
     - If not find latest vers.

    If the package is a split package, then we check that all
    packages exist. That way if first package succeeded but
    other packages failed, we will trigger a rebuild.

    Returns (found, exact_match, pvers, prel)
    """
    found: bool = False
    exact_match: bool = False

    epoch_str = ''
    if epoch:
        epoch_str = f'{epoch}:'
    pkg_pattern = f'{pname}-{epoch_str}{pvers}-{prel}-*.pkg.tar.zst'

    flist = glob.glob(pkg_pattern)
    if flist:
        found = True
        exact_match = True
    else:
        # look for same vers but different release
        pkg_pattern = f'{pname}-{epoch_str}{pvers}-*.pkg.tar.zst'
        flist = glob.glob(pkg_pattern)
        if flist:
            found = True
            flist = sorted(flist, key=os.path.getmtime)
            newest = flist[len(flist)-1]
            (pvers, prel) = _pkg_fname_vers_rel(newest)

    return (found, exact_match, pvers, prel)


def print_summary(mkpkg: MkPkgBase):
    """
    Print Summary Result
        - mkpkg.build_ok    - gives success/fail of call down to makepkg
        - mkpkg.result      - list of [what, where, comment]

        what : error, changed, up2date, success,
        1 line with:  current/success/fail - old_vers - new_vers
    """
    msg = mkpkg.msg

    rpt_key = 'mkp:'
    rpt_key_final = 'mkp-status:'

    if mkpkg.verb:
        msg('Summary of results:\n', adash=True, fg='cyan')

    pkg_vers = pkg_version(mkpkg)

    has_error = False
    has_changed = False
    has_success = False
    has_up2date = False

    for item in mkpkg.result:
        what = item[0]
        where = item[1]
        comment = item[2]
        if mkpkg.verb:
            msg(f'{rpt_key} {what:12s} {where:12s} {comment}\n', ind=1)
        if 'error' in what:
            has_error = True
        elif 'changed' in what:
            has_changed = True
        elif 'up2date' in what:
            has_up2date = True
        elif 'success' in what:
            has_success = True

    status = ''
    col = 'white'
    if has_error:
        status = 'error'
        col = 'red'
    elif has_changed or has_success:
        status = 'success'
        col = 'green'
    elif has_up2date:
        status = 'up2date'
        col = 'cyan'

    # move this outside of print_summary
    mkpkg.status = status

    msg(f'{rpt_key_final} {status} {pkg_vers}\n', fg=col)
