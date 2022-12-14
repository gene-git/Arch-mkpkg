# SPDX-License-Identifier: MIT
# Copyright (c) 2022,2023 Gene C
"""
mkpkg configuration
"""
import sys
from pathlib import Path
import argparse
from .toml import read_toml_file

class MkpkgConf:
    """ config options """
    # pylint: disable=R0903

    def __init__(self):
        self.verb = False
        self.force = False
        self.refresh = False
        self.use_makedepends = False    # deprecated
        self.soname_build = 'missing'
        self.makepkg_args = None

        #
        # load any config
        #
        homedir = str(Path.home())
        self.config_file_sys = '/etc/mkpkg/config'
        self.config_file_home = f'{homedir}/.config/mkpkg/config'

        config_sys = read_toml_file(self.config_file_sys)
        config_home = read_toml_file(self.config_file_home)
        conf = {}
        if config_sys:
            conf |= config_sys
        if config_home:
            conf |= config_home

        # map dict to attributes - Read them all
        if conf:
            for (opt,val) in conf.items():
                setattr(self, opt, val)

        # Command line args
        opts = [
                [('-v', '--verb', '--mkp-verb'),
                 {'help' : 'More verbose output'}
                ],
                [('-f', '--force', '--mkp-force'),
                 {'help' : 'Force makepkg to be run (may want -f to makepkg)',
                  'action'      : 'store_true'}
                ],
                [('-r', '--refresh', '--mkp-refresh'),
                 {'help' : 'Force makepkg to be run (may want -f to makepkg)',
                  'action'      : 'store_true'}
                ],
                [('-so-bld', '--mkp-soname-build'),
                 {'help' : f'Rebuild if soname missing, newer, never (default {self.soname_build})'}
                ],
                [('--mkp-use_makedepends'),
                 {'help' : 'Use makedepends array of no _mkpkg_xxx set (deprecated))',
                  'action'      : 'store_true'}
                ],
                [('makepkg'),
                 {'help' : 'All remaining args after -- passed to makepkg',
                  'nargs' : '*'}
                ],
               ]
        par = argparse.ArgumentParser(description='mkpkg')
        for opt in opts:
            (opts), kwargs = opt
            if isinstance(opts, tuple):
                par.add_argument(*(opts), **kwargs)
            else:
                par.add_argument(opts, **kwargs)

        (our_opts, rest) = par.parse_known_args(sys.argv)

        #
        # Save rest of options to pass to makepkg
        #
        if rest and len(rest) > 0:
            rest = rest[1:]
            self.makepkg_args = rest

        if our_opts:
            opt_dict = vars(our_opts)
            if opt_dict.get('makepkg'):
                del opt_dict['makepkg']
            for (opt, val) in opt_dict.items():
                setattr(self, opt, val)
