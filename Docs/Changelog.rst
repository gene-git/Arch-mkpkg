Changelog
=========

[4.7.0] ----- 2023-10-03
 * update project version  
 * Bug fix semantic version comparisons  
 * Stop treating Arch pkgrel as part of the last version element - its separate additional element  
 * update Docs/Changelog.rst  

[4.6.0] ----- 2023-09-28
 * update project version  
 * change pyproject to use README.rst  
 * Reorganize the tree and documents.  
 * Switch from markdown to restructured text.  
 * Now easy to build html and pdf docs using sphinx  
 * update CHANGELOG.md  

[4.5.5] ----- 2023-06-05
 * update project version  
 * Small tweaks to README  
 * update CHANGELOG.md  

[4.5.4] ----- 2023-05-18
 * update project version  
 * Change PKGBUILD makedepnds from pip to installer  
 * update CHANGELOG.md  

[4.5.3] ----- 2023-05-18
 * update project version  
 * install: switch from pip to python installer package. This adds optimized bytecode  
 * update CHANGELOG.md  

[4.5.2] ----- 2023-05-18
 * update project version  
 * PKGBUILD: build wheel back to using python -m build instead of poetry  
 * update CHANGELOG.md  

[4.5.1] ----- 2023-05-17
 * update project version  
 * Simplify Arch PKGBUILD and more closely follow arch guidelines  
 * update CHANGELOG.md  

[4.5.0] ----- 2023-02-19
 * update project version  
 * Fix bug when soname dependency drives rebuild by ensuring pkgrel is bumped  
 * update CHANGELOG.md  

[4.4.0] ----- 2023-02-18
 * update project version  
 * Bug fix extracing PKGBUILD for certain cases  
 * update CHANGELOG.md  

[4.3.0] ----- 2023-01-31
 * update project version  
 * typo  
 * Force now bumps the package release and rebuilds  

[4.2.2] ----- 2023-01-06
 * update CHANGELOG.md  

[4.2.1] ----- 2023-01-06
 * update project version  
 * Add SPDX licensing lines  
 * Lint and tidy  
 * update CHANGELOG.md  

[4.2.0] ----- 2023-01-03
 * update project version  
 * Fix for potential color match bug  
 * update CHANGELOG.md  

[4.1.1] ----- 2022-12-16
 * update project version  
 * Add toml dependency to PKGBUILD  
 * update CHANGELOG.md  

[4.1.0] ----- 2022-12-16
 * update project version  
 * Add config file support.  
 * Change option handling. Options to be passed to makepkg must now be placed after --  
 * Improveed soname treatment via option --soname-build (missing (default), newer or never)  
 * ;  
 * update CHANGELOG.md  

[4.0.0] ----- 2022-12-15
 * update project version  
 * Soname suggestion thanks to Alberto Novella Archlinux subredit.  
 * Add --mkp-refresh  
 * Attempts to update saved metadata files. Faster, if imperfect, alternative to rebuild.  
 * more work on soname change driven build  
 * refactor some code  
 * pull out pacman queries to more easily share  
 * build foundation code for soname checks  
 * ;  
 * Use poetry to build wheel.  
 * Use pip install in installer script.  
 * Rename src/mkpkg/utils -> src/mkpkg/lib  
 * update CHANGELOG.md  

[3.5.4] ----- 2022-11-29
 * update project version  
 * tweak readme  
 * improve bash variable check in installer - no functional change  
 * update CHANGELOG.md  

[3.5.3] ----- 2022-11-05
 * update project version  
 * tweak readme some  
 * tweak readme  
 * update CHANGELOG.md  
 * update CHANGELOG.md  

[3.5.2] ----- 2022-11-04
 * update project version  
 * PKGBUILD - duh - put back makedepends on poetry  
 * update CHANGELOG.md  

[3.5.1] ----- 2022-11-04
 * update project version  
 * vers now 3.5.1  
 * Add package name to screen message  
 * update CHANGELOG.md  

[3.5.0] ----- 2022-11-03
 * update project version  
 * bug fix incorrectly handling triggers pkg>xxx  
 * update CHANGELOG.md  

[3.4.0] ----- 2022-11-03
 * update project version  
 * Better handling of PKGBUILD syntax errors  
 * update CHANGELOG.md  

[3.3.1] ----- 2022-11-03
 * update project version  
 * unwind prev error check - needs more work  
 * update CHANGELOG.md  

[3.3.0] ----- 2022-11-03
 * update project version  
 * Additional check for errors when sourcing PKGBUILD  
 * info messagetypo verion -> version  
 * update CHANGELOG.md  
 * update CHANGELOG.md  
 * update CHANGELOG.md  

