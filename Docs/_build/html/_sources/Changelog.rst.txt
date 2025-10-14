Changelog
=========

Tags
====

.. code-block:: text

	1.0.0 (2022-09-03) -> 7.7.2 (2025-10-14)
	181 commits.

Commits
=======


* 2025-10-14  : **7.7.2**

.. code-block:: text

              - Switch doc build to xelatex which handles unicode characters
              - Drop unused dependency on pydantic from Arch PKGBUILD
 2025-06-26   ⋯

.. code-block:: text

              - update Docs/Changelogs Docs/mkpkg.pdf for 7.7.0

* 2025-06-26  : **7.7.0**

.. code-block:: text

              - run_prog: sync local copy with latest from pyconcurrent
 2025-06-25   ⋯

.. code-block:: text

              - update Docs/Changelogs Docs/mkpkg.pdf for 7.6.0

* 2025-06-25  : **7.6.0**

.. code-block:: text

              - Use pyconcurrent.run_prog when available otherwise local copy.
                Fix typo
 2025-06-22   ⋯

.. code-block:: text

              - update Docs/Changelogs Docs/mkpkg.pdf for 7.5.0

* 2025-06-22  : **7.5.0**

.. code-block:: text

              - Sync local copy of run_prog with latest from pyconcurrent
 2025-06-19   ⋯

.. code-block:: text

              - update Docs/Changelogs Docs/mkpkg.pdf for 7.4.0

* 2025-06-19  : **7.4.0**

.. code-block:: text

              - Keep internal copy of run_prog in sync with pyconcurrent
                   For subprocess stdin add .flush() on the file object before closing
 2025-06-16   ⋯

.. code-block:: text

              - update Docs/Changelogs Docs/mkpkg.pdf for 7.2.0

* 2025-06-16  : **7.2.0**

.. code-block:: text

              - run_prog: Fix one more possible hang. Add more exception checks that should never happen.
 2025-06-14   ⋯

.. code-block:: text

              - update Docs/Changelogs Docs/mkpkg.pdf for 7.1.0

* 2025-06-14  : **7.1.0**

.. code-block:: text

              - Fixed issue where build subprocesses that generate very large amounts
                of data on stdout/stderr could occasionally lead to blocked IO when data exceeded python
                IO.DEFAULT_BUFFER_SIZE.
                Symptom is that the build hangs waiting for IO to get unblocked.
                Fixed by enhancing run_prog() to use non-blocking I/O.
 2025-05-22   ⋯

.. code-block:: text

              - update Docs/Changelogs Docs/mkpkg.pdf for 7.0.0

* 2025-05-22  : **7.0.0**

.. code-block:: text

              - Immproved code
                  PEP-8, PEP-257, PEP-484 and PEP-561
                  Refactor & clean up
                Improved handling of split packages.
                  Now checks every packages for any being missing or out of date.
 2024-12-31   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/mkpkg.pdf for 6.2.4

* 2024-12-31  : **6.2.4**

.. code-block:: text

              - Add git signing key to Arch Package
              - update Docs/Changelog.rst Docs/mkpkg.pdf for 6.2.3

* 2024-12-31  : **6.2.3**

.. code-block:: text

              - fix typo in PKGBUILD
              - update Docs/Changelog.rst Docs/mkpkg.pdf for 6.2.2

* 2024-12-31  : **6.2.2**

.. code-block:: text

              - Git tags are now signed.
                Update python dep to 3.13
                Small clean ups and linting.
                PKGBUILD has info on how to activate verifying git signature once key is in keyring
 2024-12-19   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/mkpkg.pdf for 6.2.0

* 2024-12-19  : **6.2.0**

.. code-block:: text

              - drop tomli for tomllib (python now >= 3.11)
 2024-03-09   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/mkpkg.pdf for 6.1.0

* 2024-03-09  : **6.1.0**

.. code-block:: text

                  - soname logic updated.
                       Default is now keep which only rebuilds of a soname is no longer available.
                       This is in line with how sonames are typically used where soname only changes
                       when ABI changes.
              - update Docs/Changelog.rst Docs/mkpkg.pdf for 6.0.4

* 2024-03-09  : **6.0.4**

.. code-block:: text

              - Add missing pydantic from PKGBUILD depends
              - update Docs/Changelog.rst Docs/mkpkg.pdf for 6.0.3

* 2024-03-09  : **6.0.3**

.. code-block:: text

              - Tidy up code comments. Ensure pylint is clean.
                add comment to README - new build needed to get soname info
 2024-03-08   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/mkpkg.pdf for 6.0.1

