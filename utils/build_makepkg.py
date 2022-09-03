"""
Support tools for MkPkg class
"""
# pylint: disable=R0912,R0915
import sys
from .tools import run_prog
from .tools import pkg_version

def _makepkg_outcome(retc, output, errors):
    """
    Determine the outcome of running makepkg.
    Needs care. For example, it can return non-zero and 'ERROR: A package has already been built.
    For our needs thats not an error.
    returns:
        retc = 0 means ok (current or success)
        res = Current, Fail, Success
        pvers - result of build - should match what we got from running pkgver()
    """
    res = None
    if retc == 0 :
        res = 'Success'

    key_success = 'Finished making:'
    key_already_built = 'A package has already been built'
    key_group_already_build = 'The package group has already been built.'

    pvers = None
    if output :
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

    return retc, res, pvers

def build_w_makepkg(mkpkg):
    """
    Run usual makepkg
    """
    msg = mkpkg.msg

    pargs = ['/usr/bin/makepkg']
    if mkpkg.argv:
        pargs += mkpkg.argv

    run_args = {}

    msg('Passing the buck to makepkg:\n', adash=True, fg_col='tan')
    [retc, output, errors] = run_prog(pargs, **run_args)
    if mkpkg.verb:
        print(output)
    msg('makepkg finished:\n', bdash=True, fg_col='tan')

    #
    # what did makepkg tell us:
    #
    retc, res, vers_mp = _makepkg_outcome(retc, output, errors)

    #
    # save and check version we got with what makepkg said
    #
    #if vers_mp:
    #    vers_mp = vers_mp.strip()
    mkpkg.pkgver_makepkg  = vers_mp
    pkg_vers = pkg_version(mkpkg)

    if res == 'Success' and pkg_vers != vers_mp:
        msg(f'Warning: Expect version {pkg_vers} makepkg got {vers_mp}\n', ind=1, fg_col='yellow')

    if retc != 0:
        build_ok = False
        parg_str = ' '.join(pargs)
        msg(f'Build failed: {parg_str}\n', ind=1,fg_col='red')
        sys.stderr.write(errors)

    else:
        build_ok = True
        if res == 'Success':
            msg(f'Build suceeded : {pkg_vers}\n', ind=1, fg_col='green')
        elif res == 'Current':
            msg(f'Package Current : {pkg_vers}\n', ind=1, fg_col='green')

    return build_ok
