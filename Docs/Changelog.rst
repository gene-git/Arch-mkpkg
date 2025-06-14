=========
Changelog
=========

Tags
====

::

	1.0.0 (2022-09-03) -> 7.1.0 (2025-06-14)
	168 commits.

Commits
=======


* 2025-06-14  : **7.1.0**

::

                Fixed issue where build subprocesses that generate very large amounts
                of data on stdout/stderr could occasionally lead to blocked IO when data
                exceeded python
                IO.DEFAULT_BUFFER_SIZE.
                Symptom is that the build hangs waiting for IO to get unblocked.
                Fixed by enhancing run_prog() to use non-blocking I/O.
 2025-05-22     update Docs/Changelogs Docs/mkpkg.pdf for 7.0.0

* 2025-05-22  : **7.0.0**

::

                Immproved code
                  PEP-8, PEP-257, PEP-484 and PEP-561
                  Refactor & clean up
                Improved handling of split packages.
                  Now checks every packages for any being missing or out of date.
 2024-12-31     update Docs/Changelog.rst Docs/mkpkg.pdf for 6.2.4

* 2024-12-31  : **6.2.4**

::

                Add git signing key to Arch Package
                update Docs/Changelog.rst Docs/mkpkg.pdf for 6.2.3

* 2024-12-31  : **6.2.3**

::

                fix typo in PKGBUILD
                update Docs/Changelog.rst Docs/mkpkg.pdf for 6.2.2

* 2024-12-31  : **6.2.2**

::

                Git tags are now signed.
                Update python dep to 3.13
                Small clean ups and linting.
                PKGBUILD has info on how to activate verifying git signature once key is in
                keyring
 2024-12-19     update Docs/Changelog.rst Docs/mkpkg.pdf for 6.2.0

* 2024-12-19  : **6.2.0**

::

                drop tomli for tomllib (python now >= 3.11)
 2024-03-09     update Docs/Changelog.rst Docs/mkpkg.pdf for 6.1.0

* 2024-03-09  : **6.1.0**

::

                    soname logic updated.
                       Default is now keep which only rebuilds of a soname is no longer
                       available.
                       This is in line with how sonames are typically used where soname only
                       changes
                       when ABI changes.
                update Docs/Changelog.rst Docs/mkpkg.pdf for 6.0.4

* 2024-03-09  : **6.0.4**

::

                Add missing pydantic from PKGBUILD depends
                update Docs/Changelog.rst Docs/mkpkg.pdf for 6.0.3

* 2024-03-09  : **6.0.3**

::

                Tidy up code comments. Ensure pylint is clean.
                add comment to README - new build needed to get soname info
 2024-03-08     update Docs/Changelog.rst Docs/mkpkg.pdf for 6.0.1

* 2024-03-08  : **6.0.1**

::

                Tidy comments in soname file(s)
                README - use 6.0.0 for version in history section
 2024-03-07     update Docs/Changelog.rst Docs/mkpkg.pdf for 6.0.0

* 2024-03-07  : **6.0.0**

::

                     * soname handling has been re-written from scratch and improved
                     substantially.
                       It now identifies every soname versioned library in elf executables
                       along with their full path.  It also properly handles executables
                       built with *--rpath* loader options.
                       Previous versions relied on makepkg soname output
                       which, unfortunately, only lists sonames if they are also listed as a
                       PKGBUILD dependency.
                       We need every soname versioned library to ensure we do the right
                       thing
                       and rebuild when needed. So it was a mistake to rely on this.
                       Can also specify how to handle version comparisons similar to the way
                       package version comparisons are done (e.g. soname > major)
                     * Old options now deprecated
                        * (*--mpk-xxx*)
                        * (*--soname-build*) : use *--soname-comp* instead
 2023-12-20     update Docs/Changelog.rst Docs/mkpkg.pdf for 5.0.0

* 2023-12-20  : **5.0.0**

::

                    Fix soname dep handling when there are multiple pkgnames in PKGBUILD
                    verbose option is boolean - does not take argument
 2023-11-28     update Docs/Changelog.rst Docs/mkpkg.pdf for 4.9.0

* 2023-11-28  : **4.9.0**

::

                Switch python build backend to hatch (was poetry)
                Switch python build backend to hatch (was poetry)
 2023-11-17     update Docs/Changelog.rst Docs/mkpkg.pdf for 4.8.0

* 2023-11-17  : **4.8.0**

::

                Change to using pyalpm to compare package versions instead of packaging.
                  ing.version() barfs on systemd version 255rc2.1 for some reason
 2023-10-03     update Docs/Changelog.rst for 4.7.0

* 2023-10-03  : **4.7.0**

