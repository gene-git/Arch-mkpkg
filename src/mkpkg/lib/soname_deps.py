# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
soname dep
"""
from typing import (Any)
import os

from ._mkpkg_base import MkPkgBase
from .toml import (read_toml_file, write_toml_file)
from .soname import SonameInfo


def to_dict(infos: dict[str, SonameInfo]) -> dict[str, dict[str, Any]]:
    """
    Convert dict[SonameInfo] to dict[dict]
    """
    infos_dict: dict[str, dict[str, str | int | list[str]]] = {}

    for (key, soname_info) in infos.items():
        infos_dict[key] = soname_info.asdict()
    return infos_dict


def from_dict(infos_dict: dict[str, dict[str, Any]]) -> dict[str, SonameInfo]:
    """
    Convert dict[dict] to dict[SonameInfo]
    """
    infos: dict[str, SonameInfo] = {}

    for (key, val) in infos_dict.items():
        infos[key] = SonameInfo(**val)

    return infos


def write_soname_deps(mkpkg: MkPkgBase):
    """
    Save the soname dep info to current working dir
    We could also switch to pickle files and skip
    converting class to dict and back.
    Dict has advantage its human readable.
    """
    if not mkpkg.soname_info:
        return

    pname = os.path.join(mkpkg.cwd, '.mkpkg_dep_soname')

    #
    # dict[SonameInfo] to dict[dict]
    #
    infos_dict = to_dict(mkpkg.soname_info)
    write_toml_file(infos_dict, pname)


def _update_soname_info(infos: dict[str, SonameInfo]):
    """
    Update to newer version
    """
    for (soname, info) in infos.items():
        info.soname = soname
        info.path_vers = info.vers
        vsplit = soname.split('.so.')
        info.vers = vsplit[1]
        info.avail.append(info.vers)


def read_soname_deps(mkpkg: MkPkgBase):
    """
    Read soname deps from cwd
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
