"""
build()
    - does all the work.
    Wrapper around makepkg to ensure package gets rebuilt whenever a package from makedepends list
    is newer than the last time package was built
"""
# pylint: disable=R0902
from .tools import check_deps
from .pkgbuild import bump_pkgrel
from .pkgbuild import set_pkgrel
from .pkgbuild import get_pkgbld_data
from .tools import check_package_exists
from .build_makepkg import build_w_makepkg

def _build_if_needed(pkg_up2date, mkpkg):
    """
    Package itself is up to date - now deal with make deps
    """
    msg = mkpkg.msg
    ran_build = False

    if pkg_up2date:
        msg('Package itself up to date\n', fg_col='cyan')
        msg('Checking make deps\n', fg_col='cyan')
        (okay,deps_newer) = check_deps(mkpkg)

        if okay and deps_newer:
            mkpkg.result.append(['changed', 'deps', 'deps updated'])
            msg('Deps have changed will rebuild\n', ind=1)

            pkgrel = bump_pkgrel(mkpkg.pkgrel)
            mkpkg.pkgrel_updated = pkgrel
            msg(f'Updating pkgrel : {mkpkg.pkgrel} -> {pkgrel}\n', ind=1)
            okay = set_pkgrel(mkpkg, pkgrel)
            if okay:
                msg('Building package\n', ind=1)
                mkpkg.build_ok = build_w_makepkg(mkpkg)
                ran_build = True
            else:
                mkpkg.result.append(['error', 'pkgbuild', 'write new pkgrel'])
                msg('Failed to update pkgrel\n', fg_col='red')
        else:
            msg('Package up to date (no newer make deps)\n', ind=1)
            mkpkg.result.append(['up2date', 'all', 'current'])
            if mkpkg.force:
                mkpkg.result.append(['changed', 'force', 'rebuild forced'])
                msg('Force On : Running standard makepkg\n', ind=1)
                mkpkg.build_ok = build_w_makepkg(mkpkg)
                ran_build = True

    else:
        msg('Package is out of date, rebuilding\n', fg_col='cyan')
        mkpkg.result.append(['changed', 'package', 'version'])
        pkgrel = "1"
        mkpkg.pkgrel_updated = pkgrel
        msg('Resetting pkgrel and rebuilding : {pkgrel}\n', fg_col='cyan')
        okay  = set_pkgrel(mkpkg, pkgrel)
        if okay:
            mkpkg.build_ok = build_w_makepkg(mkpkg)
            ran_build = True
            if not mkpkg.build_ok:
                msg('Build failed\n', ind=1, fg_col='red')
        else:
            msg('Failed to update pkgrel\n', fg_col='red')
            mkpkg.result.append(['error', 'pkgbuild', 'write new pkgrel'])

    return ran_build

def build(mkpkg):
    """
    Do build
        1) Regular build
        2) If up to date - check all makedepends packages for being newer than last build
    """
    msg = mkpkg.msg

    #
    # Extract info from pkgbui;d
    #
    okay = get_pkgbld_data(mkpkg)
    if not okay:
        mkpkg.result.append(['error', 'pkgbuild', 'getting data'])
        return

    #
    # handle casw where prev build was incomplete
    #
    have_package = check_package_exists(mkpkg)

    if not have_package:
        pkg_up2date = False
    elif mkpkg.pkgver_updated:
        pkg_up2date = mkpkg.pkgver == mkpkg.pkgver_updated
    else:
        # no pkgver() function so check package exists that matches this version.
        pkg_up2date = have_package

    #
    # build if needed
    #
    msg(f'package version: {mkpkg.pkgver} up2date: {pkg_up2date}\n')
    ran_build = _build_if_needed(pkg_up2date, mkpkg)

    #
    # summarize result (for easy parsing)
    #
    if ran_build:
        if mkpkg.build_ok:
            mkpkg.result.append(['sucess', 'build', 'makepkg succeeded'])
        else:
            mkpkg.result.append(['error', 'build', 'makepkg failed'])

    #
    # If build happened check new versions match
    #