* 2024-03-08  : **6.0.1**

.. code-block:: text

              - Tidy comments in soname file(s)
              - README - use 6.0.0 for version in history section
 2024-03-07   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/mkpkg.pdf for 6.0.0

* 2024-03-07  : **6.0.0**

.. code-block:: text

                   - * soname handling has been re-written from scratch and improved substantially.
            
                       It now identifies every soname versioned library in elf executables
                       along with their full path.  It also properly handles executables
                       built with *--rpath* loader options.
            
                       Previous versions relied on makepkg soname output
                       which, unfortunately, only lists sonames if they are also listed as a PKGBUILD dependency.
                       We need every soname versioned library to ensure we do the right thing
                       and rebuild when needed. So it was a mistake to rely on this.
            
                       Can also specify how to handle version comparisons similar to the way
                       package version comparisons are done (e.g. soname > major)
            
                     * Old options now deprecated
            
                        * (*--mpk-xxx*)
                        * (*--soname-build*) : use *--soname-comp* instead
 2023-12-20   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/mkpkg.pdf for 5.0.0

* 2023-12-20  : **5.0.0**

.. code-block:: text

                  - Fix soname dep handling when there are multiple pkgnames in PKGBUILD
                    verbose option is boolean - does not take argument
 2023-11-28   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/mkpkg.pdf for 4.9.0

* 2023-11-28  : **4.9.0**

.. code-block:: text

              - Switch python build backend to hatch (was poetry)
              - Switch python build backend to hatch (was poetry)
 2023-11-17   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/mkpkg.pdf for 4.8.0

* 2023-11-17  : **4.8.0**

.. code-block:: text

              - Change to using pyalpm to compare package versions instead of packaging.
                  ing.version() barfs on systemd version 255rc2.1 for some reason
 2023-10-03   ⋯

.. code-block:: text

              - update Docs/Changelog.rst for 4.7.0

* 2023-10-03  : **4.7.0**

.. code-block:: text

              - Bug fix semantic version comparisons
                  Stop treating Arch pkgrel as part of the last version element - its separate additional element
 2023-09-28   ⋯

.. code-block:: text

              - update Docs/Changelog.rst for 4.6.0

* 2023-09-28  : **4.6.0**

.. code-block:: text

              - Reorganize the tree and documents.
                Switch from markdown to restructured text.
                Now easy to build html and pdf docs using sphinx
 2023-06-05   ⋯

.. code-block:: text

              - update CHANGELOG.md for 4.5.5

* 2023-06-05  : **4.5.5**

.. code-block:: text

              - Small tweak to README
 2023-05-18   ⋯

.. code-block:: text

              - update CHANGELOG.md for 4.5.4

* 2023-05-18  : **4.5.4**

.. code-block:: text

              - Change PKGBUILD makedepnds from pip to installer
              - update CHANGELOG.md for 4.5.3

* 2023-05-18  : **4.5.3**

.. code-block:: text

              - install: switch from pip to python installer package. This adds optimized bytecode
              - update CHANGELOG.md for 4.5.2

* 2023-05-18  : **4.5.2**

.. code-block:: text

              - PKGBUILD: build wheel back to using python -m build instead of poetry
 2023-05-17   ⋯

.. code-block:: text

              - update CHANGELOG.md for 4.5.1

* 2023-05-17  : **4.5.1**

.. code-block:: text

              - Simplify Arch PKGBUILD and more closely follow arch guidelines
 2023-02-19   ⋯

.. code-block:: text

              - update CHANGELOG.md for 4.5.0

* 2023-02-19  : **4.5.0**

.. code-block:: text

              - Fix bug when soname dependency drives rebuild by ensuring pkgrel is bumped
 2023-02-18   ⋯

.. code-block:: text

              - update CHANGELOG.md for 4.4.0

* 2023-02-18  : **4.4.0**

.. code-block:: text

              - Bug fix extracting PKGBUILD info for certain cases
 2023-01-31   ⋯

.. code-block:: text

              - update CHANGELOG.md for 4.3.0

* 2023-01-31  : **4.3.0**

.. code-block:: text

              - Force now bumps the package release and rebuilds
 2023-01-06   ⋯

.. code-block:: text

              - update CHANGELOG.md for 4.2.1

* 2023-01-06  : **4.2.1**

.. code-block:: text

              - Add SPDX licensing lines
                Lint and tidy
 2023-01-03   ⋯

.. code-block:: text

              - update CHANGELOG.md for 4.2.0

