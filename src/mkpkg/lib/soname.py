# SPDX-License-Identifier: MIT
# Copyright (c) 2022,2023 Gene C
"""
soname library management
 - get list of all sonames
 n.b. makepkg :
     - only generates sonames that are explicit in depends() array
     - pays no attention to rpath - only generates the soname-version pair
"""
import os
import stat
import glob
from pathlib import (Path, PosixPath)

from typing import (List, Dict)
from pydantic import (BaseModel, FilePath)

from .utils import os_scandir
from .elf_utils import (file_is_elf, sonames_in_elf_file)

class SonameInfo(BaseModel):
    """
    State of soname lib
    """
    path: str = None       # do NOT use FilePath as can be non existent
    mtime: int = -1
    vers: str = None
    avail: List[str] = []

def _split_soname_vers(soname:str) -> (str, str):
    """
    soname is the library name as required by the linked executable.
    strip off the soname version and return base lib name and version
    If the path is a symlink, version is extracted from link target.
    e.g.
      /usr/lib/libxxx.so.2 -> (/usr/lib/libxxx.so, 2)
      If not versioned then returns lib, None

      If so.2 is symlink to so.2.0.0 then vers will be 2.0.0
      And (/usr/lib/libxx.so.2.0.0, 2.0.0) is returned
    """
    #
    # Check has a soname version
    #
    vsplit = soname.split('.so.')
    if len(vsplit) < 2:
        return (soname, None)

    #
    # Check library exists
    #
    if not os.path.exists(soname):
        return (soname, None)

    #
    # Check if symlink
    # and get version of library file
    # NB. A versioned sym link should always have versioned target
    # But, in weird case where target has no version we use link version
    #
    vers = vers_soname = vsplit[1]
    libso = soname
    ppath = PosixPath(libso)
    if Path.is_symlink(ppath):
        libso = str(Path.resolve(ppath))
        vsplit = libso.split('.so.')
        if len(vsplit) < 2:
            libso = soname
            vers = vers_soname
        else:
            vers = vsplit[1]

    return (libso, vers)

def generate_soname_info(sonames: List[FilePath]) -> Dict[FilePath, SonameInfo]:
    """
    Input is list if libraris,
        e.g. [/usr/lib/libz.so.1, /usr/lib/libxxx.so.nnn]

    No package should have more than 1 version of soname library.
    If this happens we keep the smallest and force rebuild
    For each, find available versions
    returns dict keyed by name and each libname has dictionary of info :

    To handle mulitple versions keep use library path as key
    If the library is a symlink, vers refers to the link target file.
    That way if multiple symlinks point to same actual file they will be
    correctly treated as the same.

    result = {
            '/usr/lib/libbz2.so.1' : {
                         'path' : /usr/lib/libbz2.1.0'
                         'mtime' : xxx (secs)
                         'vers'   : '1' ,
                         'avail' : ['1', '1.0','1.0.8']
                         }
            '/usr/lib/libfoo.so.22' : ...
           }
    """
    infos = {}
    for path in sonames:
        # if path is symlink then libpath is target file
        (libpath, version) = _split_soname_vers(path)
        if not version:
            continue
        libpath_base = libpath.split('.so.')[0]

        mtime = -1
        if os.path.exists(libpath):
            mtime = os.path.getmtime(libpath)

        # Get all avail versions
        tomatch = f'{libpath_base}.*'
        avail = []
        path_list = glob.glob(tomatch)
        for lib in path_list:
            (_libpath, vers) = _split_soname_vers(lib)

            if vers and vers not in avail:
                avail.append(vers)

        info_dict = {'path' : libpath,
                     'mtime' : mtime,
                     'vers' : version,
                     'avail' : avail
                     }
        soname_info = SonameInfo(**info_dict)
        infos[path] = soname_info

    return infos


def _find_all_elf_executables(dirname:str) -> [str]:
    """
    Make list of all executables and list of soname libs they are using
    creates list of tuples: (/usr/lib/libressl/libssl.so.56, 56)
    output:
        [(libpath, version), (libpath, version), ... ]
    """
    scan = os_scandir(dirname)
    if not scan:
        return []

    elf_files = []
    for item in scan:
        if item.is_file() and file_is_elf(item.path):
            mode = os.stat(item.path).st_mode
            executable = bool(mode & (stat.S_IXUSR | stat.S_IXGRP| stat.S_IXOTH))
            if executable:
                elf_files.append(item.path)
        elif item.is_dir():
            elf_files += _find_all_elf_executables(item.path)
    scan.close()
    return elf_files

def _find_all_sonames(dirname:str) -> [str]:
    """
    Generate list of sonames from list of elf executables
     list of sonames, each item is:
     library path
      e.g. (/usr/lib/libz.so.1)
    """
    elf_files = _find_all_elf_executables(dirname)
    if not elf_files:
        return []

    sonames = []
    for file in elf_files:
        these_sonames = sonames_in_elf_file(file)
        if these_sonames:
            sonames += these_sonames
            sonames = list(set(sonames))
    return sonames

#----------------------
# public
#----------------------

def get_current_soname_info(pkgdir:str) -> dict:
    """
    Generate soname_info from all elf executables in
    found in pkgdir
    """
    if not os.path.isdir(pkgdir):
        return None

    sonames = _find_all_sonames(pkgdir)
    soname_info = generate_soname_info(sonames)
    return soname_info

def avail_soname_info(last_soname_info:dict) -> dict:
    """
    Lookup current soname info for each soname when last built
    """
    if not last_soname_info:
        return {}
    #
    # Make list of sonames and refresh soname_info
    # Check uses actual path not soname
    sonames = list(last_soname_info.keys())
    sonames = []
    for (_name, info) in last_soname_info.items():
        if info and info.path and info.path not in sonames:
            sonames.append(info.path)
    avail_info =  generate_soname_info(sonames)
    return avail_info
