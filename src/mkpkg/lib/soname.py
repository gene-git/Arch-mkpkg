# SPDX-License-Identifier: MIT
# Copyright (c) 2022,2023 Gene C
"""
Support routines for soname library management
"""
import os
import re
import glob
from packaging import version
from .tools import open_file
from .pacman import pacman_query
from .pacman import pac_qi_key
from .toml import read_toml_file
from .toml import write_toml_file

def read_pkginfo(mkpkg):
    """
    After build completes successfully,
    Read .PKGINFO file
    """
    pkgname = mkpkg.pkgname
    pkginfo = None
    pkginfo_file = f'pkg/{pkgname}/.PKGINFO'
    fobj = open_file(pkginfo_file, 'r')
    if fobj:
        pkginfo = fobj.readlines()
        fobj.close()

    return pkginfo

def pkginfo_soname_deps(mkpkg):
    """
    After build completes successfully,
    Extract any soname depends from pkg/xxx/.PKGINFO
     Take the form:
     depend = libfoo.so=1.0-64
    return list of pairs: [s1, s2,...]
        s1 = [libs1, soname1]
        e.g : ['libfoo.so', 1.0] using above example
    """
    pkginfo = read_pkginfo(mkpkg)
    sonames = []
    if not pkginfo:
        return sonames

    for line in pkginfo:
        if not line.startswith('depend'):
            continue
        lsplit = line.split('=')
        lib = lsplit[1].strip()
        if lib.endswith('.so') and len(lsplit) > 2:
            soname=lsplit[2]
            ssplit=soname.rsplit('-',1)
            soname = ssplit[0].strip()
            sonames.append([lib, soname])

    return sonames

def _extract_pkg_owner(result):
    """ parses output of pacman -Qo file """
    pkg = None
    vers = None
    #for line in result.splitlines():
    if 'owned by' in result:
        lsplit = result.split()
        if len(lsplit) > 1:
            vers = lsplit[-1]
            pkg = lsplit[-2]
    return (pkg, vers)

def package_owner(file):
    """
    Find package owner of file - None if not found
    """
    output = pacman_query(['-Qo', file])
    owner = _extract_pkg_owner(output)
    return owner

def file_to_soname(lib, file):
    """
    pull of soname from library file:
    e.g.
        lib = libfoo.so
        file = libfoo.so.1.0
        soname  = X
    """
    soname = None
    remove = f'{lib}.'
    if remove in file:
        # skip lib with no soname
        soname = file.replace(remove, '')
    return soname

def soname_package_owners(sonames):
    """
    Input is list if items, item ~ [lib, soname]
    For each, find package owner(s) of all files lib.soname*
    returns dict keyed by libray name and each libname has dictionary of info :
    -> result = {
          'libbz2.so' : {
                         'soname'   : '1' ,
                         'packages' : {'bzip2' :
                                       {
                                        'vers': '1.0.8-5',
                                        'all_sonames': ['1', '1.0','1.0.8']}
                                       }
                                      }
                          }
            'libfoo.so' : ...
            }

        where libs files are in /usr/lib/
    """
    soname_info = {}
    for [lib, soname] in sonames:
        #libpath = os.path.join('/usr/lib', f'{lib}.{soname}')
        libpath = os.path.join('/usr/lib', f'{lib}')
        tomatch = f'{libpath}*'

        packages = {}
        path_list = glob.glob(tomatch)
        if path_list:
            for lib_path in path_list:
                file = os.path.basename(lib_path)
                file_soname = file_to_soname(lib, file)
                (pkg, vers) = package_owner(lib_path)

                if not pkg in packages:
                    packages[pkg] = {'vers' : vers, 'sonames' : [] }

                if file_soname:
                    packages[pkg]['sonames'].append(file_soname)

        soname_info[lib] = {'soname' : soname, 'packages' : packages }

    return soname_info

def pkginfo_soname_dep_info(mkpkg):
    """
    After build completes successfully,
    Extract any soname depends info from pkg/xxx/.PKGINFO
    returns list of items. Each
       item ~ [package_owner, package_vers, lib, soname ]
    """

    sonames = pkginfo_soname_deps(mkpkg)
    soname_info = soname_package_owners(sonames)
    return soname_info

