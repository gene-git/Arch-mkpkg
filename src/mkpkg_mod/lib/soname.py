# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present Gene C <arch@sapience.com>
"""
soname library management.

get list of all sonames
n.b. makepkg :
  - only generates sonames that are explicit in depends() array
  - pays no attention to rpath - only generates the soname-version pair
"""
# pylint: disable=too-many-locals
import os
import stat
import glob
from pathlib import (Path, PosixPath)

from .elf_utils import (file_is_elf, sonames_in_elf_file)
from .soname_info import SonameInfo


def _split_soname_vers(soname: str) -> tuple[str, str, str]:
    """
    soname is the library name as required by the linked executable.
    Identify the soname version and the actual library path and it's
    version. Usually soname is a symlink to actual library path
    Returns:
        (libpath, soname_version, libpath_version)

    e.g.
      /usr/lib/libxxx.so    -> (/usr/lib/libxxx.so, None, None)

      /usr/lib/libxxx.so.2
        - not symlink       -> (/usr/lib/libxxx.so.2, 2, 2)
        - link to so.2.0.0  -> (/usr/lib/libxx.so.2.0.0, 2, 2.0.0)
    """
    #
    # Check has a soname version
    #
    vsplit = soname.split('.so.')
    if len(vsplit) < 2:
        return (soname, '', '')

    #
    # Check library exists
    #
    if not os.path.exists(soname):
        return (soname, '', '')

    #
    # Check if symlink (get link target) and get version of library file
    # NB. A versioned sym link should always have versioned target
    #
    libpath_vers = vers_soname = vsplit[1]
    libpath = soname
    ppath = PosixPath(libpath)
    if Path.is_symlink(ppath):
        libpath = str(Path.resolve(ppath))
        vsplit = libpath.split('.so.')
        if len(vsplit) < 2:
            libpath = soname
            libpath_vers = vers_soname
        else:
            libpath_vers = vsplit[1]

    return (libpath, vers_soname, libpath_vers)


def generate_soname_info(sonames: list[str]) -> dict[str, SonameInfo]:
    """
    Input is list if libraris,

    e.g. [/usr/lib/libz.so.1, /usr/lib/libxxx.so.nnn]

    No package should have more than 1 version of soname library.
    By keeping the dictionary key the full library path we handle
    this (odd) case anyway.

    For each library, also find available versions
    and return dict keyed by library as seen by executable.

    If the library is a symlink, vers refers to the link target file.
    That way if multiple symlinks point to same actual file they will be
    correctly treated as the same - which they obviously are.

    path is the absolute library path that is actually used.

    Result is dictionary of SonameInfo class instances.

    {
      '/usr/lib/libbz2.so.1' : SonameInfo(libz2s.o.1)
      '/usr/lib/libfoo.so.22' : ...
    }
    """
    infos: dict[str, SonameInfo] = {}

    for soname in sonames:
        # if soname is symlink (usual case) then libpath is target file
        (libpath, soname_vers, libpath_vers) = _split_soname_vers(soname)
        if not soname_vers:
            continue

        #
        # timestamp (could use soname path)
        #
        mtime = -1
        if os.path.exists(libpath):
            mtime = int(os.path.getmtime(libpath))

        #
        # Get all avail versions
        #
        libpath_base = libpath.split('.so.')[0]

        avail: list[str] = []

        tomatch = f'{libpath_base}.*'
        path_list = glob.glob(tomatch)

        for lib in path_list:
            #
            # ignore any sym link in list if it doesn't point to actual library
            #
            if not os.path.exists(lib):
                continue

            #
            # add soname and lib_vers to avail list
            #
            (libpath, this_soname_vers, this_lib_vers) = (
                    _split_soname_vers(lib)
                    )

            if this_soname_vers and this_soname_vers not in avail:
                avail.append(this_soname_vers)

            if this_lib_vers and this_lib_vers not in avail:
                avail.append(this_lib_vers)

        #
        # update soname_info
        #
        soname_info = SonameInfo(soname=soname,
                                 vers=soname_vers,
                                 path=libpath,
                                 path_vers=libpath_vers,
                                 mtime=mtime,
                                 avail=avail,
                                 class_vers=1)
        infos[soname] = soname_info

    return infos


def _find_all_elf_executables(dirname: str) -> list[str]:
    """
    Recursively find every executable and return
    a list of paths to each one.

    Output is a list of paths :
        [exe1, exe2, exe3, ... ]
    exeN ~ dirname/x/y/foo
    """
    elf_files: list[str] = []

    if not (os.path.exists(dirname) and os.path.isdir(dirname)):
        return elf_files

    try:
        scan = os.scandir(dirname)

    except OSError:
        return elf_files

    mode_executable = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH

    for item in scan:
        if item.is_file() and file_is_elf(item.path):
            mode = os.stat(item.path).st_mode
            executable = bool(mode & mode_executable)
            if executable:
                elf_files.append(item.path)
        elif item.is_dir():
            elf_files += _find_all_elf_executables(item.path)
    scan.close()

    return elf_files


def _find_all_sonames(dirname: str) -> list[str]:
    """
    Generate unique list of sonames from list of all elf executables.

    Output is list of full paths of each library:
      e.g.
         [/usr/lib/libz.so.1, /usr/lib/libxxx.so.n, ...]
    """
    sonames: list[str] = []

    elf_files = _find_all_elf_executables(dirname)
    if not elf_files:
        return sonames

    for file in elf_files:
        these_sonames = sonames_in_elf_file(file)
        if these_sonames:
            sonames += these_sonames
            sonames = list(set(sonames))
    return sonames


# ----------------------
#   public
# ----------------------
def get_current_soname_info(pkgdir: str) -> dict[str, SonameInfo]:
    """
    Generate soname info from all elf executables in
    found in pkgdir.
    Output is a dictionary of SonameInfo - key is soname path
    from executable and value is it's SonameInfo instance
    """
    soname_info: dict[str, SonameInfo] = {}
    if not os.path.isdir(pkgdir):
        return soname_info

    sonames = _find_all_sonames(pkgdir)
    soname_info = generate_soname_info(sonames)
    return soname_info


def avail_soname_info(last_soname_info: dict[str, SonameInfo]
                      ) -> dict[str, SonameInfo]:
    """
    Lookup current soname info for each soname in last_soname_info -
    Input dict of SonameInfo from last build
    input: dictionary of soname info as returned by generate_soname_info
    output: refreshed dict of same sonames as of now
    """
    avail_info: dict[str, SonameInfo] = {}
    if not last_soname_info:
        return avail_info
    #
    # Make list of sonames and refresh soname_info
    # Check uses actual path not soname
    #
    sonames = list(last_soname_info.keys())

    avail_info = generate_soname_info(sonames)
    return avail_info
