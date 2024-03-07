# SPDX-License-Identifier: MIT
# Copyright (c) 2022,2023 Gene C
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

def read_soname_deps(mkpkg):
    """
    read soname deps from cwd
    """
    pname = os.path.join(mkpkg.cwd, '.mkpkg_dep_soname')

    if os.path.exists(pname):
        infos_dict = read_toml_file(pname)
        mkpkg.soname_info = from_dict(infos_dict)
