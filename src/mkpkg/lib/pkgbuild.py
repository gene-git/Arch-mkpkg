# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
Support tools relating to PKGBUILD file used by MkPkg class
    - bump_pkgrel
    - write_pkgbuild
    - read_pkgbuild
    - set_pkgrel
    - get_pkgbld_data
"""
# pylint: disable=too-many-branches, too-many-statements
# pylint: disable=too-many-locals
import os

from ._mkpkg_base import MkPkgBase
from .file_tools import open_file
from .run_prog_local import run_prog
from .split_deps import split_deps_vers_list


def bump_pkgrel(old: str) -> str:
    """
    Bumbs pkg rel by one
        Handle case with subrelease (x.y)
    """
    if not old:
        return "1"

    if old.isdigit():
        new = str(int(old) + 1)
    else:
        new = str(float(old) + 1.0)

    return new


def _pkgbuild_path(mkpkg: MkPkgBase) -> str:
    """
    Construct path to PKGBUILD if exists
    """
    msg = mkpkg.msg
    pfile = 'PKGBUILD'
    path = os.path.join(mkpkg.cwd, pfile)
    if not os.path.exists(path):
        msg(f'Missing : {path}\n')
        path = ''
    return path


def write_pkgbuild(mkpkg: MkPkgBase, pkgbuild: list[str]) -> bool:
    """
    write PKGBUILD file
    """
    msg = mkpkg.msg
    path = _pkgbuild_path(mkpkg)
    if not path:
        return False

    okay = False
    fobj = open_file(path, 'w')
    if fobj:
        for line in pkgbuild:
            fobj.write(line)
        fobj.close()
        okay = True
    else:
        msg(f'Failed to write {path}\n', fg='red')
        okay = False
    return okay


def read_pkgbuild(mkpkg: MkPkgBase) -> bool:
    """
    read PKGBUILD file
    """
    msg = mkpkg.msg

    pkgbuild: list[str] = []
    path = _pkgbuild_path(mkpkg)
    if not path:
        return False

    fobj = open_file(path, 'r')
    if fobj:
        pkgbuild = fobj.readlines()
        fobj.close()
    else:
        msg(f'Failed to read {pkgbuild}\n', fg='red')
        return False

    mkpkg.pkgbuild = pkgbuild
    return True


def set_pkgrel(mkpkg: MkPkgBase, pkgrel: str) -> bool:
    """
    Update pkgrel in PKGBUILD
    """
    msg = mkpkg.msg
    okay = True

    okay = read_pkgbuild(mkpkg)
    if okay and mkpkg.pkgbuild:
        found_pkgrel = False
        new_pkgbuild: list[str] = []

        for line in mkpkg.pkgbuild:
            cline = line.strip()
            if cline.startswith('pkgrel='):
                found_pkgrel = True
                line = f'pkgrel={pkgrel}\n'
            new_pkgbuild.append(line)

        if found_pkgrel:
            msg(f'Saving updated PKGBUILD pkgrel = {pkgrel}\n', ind=1)
            okay = write_pkgbuild(mkpkg, new_pkgbuild)
            mkpkg.pkgbuild = new_pkgbuild
        else:
            msg('Failed to find pkgrel PKGBUILD\n', fg='red', ind=1)
            okay = False

    return okay


def get_pkgbld_data(mkpkg: MkPkgBase) -> bool:
    """
    Extract info from package build file PKGBUILD.

    If vers_update is true, run the pkgver() func if it exists
    Extract:
      _mkpkg_depends
      _mkpkg_depends_files
      pkgver    before update
      pkgver    after  update
      pkgrel
    To get update pkgver we run prepare() ; pkgver()
    """
    msg = mkpkg.msg

    #
    # make sure w have a PKGBUILD
    #
    pkgbld_file = './PKGBUILD'
    if not os.path.exists(pkgbld_file):
        msg(f'Warning: Missing {pkgbld_file} file\n', fg='yellow')
        return False

    #
    # Trap any errors
    #
    cwd = mkpkg.cwd
    srcdir = os.path.join(cwd, 'src')

    cmd_str = f"""
    # Trap any errors
    _cleanup() {{
        exit 1
    }}
    trap _cleanup ERR

    # set up srcdir / startdir before sourcing PKGBUILD
    startdir="{cwd}"
    srcdir="{srcdir}"

    cd {srcdir}
    source "$startdir/{pkgbld_file}"

    is_function() {{
        [[ $(type -t $1) ]] && echo true || echo "false"
    }}

    is_array() {{
      [[ $(declare -p $1) =~ "declare -a" ]] && echo true|| echo "false"
    }}

    is_associative_array() {{
      [[ $(declare -p $1 2>/dev/null) =~ "declare -A" ]] && echo true|| echo "false"
    }}

    echo "_X_ pkgname = ${{pkgname[@]}}"
    echo "_X_ pkgver = $pkgver"
    echo "_X_ pkgbase = $pkgbase"
    # echo "_X_ makedepends = ${{makedepends[@]}}"

    echo "_X_ _mkpkg_depends = ${{_mkpkg_depends[@]}}"
    echo "_X_ _mkpkg_depends_files = ${{_mkpkg_depends_files[@]}}"

    # call pkgver() to get updated version
    if [ $(is_function prepare) = "true" ] ; then
      prepare
    fi

    if [ $(is_function pkgver) = "true" ] ; then
      echo -n "_X_ pkgver_updated = "
      pkgver
      echo ""
    fi

    echo "_X_ pkgrel = ${{pkgrel}}"
    echo "_X_ epoch = ${{epoch}}"

    if [ $(is_associative_array _dep_vers_prog) == "true" ] ; then
        echo -n "_D_ dep_vers_prog start="
        for pkg in "${{!_dep_vers_prog[@]}}"
        do
            echo -n "$pkg,${{_dep_vers_prog[$pkg]}} "
        done
    fi

    """

    #
    # run this shell script and collect output
    #
    pargs = ['/bin/bash', '-s']
    (retc, output, errors) = run_prog(pargs, input_str=cmd_str)

    if retc != 0:
        msg('Failed to extract PKGBUILD info\n', fg='red')
        if errors:
            msg(f'{errors}')
        return False

    #
    # Extract what we want.
    #
    okay = True
    for line in output.splitlines():
        lsplit = line.strip().split('=', 1)
        nparts = len(lsplit)
        data: str = ''
        data_l: list[str] = []

        if nparts > 1:
            data = lsplit[1].strip()

        if data:
            # if bash array store into list data_l
            data_l = data.split()
            if len(data_l) > 1:
                data_l = list(map(str.strip, data_l))
            else:
                data_l = [data.strip()]

        if line.startswith('_X_ pkgname ='):
            if data:
                mkpkg.pkgname = data_l[0]
                mkpkg.pkgnames = data_l
            else:
                msg('Warning: PKGBUILD missing pkgname\n', fg='yellow')
                okay = False

        elif line.startswith('_X_ pkgbase ='):
            mkpkg.pkgbase = data

        elif line.startswith('_X_ pkgrel ='):
            mkpkg.pkgrel = data
            if not data:
                msg('Warning: PKGBUILD missing pkgrel\n', fg='yellow')
                okay = False

        elif line.startswith('_X_ pkgver ='):
            mkpkg.pkgver = data
            if not data:
                msg('Warning: PKGBUILD missing pkgver\n', fg='yellow')
                okay = False

        elif line.startswith('_X_ pkgver_updated ='):
            mkpkg.pkgver_updated = data

        elif line.startswith('_X_ epoch ='):
            if data and int(data) > 0:
                mkpkg.epoch = data

        elif line.startswith('_X_ _mkpkg_depends ='):
            mkpkg.depends = data_l          # always a list

        elif line.startswith('_X_ _mkpkg_depends_files ='):
            mkpkg.depends_files = data_l          # always a list

        elif line.startswith('_D_ dep_vers_prog start'):
            # list of pkg-name,versions
            for item in data_l:
                pkg_prog = item.split(',')
                if len(pkg_prog) > 1:
                    pkg = pkg_prog[0]
                    prog = pkg_prog[1]
                    mkpkg.dep_vers_prog[pkg] = prog
                else:
                    msg(f'Warning: PKGBUILD _dep_vers_prog invalid {item}\n', fg='yellow')

    #
    # split out version deps into mkpkg_depends_vers
    #
    split_deps_vers_list(mkpkg)
    return okay
