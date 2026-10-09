.. SPDX-License-Identifier: GPL-2.0-or-later

=====
mkpkg
=====

Synopsis
========

Tool to rebuild Arch packages triggered by changes in specified dependencies.

Overview
========

By default Arch packages are rebuilt when the package version changes. This 
happens when the tool has an update or by incrementing the package "release" number
which forces a rebuild. 

It would be helpful to rebuild when something the package depends on has
changed in a way that requires a rebuild. This might be a new shared library
or a major version bump in something that is used by the package. It could be
be a systemd service file provided by the packager.

This is where *mkpkg* can be useful. It helps automate rebuilds when
something the package depends on has changed in a way that requries
a fresh build, even when the package itself has not changed.

mkpkg uses a list of triggers that it uses to decide when a rebuild 
is required. Some triggers are automatic like shared library soname versions
while others are provided by the packager.

The list of provided triggers is read from the variable *_mkpkg_depends* 
in the PKGUILD. This should contain a list of files or packages.
When mkpkg detects a change in one or more of these it bumps the package
release number and rebuilds the package. 

Of course if there is a change in the actual package itself, then the package 
is rebuilt anyway for the new version, independent of any changes in dependencies.

If you have ever needed to rebuild a package by manually bumping the release version, then
something is less than ideal. If something requires a rebuild, other than 
the package itself having an update, it should happen automatically.

A rebuild is triggered when a trigger file changes or if a package changes.
package changes can limited by it's version. For example the trigger::

    'python>major'

causes a rebuild when Python's major version changes. Similarly::

    'python>minor'

triggers a rebuild when the minor version changes.

Once run is complete mkpkg outputs::

    mkp-status: <status> <package-version>

Which is designed to be easily parsed programmatically. Useful when tools are
used to run all the builds. Status is one of current, success, or error.
Current means packaghe is up to date while success means package was built successfully.

Documentation
-------------

The manual, in both HTML and PDF formats, is installed under */usr/share/mkpkg/docs*.
and also available at: `readthedocs <https://arch-mkpkg.readthedocs.io>`_.

Signed Source
-------------

All git tags are signed with arch@sapience.com key which is available via WKD
or download from https://www.sapience.com/tech. Add the key to your package builder gpg keyring.
The key is included in the Arch package and the source= line with *?signed* at the end can be used
to verify the git tag.  You can also manually verify the signature
using manually verify using *git tag -v <tag-name>*

Triggers Introduction
=====================

Triggers are discussed in detail in :ref:`mkpkg-triggers`.

mkpkg allows you to define a set of event rules that trigger a rebuild. 
A rule might be a new version of a package or a change in a file.

The packager is responsible for providing the list of triggers.
Other than changes in *sonames*, which are handled automatically.

Triggers are given by a PKGBUILD array variable.

This example leads to a rebuild if either systemd or openssl is updated::

    _mkpkg_depends=(openssl systemd)

While this one only rebuild when python package has a minor (or major) version change:

    _mkpkg_depends=('python > minor')


In this example changes to the service file tigger a reubild::

        _mkpkg_depends_file=('xxx.service')
        
Thus ensuring that the new service file is packaged.

An additional little benefit, if packages are up to date then running mkpkg is significantly
faster than makepkg; it can be something like 10x faster or even more.  

Background Motivation 
=====================

mkpkg has one run-time dependency,  python. 

It uses makepkg to perform the actual package builds in the usual way. That said,  makepkg is 
a part of pacman which is always installed and thus not a *dependency* as far
as PKGBUILD is concerned.

When a tool chain used to build a package is updated, it's good practice, IMHO, to 
rebuild packages which use that tool chain.  For example, when gcc, cargo, binutils et al are updated 
packages using those tools should also be updated.  It is standard practice to rebuild and 
test kernel packages when the build toolchain is updated. The same is true for many other
packages.

This ensures that things compile and work properly with the new build tools and 
may be critical in reducing an attack surface. 
A little example, as of time of writing, not to pick on cargo, is `CVE-2022-36113`_

