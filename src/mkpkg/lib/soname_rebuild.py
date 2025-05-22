# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
soname library management

 - Makes decision whether any new soname library versions
   require a rebuild of package.
N.B. we don't use makepkg get sonames:
 - only generates sonames that are explicit in depends() array
 - pays no attention to rpath - only generates the soname-version pair
"""
from collections.abc import (Callable)
from .version_compare import check_version_trigger
from .soname import avail_soname_info
from .soname import SonameInfo
from ._mkpkg_base import MkPkgBase


def _check_rebuild_needed(msg: Callable[..., None],
                          comp: str,
                          info_last: SonameInfo,
                          info_avail: SonameInfo):
    """
    Check if this soname should trigger a rebuild.

    Input:
      Rebuild rules
      If the soname is no longer available - then rebuild is forced.

      comp -  comparison operator for versions

        keep:
         this is the default and is generally how sonames are used
         no abi change so fine to keep using the library.
         if 'soname version' from last build is available do nothing

        newer:
         if there is a newer (timestamp) soname library rebuild

        <comp_op>
          This compares actual library versions not just the soname.
          operators are same as for package versions, major, minor etc

    Returns True if rebuild is needed otherwise False
    """
    #
    # check if soname exists - rebuild if library no longer available
    #
    available = False
    if info_avail and info_last and info_last.vers and info_avail.avail:
        available = info_last.vers in info_avail.avail

    if not available:
        msg(f' soname {info_last.path} no longer avail -> rebuild\n')
        return True

    #
    # Are we checking sonames (other than vanished)
    #
    if comp == 'keep':
        return False

    path = info_last.path
    if comp == 'newer':
        #
        # check if name itself is newer
        #
        if info_last.mtime < info_avail.mtime:
            msg(f' soname {path} : newer avail\n')
            return True
        #
        # newer by version comparison
        #
        ucomp = 'last'
    else:
        # user provided how to compare versions
        ucomp = comp

    #
    # check any available version greater than last
    #
    last_vers = info_last.vers
    for avail_vers in info_avail.avail:
        #
        # nmo = new - old : > 0 means rebuild
        #
        (nmo, _used, _used) = check_version_trigger(msg, '>', ucomp,
                                                    avail_vers, last_vers)
        if nmo > 0:
            msg(f' soname {path} : update avail {avail_vers} (or newer)\n')
            return True
    return False


# ------------------------------
#       Public
# ------------------------------
def soname_rebuild_needed(mkpkg: MkPkgBase) -> bool:
    """
    Decide if any soname changes require package rebuild.

    We need:
     - last_soname_deps (as of build)
     - avail_soname_deps for each prev soname

    soname_comp:
     if vers not avail - always try rebuild

     'never' - nothing to do (after still avail check)
     'keep'  - keep if soname is available regardless of modify time
     'newer' - Same as keep unless mtime is newer - then rebuild
     'vcomp'
       if avail > vers - rebuild
       if avail = vers nothing to do
       'neverever' - developer option - turn off rebuild even if needed

     lib exists:
       if 'newer' and avail_mtime > mtime - rebuild
       if soname_older - no rebuild otherwise rebuild
       if vcomp
         soname exists - all fine
                status - current - advise newer soname avail
         soname not available (newer) -> rebuild
                hope works with newer sonames
         soname no sonames provided at all.
                can try rebuild and hope works without sonames

      lib gone - nothing we can do - package is broken - rebuild
    """
    msg = mkpkg.msg
    comp: str = mkpkg.soname_comp

    soname_info_last = mkpkg.soname_info
    soname_info_avail = avail_soname_info(soname_info_last)

    #
    # Check every soname - any one can trigger rebuild
    #
    rebuild = False
    for (_name, info_last) in soname_info_last.items():
        info_avail = soname_info_avail.get(info_last.soname)
        if info_avail:
            rebuild = _check_rebuild_needed(msg, comp, info_last, info_avail)
        else:
            rebuild = True

    if rebuild and comp == 'neverever':
        if mkpkg.verb:
            txt = 'Soname rebuild set to neverever - skip needed rebuild'
            msg(f'  **Warning: {txt}\n')
            rebuild = False
    return rebuild
