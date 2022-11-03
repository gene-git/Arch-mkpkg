"""
 Package dependency support tools for MkPkg class
    - split_deps_vers_list()
        splits depends list into 2 lists:
        mkpkg.depends       - package names with no version requirement
        mkpkg.depends_vers  - packages with version requirements
"""
# pylint: disable=R0912,R0915
from .dep_vers import read_last_dep_vers

def _split_pkg_vers_constraint(mkpkg, item):
    """
    Takes a string in form 'pkgname oper vers'
        where oper is one of the opers list
        returns (pkgname, oper,  vers)
        opers can be: '>', '>=' or '<' (the latter being to handle downgrades: pkg<last
    """
    pkg = None
    oper = None
    vers_trigger = None
    wmsg = mkpkg.wmsg

    #
    # add white space
    #
    xitem = item.replace('>', ' > ')
    xitem = xitem.replace('<', ' < ')
    xitem = xitem.replace('< =', '<= ')
    xitem = xitem.replace('> =', '>= ')

    splitem = xitem.split()
    num_items = len(splitem)
    if num_items == 1:
        pkg = splitem[0]

    elif num_items == 2:
        # incomplete either a) (pkg oper) or (pkg vers)
        # we can return orig or first piece as it makes no sense
        # we return orig
        pkg = item.strip()
        wmsg(f'Error _mkpkg_depends item should be "X" or "X>Y" etc. Got: {item}')

    elif num_items == 3:
        pkg = splitem[0]
        oper = splitem[1]
        vers_trigger = splitem[2]

    else:
        # ug - also makes no sense
        pkg = item.strip()
        wmsg(f'Error _mkpkg_depends item should be "X" or "X>Y" etc. Got: {item}')

    return (pkg, oper, vers_trigger)



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
        (pkg, oper, vers_trigger) = _split_pkg_vers_constraint(mkpkg, item)
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