* 2023-01-03  : **4.2.0**

.. code-block:: text

              - Fix for potential color name match bug - not with current color sets
 2022-12-16   ⋯

.. code-block:: text

              - update CHANGELOG.md for 4.1.1

* 2022-12-16  : **4.1.1**

.. code-block:: text

              - Add toml dependency to PKGBUILD
              - update CHANGELOG.md for 4.1.0

* 2022-12-16  : **4.1.0**

.. code-block:: text

              - Add config file support.
                    Change option handling. Options to be passed to makepkg must now be placed after --
                    Improveed soname treatment via option --soname-build (missing (default), newer or never)
 2022-12-15   ⋯

.. code-block:: text

              - update CHANGELOG.md

* 2022-12-15  : **4.0.0**

.. code-block:: text

              - Add --mkp-refresh
                    Attempts to update saved metadata files. Faster, if imperfect, alternative to rebuild.
                refactor some code
                pull out pacman queries to more easily share
                Add suport for missing soname library driving rebuild
                    suggestion thanks to Alberto Novella Archlinux subredit.
 2022-11-29   ⋯

.. code-block:: text

              - update CHANGELOG.md

* 2022-11-29  : **3.5.4**

.. code-block:: text

              - Small change to README.
                Change variable check in installer (no functional change)
 2022-11-05   ⋯

.. code-block:: text

              - update CHANGELOG.md

* 2022-11-05  : **3.5.3**

.. code-block:: text

              - tweak readme
                installer script change list to bash array for apps being installed. zero impact
 2022-11-04   ⋯

.. code-block:: text

              - update CHANGELOG.md

* 2022-11-04  : **3.5.2**

.. code-block:: text

              - PKGBUILD - duh - put back makedepends on poetry
              - update CHANGELOG.md

* 2022-11-04  : **3.5.1**

.. code-block:: text

              - Add package name to screen message
 2022-11-03   ⋯

.. code-block:: text

              - update CHANGELOG.md

* 2022-11-03  : **3.5.0**

.. code-block:: text

              - bug fix incorrectly handling triggers pkg>xxx
              - update CHANGELOG.md

* 2022-11-03  : **3.4.0**

.. code-block:: text

              - Better handling of PKGBUILD syntax errors
              - update CHANGELOG.md

* 2022-11-03  : **3.3.1**

.. code-block:: text

              - unwind prev error check - needs more work
              - update CHANGELOG.md

* 2022-11-03  : **3.3.0**

.. code-block:: text

              - Additional check for errors when sourcing PKGBUILD
 2022-10-31   ⋯

.. code-block:: text

              - update CHANGELOG.md

* 2022-10-31  : **3.2.0**

.. code-block:: text

              - typo - so sorry
              - update CHANGELOG.md

* 2022-10-31  : **3.1.0**

.. code-block:: text

              - Add more aliases of First_N for version comparisons (micro, serial)
                Change build from poetry/pip to python -m build/installer
 2022-10-30   ⋯

.. code-block:: text

              - update CHANGELOG.md

* 2022-10-30  : **3.0.0**

.. code-block:: text

              - update CHANGELOG.md
              - Add epoch support - needs wider testing
 2022-10-26   ⋯

.. code-block:: text

              - update changelog

* 2022-10-26  : **2.5.0**

.. code-block:: text

              - bug fix for _mkpkg_depends_files - silly typo
 2022-10-24   ⋯

.. code-block:: text

              - CHANGELOG.md

* 2022-10-24  : **2.4.1**

.. code-block:: text

              - update pyproject.toml vers
              - update changelog

* 2022-10-24  : **2.4.0**

.. code-block:: text

              - oops - accidently left debugger on!
              - update changelog

* 2022-10-24  : **2.3.6**

.. code-block:: text

              - Fix bug parsion <package> >= xxx.  Greater than is fine.
 2022-10-23   ⋯

.. code-block:: text

              - update changelog

* 2022-10-23  : **2.3.5**

.. code-block:: text

              - avoid all but tag in pkgver()
                update pyproject.toml vers
              - update changelog

* 2022-10-23  : **2.3.4**

.. code-block:: text

              - PKGBUILD - remove tag= now that pgkver() is getting latest tag

* 2022-10-23  : **2.3.3**

.. code-block:: text

              - PKGBUILD now builds latest release tag
 2022-10-14   ⋯

.. code-block:: text

              - update changelog
              - Add comment about being fast
              - update changelog

* 2022-10-14  : **2.3.2**

