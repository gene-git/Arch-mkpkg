Changelog
=========

**[6.2.4] ----- 2024-12-31** ::

	    Add git signing key to Arch Package
	    update Docs/Changelog.rst Docs/mkpkg.pdf for 6.2.3


**[6.2.3] ----- 2024-12-31** ::

	    fix typo in PKGBUILD
	    update Docs/Changelog.rst Docs/mkpkg.pdf for 6.2.2


**[6.2.2] ----- 2024-12-31** ::

	    Git tags are now signed.
	    Update python dep to 3.13
	    Small clean ups and linting.
	    PKGBUILD has info on how to activate verifying git signature once key is in keyring
	    update Docs/Changelog.rst Docs/mkpkg.pdf for 6.2.0


**[6.2.0] ----- 2024-12-19** ::

	    drop tomli for tomllib (python now >= 3.11)
	    update Docs/Changelog.rst Docs/mkpkg.pdf for 6.1.0


**[6.1.0] ----- 2024-03-09** ::

	        soname logic updated.
	           Default is now keep which only rebuilds of a soname is no longer available.
	           This is in line with how sonames are typically used where soname only changes
	           when ABI changes.
	    update Docs/Changelog.rst Docs/mkpkg.pdf for 6.0.4


**[6.0.4] ----- 2024-03-09** ::

	    Add missing pydantic from PKGBUILD depends
	    update Docs/Changelog.rst Docs/mkpkg.pdf for 6.0.3


**[6.0.3] ----- 2024-03-09** ::

	    Tidy up code comments. Ensure pylint is clean.
	    add comment to README - new build needed to get soname info
	    update Docs/Changelog.rst Docs/mkpkg.pdf for 6.0.1


**[6.0.1] ----- 2024-03-08** ::

	    Tidy comments in soname file(s)
	    README - use 6.0.0 for version in history section
	    update Docs/Changelog.rst Docs/mkpkg.pdf for 6.0.0


**[6.0.0] ----- 2024-03-07** ::

	         * soname handling has been re-written from scratch and improved substantially.
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
	    update Docs/Changelog.rst Docs/mkpkg.pdf for 5.0.0


**[5.0.0] ----- 2023-12-20** ::

	        Fix soname dep handling when there are multiple pkgnames in PKGBUILD
	        verbose option is boolean - does not take argument
	    update Docs/Changelog.rst Docs/mkpkg.pdf for 4.9.0


**[4.9.0] ----- 2023-11-28** ::

	    Switch python build backend to hatch (was poetry)
	    Switch python build backend to hatch (was poetry)
	    update Docs/Changelog.rst Docs/mkpkg.pdf for 4.8.0


**[4.8.0] ----- 2023-11-17** ::

	    Change to using pyalpm to compare package versions instead of packaging.
	      ing.version() barfs on systemd version 255rc2.1 for some reason
	    update Docs/Changelog.rst for 4.7.0


**[4.7.0] ----- 2023-10-03** ::

	    Bug fix semantic version comparisons
	      Stop treating Arch pkgrel as part of the last version element - its separate additional element
	    update Docs/Changelog.rst for 4.6.0


**[4.6.0] ----- 2023-09-28** ::

	    Reorganize the tree and documents.
	    Switch from markdown to restructured text.
	    Now easy to build html and pdf docs using sphinx
	    update CHANGELOG.md for 4.5.5


**[4.5.5] ----- 2023-06-05** ::

	    Small tweak to README
	    update CHANGELOG.md for 4.5.4


**[4.5.4] ----- 2023-05-18** ::

	    Change PKGBUILD makedepnds from pip to installer
	    update CHANGELOG.md for 4.5.3


**[4.5.3] ----- 2023-05-18** ::

	    install: switch from pip to python installer package. This adds optimized bytecode
	    update CHANGELOG.md for 4.5.2


**[4.5.2] ----- 2023-05-18** ::

	    PKGBUILD: build wheel back to using python -m build instead of poetry
	    update CHANGELOG.md for 4.5.1


**[4.5.1] ----- 2023-05-17** ::

	    Simplify Arch PKGBUILD and more closely follow arch guidelines
	    update CHANGELOG.md for 4.5.0


