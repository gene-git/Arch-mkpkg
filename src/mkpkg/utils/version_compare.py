"""
 Package dependency support tools for MkPkg class
    - version comparison tools
"""
from packaging import version

def _semantic_vers_parse(vers):
    """
    split semantic version into its components
        major.minor.patch
    """
    major = None
    minor = None
    patch = None
    if vers:
        vsplit = vers.split('.')
        major = vsplit[0].strip()
        if len(vsplit) > 1:
            minor = vsplit[1].strip()
            if len(vsplit) > 2:
                patch = vsplit[2].strip()

    return (major, minor, patch)


def _versions_to_compare(vers_trigger, pkg_vers, last_vers):
    """
    Extract whats needed to compare versions.
    think don't need last_vers_comp can use last_vers always
    Returns:   (pkg_vers_comp, last_vers_comp)
    """
    #(last_major, last_minor, last_patch) = _semantic_vers_parse(last_vers)
    (pkg_major, pkg_minor, pkg_patch) = _semantic_vers_parse(pkg_vers)

    last_vers_comp = last_vers
    if not vers_trigger:
        pkg_vers_comp = pkg_vers
        return (pkg_vers_comp, last_vers_comp)

    match(vers_trigger):
        case 'last':
            #last_vers_comp = last_vers
            pkg_vers_comp = pkg_vers

        case 'major':
            #last_vers_comp = last_major
            pkg_vers_comp = pkg_major

        case 'minor':
            #last_vers_comp = f'{last_major}.{last_minor}'
            pkg_vers_comp = f'{pkg_major}.{pkg_minor}'

        case 'patch':
            #last_vers_comp = f'{last_major}.{last_minor}.{last_patch}'
            pkg_vers_comp = f'{pkg_major}.{pkg_minor}.{pkg_patch}'

        case _:
            #
            # specific version
            # Handle same as above if major.minor or major etc
            #
            (trig_major, trig_minor, trig_patch) = _semantic_vers_parse(vers_trigger)
            if trig_patch:
                #last_vers_comp = f'{trig_major,}.{trig_minor}.{trig_patch}'
                pkg_vers_comp = f'{pkg_major}.{pkg_minor}.{pkg_patch}'

            elif trig_minor:
                #last_vers_comp = f'{trig_major,}.{trig_minor}'
                pkg_vers_comp = f'{pkg_major}.{pkg_minor}'

            elif trig_major :
                #last_vers_comp = f'{trig_major,}'
                pkg_vers_comp = f'{pkg_major}'

            else:
                #last_vers_comp = vers_trigger
                pkg_vers_comp = pkg_vers

    return (pkg_vers_comp, last_vers_comp)

def check_version_trigger(mkpkg, oper, vers_trigger, pkg_vers, last_vers):
    """
    Check if the version trigger is true
        vers_trigger :
            specific version, or one of key words 'major' 'minor', 'patch' 'last'
        oper :
            - '>' or '>='
        pkg_vers
            - current version of package
        last_vers
            - version of package when this was last built
    Returns:
        (trigger, pkg_vers_comp, last_vers_comp)
        where trigger is True if package is to be rebuilt
        The package vers and last_vers are what was use for the final comparison.
    """

    if not last_vers:
        trigger = True
        return (trigger, pkg_vers, last_vers)

    if not pkg_vers:
        trigger = False
        return (trigger, pkg_vers, last_vers)

    (pkg_vers_comp, last_vers_comp) = _versions_to_compare(vers_trigger, pkg_vers, last_vers)

    match(oper):
        case '>=':
            trigger = version.parse(pkg_vers_comp) >= version.parse(last_vers_comp)
        case '>':
            trigger = version.parse(pkg_vers_comp) >  version.parse(last_vers_comp)
        case '<':
            trigger = version.parse(pkg_vers_comp) <  version.parse(last_vers_comp)
        case _:
            msg = mkpkg.msg
            msg(f'Unkown package version operator : {oper} ignoring\n', fg_col='yellow', ind=1)

    return (trigger, pkg_vers_comp, last_vers_comp)
