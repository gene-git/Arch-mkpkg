"""
Support tools for MkPkg class
"""
# pylint: disable=R0912,R0915
import os
import sys
import glob

def primary_pkgname(mkpkg):
    """
    return the pkgname string
    """
    pkgname = mkpkg.pkgname
    if isinstance(pkgname, list):
        pname = pkgname[0]
    else:
        pname = pkgname

    return pname

def pkg_version_release(mkpkg):
    """ Returns version and release number"""
    pvers = mkpkg.pkgver
    if mkpkg.pkgver_updated:
        pvers = mkpkg.pkgver_updated

    prel = mkpkg.pkgrel
    if mkpkg.pkgrel_updated:
        prel = mkpkg.pkgrel_updated

    epoch = None
    if mkpkg.epoch:
        epoch = mkpkg.epoch

    return (epoch, pvers, prel)

def pkg_version(mkpkg):
    """ construct the latest package version/release string """
    (epoch, pvers,prel) = pkg_version_release(mkpkg)
    if epoch:
        full_vers = f'{epoch}:{pvers}-{prel}'
    else:
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

def argv_parser(mkpkg):
    """
    We accept one argument only - it must be first arg.
    Remaining args are passed down to makepkg
    Args intended for mkpkg itself are all of the form:
        --mkp-<option>
    Options are:
        verb            - show makepkg (stdout) output
        force           - always run makepkg even if not needed
                        - you may want to set makepkg force as well (-f)
        use_makedepends - use makedepends array if no _mkpkg_xxx are set
    """
    opt_keys = ['--mkp-verb', '--mkp-force', '--mkp-use_makedepends']
    argv = []
    for opt in sys.argv[1:]:
        if opt in opt_keys:
            option = opt.split('--mkp-')[1]
            setattr(mkpkg, option, True)
        else:
            argv += [opt]

    return argv

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
        - Check for [epoch:]vers-rel
        - If not find latest vers.
    """
    pname = primary_pkgname(mkpkg)

    (epoch, pvers,prel) = pkg_version_release(mkpkg)

    found = False
    exact_match = False

    epoch_str=''
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

    # move this outside of print_summary
    mkpkg.status = status

    msg(f'{rpt_key_final} {status} {pkg_vers}\n', fg_col=col)