**[4.5.0] ----- 2023-02-19** ::

	    Fix bug when soname dependency drives rebuild by ensuring pkgrel is bumped
	    update CHANGELOG.md for 4.4.0


**[4.4.0] ----- 2023-02-18** ::

	    Bug fix extracting PKGBUILD info for certain cases
	    update CHANGELOG.md for 4.3.0


**[4.3.0] ----- 2023-01-31** ::

	    Force now bumps the package release and rebuilds
	    update CHANGELOG.md for 4.2.1


**[4.2.1] ----- 2023-01-06** ::

	    Add SPDX licensing lines
	    Lint and tidy
	    update CHANGELOG.md for 4.2.0


**[4.2.0] ----- 2023-01-03** ::

	    Fix for potential color name match bug - not with current color sets
	    update CHANGELOG.md for 4.1.1


**[4.1.1] ----- 2022-12-16** ::

	    Add toml dependency to PKGBUILD
	    update CHANGELOG.md for 4.1.0


**[4.1.0] ----- 2022-12-16** ::

	    Add config file support.
	        Change option handling. Options to be passed to makepkg must now be placed after --
	        Improveed soname treatment via option --soname-build (missing (default), newer or never)
	    update CHANGELOG.md


**[4.0.0] ----- 2022-12-15** ::

	    Add --mkp-refresh
	        Attempts to update saved metadata files. Faster, if imperfect, alternative to rebuild.
	    refactor some code
	    pull out pacman queries to more easily share
	    Add suport for missing soname library driving rebuild
	        suggestion thanks to Alberto Novella Archlinux subredit.
	    update CHANGELOG.md


**[3.5.4] ----- 2022-11-29** ::

	    Small change to README.
	    Change variable check in installer (no functional change)
	    update CHANGELOG.md


**[3.5.3] ----- 2022-11-05** ::

	    tweak readme
	    installer script change list to bash array for apps being installed. zero impact
	    update CHANGELOG.md


**[3.5.2] ----- 2022-11-04** ::

	    PKGBUILD - duh - put back makedepends on poetry
	    update CHANGELOG.md


**[3.5.1] ----- 2022-11-04** ::

	    Add package name to screen message
	    update CHANGELOG.md


**[3.5.0] ----- 2022-11-03** ::

	    bug fix incorrectly handling triggers pkg>xxx
	    update CHANGELOG.md


**[3.4.0] ----- 2022-11-03** ::

	    Better handling of PKGBUILD syntax errors
	    update CHANGELOG.md


**[3.3.1] ----- 2022-11-03** ::

	    unwind prev error check - needs more work
	    update CHANGELOG.md


**[3.3.0] ----- 2022-11-03** ::

	    Additional check for errors when sourcing PKGBUILD
	    update CHANGELOG.md


**[3.2.0] ----- 2022-10-31** ::

	    typo - so sorry
	    update CHANGELOG.md


**[3.1.0] ----- 2022-10-31** ::

	    Add more aliases of First_N for version comparisons (micro, serial)
	    Change build from poetry/pip to python -m build/installer
	    update CHANGELOG.md


**[3.0.0] ----- 2022-10-30** ::

	    update CHANGELOG.md
	    Add epoch support - needs wider testing
	    update changelog


**[2.5.0] ----- 2022-10-26** ::

	    bug fix for _mkpkg_depends_files - silly typo
	    CHANGELOG.md


**[2.4.1] ----- 2022-10-24** ::

	    update pyproject.toml vers
	    update changelog


**[2.4.0] ----- 2022-10-24** ::

	    oops - accidently left debugger on!
	    update changelog


**[2.3.6] ----- 2022-10-24** ::

	    Fix bug parsion <package> >= xxx.  Greater than is fine.
	    update changelog


**[2.3.5] ----- 2022-10-23** ::

	    avoid all but tag in pkgver()
	    update pyproject.toml vers
	    update changelog


**[2.3.4] ----- 2022-10-23** ::

	    PKGBUILD - remove tag= now that pgkver() is getting latest tag


