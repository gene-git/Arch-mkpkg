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
     - soname is just the soname path (/usr/lib/libfoo.so.1) 
     - soname_vers is it's associated version   (1)
     - path is the actual library being used    (/usrlib.foo.so.1.1.0)
     - path_vers is its version                 (1.1.0)
     - avail list of all available versions     (1, 1.1.0, 1.2.0, ...)
     do NOT use FilePath for soname/path since it may not exist
    """
    soname: str = None
    vers: str = None
    path: str = None
    path_vers: str = None
    mtime: int = -1
    avail: List[str] = []
    class_vers: int = 1

def _split_soname_vers(soname:str) -> (str, str):
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
        return (soname, None, None)

    #
    # Check library exists
    #
    if not os.path.exists(soname):
        return (soname, None, None)

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

def generate_soname_info(sonames: List[FilePath]) -> Dict[FilePath, SonameInfo]:
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
    # pylint: disable=too-many-locals
    infos = {}
    for soname in sonames:
        # if soname is symlink (usual case) then libpath is target file
        (libpath, soname_vers, libpath_vers) = _split_soname_vers(soname)
        if not soname_vers:
            # not a soname
            continue

        #
        # timestamp (could also use soname path here)
        #
        mtime = -1
        if os.path.exists(libpath):
            mtime = os.path.getmtime(libpath)

        #
        # Get all avail versions
        #
        libpath_base = libpath.split('.so.')[0]

        tomatch = f'{libpath_base}.*'
        avail = []
        path_list = glob.glob(tomatch)
        for lib in path_list:
            # ignore any sym link in list if it doesn't point to actual library
            if not os.path.exists(lib):
                continue

            # add soname and lib_vers to avail list
            (libpath, this_soname_vers, this_lib_vers) = _split_soname_vers(lib)

            if this_soname_vers and this_soname_vers not in avail:
                avail.append(this_soname_vers)

            if this_lib_vers and this_lib_vers not in avail:
                avail.append(this_lib_vers)

        #
        # update soname_info
        #
        info_dict = {'soname' : soname,
                     'vers' : soname_vers,
                     'path' : libpath,
                     'path_vers' : libpath_vers,
                     'mtime' : mtime,
                     'avail' : avail
                     }
        soname_info = SonameInfo(**info_dict)
        infos[soname] = soname_info

    return infos


def _find_all_elf_executables(dirname:str) -> [str]:
    """
    Recursively find every executable and return
    as a list of paths to each one.
    Output is a list of paths : 
        [exe1, exe2, exe3, ... ]
    exeN ~ dirname/x/y/foo
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
    Generate unique list of sonames from list of all elf executables
    Output is list of full paths of each library:
      e.g. 
         [/usr/lib/libz.so.1, /usr/lib/libxxx.so.n, ...]
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
    Generate soname info from all elf executables in
    found in pkgdir. 
    Output is a dictionary of SonameInfo - key is soname path
    from executable and value is it's SonameInfo instance
    """
    if not os.path.isdir(pkgdir):
        return None

    sonames = _find_all_sonames(pkgdir)
    soname_info = generate_soname_info(sonames)
    return soname_info

def avail_soname_info(last_soname_info:dict) -> dict:
    """
    Lookup current soname info for each soname in last_soname_info - 
    Input dict of SonameInfo from last build 
    input: dictionary of soname info as returned by generate_soname_info
    output: refreshed dict of same sonames as of now
    """
    if not last_soname_info:
        return {}
    #
    # Make list of sonames and refresh soname_info
    # Check uses actual path not soname
    sonames = list(last_soname_info.keys())
    #sonames = []
    #for (_name, info) in last_soname_info.items():
    #    if info and info.path and info.path not in sonames:
    #        sonames.append(info.path)
    avail_info =  generate_soname_info(sonames)
    return avail_info