[3.2.0] ----- 2022-10-31
 * update project version  
 * bah typo - sorry  
 * tidy  
 * update CHANGELOG.md  

[3.1.0] ----- 2022-10-31
 * update project version  
 * duh me - do-install  
 * typo - missing if in do-install  
 * update CHANGELOG.md  

[3.0.1] ----- 2022-10-31
 * update project version  
 * Add more aliases of First_N for version comparisons (micro, serial)  
 * Change build from poetry/pip to python -m build/installer  
 * sync PKGBUILD from aur  
 * update CHANGELOG.md  

[3.0.0] ----- 2022-10-30
 * update project version  
 * Add epoch support - needs wider testing  
 * debug off  
 * upd changelog  

[2.5.0] ----- 2022-10-26
 * bug fix for _mkpkg_depends_files - silly typo  
 * upd changelog  

[2.4.1] ----- 2022-10-24
 * update pyproject vers  
 * update changelog  

[2.4.0] ----- 2022-10-24
 * oops - accidently left debugger on!  
 * update changelog  
 * update 2.3.6  
 * Fix bug parsion <package> >= xxx.  Greater than is fine.  
 * Fix bug parsion <package> >= xxx.  Greater than is fine.  

[2.3.5] ----- 2022-10-23
 * update pyproject.toml vers  
 * avoid all but tag in pkgver()  

[2.3.4] ----- 2022-10-23
 * Prep for 2.3.4  
 * PKGBUILD - remove tag= now that pgkver() is getting latest tag  
 * typo  
 * update changelog  

[2.3.3] ----- 2022-10-23
 * update pyproject.toml version to 2.3.3 release  
 * Update PKGBUILD to get build latest release tag  
 * update changelog  
 * Add comment about being fast  
 * bump aur to latest tag  
 * update changelog  

[2.3.2] ----- 2022-10-14
 * remove execute mode on license file  
 * Clean the dist directory before doing poetry build  
 * update pyproject.toml version  
 * Improve PKGBUILD for aur as per comments  
 * fix python depends version > 3.9  
 * Update minimum python in PKGBUILD dependency  
 * Remove python from  makedepends PKGBUILD as in depends  
 * Add makedepends packages in aur PKGBUILD  
 * fix comment  
 * add aur comment  
 * update changelog  

[2.3.1] ----- 2022-10-13
 * Update readme with link to AUR for mkpkg  
 * Prep PKGBUILD for aur  
 * little word smithing on readme  
 * Clean up some comments  
 * readme word smithing  
 * update changelog  

[2.3.0] ----- 2022-10-13
 * turn off debug  
 * In the event mkpkg_depends / mkpkg_depends_files are absent,  
 * no longer fall back to use makedepends unless turned on with the --mkp-use_makedepends option  
 * update changelog  

[2.2.1] ----- 2022-10-13
 * Bug fix for _mkpkg_depends_files  
 * better packge description in PKGBUILD  
 * readme markdown missed 2 spaces for newline  
 * Readme - markdown requires escape for underscore  
 * update CHANGELOG.md  

[2.2.0] ----- 2022-10-13
 * Change PKGBUILD variables to have leading "_" to follow arch packaging guidelines  
 * Code is backward compatible and will work with or without the _  
 * New names are: _mkpkg_depends and _mkpkg_depends_files  
 * update changelog  
 * more readme tweaks  
 * update changelog  
 * update changelog  

[2.1.1] ----- 2022-10-13
 * update do-install to share PKGBUILD  
 * update changelog  
 * Provide sample PKGBUILD to build mkpkg  
 * update changelog  
 * typo in readme  
 * update changelog  
 * README tweak to explain "patch" being same as "First_3" for version triggers  
 * update CHANGELOG.md  

[2.1.0] ----- 2022-10-13
 * Enhance version triggers to handle version with more than 3 elements  
 * update changelog  
 * readme tweaks  
 * update CHANGELOG  

[2.0.1] ----- 2022-10-12
 * update changelog  
 * remove unused from do-install  
 * update changelog  

[2.0.0] ----- 2022-10-12
 * tweak readme  
 * tweak readme  
 * Update Changelog  
 * Update README with whats new  
 * use ln -sf when making link in /usr/bin/mkpkg to handle a previous build failure  
 * buglet do-install  
 * update changelog  

[1.9.9] ----- 2022-10-12
 * Reorganize directory structure and use poetry for packaging.  
 * Add support for triggers now based on semantic versions.  
 * e.g python>3.12 or python>minor - where minor triggers build if  
 * major.minor version of dependency package is greater than that used when  
 * it was last built.  