.. _`CVE-2022-36113`: https://nvd.nist.gov/vuln/detail/CVE-2022-36113

Of course this would require a case where cargo is actually downloading something which
should never be permitted; still, it's a conceivable danger.

While static linked libraries surely don't demand a rebuild to function, obviously, because 
the older library is part of the binary itself, it's still a good idea to rebuild it. 
This will pick up bug fixes, including security related ones, as well as improvements.  Of course,
it's always sensible to confirm that an application properly builds and works with 
the newer tool or library as well.

It is also helpful to know as early as possible that a package continues to build and pass 
all it's tests when things it depends on change.

Obviously it makes more sense to set up the rules that should lead to rebuilding a
package rather than relying on human judgement. Since the triggers are known in advance
it makes perfect sense to automate this.

A small comment on shared libraries. While these are generally not a problem, 
there is an assumption that the library itself still functions the same for whatever part 
of it the tool is using.  

The majority of providers are careful with *sonames* as well, so most of the time 
that's likely true, however, the cautious among us may want to run regression 
tests even in this case. 

Certainly for mission critical tools. Bugs happen, and it's good to 
learn about any issues as soon as possible.  

But there are indeed some shared library packages, some with dynamically loaded 
libraries (plugins) that may also be trigger packages.  One symptom of that need are those
packages that are manually rebuilt by forcing a release version bump typically with a comment
such as *rebuilt with latest ...* - we see plenty of that happening.

Getting Started
===============

Edit the PKGBUILD and add a *_mkpkg_depends* variable with a list of triggers that
should cause a rebuild when the condition is met. Triggers are discussed in 
in detail (:ref:`mkpkg-triggers`), but a simple example is::

    _mkpkg_depends=('python>major', 'python-foo') 

This would trigger a package rebuild if a version of *python-foo* is installed more recently 
than the last package build or if *python* has a major version which is larger than that
used when package was last built.

With the trigger conditions in the PKGBUID, then simply call mkpkg instead of makepkg. Couldn't be simpler. 
Options for mkpkg are those before any double dash *--*. Any options following *--*
are passed through to *makepkg*.

Options
=======

The options currently supported by mkpkg are::

    positional arguments:
      makepkg               All args after -- passed to makepkg.

    options:
      -h, --help                    show this help message and exit
      -f, --force                   Bump package release and rebuild
      -r, --refresh                 Update saved metadata files.
      -so-comp, --soname-comp COMP  soname rebuilds never, newer, keep, major/minor/last (keep)
      -v, --verb                    More verbose output - shows output of makepkg.

Config file
-----------

Configs are looked for in first in /etc/mkpkg/config and then in
~/.config/mkpkg/config. Config files are in TOML format.  Config options
are the same as command line options with '-' replaces by '_'.

e.g. to change the default soname rebuild compare option to newer::

    soname_comp = "newer"

Note on refresh
---------------

Attempts to update saved metadata files. Faster, if imperfect, alternative to rebuild.
If there is no saved metadata, and build is up to date, will try refresh the build info.
See the :ref:`metadata` section in the Appendix.

Note that *sonames* are found by examining any executables in the *pkg* directory.
If the *pkg* directory is empty, the refresh will not find any sonames.
   
Note on -soname-comp
--------------------

How to handle automatic soname changes. Default value is *keep* - only rebuilds if
soname is no longer available.

* *newer* 
  
  if soname is newer then reubild (time based)

* *keep* 
  
  if soname library is still available, then dont rebuild even if newer version(s) are available

* *vcomp* 
  
  rebuild if soname version is greater than the *vcomp* version. *vcomp* is one of *major*, *minor*, *patch*, *extra* or *last* - same as for regular depenencies.

* *neverever* 
  
  Developer option - will not rebuild even if the soname library is no longer available.


Note on passing options to makepkg
----------------------------------

All options following a double dash *--* are passed through to makepkg 