def pkg_soname_provides(pkg):
    """
    Lookup current soname versions provided by a package
    """
    output = pacman_query(['-Qi', pkg])
    provides = pac_qi_key(output, 'Provides')
    if not provides:
        return None
    provides = provides.split()

    # soname ~ libfoo.so=x-64
    regex = r'^(?P<lib>lib.*\.so)=(?P<soname>[0-9.-]*)$'
    re_soname = re.compile(regex)

    soname_provides = []
    for item in provides:
        dat = re_soname.search(item)
        if not dat:
            continue
        dat_dict = dat.dat.groupdict()
        lib = dat_dict['lib']
        lib = f'lib{lib}'
        soname = dat_dict['soname']
        soname_provides.append([lib, soname])
    return soname_provides


def current_soname_provides(mkpkg):
    """
    Lookup current soname versions for each soname dependency
    """
    if not mkpkg.soname_info:
        return None

    #
    # list of [lib, soname]
    #
    sonames = []
    for (lib, info) in mkpkg.soname_info.items():
        soname = info['soname']
        sonames.append([lib, soname])

    soname_info =  soname_package_owners(sonames)
    return soname_info

#
# soname driving rebuild
#
def _info_to_sonames(info):
    """ extract all sonames from soname_info """
    sonames = []
    if not info:
        return sonames

    packages = info.get('packages')
    if not packages:
        return sonames
    for (_pkg, pkg_info) in packages.items():
        this_sonames = pkg_info.get('sonames')
        if this_sonames:
            sonames += this_sonames
    # large to small
    sonames_sorted = sorted(sonames, key=version.parse,reverse=True)
    return sonames_sorted

def soname_rebuild_needed(mkpkg):
    """
    decide if need rebuild.
    we always search for packages owning the libs -
      (a) lib exists:
            soname - exists - all fine (status - current - advise newer soname avail)
            soname - not available (newe ) -> rebuild (hope works with newer sonames)
            soname - no sonames provided at all.
                     can try rebuild and hope works without sonames
      (b) lib gone - nothing we can do - package is broken - error
    """
    # pylint: disable=R0912
    msg = mkpkg.msg
    soname_info_last = mkpkg.soname_info
    soname_info_curr = current_soname_provides(mkpkg)

    rebuild = False
    for (lib, info_last) in soname_info_last.items():
        this_rebuild = False
        soname_last = info_last['soname']
        sonames_last = _info_to_sonames(info_last)

        info_curr = soname_info_curr.get(lib)
        sonames_curr = _info_to_sonames(info_curr)

        soname_avail = False
        soname_newer = False
        if sonames_curr :
            if soname_last in sonames_curr:
                soname_avail = True
            if sonames_last:
                if version.parse(sonames_curr[0]) > version.parse(sonames_last[0]):
                    soname_newer = True
            else:
                if mkpkg.verb:
                    msg('  No sonames version list from last build\n')

            if not soname_avail:
                msg(f'  {lib} soname gone {soname_last} : have {sonames_curr}\n', fg_col='yellow')
                if mkpkg.soname_build in ('missing', 'newer') :
                    this_rebuild = True

            if soname_newer:
                msg(f'  {lib} has newer soname {sonames_curr[0]} > {sonames_last[0]}\n')
                if mkpkg.soname_build in ('newer'):
                    this_rebuild = True
        else:
            msg(f'{lib} soname {soname_last} - no sonames found.', fg_col='red')
            this_rebuild = True

        if this_rebuild:
            rebuild = True

    if rebuild and mkpkg.soname_build == 'never':
        if mkpkg.verb:
            msg('  Soname rebuild set to never - no rebuild\n')
            rebuild = False

    return rebuild

#
# Save / Restore
#
def write_current_pkg_dep_soname(mkpkg):
    """ save the soname dep info """
    if not mkpkg.soname_info:
        return

    pname = os.path.join(mkpkg.cwd, '.mkpkg_dep_soname')
    write_toml_file(mkpkg.soname_info, pname)

def read_last_pkg_dep_soname(mkpkg):
    """ read thew soname dep info """
    pname = os.path.join(mkpkg.cwd, '.mkpkg_dep_soname')

    if os.path.exists(pname):
        mkpkg.soname_info = read_toml_file(pname)
