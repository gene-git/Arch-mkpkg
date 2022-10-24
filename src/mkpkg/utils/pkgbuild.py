"""
Support tools relating to PKGBUILD file used by MkPkg class
    - bump_pkgrel
    - write_pkgbuild
    - read_pkgbuild
    - set_pkgrel
    - get_pkgbld_data
"""
# pylint: disable=R0912,R0915
import os
from .tools import open_file
from .run_prog import run_prog
from .split_deps import split_deps_vers_list

def bump_pkgrel(old):
    """
    Bumbs pkg rel by one
        Handle case with subrelease (x.y)
    """
    if not old:
        return "1"

    if old.isdigit():
        new = int(old) + 1
    else:
        new = float(old) + 1.0

    new = str(new)
    return new

def _pkgbuild_path(mkpkg):
    """ construct path to PKGBUILD if exists"""
    msg = mkpkg.msg
    pfile = 'PKGBUILD'
    path = os.path.join(mkpkg.cwd, pfile)
    if not os.path.exists(path):
        msg(f'Missing : {path}\n')
        path = None
    return path

def write_pkgbuild(mkpkg, pkgbuild):
    """ write PKGBUILD file """
    msg = mkpkg.msg
    okay = False
    path = _pkgbuild_path(mkpkg)
    if not path:
        return okay

    fobj = open_file(path, 'w')
    if fobj:
        for line in pkgbuild:
            fobj.write(line)
        fobj.close()
        okay = True
    else:
        msg(f'Failed to write {path}\n', fg_col='red')
    return okay

def read_pkgbuild(mkpkg):
    """ read PKGBUILD file """
    msg = mkpkg.msg

    okay = True
    pkgbuild = None
    path = _pkgbuild_path(mkpkg)
    if not path:
        okay = False
        return okay

    fobj = open_file(path, 'r')
    if fobj:
        pkgbuild = fobj.readlines()
        fobj.close()
    else:
        okay = False
        msg(f'Failed to read {pkgbuild}\n', fg_col='red')

    mkpkg.pkgbuild = pkgbuild
    return okay

def set_pkgrel(mkpkg, pkgrel):
    """ Update pkgrel in PKGBUILD """
    msg = mkpkg.msg
    okay = True

    okay = read_pkgbuild(mkpkg)
    if okay and mkpkg.pkgbuild:
        found_pkgrel = False
        new_pkgbuild = []
        for line in mkpkg.pkgbuild:
            cline = line.strip()
            if cline.startswith('pkgrel='):
                found_pkgrel = True
                line = f'pkgrel={pkgrel}\n'
            new_pkgbuild.append(line)

        if found_pkgrel:
            msg(f'Saving updated PKGBUILD with pkgrel: {pkgrel}\n', ind=1)
            okay = write_pkgbuild(mkpkg, new_pkgbuild)
            mkpkg.pkgbuild = new_pkgbuild
        else:
            msg('Failed to find pkgrel line in PKGBUILD\n', fg_col='red', ind=1)
            okay = False

    return okay

