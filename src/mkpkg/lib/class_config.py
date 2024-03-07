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
    # pylint: disable=too-many-instance-attributes,too-few-public-methods

    def __init__(self):
        self.verb = False
        self.force = False
        self.refresh = False

        self.soname_comp = 'last' # was previously soname_build
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

        opts = get_available_opts(self)
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

def get_available_opts(conf) -> [[tuple, dict]]:
    """
    Available options
    """
    # Command line args
    opts = []
    act = 'action'
    act_on = 'store_true'

    ohelp = 'More verbose output'
    opt = [('-v', '--verb'), {'help' : ohelp, act : act_on}]
    opts.append(opt)

    ohelp = 'Bump package release and rebuild'
    opt = [('-f', '--force'), {'help' : ohelp, act : act_on}]
    opts.append(opt)

    ohelp = 'Update saved metadata files.'
    opt = [('-r', '--refresh'), {'help' : ohelp, act : act_on}]
    opts.append(opt)

    default = conf.soname_comp
    ohelp = 'When soname rebuilds: never, newer, keep or major/minor/last etc (default {default})'
    opt = [('-so-comp', '--soname-comp'), {'help' : ohelp, act : act_on, 'default' : default}]
    opts.append(opt)

    ohelp = 'All remaining args after -- passed to makepkg'
    opt = [('makepkg'), {'help' : ohelp, 'nargs' : '*'}]
    opts.append(opt)

    return opts
