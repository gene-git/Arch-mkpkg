
# OVERVIEW of mkpkg

Building an Arch package requires invoking *makepkg* with *PKGBUILD* file.
PKGBUILD file uses a *depends* variable to descibe a list of packages needed to employ the 
tool provided by the package.

It also optionally uses a 'makedepends' variable which is a list of packages that are
needed to build the package. Contrast this to *depends* which are needed to use it.

The only thing which causes a rebuild is a change to the package version - either because
the underlying tool itself changed or because the packager manually forced a rebuild
by changing the release version.

If you ever needed to manually rebuild a package by bumping the release version, then
something is clearly not right. If something triggered a rebuild other than the package itself updating
it would be better if this were automatic and not manual - especially if something broke, and then you
discovered a need to 'rebuild' a package as a result of something it uses having changed.

This is what mkpkg helps with - it automates rebuilds when they are needed for some reason 
other than the tool / package version itself changing. 

Ordinarily, if the tool hasn't changed running *makephg*  does nothing as it deems the package up to date.

mkpkg allows you to define a set of *trigger* packages. These are packages that, well yes, trigger
 a rebuild whenever they change. Simple.

The packager is responsible for making the list of those trigger packages which are appropriate.  

The preferred way to provide the list of these trigger packages is by using the PKGBUILD variable
*mkpkg_depends*. However, if that is not provided, then mkpkg defaults to using the *makedepends* variable.
As discussed below the latter is quite likely a bit too conservative and it may miss things
that should be there.  The fall through to using *makedepends* only 
occurs When *mkpkg_depends* variable is absent.

mkpkg provides a mechanism to rebuild a package whenever any one of of the trigger packages is 
newer than the last time the package was built, even if the tool itself is otherwise up to date.

This is perhaps most useful for packages which statically link libraries, or when core build tools
change and it's important to rebuild with the newer versions. Do we really need to rebuild a package
when tool chain changes? Sometimes yes; as an example whenever the toolchain is updated, 
I always rebuild my kernel packages and test.  


Majority of packages are built against shared libraries which are usually less of a problem, but 
sometimes it may be relevant there as well; there are additional comments on this topic below.


## Contents

    1. Introduction
    2. Source code 
    3. How to use mkpkg
    4. PKGBUILD Variables
    5. Discussion and Next Steps
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
tool chain changes, I always rebuild and test my kernel packages. This not only ensures that
things compile and work properly with the new build tools but can also be key to reducing the attack
surface. One recent little example, not to pick on cargo, is 
[CVE-2022-36113](https://nvd.nist.gov/vuln/detail/CVE-2022-36113). 
Of course this would require a case where cargo is actually downloading something which
should never be permitted; still, it's a conceivable danger.

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

But there are indeed some shared library packages, some with dynamically loaded 
libraries (plugins) that may also be trigger packages.  One symptom of that need are those
packages that are manually rebuilt by forcing a release version bump typically with a comment
such as *rebuilt with latest ...* - we certainly see plenty of that happening.


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

  Obviously, package-version is what is sounds like.

It is possible for mkpkg itself to fail for some reason, in which case the *mkp-status:* line could be absent.
This is equally simple to detect.
  

# 4. PKGBUILD Variables 

## mkpkg_depends, mkpkg_depends_files and makedepends

The preferred way to list trigger packages is to use:

 - *mkpkg_depends*

Using this variable is the best way to assign trigger dependency packages. Unlike the *makedepends*
variable, it allows ignoring things like 'git' or 'pandoc' etc. which, while required 
for building, don't usually have any affect on the tool function. 
If this variable is absent in PKGBUILD, then by the *makedepends* variable is used as a fall 
through second choice.  This is certainly likely to be conservative, but may trigger unnecessarily.

 - *mkpkg_depends_files*

This variable can be used to provide a list of trigger files which are also be used to trigger a build.
The files are relative the directory containing PKGBUILD.
This might be convenient, for example, if the source for some daemon doesn't provide a 
systemd service file, and the packager adds one. In which case you may want to trigger on that file
to handle changes to it. For one file this may be simpler than using a companion git repo.

These 2 variables offer considerable control over what can be used to trigger rebuilds.

 - *makedepends_add* : deprecated

This is now superceded by *mkpkg_depends* and will be removed at some point.
mkpkg still used it and any packages listed continue to be simply treated as additional 
trigger dependencies. 

# 5. Discussion and Next Steps

While mkpkg works for all the packages I build, I consider this *beta* until it's had
sufficient time to get beaten up some more :)

Possible future enhancement: 

As mentioned earlier, it's pretty useful to run regression tests after run-time dependencies change.
For example shared libraries or other programs used by the tool.
To handle this case we might consider adding a separate variable - such as *mkpkg_test_depends* 
which lists these kind of dependencies.  
We note that *checkdepends* are quite different in intent, as they identify 
those packages used for testing but NOT for running the tool. Testing tools and such.

# 6. Arch AUR Package - TBD

 - On the todo list - volunteers appreciated :)