def get_pkgbld_data(mkpkg):
    """
    Extract info from package build file PKGBUILD.
    If vers_update is true, run the pkgver() func if it exists
        Extract:
          makedepends
          _mkpkg_depends
          _mkpkg_depends_files
          pkgver    before update
          pkgver    after  update
          pkgrel
          To get update pkgver we run prepare() ; pkgver()
    """
    # pylint: disable=R0914
    msg = mkpkg.msg

    pkgbld_file = './PKGBUILD'
    #
    # make sure w have a PKGBUILD
    #
    if not os.path.exists(pkgbld_file):
        msg(f'Warning: Missing {pkgbld_file} file\n', fg_col='yellow')
        return False

    #
    # set up srcdir and startdir before sourcing PKGBUILD in case overwritten
    #
    srcdir = os.path.join(mkpkg.cwd,'src')
    cmd_str = f'startdir="{mkpkg.cwd}"\n'
    cmd_str += f'srcdir="{srcdir}"\n'

    cmd_str += f'source "{pkgbld_file}"\n'

    cmd_str += 'is_function() {\n'
    cmd_str += '  [[ $(type -t $1) ]] && echo true || echo "false"\n'
    cmd_str += '}\n'

    cmd_str += 'is_array() {\n'
    cmd_str += '  [[ $(declare -p $1) =~ "declare -a" ]] && echo true|| echo "false"\n'
    cmd_str += '}\n'

    cmd_str += 'echo "_X_ pkgname = ${pkgname[@]}"\n'
    cmd_str += 'echo "_X_ pkgver = $pkgver"\n'
    cmd_str += 'echo "_X_ makedepends = ${makedepends[@]}"\n'

    # arch guidelines require custom variables start with "_"- support old for backward compat
    cmd_str += 'echo "_X_ mkpkg_depends = ${mkpkg_depends[@]}"\n'
    cmd_str += 'echo "_X_ mkpkg_depends_files = ${mkpkg_depends_files[@]}"\n'
    cmd_str += 'echo "_X_ _mkpkg_depends = ${_mkpkg_depends[@]}"\n'
    cmd_str += 'echo "_X_ _mkpkg_depends_files = ${_mkpkg_depends_files[@]}"\n'

    # call the pkgver() to get updated version
    cmd_str += 'if [ $(is_function prepare) = "true" ] ; then\n'
    cmd_str += '  prepare\n'
    cmd_str += 'fi\n'
    cmd_str += 'if [ $(is_function pkgver) = "true" ] ; then\n'
    cmd_str += '  echo -n "_X_ pkgver_updated = "\n'
    cmd_str += '  pkgver\n'
    cmd_str += '  echo ""\n'
    cmd_str += 'fi\n'

    cmd_str += 'echo "_X_ pkgrel = ${pkgrel}"\n'
    cmd_str += '\n'

    #
    # run this shell script and collect output
    #
    pargs = ['/bin/bash', '-s']
    [retc, output, _errors] = run_prog (pargs, input_str=cmd_str)

    if retc != 0:
        msg('Failed to extract PKGBUILD info\n', fg_col='red')
        return False

    #
    # Extract what we want.
    #
    okay = True
    mkpkg_depends_files_old = None
    mkpkg_depends_old = None

    for line in output.splitlines():
        lsplit = line.strip().split('=',1)
        nparts = len(lsplit)
        data = None
        data_l = None
        if nparts > 1:
            data = lsplit[1]

        if data :
            # if bash array then store as list

            data_l = data.split()
            if len(data_l) > 1:
                data_l = list(map(str.strip, data_l))
                data = data_l
            else:
                data = data.strip()
                data_l = [data]

        if line.startswith('_X_ pkgname ='):
            mkpkg.pkgname = data
            if not data:
                msg('Warning: PKGBUILD missing pkgname\n', fg_col='yellow')
                okay = False

        elif line.startswith('_X_ pkgrel ='):
            mkpkg.pkgrel = data
            if not data:
                msg('Warning: PKGBUILD missing pkgrel\n', fg_col='yellow')
                okay = False

        elif line.startswith('_X_ pkgver ='):
            mkpkg.pkgver = data
            if not data:
                msg('Warning: PKGBUILD missing pkgrel\n', fg_col='yellow')
                okay = False

        elif line.startswith('_X_ pkgver_updated ='):
            mkpkg.pkgver_updated = data

        elif line.startswith('_X_ makedepends ='):
            mkpkg.makedepends = data_l          # always a list

        elif line.startswith('_X_ _mkpkg_depends ='):
            mkpkg.depends = data_l          # always a list

        elif line.startswith('_X_ mkpkg_depends ='):    # backward compat
            mkpkg_depends_old = data_l

        elif line.startswith('_X_ _mkpkg_depends_files ='):
            mkpkg.depends_files = data_l          # always a list

        elif line.startswith('_X_ mkpkg_depends_files ='):
            mkpkg_depends_files_old = data_l

    #
    # handle backward compat of variables without +_"
    #
    if mkpkg_depends_old:
        if not mkpkg.depends:
            msg('N.B.: please use underscore : "_mkpkg_depends"\n', fg_col='yellow')
            mkpkg.depends = mkpkg_depends_old
            mkpkg.depends = data_l          # always a list
        else:
            msg('Found "_mkpkg_depends"  - ignoring "mkpkg_depends"\n', fg_col='yellow')

    if mkpkg_depends_files_old:
        if not mkpkg.depends_files:
            msg('N.B.: please use undserscore : "_mkpkg_depends_files"\n', fg_col='yellow')
            mkpkg.depends_files = mkpkg_depends_files_old
        else:
            msg('Found "_mkpkg_depends_files" - ignoring "mkpkg_depends_files"\n', fg_col='yellow')

    #
    # If mkpkg_depends set it overrides makedepends.
    #
    got_mkpkg_vars = False
    if mkpkg.depends or mkpkg.depends_files:
        got_mkpkg_vars = True

    if (not got_mkpkg_vars) and mkpkg.use_makedepends and mkpkg.makedepends:
        if mkpkg.verb:
            msg('mkpkg_depends(_vers) not found - falling back to makedepends\n',ind=1, fg_col='yellow' )
        mkpkg.depends = mkpkg.makedepends

    #
    # split out version deps into mkpkg_depends_vers
    #
    split_deps_vers_list(mkpkg)
    return okay
