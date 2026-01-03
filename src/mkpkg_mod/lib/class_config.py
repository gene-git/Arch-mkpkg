# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present Gene C <arch@sapience.com>
"""
mkpkg configuration
"""
# pylint: disable=too-many-instance-attributes,too-few-public-methods
from typing import (Any)
import sys
from pathlib import Path
import argparse

from .toml import read_toml_file

type Opt = tuple[str | tuple[str, str], dict[str, Any]]


class MkpkgConf:
    """
    Config and command line options
    """
    def __init__(self):
        self.verb: bool = False
        self.force: bool = False
        self.refresh: bool = False

        self.soname_comp: str = 'keep'
        self.makepkg_args: list[str] = []

        #
        # load any config
        #
        homedir = str(Path.home())
        self.config_file_sys = '/etc/mkpkg/config'
        self.config_file_home = f'{homedir}/.config/mkpkg/config'

        # config dictionary
        conf = _load_configs(self.config_file_sys, self.config_file_home)

        # map config dict to attributes.
        #  - keep them all
        if conf:
            for (opt, val) in conf.items():
                setattr(self, opt, val)

        # command line options
        _parse_args(self)


def _load_configs(config_file_sys: str, config_file_home: str
                  ) -> dict[str, Any]:
    """
    Load and merge system and personal configs
    """
    config_sys = read_toml_file(config_file_sys)
    config_home = read_toml_file(config_file_home)

    conf: dict[str, Any] = {}

    if config_sys:
        conf |= config_sys

    if config_home:
        conf |= config_home

    return conf


def _available_opts(soname_comp: str) -> list[Opt]:
    """
    Available options
    """
    # Command line args
    opts: list[Opt] = []

    opts.append((('-v', '--verb'),
                 {'action': 'store_true',
                  'help': 'More verbose output',
                  }
                 ))

    opts.append((('-f', '--force'),
                 {'action': 'store_true',
                  'help': 'Bump package release and rebuild',
                  }
                 ))

    opts.append((('-r', '--refresh'),
                 {'action': 'store_true',
                  'help': 'Update saved metadata files.',
                  }
                 ))

    txt = f'never, newer, keep, major/minor/last etc ({soname_comp}).'
    opts.append((('-so-comp', '--soname-comp'),
                 {'default': soname_comp,
                  'help': f'soname rebuilds: ({txt})',
                  }
                 ))

    opts.append((('makepkg'),
                 {'nargs': '*',
                  'help': 'All args after -- passed to makepkg.',
                  }
                 ))

    opts.sort(key=lambda item: item[0][0])

    return opts


def _parse_args(conf: MkpkgConf):
    """
    Parse command line options and save into conf class attributes.

    Any options listed after "--" are passed onto makepkg as are any
    unknown options.
    """
    opts = _available_opts(conf.soname_comp)

    par = argparse.ArgumentParser(description='mkpkg')

    for opt in opts:
        opt_list, kwargs = opt
        if isinstance(opt_list, str):
            par.add_argument(opt_list, **kwargs)
        else:
            par.add_argument(*opt_list, **kwargs)

    (our_opts, rest) = par.parse_known_args(sys.argv)

    # our options
    if our_opts:
        opt_dict = vars(our_opts)
        for (key, val) in opt_dict.items():
            setattr(conf, key, val)

    # rest are for makepkg
    if rest and len(rest) > 0:
        rest = rest[1:]
        conf.makepkg_args = rest
