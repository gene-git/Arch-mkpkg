# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
soname dep 
"""
import os
from .toml import (read_toml_file, write_toml_file)
from .soname import SonameInfo

#
# Save / Restore
#
def to_dict(infos):
    """
    Convert dict[SonameInfo] to dict[dict]
    """
    infos_dict = {}
    for (key, val) in infos.items():
        infos_dict[key] = val.dict()
    return infos_dict

def from_dict(infos_dict):
    """
    Convert dict[SonameInfo] to dict[dict]
    """
    infos = {}
    for (key, val) in infos_dict.items():
        info = SonameInfo(**val)
        infos[key] = info
    return infos

def write_soname_deps(mkpkg):
    """
    save the soname dep info to current working dir
    """
    if not mkpkg.soname_info:
        return
    pname = os.path.join(mkpkg.cwd, '.mkpkg_dep_soname')

    #
    # dict[SonameInfo] to dict[dict]
    #
    infos_dict = to_dict(mkpkg.soname_info)
    write_toml_file(infos_dict, pname)

def _update_soname_info(infos):
    """
    Update to newer version
    """
    for (soname, info) in infos.items():
        info.soname = soname
        info.path_vers = info.vers
        vsplit = soname.split('.so.')
        info.vers = vsplit[1]
        info.avail.append(info.vers)

def read_soname_deps(mkpkg):
    """
    read soname deps from cwd
    """
    pname = os.path.join(mkpkg.cwd, '.mkpkg_dep_soname')

    curr_class_vers = SonameInfo().class_vers

    if os.path.exists(pname):
        infos_dict = read_toml_file(pname)


        #
        # update to new soname_info if needed
        #
        info = infos_dict[list(infos_dict.keys())[0]]
        class_vers = info.get('class_vers')

        infos = from_dict(infos_dict)
        if not class_vers or class_vers < curr_class_vers:
            _update_soname_info(infos)

        # all done
        mkpkg.soname_info = infos