**[2.3.3] ----- 2022-10-23** ::

	    PKGBUILD now builds latest release tag
	    update changelog
	    Add comment about being fast
	    update changelog


**[2.3.2] ----- 2022-10-14** ::

	    Improve PKGBUILD for aur as per comments
	    update pyproject.toml version
	    Clean the dist directory before doing poetry build
	    fix python depends version > 3.9
	    Add makedepends packages in aur PKGBUILD
	    fix comment
	    add aur comment
	    update changelog


**[2.3.1] ----- 2022-10-13** ::

	    Update readme with link to AUR for mkpkg
	    Change PKGBUILD for AUR
	    little word smithing on readme
	    Clean up some comments
	    readme word smithing
	    update changelog


**[2.3.0] ----- 2022-10-13** ::

	    In the event mkpkg_depends / mkpkg_depends_files are absent,
	    no longer fall back to use makedepends unless turned on with the --mkp-use_makedepends option
	    update changelog


**[2.2.1] ----- 2022-10-13** ::

	    Bug fix for _mkpkg_depends_files
	    better packge description in PKGBUILD
	    readme markdown missed 2 spaces for newline
	    Readme - markdown requires escape for underscore
	    update CHANGELOG.md


**[2.2.0] ----- 2022-10-13** ::

	    Change PKGBUILD variables to have leading "_" to follow arch packaging guidelines
	    Code is backward compatible and will work with or without the _
	    New names are: _mkpkg_depends and _mkpkg_depends_files
	    update changelog
	    more readme tweaks
	    update changelog


**[2.1.1] ----- 2022-10-13** ::

	    Provide sample PKGBUILD to build mkpkg
	    update changelog
	    typo in readme
	    update changelog
	    README tweak to explain "patch" being same as "First_3" for version triggers
	    update CHANGELOG.md


**[2.1.0] ----- 2022-10-13** ::

	    Enhance version triggers to handle version with more than 3 elements
	    update changelog
	    readme tweaks
	    update CHANGELOG


**[2.0.1] ----- 2022-10-12** ::

	    update changelog
	    remove unused from do-install
	    update CHANGELOG
	    tweak readme
	    update changelog


**[2.0.0] ----- 2022-10-12** ::

	    Reorganize directory structure and use poetry for packaging.
	    Add support for triggers now based on semantic versions.
	    e.g python>3.12 or python>minor - where minor triggers build if
	    major.minor version of dependency package is greater than that used when
	    it was last built.
	    Reorganize source tree
	    Update changelog
	    tweak readme little more
	    update Changelog
	    Tweak README
	    tweak README


**[1.3.1] ----- 2022-09-22** ::

	    Update Changelog
	    Add CVE-2022-36113 as example of build tool danger
	    Update Changelog
	    Add Changelog


**[1.3.0] ----- 2022-09-07** ::

	    fix out of date comment in mkpkg.py
	    fix little markdown issue
	    tweak readme format


**[1.2.0] ----- 2022-09-06** ::

	    Add support for trigger files : mkpkg_depends_files
	    add README discssion comment
	    lint picking
	    Add comment in README
	    few more README tweaks


**[1.1.1] ----- 2022-09-04** ::

	    tidy message output
	    typo
	    Little tidy on README


**[1.1.0] ----- 2022-09-04** ::

	    Handle edge case when PKGBUILD hand edited
	    Bug fix for case when override mkpkg_depends set to empty set


**[1.0.5] ----- 2022-09-03** ::

	    Now that we implemented mkpkg_depends, remove some readme comments
	    typo
	    minor README tweak
	    Fix typo (resolves issue #1) and tweak README


**[1.0.4] ----- 2022-09-03** ::

	    fix section numbers in README


**[1.0.3] ----- 2022-09-03** ::

	    Support mkpkg_depends overriding makepends - gives full control to user


**[1.0.2] ----- 2022-09-03** ::

	    README use lower case for mkpkg


**[1.0.1] ----- 2022-09-03** ::

	    Tidy couple comments


**[1.0.0] ----- 2022-09-03** ::

	    Initial Revision of mkpkg.
	    mkpkg builds Arch packages and rebuilds them whenever a make dependency is more recent than the last package


