# Changelog

## [2.0.0] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2022-10-12
 - Reorganize directory structure and use poetry for packaging.  
   Add support for triggers now based on semantic versions.  
   e.g python>3.12 or python>minor - where minor triggers build if  
   major.minor version of dependency package is greater than that used when  
   it was last built.  
 - Reorganize source tree  
 - Update changelog  
 - tweak readme little more  
 - update Changelog  
 - Tweak README  
 - tweak README  

## [1.3.1] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2022-09-22
 - Update Changelog  
 - Add CVE-2022-36113 as example of build tool danger  
 - Update Changelog  
 - Add Changelog  

## [1.3.0] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2022-09-07
 - fix out of date comment in mkpkg.py  
 - fix little markdown issue  
 - tweak readme format  

## [1.2.0] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2022-09-06
 - Add support for trigger files : mkpkg_depends_files  
 - add README discssion comment  
 - lint picking  
 - Add comment in README  
 - few more README tweaks  

## [1.1.1] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2022-09-04
 - tidy message output  
 - typo  
 - Little tidy on README  

## [1.1.0] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2022-09-04
 - Handle edge case when PKGBUILD hand edited  
 - Bug fix for case when override mkpkg_depends set to empty set  

## [1.0.5] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2022-09-03
 - Now that we implemented mkpkg_depends, remove some readme comments  
 - typo  
 - minor README tweak  
 - Fix typo (resolves issue #1) and tweak README  

## [1.0.4] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2022-09-03
 - fix section numbers in README  

## [1.0.3] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2022-09-03
 - Support mkpkg_depends overriding makepends - gives full control to user  

## [1.0.2] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2022-09-03
 - README use lower case for mkpkg  

## [1.0.1] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2022-09-03
 - Tidy couple comments  

## [1.0.0] ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 2022-09-03
 - Initial Revision of mkpkg.  
   mkpkg builds Arch packages and rebuilds them whenever a make dependency is more recent than the last package  

