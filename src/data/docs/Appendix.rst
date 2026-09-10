.. SPDX-License-Identifier: GPL-2.0-or-later

========
Appendix
========

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
   

Older
-----

Adds support for epoch.

Version 2.x.y brings fine grain control by allowing package dependences to trigger 
builds using semantic version. For example 'python>minor' will rebuild only if a new
python package has it's major.minor greater than what it was when package was last built.
See *_mkpkg_depends* below for more detail. 

The source has been reorganized and packaged using poetry which simplifies installation.
The installer script, callable from package() function in PKGBUILD has been updated 
accordingly. Ther build() function uses python build module to generate the
wheel package, as outlined above.

Changed the PKGBUILD variables to have underscore prefix to follow Arch Package Guidelines.
Variables are now: *_mkpkg_depends* and *_mkpkg_depends_files*. 
The code is backward compatible and supports the previous variable names without the 
leading "\_" as well as the ones with the "\_".

Now also available on aur.

