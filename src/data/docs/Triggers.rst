
.. _mkpkg-triggers:

========
Triggers
========

There are 2 kinds of triggers. A trigger based on package and a trigger based on a file.
Each of these uses a PKGBUILD variable with an array of triggers. 

_mkpkg_depends
--------------

This is used to confugure packages. Changes in one of the packages that meets
the condition of the trigger, will cause a rebuild.

The variable in PKGBUILD is: **_mkpkg_depends**

This holds an arry of package based triggers. Each trigger in the list can take one of 2 forms:

* **package_name**

  This item is the name of a package.
  Rebuild is triggered if the install time of this package is newer than the
  the last build time.  

* **package_name compare-op vers_trigger**

  This is a semantic version trigger. Versions are 
  of the form 'major.minor.patch' or more generally 'elem1.elem2.elem3....'
  White space around the comparison operator is optional. 
  Rebuild is triggered when the version of *package_name* satisfies the rule.

  e.g. 'python > minor' causes a rebuild when the minor version is larger than 
  the minor version used in previous build.

Where:

* *compare-op* 

  is one of : **>**, **>=** or **<**

* *vers_trigger* 

  Based on comparing the first [N] elems of the version or the entire version.

  * First_[N] : rebuild if first [N] elems of package version greater than when last built

  * major     : alias for First_1 (rebuild if major > last_build)

  * minor     : alias for First_2 (rebuild if major.minor > last_build)

  * patch     : alias for First_3 (if major.minor.patch > last_build). Also called *micro*  

  * extra     : alias for First_4 (major.minor.patch.extra)  Also called *releaselevel*

  * serial    : alias for First_5 (major.minor.patch.extra.serial)  

  * last      : rebuild if package version > last_build version.
    
*last* is very similar to a time based trigger but based on version instead of time.

For example, the expression ::

    'pkg_name>First_2' 

or equivalently::

    'pkg_name>minor' 
    
Say the current package version is 1.2.3,  and the version when last built was 1.2.0 then
the versions being compared would be ::

    '1.2' > '1.2' which is false. 

Whereas if the expression was::

    'pkg_name>First_3'

then the comparison would be ::

    '1.2.3' > '1.2.0' 

which is true

N.B. The package must be built at least once using mkpkg so it can save the various package
versions used. So if a version trigger is added,  then this triggers a rebuild as it treats this
as if the dependent package version is greater than last used (which is not known at this point).
On subsequent builds the last built version of each dependent package is then known.

Unlike the standard *makedepends* variable, this allows one to not include things 
that are required to build the package but don't have any affect on the tool function. 
For example 'git' - which while required to build will not generally change the tool.

Another example, if python was version 3.13 when the package was last built and we have:::

        _mkpkg_depends=('python>minor' 'python-dnspython')

Then a rebuild will be done if python is greater than or equal to 3.13.x or if
python-dnspython was installed more recently than the last build. This will not trigger
a rebuild if python is updated from 3.13.7 to 3.13.8,  since this is a patch update 
not a minor or major update. 

Why support '<' you may ask.  The only sensible use for less than operator would be to 
provide a mechanism to trigger a rebuild when a package gets downgraded. This would be
accomplished using ::

        pkg_name < last 

_mkpkg_depends_files
--------------------

The variable **_mkpkg_depends_files**  is used to track changes in files.
Filenames are relative to the directory containing PKGBUILD.  

This might be useful, for example, if the source for some daemon doesn't provide a 
systemd service file, and the packager adds one. If that file is in *_mkpkg_depends_files*,
then changes to the file trigger rebuilds.

These variables offer considerable control over what can be used to trigger rebuilds.

For example::

    _mkpkg_depends_file=('xxx.service')

This directs a rebuild when the file *xxx.service* changes.

Variable _dep_vers_prog
-----------------------

In cases where a dependent package being used to build against is not yet installed,
then it's version cannot be extracted by calling *pacman -Qi*. Instead, a script
can be provided in PKGBUILD which returns the version of the package name provided
as an argument.

For example if we have the following dependencies where *foo* and *goo* are used but
not yet installed on the build machine (at least not the version being built against)::

   _mkpkg_depends=('python>minor', 'openssl>3.0', 'foo', 'goo')

   declare -A _dep_vers_prog
   _dep_vers_prog['foo']='./dep-vers'
   _dep_vers_prog['goo']='./dep-vers'

where the script *./dep-vers* returns the version of it's one argument - where
arguments can be *foo* or *goo*.

One example is pigeonhole and dovecot. This are in separate git repos and built
as separate packages. pigeonhole is built against the just compiled version
of dovecot. In this case a script which extracts *pkgver* from the .PKGINFG file
either in the dovecot *pkg* directory, or by extracting it from the just built 
package does the trick.


