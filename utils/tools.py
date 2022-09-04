"""
Support tools for MkPkg class
"""
# pylint: disable=R0912,R0915
import os
import sys
import subprocess
import glob
import datetime

def pkg_version_release(mkpkg):
    """ Returns version and release number"""
    pvers = mkpkg.pkgver
    if mkpkg.pkgver_updated:
        pvers = mkpkg.pkgver_updated

    prel = mkpkg.pkgrel
    if mkpkg.pkgrel_updated:
        prel = mkpkg.pkgrel_updated

    return (pvers, prel)

def pkg_version(mkpkg):
    """ construct the latest package version/release string """
    (pvers,prel) = pkg_version_release(mkpkg)
    full_vers = f'{pvers}-{prel}'
    return full_vers

def open_file (pathname, mode):
    """
     Wrapper to open file and handle errors = returns file object if successfuke or None
    """
    # pylint: disable=W1514,R1732
    try:
        fobj = open(pathname, mode)
    except OSError as err:
        print(f'Error opening file {pathname} : {err}')
        fobj = None
    return fobj

def run_prog(pargs, input_str=None,stdout=subprocess.PIPE,stderr=subprocess.PIPE):
    """
    Run a program
    """
    bstring = None
    if input_str:
        bstring = bytearray(input_str,'utf-8')

    ret = subprocess.run(pargs, input=bstring, stdout=stdout, stderr=stderr,check=False)
    retc = ret.returncode
    output = None
    errors = None
    if ret.stdout :
        output = str(ret.stdout, 'utf-8',errors='ignore')
    if ret.stderr :
        errors = str(ret.stderr, 'utf-8',errors='ignore')

    return [retc, output, errors]

def _is_pkg_up2date(output):
    """ checks if no build due to ppackage being up to date """
    up2date = False
    key = 'ERROR: The package group has already been built'

    for line in output:
        if key in line:
            up2date = True
            break

    return up2date

def argv_parser(mkpkg):
    """
    We accept one argument only - it must be first arg.
    Remaining args are passed down to makepkg
    Args intended for mkpkg itself are all of the form:
        --mkp-<option>
    Options are:
        verb       - show makepkg (stdout) output
        force       - always run makepkg even if not needed
                    - you may want to set makepkg force as well (-f)
    """
    opt_keys = ['--mkp-verb', '--mkp-force']
    argv = []
    for opt in sys.argv[1:]:
        if opt in opt_keys:
            option = opt.split('--mkp-')[1]
            setattr(mkpkg, option, True)
        else:
            argv += [opt]

    return argv

def _line_clean(line):
    """ clean up a line """
    txt = line.strip()
    if txt.startwith('#'):
        return None

    tspl = txt.split('#')
    txt = tspl[0].split()
    return txt

def _last_package_date(mkpkg):
    """
    Find modified time of package
        We just pick first (assuming ends in .zst)
    """
    pkgname = mkpkg.pkgname
    if isinstance(pkgname, list):
        pname = pkgname[0]
    else:
        pname = pkgname

    full_vers = pkg_version(mkpkg)

    # package must be there as called after a first build
    dtime = None
    #pkg_pattern = f'{pname}*zst'
    pkg_pattern = f'{pname}-{full_vers}-*.pkg.tar.zst'
    flist = glob.glob(pkg_pattern)
    for pkgfile in flist:
        mod_time = os.path.getmtime(pkgfile)
        pkg_dtime = datetime.datetime.fromtimestamp(mod_time)
        if dtime :
            if pkg_dtime > dtime:
                dtime = pkg_dtime
        else:
            dtime = pkg_dtime
    return dtime

def _pac_query_date(result):
    """
    Extract install date from pacman -Qi output
        date time string format: Wed 06 Jul 2022 07:06:39 PM EDT
    """
    key = 'Install Date'
    fmt = '%a %d %b %Y %I:%M:%S %p %Z'
    dtime = None
    for line in result.splitlines():
        if line.startswith(key):
            lsplit = line.split(':', 1)
            dt_str = lsplit[1].strip()
            dtime = datetime.datetime.strptime(dt_str, fmt)
            break

    return dtime

