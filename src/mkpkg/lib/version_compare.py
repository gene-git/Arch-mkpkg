# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
 Package dependency support tools for MkPkg class
    - version comparison tools
"""
from collections.abc import (Callable)
import pyalpm    # type: ignore


def _semantic_vers_to_elems(vers: str) -> list[str]:
    """
    Split version into its components each separated by period:

    vers_components = [major, minor, patch, elem4, ele5, ...]

    While standard semantic versionong has 3 elements,
    we allow for 4 or more.

    NB. Arch pkgrel is always in the last element - and we handle it.
    We treat the pkgrel as an additional element in the list
    to ensure correct comparisons.

    e.g. Compare minor (or first_2) : 2.30-8   with 2.30-7
         Correct: same as 2.30 == 2.30
         Wrong: 2.30-8 > 20.30-7

    Return list of elements [elem1, elem2, ...]
    """
    elems: list[str] = []
    if vers:
        # Split by period
        vsplit = [elem.strip() for elem in vers.split('.')]

        # split out Arch pkgrel
        last = vsplit[-1]
        elems = vsplit[:-1] + last.rsplit('-', 1)

    return elems


def _vers_trigger_to_num_elems(vers_trigger: str) -> int:
    """
    Map First_N to integer N
        'major' is alias for 'First_1'
        'minor' is alias for 'First_2'
        'patch' is alias for 'First_3'
        'extra' is alias for 'First_4'
        'last' compares the entire version
        Also in use: major, minor, micro, releaselevel, serial
    """
    if not vers_trigger:
        return 0

    key = vers_trigger.lower()
    num_elems = 0
    match(key):
        case 'major':
            num_elems = 1
        case 'minor':
            num_elems = 2
        case 'patch':
            num_elems = 3
        case 'micro':
            num_elems = 3
        case 'extra':
            num_elems = 4
        case 'releaselevel':
            num_elems = 4
        case 'serial':
            num_elems = 5
        case 'last':
            num_elems = -1      # special case to match entire version string
        case _:
            if key.startswith('first_'):
                esplit = key.split('_')
                if len(esplit) > 1:
                    num_elems = int(esplit[1])

    return num_elems


def _elems_to_version(num: int, elems: list[str]) -> str:
    """
    simply concatenate the first 'num' elems:
     -> elem1.elem2.elem3...elem<num>
    """
    vers = ''
    if num <= 0 or not elems:
        return vers

    num = min(num, len(elems))
    vers = elems[0]
    for cnt in range(1, num):
        next_elem = elems[cnt]
        vers = f'{vers}.{next_elem}'

    return vers


def _versions_to_compare(vers_trigger: str, pkg_vers: str,
                         last_vers: str) -> tuple[str, str]:
    """
    Extract whats needed to compare current pkg_vers
    with last_vers used.

    Returns:   (pkg_vers_comp, last_vers_comp)
    """
    #
    # Use number of elements of trigger to get the version strings compare
    #
    num_elems = _vers_trigger_to_num_elems(vers_trigger)

    if num_elems > 0:
        pkg_vers_elems = _semantic_vers_to_elems(pkg_vers)
        last_vers_elems = _semantic_vers_to_elems(last_vers)

        pkg_vers_comp = _elems_to_version(num_elems, pkg_vers_elems)
        last_vers_comp = _elems_to_version(num_elems, last_vers_elems)
    else:
        pkg_vers_comp = pkg_vers
        last_vers_comp = last_vers

    return (pkg_vers_comp, last_vers_comp)


def check_version_trigger(msg: Callable[..., None],
                          oper: str,
                          vers_trigger: str,
                          pkg_vers: str,
                          last_vers: str) -> tuple[bool, str, str]:
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
        The package vers and last_vers are what was used
        for the final comparison.
    """
    # pylint: disable=c-extension-no-member
    if not last_vers:
        trigger = True
        return (trigger, pkg_vers, last_vers)

    if not pkg_vers:
        trigger = False
        return (trigger, pkg_vers, last_vers)

    (pkg_vers_comp, last_vers_comp) = (
            _versions_to_compare(vers_trigger, pkg_vers, last_vers)
            )

    # use pyalpm
    new_minus_old = pyalpm.vercmp(pkg_vers_comp, last_vers_comp)

    match(oper):
        case '>=':
            trigger = new_minus_old >= 0
        case '>':
            trigger = new_minus_old > 0
        case '<':
            trigger = new_minus_old < 0
        case _:
            msg(f'Unkown package version operator : {oper} ignoring\n',
                fg='yellow', ind=1)

    return (trigger, pkg_vers_comp, last_vers_comp)
