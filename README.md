
# OVERVIEW of mkpkg

Building an Arch package requires invoking *makepkg* with *PKGBUILD* file.
PKGBUILD file uses a *depends* variable to descibe a list of packages needed to use the tool the package 
provides.

It also optionally uses a 'makedepends' variable which is a list of packages that are
needed to build the package. Contrast this to *depends* which are needed to use it.

Ordinarily, if the tool hasn't changed but something in the *makedepends* list has changed,
running *makephg* will do nothing as it deems the package up to date.

The mkpkg tool provides a mechanism to rebuild a package whenever any one of of the makedepends packages is 
newer than the last time the package was built, even if the tool itself is otherwise up to date.
If you don't want every package in makepends to be used a build trigger, then simply
use *mkpkg_depends* instead. If this variable is used, the packages listed in *makedepends* will not be used.

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

It does use makepkg to perform package builds in the usual way. That said,  makepkg is 
a part of pacman which is always installed and thus not a 'dependency' in the PKGBUILD meaning.

When a tool chain used to build a package is updated, then it's good practice to 
rebuild packages which use that tool chain.  For example, when gcc, cargo, binutils et al are updated 
packages using those tools should also be updated.

While static linked libraries surely don't demand a ebuild to function, because the older library 
is part of the binary itself, it's still good idea to rebuild it. This will pick up fixes, 
including security related ones,  as well as improvements.  Of course,
it's always sensible to confirm that the application properly builds and works with 
the newer tool or library.

Another example. The *refind* boot manager statically links against gnu-efi. So when gnu-efi is updated, refind
should probably be rebuilt as well.

mkpkg was created to address this need.

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

So, if a package builds and gets bugger package releae number, it was because of make depends. If 
package release is "1" - then you know its a new package.

I use another tool to run all my package builds so I prefer the output to be easily parseable and provide
simple clear information.

mkpkg thus prints a line of the form:

    *mkp-status: <status> <package-version>*

Where status is one of :
 
 - current -> package is up to date
 - success -> package was built successfully
 - error   -> problem occurred.

  Obviously, <package-version> is what is sounds like.

It is possible for mkpkg itself to fail for some reason, in which case the *mkp-status:* line would be absent.
This is also simple to detect.
  

# 4. Variables mkpkg_depends and makedepends_add

If the list of makedepends does not meet user needs, then the variable 

 - *mkpkg_depends*

may be used - if present its list of dependencies are used in place of the standard *makedepends* 
variable. This offers complete control over what actually triggers rebuilds.

While depends are also treated by makepkg as build dependencies, mkpkg does not.  Why?
For starters, frequently these are really run time only dependencies and 
as such are not actually needed to build the package. 

Secondly, split packages may have separate depends lists which would add some unnecessary complexity. 

Also, the PKGBUILD wiki discourages duplicating any depends packages into makdepends. 
Therefore in order to permit including specific sets of packages as makepends which are also in 
the depends list, we allow those to be in a second list in the PKGBUILD. The 
PKGBUI:D variable makedepends_add does this.

Any packages listed in *makedepends_add* will be appended to the *makedepend* list.
This allows for additional packages, treated exactly same as makedepends,  while following 
the PKGBUILD guidelines should they be in the depends list.

While some may prefer that depends and makedepends lists to be for distinct purposes - one for run 
time the other for build time, makepkg treats depends as makedepends - we do not 
as explained above. From mkpkg perspective we consider depends to be runtime, and 
build time are given by makedepnds and makedepends_add or more simply by mkpkg_depends.

# 5. Discussion

While mkpkg works for all the packages I build, I consider this *beta* until it's had
sufficient time to get beaten up some more :)

One possible area for extension is for those packages in makedepends that arguably may not require 
rebuild. While compiler tools certainly do demand a rebuild things such as *git* may not.
While it's better to err on being conservative and build when not entirely needed, it's
certainly better than vice versa. On the other hand, packages such as python, in my view do
demand a rebuild.

That said we may consider a future enhancement which could mark such dependencies so as to
be ignored as far as makepdends checks go.

One simple way to achieve that would be to add a new variable to the PKGBUILD with the list of those
packages which should be ignord for driving a rebuild. 

# 6. Arch AUR Package - TBD

 - On the todo list - volunteers appreciated :)

