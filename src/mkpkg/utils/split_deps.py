"""
 Package dependency support tools for MkPkg class
    - split_deps_vers_list()
        splits depends list into 2 lists:
        mkpkg.depends       - package names with no version requirement
        mkpkg.depends_vers  - packages with version requirements
"""
# pylint: disable=R0912,R0915
from .dep_vers import read_last_dep_vers

def _split_pkg_vers_constraint(opers, item):
    """
    Takes a string in form 'pkgname oper vers'
        where oper is one of the opers list
        returns (pkgname, oper,  vers)
        opers can be: '>', '>=' or '<' (the latter being to handle downgrades: pkg<last
    """
    pkg = None
    oper = None
    vers_trigger = None
    for oper_try in opers:
        if oper_try in item:
            oper = oper_try
            isplit = item.split(oper)
            pkg = isplit[0].strip()
            if len(isplit) > 1:
                if '>=' in isplit:
                    vsplit = isplit[1].split('=')
                    if len(vsplit) > 1:
                        vers_trigger = vsplit[1]
                    else:
                        vers_trigger = isplit[1].strip()
            break

    return (pkg, oper, vers_trigger)

def split_deps_vers_list(mkpkg):
    """
    Splits the mkpkg.depends list into 2 lists:
        mkpkg.depends       - package names with no version requirement
        mkpkg.depends_vers  - packages with version requirements
    """
    if not mkpkg.depends:
        return

    dep_names = []
    dep_vers = []
    opers = mkpkg.dep_vers_opers
    for item in mkpkg.depends:
        (pkg, oper, vers_trigger) = _split_pkg_vers_constraint(opers, item)
        if oper:
            this = (pkg, oper, vers_trigger)
            dep_vers.append(this)
        else:
            pkg = item.strip()
            dep_names.append(pkg)

    mkpkg.depends_vers = dep_vers
    mkpkg.depends = dep_names

    if mkpkg.depends_vers:
        mkpkg.dep_vers_last = read_last_dep_vers(mkpkg)
