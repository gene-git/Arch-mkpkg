
# OVERVIEW of mkpkg

Building an Arch package requires invoking *makepkg* with *PKGBUILD* file.
PKGBUILD file uses a *depends* variable to descibe a list of packages needed to employ the 
tool provided by the package.

It also optionally uses a 'makedepends' variable which is a list of packages that are
needed to build the package. Contrast this to *depends* which are needed to use it.

Ordinarily, if the tool hasn't changed but something in the *makedepends* list has changed,
running *makephg* will do nothing as it deems the package up to date.

We consider packages that you deem appropriate to trigger a build as trigger packages.
The preferred way to provide the list of these packages is using the PKGBUILD variable
*mkpkg_depends*. If that is not provided then mkpkg defaults to using the *makedepends* variable.
As discussed below the latter is likely a bit too conersvative. 

The mkpkg tool provides a mechanism to rebuild a package whenever any one of of the trigger packages is 
newer than the last time the package was built, even if the tool itself is otherwise up to date.
When *mkpkg_depends* variable is found the packages listed in *makedepends* will not be used.

This is perhaps most useful for packages which statically link libraries, or when core build tools
change and it's important to rebuild with the newer versions. Do we really need to rebuild a package
when tool chain changes? Sometimes yes; as an example whenever the toolchain is updated, 
I always rebuild my kernel packages and test. 

Majority of packages are built against shared libraries which are usually less of a problem of course.


## Contents

    1. Introduction
    2. Source code 
    3. How to use mkpkg
    4. mkpg_depends and makedepends_add
    5. Discussion
    6. Arch AUR package - TBD

### See:

 - [Github source ](https://github.com/gene-git/Arch-mkpkg)
 - [Arch Wiki page ](https://wiki.archlinux.org/title/mkpkg) - TBD 

# 1. Introduction 

mkpkg has one dependency,  python. 

It uses makepkg to perform the actual package builds in the usual way. That said,  makepkg is 
a part of pacman which is always installed and thus not a 'dependency' in the PKGBUILD meaning.

When a tool chain used to build a package is updated, it's good practice, IMHO, to 
rebuild packages which use that tool chain.  For example, when gcc, cargo, binutils et al are updated 
packages using those tools should also be updated. As mentioned above, whenever compiler/binutils 
tool chain changes, I always rebuild and test my kernel packages.

While static linked libraries surely don't demand a rebuild to function, obviously, because 
the older library is part of the binary itself, it's still a good idea to rebuild it. 
This will pick up bug fixes, including security related ones, as well as improvements.  Of course,
it's always sensible to confirm that an application properly builds and works with 
the newer tool or library as well.

Here's an example. The *refind* boot manager statically links against gnu-efi. So when gnu-efi is updated, 
refind should be rebuilt as well even though the previous one will continue to work just fine.

Recently, arch started switching many packages to be compiled with lto. The gnu-efi package 
was subsequently compiled with " -flto -ffat-lto-object".  The refind boot manager statically 
links gnu-efi.  At this point, refind itself had not changed and so it's up to date as far 
standard approach is concerned. 

However, I would like to know as early as possible that refind builds and runs with the the 
new gnu--efi library that was updated. In fact, unfortunately perhaps, this build failed and 
refind not longer builds with the updated gnu-efi library due to lto changes. Good to know.

You could of course have waited until refind itself gets an update and then discover - oh 
no it no longer builds. But, by doing this early and in this case knowing refind itself has 
not changed, I know with certainty that this problem stems from the gnu-efi rebuild and not from a 
refind change - without even looking at any refind source changes.

Given the large number of packages I build I doubt I'd remember what trigger packages 
are approprate for every package anyway. Computers are good at automating
repetitive tasks after all and are much quicker at identifying the trigger packages.

mkpkg was created to address this need. It automates this for you and rebuilds packages when needed.
This allows for early detection of problems or confirmation that things are actually fine.

A small side comment on shared libraries. While these are generally not a problem, 
there is an assumption that the library itself still functions the same for whatever part 
of it the tool is using.  Majority of providers are careful with *soname*s as well, so most of the time 
that's likely true - however, the cautious among us may want to run regression tests even in this case, 
certainly for mission critical tools. Bugs happen, and it's good to learn of any issues as quickly 
as possible.


# 2. Source for mkpkg

The source is kept in the github repository Arch-mkpkg, link above.


# 3. How to use mkpkg

Simply call mkpkg instead of makepkg. Couldn't be simpler. 
Arguments for mkpkg are all passed through to *makepkg* execpt for those of the form:

 - **--mkp-\<option\>**

These are used by mkpkg itself. The options currently supported are:

 - **--mkp-verb**   
   Show (stdout) output of makepkg.  Default is not to show it.

 - **--mkp-force**   
   Force a makepkg run even if not needed. You may want to also set the *-f* option to be passed on to makepkg.

What mkpkg does is roughly:
    
 - If PKGBUILD has a pkgver() function, check if the pkgver variable matches its output
 - If the 2 pkgver match or if there is no pkgver() function then check if a matching package exists
 - If package not up to date, then run usual makepkg build.
 - If package seems otherwise up to date, then check if any of the makedepend packages is newer
   than the package file and if found, bump the pkgrel and rebuild package.
 - If the package is out of date, as there is newer version then reset pkgrel back to "1" and build.

So, if a package builds and gets larger package releae number, it was because of some trigger package 
dependency. If package release is "1" - then you know its a fresh package version.

I use separate tool to run all my package builds so I prefer the output to be easily parseable and provide
simple clear information.

mkpkg thus prints a line of the form:

    *mkp-status: <status> <package-version>*

Where status is one of :
 
 - current -> package is up to date
 - success -> package was built successfully
 - error   -> problem occurred.

  Obviously, <package-version> is what is sounds like.

It is possible for mkpkg itself to fail for some reason, in which case the *mkp-status:* line could be absent.
This is equally simple to detect.
  

# 4. Variables mkpkg_depends and makedepends_add

If the list of makedepends does not meet user needs, then the PKGBUILD variable 

 - *mkpkg_depends*

Using this varible the much preferred way to assign trigger dependencies, and allows for removal
of  things like 'git', 'pandoc' etc. which, while required for building, don't usually have any 
affect on the tool function. Without adding this variable to PKGBUILD, then by default
the makedepends variable is used, which is certainly likely to be conservative.

When mkpkg_depens is present is used as the provider of the trigger dependencies in place 
of the standard *makedepends* variable.  This offers complete control over what actually triggers rebuilds.

While depends are also treated by makepkg as build dependencies, mkpkg does not.  Why?
For starters, frequently these are really run time only dependencies and 
as such are not actually needed to build the package. 

Secondly, split packages may have separate depends lists which would add some unnecessary complexity. 

mkpkg also reads the variable makedepends_add - which are simply treated as additional 
trigger dependencies. When using mkpkg_depends, this is unncessary.

# 5. Discussion

While mkpkg works for all the packages I build, I consider this *beta* until it's had
sufficient time to get beaten up some more :)

Possible future enhancement: 

As said above, it's pretty useful to run regression tests after run-time dependencies change.
For example shared libraries or other programs used by the tool.
To handle this case we might consider adding a separate variable - such as *mkpkg_test_depends* 
which lists these kind of dependencies.  Some thought is warranted around how this might 
intersect, or not,  with *checkdepends*. These are of course different as they are for 
those packages used for testing but NOT for running the tool.

# 6. Arch AUR Package - TBD

 - On the todo list - volunteers appreciated :)