::

                Bug fix semantic version comparisons
                  Stop treating Arch pkgrel as part of the last version element - its
                  separate additional element
 2023-09-28     update Docs/Changelog.rst for 4.6.0

* 2023-09-28  : **4.6.0**

::

                Reorganize the tree and documents.
                Switch from markdown to restructured text.
                Now easy to build html and pdf docs using sphinx
 2023-06-05     update CHANGELOG.md for 4.5.5

* 2023-06-05  : **4.5.5**

::

                Small tweak to README
 2023-05-18     update CHANGELOG.md for 4.5.4

* 2023-05-18  : **4.5.4**

::

                Change PKGBUILD makedepnds from pip to installer
                update CHANGELOG.md for 4.5.3

* 2023-05-18  : **4.5.3**

::

                install: switch from pip to python installer package. This adds optimized
                bytecode
                update CHANGELOG.md for 4.5.2

* 2023-05-18  : **4.5.2**

::

                PKGBUILD: build wheel back to using python -m build instead of poetry
 2023-05-17     update CHANGELOG.md for 4.5.1

* 2023-05-17  : **4.5.1**

::

                Simplify Arch PKGBUILD and more closely follow arch guidelines
 2023-02-19     update CHANGELOG.md for 4.5.0

* 2023-02-19  : **4.5.0**

::

                Fix bug when soname dependency drives rebuild by ensuring pkgrel is bumped
 2023-02-18     update CHANGELOG.md for 4.4.0

* 2023-02-18  : **4.4.0**

::

                Bug fix extracting PKGBUILD info for certain cases
 2023-01-31     update CHANGELOG.md for 4.3.0

* 2023-01-31  : **4.3.0**

::

                Force now bumps the package release and rebuilds
 2023-01-06     update CHANGELOG.md for 4.2.1

* 2023-01-06  : **4.2.1**

::

                Add SPDX licensing lines
                Lint and tidy
 2023-01-03     update CHANGELOG.md for 4.2.0

* 2023-01-03  : **4.2.0**

::

                Fix for potential color name match bug - not with current color sets
 2022-12-16     update CHANGELOG.md for 4.1.1

* 2022-12-16  : **4.1.1**

::

                Add toml dependency to PKGBUILD
                update CHANGELOG.md for 4.1.0

* 2022-12-16  : **4.1.0**

::

                Add config file support.
                    Change option handling. Options to be passed to makepkg must now be
                    placed after --
                    Improveed soname treatment via option --soname-build (missing (default),
                    newer or never)
 2022-12-15     update CHANGELOG.md

* 2022-12-15  : **4.0.0**

::

                Add --mkp-refresh
                    Attempts to update saved metadata files. Faster, if imperfect,
                    alternative to rebuild.
                refactor some code
                pull out pacman queries to more easily share
                Add suport for missing soname library driving rebuild
                    suggestion thanks to Alberto Novella Archlinux subredit.
 2022-11-29     update CHANGELOG.md

* 2022-11-29  : **3.5.4**

::

                Small change to README.
                Change variable check in installer (no functional change)
 2022-11-05     update CHANGELOG.md

* 2022-11-05  : **3.5.3**

::

                tweak readme
                installer script change list to bash array for apps being installed. zero
                impact
 2022-11-04     update CHANGELOG.md

* 2022-11-04  : **3.5.2**

::

                PKGBUILD - duh - put back makedepends on poetry
                update CHANGELOG.md

* 2022-11-04  : **3.5.1**

::

                Add package name to screen message
 2022-11-03     update CHANGELOG.md

* 2022-11-03  : **3.5.0**

::

                bug fix incorrectly handling triggers pkg>xxx
                update CHANGELOG.md

* 2022-11-03  : **3.4.0**

::

                Better handling of PKGBUILD syntax errors
                update CHANGELOG.md

* 2022-11-03  : **3.3.1**

::

                unwind prev error check - needs more work
                update CHANGELOG.md

* 2022-11-03  : **3.3.0**

::

                Additional check for errors when sourcing PKGBUILD
 2022-10-31     update CHANGELOG.md

* 2022-10-31  : **3.2.0**

::

                typo - so sorry
                update CHANGELOG.md

* 2022-10-31  : **3.1.0**

::

                Add more aliases of First_N for version comparisons (micro, serial)
                Change build from poetry/pip to python -m build/installer
 2022-10-30     update CHANGELOG.md

* 2022-10-30  : **3.0.0**

::

                update CHANGELOG.md
                Add epoch support - needs wider testing
 2022-10-26     update changelog

* 2022-10-26  : **2.5.0**

::

                bug fix for _mkpkg_depends_files - silly typo
 2022-10-24     CHANGELOG.md

