.. SPDX-License-Identifier: GPL-2.0-or-later

========
Appendix
========

.. _metadata:

Metadata Files
==============

mkpkg keeps metadata information in files. These files are in the same directory as the PKGBUILD file:

* **.build-info**:         last version built
* **.build_time**:         time and status of last build
* **.mkpkg_dep_soname**:   list of all shared libraries and sonames
* **.mkpkg_dep_vers**:     list of triggger pacakges and versions last built against

How mkpkg works
===============

Outline of what it does

* If PKGBUILD has a pkgver() function, check if the pkgver variable matches its output

* If the 2 pkgver match or if there is no pkgver() function then check if a matching package exists

* If package not up to date, then run makepkg build.

* If package seems otherwise up to date, then check if any of the conditions given by
  *mkpkg_depends* or *mkpkg_depends_files* triggers a build.  If a build is called for,
  then bump the pkgrel and rebuild.

* If the package is out of date, as there is newer version then reset pkgrel back to "1" and build.

So, if a package builds and gets larger package release number, it was because of some trigger package
dependency; absent manual modification.  If package release is "1" - then you know its a fresh package version.

I use separate tool to run all my package builds so I prefer the output to be easily parseable and provide
simple and clear information to feed the builder too.

mkpkg thus prints a line of the form::

    *mkp-status: <status> <package-version>*

Where status is one of :

 * **current** -> package is up to date
 * **success** -> package was built successfully
 * **error**   -> problem occurred.

Obviously, package-version is what is sounds like.

It is possible for mkpkg itself to fail for some reason, in which case the *mkp-status:* line could be absent.
This is also simple to detect programatically.


Installation
============

Available on

* `Github-mkpkg <https://github.com/gene-git/Arch-mkpkg>`_
* `Archlinux AUR <https://aur.archlinux.org/packages/mkpkg>`_

On Arch you can build using the provided PKGBUILD in the packaging directory or from the AUR.
All git tags are signed with arch@sapience.com key which is available via WKD
or download from https://www.sapience.com/tech. Add the key to your package builder gpg keyring.
In PKGBUILD use source= line with *?signed* at the end. You can also manually verify the signature

To build manually, clone the repo and::

    ./scripts/do-build
    ./scripts/do-install <destination-directory>

Dependencies
============

- Run Time:
  - python (3.14 or later)
  - pyalpm
  - python-tomli-w
  - python-pyelftools
  - python-pyconcurrent

- Building Package :

  - git
  - meson
  - meson-python
  - rsync
  - bash

Created by Gene C. and licensed under the terms of the GPL-2.0-or-later license.

* SPDX-License-Identifier: GPL-2.0-or-later  
* SPDX-FileCopyrightText: © 2022-present Gene C <arch@sapience.com>


Some history
============

Version 6.0.0
-------------

 * soname rewrite
   
   New argument for how soname changes are treated : *-so-comp, --soname-comp*. 

   Can be *<compare>*, *newer*,  *never* or key how to compare the soname versions. 
   The comparison types are the same as for package dependencies described above.
   Default is *last* which means the entire soname version will be compared to 
   whats available and rebuild will be triggered if a later version now available.

   *<compare>* e.g. *>major* or *>minor*' or *last* etc. 
   If the last built soname was 5.1, and now available is 5.2 then
   *minor* and *last* will trigger rebuild while *major* would not. *newer* triggers if the
   last modify time of the library is newer.

   Previous version used sonmaes produced by makepkg - however this only generates
   sonames if they are listed as dependencies. We want to get every soname - so 
   we started over from scratch. By using our own soname generate we catch
   every soname and its absolute path - this enables us to correctly treat soname
   changes. This approach will also correctly deal with any *rpath* loader flags
   causing executable to use shared library from path(s) specified at compile time.


Version 4.1.0
-------------

 * Arguments  

    Change in argument handling. Arguments to be passed to *makepkg* must now follow *--*.
    Arguments before the double dash are used by mkpkg itself. To keep backward
    compatibility the older *--mkp-* style arguments are honored, but the newer simpler
    ones are preferred. e.g. *-v, --verb* for verbose. Help availble via *-h*. 


 * Config file now available.

   Configs are looked for in /etc/mkpkg/config then ~/.config/mkpkg/config. It should
   be in TOML format. e.g. to change the default soname rebuild option::

        soname_comp = "newer"

Version 4.0.0
-------------

 * Soname drive rebuilds.  

   Adds support for detecting missing soname libraries, and triggering rebuild.
   If soname is found then no rebuild is done. Typically happens when
   older soname is deprecated.

 * Adds new option *--mkp-refresh*.  

   Attempts to update saved metadata files. Faster, if imperfect, alternative to rebuild.
   