def _get_dep_dates(pkglist):
    """
    For each package in makedepend lookup the install date using pacman
        return list of [pkgname, date]
        handle case of pkg not installed - set it's date None
    """
    dep_dates = []
    if pkglist:
        for pkg in pkglist:
            pac_cmd = ['/usr/bin/pacman', '-Qi']
            pargs = pac_cmd + [pkg]
            [retc, output, _error] = run_prog(pargs)
            if retc == 0:
                dtime = _pac_query_date(output)
            else:
                dtime = None
            this_one = [pkg, dtime]
            dep_dates.append(this_one)

    return dep_dates

def check_deps(mkpkg):
    """
        check if any makedepend dep has changed since last build
        if we have no deps saved we rebuild package to be safe and save deps used
            or get newest package timesamp and compare to 'Install Date' of package
        get_pkgbld_data() must be called prior to calling this func.
    """
    msg = mkpkg.msg

    #
    # if no deps then nothing to do
    if not mkpkg.makedepends:
        return (False, False)

    # make sure we have pulled PKGBUILD info
    okay = True
    if not mkpkg.pkgname:
        msg('error: Missing pkgbuild data\n', fg_col='red', ind=1)
        return (False, False)

    # current package datetime
    pkg_date = _last_package_date(mkpkg)
    if not pkg_date:
        # interuppted build - missing package - force rebuild
        return (True, True)

    #get list of datetime for each makedep
    deps = _get_dep_dates(mkpkg.makedepends)

    deps_newer = False
    for pkg,dtime in deps:
        if not dtime:
            msg(f'Dependency not installed {pkg}\n', ind=1)
            okay = False
        elif dtime > pkg_date:
            deps_newer = True
            msg(f'Dependency newer: {pkg}\n', ind=1)
            # dont break so can print all deps
            #break

    return (okay, deps_newer)

def _pkg_fname_vers_rel(fname):
    """ parse package file and extract version and release """
    pvers = None
    prel = None
    if fname:
        fsplit = fname.split('-')
        pvers = fsplit[1]
        prel = fsplit[2]
    return (pvers, prel)

def check_package_exists(mkpkg):
    """
    Used when PKGBUILD has not pkgver() update function.
    Check that current pkgver/rel has corresponding package
        - Check for vers-rel
        - If not find latest vers.
    """
    pkgname = mkpkg.pkgname
    if isinstance(pkgname, list):
        pname = pkgname[0]
    else:
        pname = pkgname

    (pvers,prel) = pkg_version_release(mkpkg)

    found = False
    exact_match = False
    pkg_pattern = f'{pname}-{pvers}-{prel}-*.pkg.tar.zst'
    flist = glob.glob(pkg_pattern)
    if flist:
        found = True
        exact_match = True
    else:
        # look for same vers but different release
        pkg_pattern = f'{pname}-{pvers}-*.pkg.tar.zst'
        flist = glob.glob(pkg_pattern)
        if flist:
            found = True
            #flist.sort(key=x: os.path.getmtime(x))
            flist = sorted(flist, key=os.path.getmtime)
            newest = flist[len(flist)-1]
            (pvers, prel) = _pkg_fname_vers_rel(newest)

    pkg_file_info = {
            'found'         : found,
            'exact_match'   : exact_match,
            'pvers'         : pvers,
            'prel'          : prel,
            }
    return pkg_file_info

def print_summary(mkpkg):
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
        msg('Summary of results:\n', adash=True, fg_col='cyan')

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

    if has_error:
        status = 'error'
        col = 'red'
    elif has_changed or has_success:
        status = 'success'
        col = 'green'
    elif has_up2date:
        status = 'up2date'
        col = 'cyan'

    msg(f'{rpt_key_final} {status} {pkg_vers}\n', fg_col=col)
