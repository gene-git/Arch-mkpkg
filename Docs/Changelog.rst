------------------------------
Changes 
------------------------------
* 2023-10-03 | update Docs/Changelog.rst for 4.7.0 (HEAD -> master, origin/master) 
* 2023-10-03 | Bug fix semantic version comparisons   Stop treating Arch pkgrel as part of the last version element - its separate additional element (tag: 4.7.0) 
* 2023-09-28 | update Docs/Changelog.rst for 4.6.0 
* 2023-09-28 | Reorganize the tree and documents. Switch from markdown to restructured text. Now easy to build html and pdf docs using sphinx (tag: 4.6.0) 
* 2023-06-05 | update CHANGELOG.md for 4.5.5 
* 2023-06-05 | Small tweak to README (tag: 4.5.5) 
* 2023-05-18 | update CHANGELOG.md for 4.5.4 
* 2023-05-18 | Change PKGBUILD makedepnds from pip to installer (tag: 4.5.4) 
* 2023-05-18 | update CHANGELOG.md for 4.5.3 
* 2023-05-18 | install: switch from pip to python installer package. This adds optimized bytecode (tag: 4.5.3) 
* 2023-05-18 | update CHANGELOG.md for 4.5.2 
* 2023-05-18 | PKGBUILD: build wheel back to using python -m build instead of poetry (tag: 4.5.2) 
* 2023-05-17 | update CHANGELOG.md for 4.5.1 
* 2023-05-17 | Simplify Arch PKGBUILD and more closely follow arch guidelines (tag: 4.5.1) 
* 2023-02-19 | update CHANGELOG.md for 4.5.0 
* 2023-02-19 | Fix bug when soname dependency drives rebuild by ensuring pkgrel is bumped (tag: 4.5.0) 
* 2023-02-18 | update CHANGELOG.md for 4.4.0 
* 2023-02-18 | Bug fix extracting PKGBUILD info for certain cases (tag: 4.4.0) 
* 2023-01-31 | update CHANGELOG.md for 4.3.0 
* 2023-01-31 | Force now bumps the package release and rebuilds (tag: 4.3.0) 
* 2023-01-06 | update CHANGELOG.md for 4.2.1 
* 2023-01-06 | Add SPDX licensing lines Lint and tidy (tag: 4.2.1) 
* 2023-01-03 | update CHANGELOG.md for 4.2.0 
* 2023-01-03 | Fix for potential color name match bug - not with current color sets (tag: 4.2.0) 
* 2022-12-16 | update CHANGELOG.md for 4.1.1 
* 2022-12-16 | Add toml dependency to PKGBUILD (tag: 4.1.1) 
* 2022-12-16 | update CHANGELOG.md for 4.1.0 
* 2022-12-16 | Add config file support.     Change option handling. Options to be passed to makepkg must now be placed after --     Improveed soname treatment via option --soname-build (missing (default), newer or never) (tag: 4.1.0) 
* 2022-12-15 | update CHANGELOG.md 
* 2022-12-15 | Add --mkp-refresh     Attempts to update saved metadata files. Faster, if imperfect, alternative to rebuild. refactor some code pull out pacman queries to more easily share Add suport for missing soname library driving rebuild     suggestion thanks to Alberto Novella Archlinux subredit. (tag: 4.0.0) 
* 2022-11-29 | update CHANGELOG.md 
* 2022-11-29 | Small change to README. Change variable check in installer (no functional change) (tag: 3.5.4) 
* 2022-11-05 | update CHANGELOG.md 
* 2022-11-05 | tweak readme installer script change list to bash array for apps being installed. zero impact (tag: 3.5.3) 
* 2022-11-04 | update CHANGELOG.md 
* 2022-11-04 | PKGBUILD - duh - put back makedepends on poetry (tag: 3.5.2) 
* 2022-11-04 | update CHANGELOG.md 
* 2022-11-04 | Add package name to screen message (tag: 3.5.1) 
* 2022-11-03 | update CHANGELOG.md 
* 2022-11-03 | bug fix incorrectly handling triggers pkg>xxx (tag: 3.5.0) 
* 2022-11-03 | update CHANGELOG.md 
* 2022-11-03 | Better handling of PKGBUILD syntax errors (tag: 3.4.0) 
* 2022-11-03 | update CHANGELOG.md 
* 2022-11-03 | unwind prev error check - needs more work (tag: 3.3.1) 
* 2022-11-03 | update CHANGELOG.md 
* 2022-11-03 | Additional check for errors when sourcing PKGBUILD (tag: 3.3.0) 
* 2022-10-31 | update CHANGELOG.md 
* 2022-10-31 | typo - so sorry (tag: 3.2.0) 
* 2022-10-31 | update CHANGELOG.md 
* 2022-10-31 | Add more aliases of First_N for version comparisons (micro, serial) Change build from poetry/pip to python -m build/installer (tag: 3.1.0) 
* 2022-10-30 | update CHANGELOG.md 
* 2022-10-30 | update CHANGELOG.md (tag: 3.0.0) 
* 2022-10-30 | Add epoch support - needs wider testing 
* 2022-10-26 | update changelog 
* 2022-10-26 | bug fix for _mkpkg_depends_files - silly typo (tag: 2.5.0) 
* 2022-10-24 | CHANGELOG.md 
* 2022-10-24 | update pyproject.toml vers (tag: 2.4.1) 
* 2022-10-24 | update changelog 
* 2022-10-24 | oops - accidently left debugger on! (tag: 2.4.0) 
* 2022-10-24 | update changelog 
* 2022-10-24 | Fix bug parsion <package> >= xxx.  Greater than is fine. (tag: 2.3.6) 
* 2022-10-23 | update changelog 
* 2022-10-23 | avoid all but tag in pkgver() update pyproject.toml vers (tag: 2.3.5) 
* 2022-10-23 | update changelog 
* 2022-10-23 | PKGBUILD - remove tag= now that pgkver() is getting latest tag (tag: 2.3.4) 
* 2022-10-23 | PKGBUILD now builds latest release tag (tag: 2.3.3) 
* 2022-10-14 | update changelog 
* 2022-10-14 | Add comment about being fast 
* 2022-10-14 | update changelog 
* 2022-10-14 | Improve PKGBUILD for aur as per comments update pyproject.toml version Clean the dist directory before doing poetry build (tag: 2.3.2) 
* 2022-10-14 | fix python depends version > 3.9 
* 2022-10-13 | Add makedepends packages in aur PKGBUILD 
* 2022-10-13 | fix comment 
* 2022-10-13 | add aur comment 
* 2022-10-13 | update changelog 
* 2022-10-13 | Update readme with link to AUR for mkpkg Change PKGBUILD for AUR (tag: 2.3.1) 
* 2022-10-13 | little word smithing on readme 
* 2022-10-13 | Clean up some comments 
* 2022-10-13 | readme word smithing 
* 2022-10-13 | update changelog 
* 2022-10-13 | In the event mkpkg_depends / mkpkg_depends_files are absent, no longer fall back to use makedepends unless turned on with the --mkp-use_makedepends option (tag: 2.3.0) 
* 2022-10-13 | update changelog 
* 2022-10-13 | Bug fix for _mkpkg_depends_files (tag: 2.2.1) 
* 2022-10-13 | better packge description in PKGBUILD 
* 2022-10-13 | readme markdown missed 2 spaces for newline 
* 2022-10-13 | Readme - markdown requires escape for underscore 
* 2022-10-13 | update CHANGELOG.md 
* 2022-10-13 | Change PKGBUILD variables to have leading "_" to follow arch packaging guidelines Code is backward compatible and will work with or without the _ New names are: _mkpkg_depends and _mkpkg_depends_files (tag: 2.2.0) 
* 2022-10-13 | update changelog 
* 2022-10-13 | more readme tweaks 
* 2022-10-13 | update changelog 
* 2022-10-13 | Provide sample PKGBUILD to build mkpkg (tag: 2.1.1) 
* 2022-10-13 | update changelog 
* 2022-10-13 | typo in readme 
* 2022-10-13 | update changelog 
* 2022-10-13 | README tweak to explain "patch" being same as "First_3" for version triggers 
* 2022-10-13 | update CHANGELOG.md 
* 2022-10-13 | Enhance version triggers to handle version with more than 3 elements (tag: 2.1.0) 
* 2022-10-12 | update changelog 
* 2022-10-12 | readme tweaks 
* 2022-10-12 | update CHANGELOG 
* 2022-10-12 | update changelog (tag: 2.0.1) 
* 2022-10-12 | remove unused from do-install 
* 2022-10-12 | update CHANGELOG 
* 2022-10-12 | tweak readme 
* 2022-10-12 | update changelog 
* 2022-10-12 | Reorganize directory structure and use poetry for packaging. Add support for triggers now based on semantic versions. e.g python>3.12 or python>minor - where minor triggers build if major.minor version of dependency package is greater than that used when it was last built. (tag: 2.0.0) 
* 2022-10-12 | Reorganize source tree 
* 2022-09-28 | Update changelog 
* 2022-09-28 | tweak readme little more 
* 2022-09-28 | update Changelog 
* 2022-09-28 | Tweak README 
* 2022-09-22 | tweak README 
* 2022-09-22 | Update Changelog (tag: 1.3.1) 
* 2022-09-22 | Add CVE-2022-36113 as example of build tool danger 
* 2022-09-18 | Update Changelog 
* 2022-09-18 | Add Changelog 
* 2022-09-07 | fix out of date comment in mkpkg.py (tag: 1.3.0) 
* 2022-09-07 | fix little markdown issue 
* 2022-09-06 | tweak readme format 
* 2022-09-06 | Add support for trigger files : mkpkg_depends_files (tag: 1.2.0) 
* 2022-09-06 | add README discssion comment 
* 2022-09-04 | lint picking 
* 2022-09-04 | Add comment in README 
* 2022-09-04 | few more README tweaks 
* 2022-09-04 | tidy message output (tag: 1.1.1) 
* 2022-09-04 | typo 
* 2022-09-04 | Little tidy on README 
* 2022-09-04 | Handle edge case when PKGBUILD hand edited (tag: 1.1.0) 
* 2022-09-04 | Bug fix for case when override mkpkg_depends set to empty set 
* 2022-09-03 | Now that we implemented mkpkg_depends, remove some readme comments (tag: 1.0.5) 
* 2022-09-03 | typo 
* 2022-09-03 | minor README tweak 
* 2022-09-03 | Fix typo (resolves issue #1) and tweak README 
* 2022-09-03 | fix section numbers in README (tag: 1.0.4) 
* 2022-09-03 | Support mkpkg_depends overriding makepends - gives full control to user (tag: 1.0.3) 
* 2022-09-03 | README use lower case for mkpkg (tag: 1.0.2) 
* 2022-09-03 | Tidy couple comments (tag: 1.0.1) 
* 2022-09-03 | Initial Revision of mkpkg. mkpkg builds Arch packages and rebuilds them whenever a make dependency is more recent than the last package (tag: 1.0.0) 

------------------------------
FIle stats
------------------------------
 Docs/Changelog.rst               | 419 ++++++++++++++-------------------------
 Docs/conf.py                     |   2 +-
 Docs/mkpkg.pdf                   |   1 -
 README.rst                       |   6 +-
 packaging/PKGBUILD               |   4 +-
 pyproject.toml                   |   2 +-
 src/mkpkg/lib/version_compare.py |  13 +-
 7 files changed, 162 insertions(+), 285 deletions(-)
