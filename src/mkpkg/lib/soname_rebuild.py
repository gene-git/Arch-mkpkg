# SPDX-License-Identifier: MIT
# Copyright (c) 2022,2023 Gene C
"""
soname library management
 - Makes decision whether any new soname library versions 
   require a rebuild of package.
 N.B. we don't use makepkg get sonames:
     - only generates sonames that are explicit in depends() array
     - pays no attention to rpath - only generates the soname-version pair
"""
from .version_compare import check_version_trigger
from .soname import avail_soname_info

def _check_rebuild_needed(msg, comp, info_last, info_avail):
    """
    Private support routine
    Check if this soname has changed and should trigger a rebuild
    Input:
      * msg
      * comp - comparison operator for versions
        * never, newer, keep, comparison
        keep means keep if same version available even if newer

    returns True if rebuild is needed otherwise False
    """
    #
    # check if soname still exists - always rebuild if library no longer available
    #
    still_available = False
    if (info_avail and info_last and info_last.vers and info_avail.vers):
        still_available = info_last.vers in info_avail.avail

    if not still_available:
        msg(f' soname {info_last.path} no longer avail -> rebuild\n')
        return True

    #
    # Are we checking sonames (other than vanished)
    #
    if comp == 'never':
        return False

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
        (nmo, _used, _used) = check_version_trigger(msg, '>', ucomp, avail_vers, last_vers)
        if nmo > 0:
            msg(f' soname {path} : update avail {avail_vers} (or newer)\n')
            return True
    return False

#------------------------------
# Public
#------------------------------
def soname_rebuild_needed(mkpkg):
    """
    decide if any soname changes require package rebuild.

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
        'neverever' - developer option - will turn off rebuild even if needed

      (a) lib exists:
            if 'newer' and avail_mtime > mtime - rebuild
               if soname_older - no rebuild otherwise rebuild
            if vcomp
            soname - exists - all fine (status - current - advise newer soname avail)
            soname - not available (newe ) -> rebuild (hope works with newer sonames)
            soname - no sonames provided at all.
                     can try rebuild and hope works without sonames
      (b) lib gone - nothing we can do - package is broken - rebuild
    """
    msg = mkpkg.msg
    comp = mkpkg.soname_comp

    soname_info_last = mkpkg.soname_info
    soname_info_avail = avail_soname_info(soname_info_last)

    #
    # Check every soname - any one can trigger rebuild
    #
    rebuild = False
    for (_name, info_last) in soname_info_last.items():
        info_avail = soname_info_avail.get(info_last.path)
        if _check_rebuild_needed(msg, comp, info_last, info_avail) :
            rebuild = True

    if rebuild and comp == 'neverever':
        if mkpkg.verb:
            msg('  **Warning: Soname rebuild set to neverever - skip needed rebuild\n')
            rebuild = False
    return rebuild