* 2022-10-24  : **2.4.1**

::

                update pyproject.toml vers
                update changelog

* 2022-10-24  : **2.4.0**

::

                oops - accidently left debugger on!
                update changelog

* 2022-10-24  : **2.3.6**

::

                Fix bug parsion <package> >= xxx.  Greater than is fine.
 2022-10-23     update changelog

* 2022-10-23  : **2.3.5**

::

                avoid all but tag in pkgver()
                update pyproject.toml vers
                update changelog

* 2022-10-23  : **2.3.4**

::

                PKGBUILD - remove tag= now that pgkver() is getting latest tag

* 2022-10-23  : **2.3.3**

::

                PKGBUILD now builds latest release tag
 2022-10-14     update changelog
                Add comment about being fast
                update changelog

* 2022-10-14  : **2.3.2**

::

                Improve PKGBUILD for aur as per comments
                update pyproject.toml version
                Clean the dist directory before doing poetry build
                fix python depends version > 3.9
 2022-10-13     Add makedepends packages in aur PKGBUILD
                fix comment
                add aur comment
                update changelog

* 2022-10-13  : **2.3.1**

::

                Update readme with link to AUR for mkpkg
                Change PKGBUILD for AUR
                little word smithing on readme
                Clean up some comments
                readme word smithing
                update changelog

* 2022-10-13  : **2.3.0**

::

                In the event mkpkg_depends / mkpkg_depends_files are absent,
                no longer fall back to use makedepends unless turned on with the --mkp-
                use_makedepends option
                update changelog

* 2022-10-13  : **2.2.1**

::

                Bug fix for _mkpkg_depends_files
                better packge description in PKGBUILD
                readme markdown missed 2 spaces for newline
                Readme - markdown requires escape for underscore
                update CHANGELOG.md

* 2022-10-13  : **2.2.0**

::

                Change PKGBUILD variables to have leading "_" to follow arch packaging
                guidelines
                Code is backward compatible and will work with or without the _
                New names are: _mkpkg_depends and _mkpkg_depends_files
                update changelog
                more readme tweaks
                update changelog

* 2022-10-13  : **2.1.1**

::

                Provide sample PKGBUILD to build mkpkg
                update changelog
                typo in readme
                update changelog
                README tweak to explain "patch" being same as "First_3" for version triggers
                update CHANGELOG.md

* 2022-10-13  : **2.1.0**

::

                Enhance version triggers to handle version with more than 3 elements
 2022-10-12     update changelog
                readme tweaks
                update CHANGELOG

* 2022-10-12  : **2.0.1**

::

                update changelog
                remove unused from do-install
                update CHANGELOG
                tweak readme
                update changelog

* 2022-10-12  : **2.0.0**

::

                Reorganize directory structure and use poetry for packaging.
                Add support for triggers now based on semantic versions.
                e.g python>3.12 or python>minor - where minor triggers build if
                major.minor version of dependency package is greater than that used when
                it was last built.
                Reorganize source tree
 2022-09-28     Update changelog
                tweak readme little more
                update Changelog
                Tweak README
 2022-09-22     tweak README

* 2022-09-22  : **1.3.1**

::

                Update Changelog
                Add CVE-2022-36113 as example of build tool danger
 2022-09-18     Update Changelog
                Add Changelog

* 2022-09-07  : **1.3.0**

::

                fix out of date comment in mkpkg.py
                fix little markdown issue
 2022-09-06     tweak readme format

* 2022-09-06  : **1.2.0**

::

                Add support for trigger files : mkpkg_depends_files
                add README discssion comment
 2022-09-04     lint picking
                Add comment in README
                few more README tweaks

* 2022-09-04  : **1.1.1**

::

                tidy message output
                typo
                Little tidy on README

* 2022-09-04  : **1.1.0**

::

                Handle edge case when PKGBUILD hand edited
                Bug fix for case when override mkpkg_depends set to empty set

* 2022-09-03  : **1.0.5**

::

                Now that we implemented mkpkg_depends, remove some readme comments
                typo
                minor README tweak
                Fix typo (resolves issue #1) and tweak README

* 2022-09-03  : **1.0.4**

::

                fix section numbers in README

* 2022-09-03  : **1.0.3**

::

                Support mkpkg_depends overriding makepends - gives full control to user

* 2022-09-03  : **1.0.2**

::

                README use lower case for mkpkg

* 2022-09-03  : **1.0.1**

::

                Tidy couple comments

* 2022-09-03  : **1.0.0**

::

                Initial Revision of mkpkg.
                mkpkg builds Arch packages and rebuilds them whenever a make dependency is
                more recent than the last package


