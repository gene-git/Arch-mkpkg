#
# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2026 Gene C <arch@sapience.com>
#

project('mkpkg', ['c'],
  version: files('src/version.txt'),
  meson_version: '>=1.10.0',
  default_options: [
    'c_std=c23',
    'warning_level=3',
    'b_pie=true',
    'prefix=/usr',
    'mandir=share/man',
    ],
)

d_etc = get_option('sysconfdir')
d_lib = get_option('libdir')
d_bin = get_option('bindir')
d_man = get_option('mandir')
d_share = get_option('datadir')

py_mod = import('python')
py = py_mod.find_installation(pure: false)
proj_root = meson.project_source_root()
py_dep = py.dependency(embed: true)

inc_dir = []
lib_sources = []

#
# top-level files
#

#
# Python submodules
#
subdir('src/mkpkg_mod')

#
# Deps
#

#
# Executables
#
configure_file(
  input: 'src/mkpkg_mod/apps/mkpkg.py',
  output: 'mkpkg',
  copy: true,
  install_dir: d_bin,
  install_mode: 'rwxr-xr-x'
)

#
# Install
#
s_etc_scripts = 'src/scripts'
s_scripts = './scripts'
s_license = 'src/data/license'
s_changelog = 'src/data/changelog'
s_docs = 'src/data/docs'
s_configs = 'configs'
manual = 'mkpkg.pdf'

# 
# /usr/share/mkpkg/docs
# 
install_data(
  [
    s_docs / manual,
  ],
  install_dir: d_share / 'mkpkg/docs'
)

install_subdir(
  [
    s_docs / 'html',
  ],
  install_dir: d_share / 'mkpkg/docs',
  strip_directory: false
)

# 
# /usr/share/mkpkg 
# 
install_data(
  [
    'README.rst',
    s_changelog / 'Changelog.rst',
    'packaging/PKGBUILD',
    'packaging/.nvchecker.toml',
    'packaging/Changelog',
  ],
  install_dir: d_share / 'mkpkg'
)

# 
# /usr/share/licenses/mkpkg 
# 
install_data(
  [
    s_license / 'License-gpl-2.0.txt',
    s_license / 'License.rst',
  ],
  install_dir: d_share / 'licenses/mkpkg'
)

