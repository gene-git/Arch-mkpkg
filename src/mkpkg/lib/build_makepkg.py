# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
Support tools for MkPkg class
    - build_w_makepkg: Use makepkg to do build
"""
import sys
from .run_prog_local import run_prog
from .tools import pkg_version


def _makepkg_outcome(retc: int, output: str, errors: str
                     ) -> tuple[int, str, str]:
    """
    Determine the outcome of running makepkg.

    Needs some care. e.g. makepkg can return non-zero
    and 'ERROR: A package has already been built.

    For our purpose thats not an error.

    Returns:
        retc = 0 means ok (current or success)
        res = Current, Fail, Success
        pvers = result of build - should match output of pkgver()
    """
    res = ''
    if retc == 0:
        res = 'Success'

    key_success = 'Finished making:'
    key_already_built = 'A package has already been built'
    key_group_already_build = 'The package group has already been built.'

    pvers = ''
    if output:
        if key_success in output:
            res = 'Success'
            retc = 0
            lines = output.split('\n')
            for row in lines:
                if key_success in row:
                    row_split = row.split()
                    pvers = row_split[4]

    if not pvers and errors:
        if key_already_built in errors or key_group_already_build in errors:
            res = 'Current'
            retc = 0

    if not res:
        res = 'Fail'

    return (retc, res, pvers)


def build_w_makepkg(mkpkg):
    """
    Run usual makepkg
    """
    msg = mkpkg.msg

    pargs = ['/usr/bin/makepkg']
    if mkpkg.argv:
        pargs += mkpkg.argv

    msg('Passing the buck to makepkg:\n', adash=True, fg='tan', ind=1)
    (retc, output, errors) = run_prog(pargs)
    if mkpkg.verb:
        print(output)
    msg('------------------------------\n', fg='tan', ind=1)

    #
    # what did makepkg tell us:
    #
    (retc, res, vers_mp) = _makepkg_outcome(retc, output, errors)

    #
    # save and check version we got with what makepkg said
    #
    mkpkg.pkgver_makepkg = vers_mp
    pkg_vers = pkg_version(mkpkg)

    if res == 'Success' and pkg_vers != vers_mp:
        txt = f'Expect version {pkg_vers} makepkg got {vers_mp}'
        msg('Warning: {txt}\n', ind=1, fg='yellow')

    if retc != 0:
        build_ok = False
        parg_str = ' '.join(pargs)
        msg(f'Build failed: {parg_str}\n', ind=1, fg='red')
        sys.stderr.write(errors)

    else:
        build_ok = True
        status = 'good'
        if res == 'Success':
            status = 'succeeded'
        elif res == 'Current':
            status = 'Current'

        txt = f'{mkpkg.pkgname} {pkg_vers}'
        msg(f'Package {status} : {txt}\n', ind=1, fg='green')

    return build_ok
