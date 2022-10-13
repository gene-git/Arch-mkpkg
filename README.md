
# OVERVIEW of mkpkg

Building an Arch package requires invoking *makepkg* with *PKGBUILD* file.
PKGBUILD file uses a *depends* variable to list those packages needed to employ the 
tool provided by the package.

It also optionally uses a 'makedepends' variable which is a list of packages that are
needed to build the package. 

The only thing which causes a rebuild is a change to the package version - either because
the underlying tool itself changed or because the packager manually forced a rebuild
by changing the release version.

If you ever needed to manually rebuild a package by bumping the release version, then
something is clearly not right. If something triggered a rebuild other than the package itself updating
it would be better if this were automatic and not manual - especially if something broke, and then you
discovered a need to 'rebuild' a package as a result of something it uses having changed.

This is what mkpkg helps with - it automates rebuilds when they are needed for some reason 
other than the tool / package version itself changing. 

mkpkg allows you to define a set of *trigger* packages. These are packages that, well yes, trigger
 a rebuild whenever they change. Simple.

The packager is responsible for making the list of those trigger packages which are appropriate.  

The way to provide the list of these trigger packages is by using the PKGBUILD variable
*_mkpkg_depends*. There are 2 ways to specify a trigger package - (1) a package name and 
(2) a package and a requirement about its version. 

  - *_mkpkg_depends* is a list of packages which can trigger a rebuild   
     Each item in the list is either   
    (1) A package name   
        Rebuilds if the install date is more recent than the last build time 

    (2) A package version requirement    
        It can be an explicit version or a key word such as *major* which would then only trigger
        rebuild when the major version of that package was greater than that at the last build. 
        More details are below.
      
It can also use any file to trigger a build using *_mkpkg_depends_file*. Typical use case
for these might be files provided by the packager, rather than the source, which include 
things such as systemd unit files or pacman hook files or other package related items.

This is useful to ensure packages build and work when other packages get updated.
It is also useful for packages which statically link libraries, or when core build tools
change and it's important to rebuild with the newer versions. Do we really need to rebuild a package
when tool chain changes? Sometimes yes; as an example whenever the compiler toolchain is updated, 
I always rebuild my kernel packages and test. 


Majority of packages are built against shared libraries  but may be helpful there too; 
there are additional comments on this topic below.  As an example, I rebuild my python 
applications when python's major.minor is larger than what was used for previous build.

## Whats New

Version 2.x.y brings fine grain control by allowing package dependences to trigger 
builds using semantic version. For example 'python>minor' will rebuild only if a new
python package has it's major.minor greater than what it was when package was last built.
See *_mkpkg_depends* below for more detail. 

The source has been reorganized and packaged using poetry which simplifies installation.
The installer script, callable from package() function in PKGBUILD has been updated 
accordingly. Ther build() function should now just call poetry build to generate the
wheel package.

Changed the PKGBUILD variables to have underscore prefix to follow Arch Package Guidelines.
Variables are now: *_mkpkg_depends* and *_mkpkg_depends_files*. 
The code is backward compatible and supports the previous variable names without the 
leading "\_" as well as the ones with the "\_".

## Contents

    1. Introduction
    2. Source code 
    3. How to use mkpkg
    4. PKGBUILD Variables
    5. Discussion and Next Steps
    6. Installation
    7. Arch AUR package - TBD

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

## _mkpkg_depends and _mkpkg_depends_files

The preferred way to list trigger packages is to use:

 - *_mkpkg_depends*

This variable provides a list of packages which should trigger a rebuild. 
Each item in the list can be in one of 2 forms:

  1. *name*
     If the item is simply the name of the package then,
     this will trigger a rebuild if the install time of a listed package is newer than the
     time of the last build.  

  2. *package_name* *compare op* *vers_trigger*
     This provides semantic version triggers. Package versions are taken
     to be of the form 'major.minor.patch' or more generally 'elem1.elem2.elem3....'
     White space around the comparison operator is optional. 

  - *compare op* 
        is one of : >, >= or <

  - *vers_trigger* 
    Based on comparing the first [N] elems of the version or the entire version.
    - First_[N] : rebuild if first [N] elems of package version greater than when last built
    - major     : alias for First_1 (rebuild if major > last_build_major version)
    - minor     : alias for First_2 (rebuild if major.minor > last_build_major.minor version)
    - patch     : alias for First_3 (rebuild if major.minor.patch > last_build_major.minor.patch version)
    - last      : rebuild if package version > last_build version.
    
*last* is very similar to a time based trigger but based on version instead of time.

For example if the expression is 'pkg_name>First_2' or equivalently 'pkg_name>minor' and
the current package version is 1.2.3 while the version when last built was 1.2.0 then
the versions being compared would be is 

'1.2' > '1.2' which is false. 

Whereas if the expression was 'pkg_name>First_3' then the comparison would be  

'1.2.3' > '1.2.0' which is true


N.B. The package must be built at least once using mkpkg so it can save the dependent package
versions used. So if a version trigger is added,  then this triggers a rebuild as it treats this
as if the dependent package version is greater than last used (which is not known at this point).
On subsequent builds the last built version of each dependent package is then known.

Unlike *makedepends* variable, this allows one not include things that are required to build the
package but don't have any affect on the tool function. E.g. things like 'git'.

For example if at last build python was 3.10 :

        _mkpkg_depends=('python>minor' 'python-dnspython')

Then a rebuild will be done if python is greater than or equal to 3.11.x or if
python-dnspython was installed more recently than the last build. This will not trigger
a rebuild if python is updated from 3.10.7 to 3.10.8 which is a patch update not a minor
or major update. 

Why support '<' you may ask.  The only sensible use for less than operator would be to 
provide a mechanism to trigger a rebuild when a package gets downgraded. This would be
accomplished using :

        pkg_name < last 

 - *_mkpkg_depends_files*
    This variable can be used to provide a list of files used to trigger a build.
    The files are relative the directory containing PKGBUILD.  

    This might be useful, for example, if the source for some daemon doesn't provide a 
    systemd service file, and the packager adds the file. Adding the file to this list 
    would now trigger rebuilds should there be changes to the service file.
    An alternative would be to put these files into a git repo and just using the git version.
    For a small number of files this may be more convenient/simpler.

These variables offer considerable control over what can be used to trigger rebuilds.
If none of the mkpkg_xxx variables are found in PKGBUILD, then *makedepends* variable is used 
as a fall back.  This is likely to be conservative, and may trigger unnecessarily, but may not 
have other desirable trigger packages. This only happens when the variables are missing so
an empty _mkpkg_depends variable will prevent the fallback.

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

# 6. Installation

    First cd to the source git area and pulling from git as usual :
        git fetch
        git pull origin

    Build:
        poetry build

    Install:
        ./do-install ${pkgdir}

# 7. Arch AUR Package - TBD

 - Sample PKGBUILD provided which builds latest from git
 - Should be made available on AUR - On the todo list - feel free :)