.. code-block:: text

              - Improve PKGBUILD for aur as per comments
                update pyproject.toml version
                Clean the dist directory before doing poetry build
              - fix python depends version > 3.9
 2022-10-13   ⋯

.. code-block:: text

              - Add makedepends packages in aur PKGBUILD
              - fix comment
              - add aur comment
              - update changelog

* 2022-10-13  : **2.3.1**

.. code-block:: text

              - Update readme with link to AUR for mkpkg
                Change PKGBUILD for AUR
              - little word smithing on readme
              - Clean up some comments
              - readme word smithing
              - update changelog

* 2022-10-13  : **2.3.0**

.. code-block:: text

              - In the event mkpkg_depends / mkpkg_depends_files are absent,
                no longer fall back to use makedepends unless turned on with the --mkp-use_makedepends option
              - update changelog

* 2022-10-13  : **2.2.1**

.. code-block:: text

              - Bug fix for _mkpkg_depends_files
              - better packge description in PKGBUILD
              - readme markdown missed 2 spaces for newline
              - Readme - markdown requires escape for underscore
              - update CHANGELOG.md

* 2022-10-13  : **2.2.0**

.. code-block:: text

              - Change PKGBUILD variables to have leading "_" to follow arch packaging guidelines
                Code is backward compatible and will work with or without the _
                New names are: _mkpkg_depends and _mkpkg_depends_files
              - update changelog
              - more readme tweaks
              - update changelog

* 2022-10-13  : **2.1.1**

.. code-block:: text

              - Provide sample PKGBUILD to build mkpkg
              - update changelog
              - typo in readme
              - update changelog
              - README tweak to explain "patch" being same as "First_3" for version triggers
              - update CHANGELOG.md

* 2022-10-13  : **2.1.0**

.. code-block:: text

              - Enhance version triggers to handle version with more than 3 elements
 2022-10-12   ⋯

.. code-block:: text

              - update changelog
              - readme tweaks
              - update CHANGELOG

* 2022-10-12  : **2.0.1**

.. code-block:: text

              - update changelog
              - remove unused from do-install
              - update CHANGELOG
              - tweak readme
              - update changelog

* 2022-10-12  : **2.0.0**

.. code-block:: text

              - Reorganize directory structure and use poetry for packaging.
                Add support for triggers now based on semantic versions.
                e.g python>3.12 or python>minor - where minor triggers build if
                major.minor version of dependency package is greater than that used when
                it was last built.
              - Reorganize source tree
 2022-09-28   ⋯

.. code-block:: text

              - Update changelog
              - tweak readme little more
              - update Changelog
              - Tweak README
 2022-09-22   ⋯

.. code-block:: text

              - tweak README

* 2022-09-22  : **1.3.1**

.. code-block:: text

              - Update Changelog
              - Add CVE-2022-36113 as example of build tool danger
 2022-09-18   ⋯

.. code-block:: text

              - Update Changelog
              - Add Changelog

* 2022-09-07  : **1.3.0**

.. code-block:: text

              - fix out of date comment in mkpkg.py
              - fix little markdown issue
 2022-09-06   ⋯

.. code-block:: text

              - tweak readme format

* 2022-09-06  : **1.2.0**

.. code-block:: text

              - Add support for trigger files : mkpkg_depends_files
              - add README discssion comment
 2022-09-04   ⋯

.. code-block:: text

              - lint picking
              - Add comment in README
              - few more README tweaks

* 2022-09-04  : **1.1.1**

.. code-block:: text

              - tidy message output
              - typo
              - Little tidy on README

* 2022-09-04  : **1.1.0**

.. code-block:: text

              - Handle edge case when PKGBUILD hand edited
              - Bug fix for case when override mkpkg_depends set to empty set

* 2022-09-03  : **1.0.5**

.. code-block:: text

              - Now that we implemented mkpkg_depends, remove some readme comments
              - typo
              - minor README tweak
              - Fix typo (resolves issue #1) and tweak README

* 2022-09-03  : **1.0.4**

.. code-block:: text

              - fix section numbers in README

* 2022-09-03  : **1.0.3**

.. code-block:: text

              - Support mkpkg_depends overriding makepends - gives full control to user

* 2022-09-03  : **1.0.2**

.. code-block:: text

              - README use lower case for mkpkg

* 2022-09-03  : **1.0.1**

.. code-block:: text

              - Tidy couple comments

* 2022-09-03  : **1.0.0**

.. code-block:: text

              - Initial Revision of mkpkg.
                mkpkg builds Arch packages and rebuilds them whenever a make dependency is more recent than the last package


