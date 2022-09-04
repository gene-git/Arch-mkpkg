"""
build()
    - does all the work.
    Wrapper around makepkg to ensure package gets rebuilt whenever a package from makedepends list
    is newer than the last time package was built
"""
# pylint: disable=R0902,R0912,R0915
from .tools import check_deps
from .pkgbuild import bump_pkgrel
from .pkgbuild import set_pkgrel
from .pkgbuild import get_pkgbld_data
from .tools import check_package_exists
from .build_makepkg import build_w_makepkg

def _build_if_needed(pkg_vers_changed, pkg_file_info, mkpkg):
    """
    Package itself is up to date - now deal with make deps
        - pkgver changed (pkgver_updated)
            - reset pkgrel and rebuild
        - pgver unchanged
            - pkg_file found
                - pfile matches vers
                    - pfile matches pkrel
                        check for newer deps - if so bump rel and rebuild
                - pfile rel not same
                    - rebuild (no rel bump as no package. deps not relevant as we building
            - pkg_file not found
                - rebuild (no rel bump as no package. deps not relevant as we building
    """
    msg = mkpkg.msg
    ran_build = False
    needs_build = False

    pkg_file_found = pkg_file_info['found']
    pkg_file_exact_match = pkg_file_info['exact_match']
    #pkg_file_pvers = pkg_file_info['pvers']
    #pkg_file_prel = pkg_file_info['prel']

    if pkg_vers_changed:
        msg('Package vers changed\n', fg_col='cyan')
        mkpkg.result.append(['changed', 'package', 'version'])
        pkgrel = "1"
        mkpkg.pkgrel_updated = pkgrel
        msg('Resetting pkgrel and rebuilding : {pkgrel}\n', fg_col='cyan')
        okay  = set_pkgrel(mkpkg, pkgrel)
        if okay:
            needs_build = True
        else:
            msg('Failed to update pkgrel\n', fg_col='red')
            mkpkg.result.append(['error', 'pkgbuild', 'write new pkgrel'])
    else:
        msg('Package vers unchanged\n', fg_col='cyan')
        if pkg_file_found:
            if pkg_file_exact_match:
                # pkg file vers and release match
                msg('Checking make deps\n', fg_col='cyan')
                (okay,deps_newer) = check_deps(mkpkg)
                if okay and deps_newer:
                    mkpkg.result.append(['changed', 'deps', 'deps updated'])
                    msg('Trigger Deps have changed will rebuild\n', ind=1)

                    pkgrel = bump_pkgrel(mkpkg.pkgrel)
                    mkpkg.pkgrel_updated = pkgrel
                    msg(f'Updating pkgrel : {mkpkg.pkgrel} -> {pkgrel}\n', ind=1)
                    okay = set_pkgrel(mkpkg, pkgrel)
                    if okay:
                        needs_build = True
                    else:
                        mkpkg.result.append(['error', 'pkgbuild', 'write new pkgrel'])
                        msg('Failed to update pkgrel\n', fg_col='red')
                else:
                    msg('No new trigger dependencies)\n', ind=1)
                    mkpkg.result.append(['up2date', 'all', 'current'])

            else:
                # pkg file has vers but release doesn't match
                msg('Pkg file matches version but not release - rebuilding\n', fg_col='cyan')
                needs_build = True
                mkpkg.result.append(['changed', 'no-package', 'packge missing'])
        else:
            msg('Pkg file not found - rebuilding\n', fg_col='cyan')
            needs_build = True
            mkpkg.result.append(['changed', 'no-package', 'packge missing'])


    if not needs_build and mkpkg.force:
        needs_build = True
        msg('Force active : Running build\n', ind=1)
        mkpkg.result.append(['changed', 'force', 'rebuild forced'])

    if needs_build:
        msg('Building package with makepkg\n', ind=1)
        mkpkg.build_ok = build_w_makepkg(mkpkg)
        ran_build = True
        if not mkpkg.build_ok:
            msg('Build failed\n', ind=1, fg_col='red')


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
    #   look for package matchin vers-rel (exact_match) or just latest release vers-
    pkg_file_info = check_package_exists(mkpkg)
    #have_package = check_package_exists(mkpkg)

    pkg_vers_changed = False
    if mkpkg.pkgver_updated and mkpkg.pkgver_updated != mkpkg.pkgver:
        pkg_vers_changed = True

    #
    # build if needed
    #
    msg(f'package version: {mkpkg.pkgver} changed {pkg_vers_changed}\n')
    ran_build = _build_if_needed(pkg_vers_changed, pkg_file_info, mkpkg)

    #
    # summarize result (for easy parsing)
    #
    if ran_build:
        if mkpkg.build_ok:
            mkpkg.result.append(['sucess', 'build', 'makepkg succeeded'])
        else:
            mkpkg.result.append(['error', 'build', 'makepkg failed'])
