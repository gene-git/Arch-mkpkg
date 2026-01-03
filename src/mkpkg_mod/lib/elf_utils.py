# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present Gene C <arch@sapience.com>
"""
soname tools
"""
import os
from elftools.elf.elffile import ELFFile
from elftools.common.exceptions import ELFError

from .run_prog_local import run_prog


def file_is_elf(filename: str):
    """
    Return True if filename is elf executable
    """
    is_elf = False
    if not os.path.exists(filename):
        return is_elf

    with open(filename, 'rb') as fob:
        try:
            elffile = ELFFile(fob)
            header = elffile.header
            e_ident = header.get('e_ident')
            if e_ident:
                ei_class = e_ident.get('EI_CLASS')
                if ei_class and ei_class.startswith('ELFCLASS'):
                    is_elf = True
        except ELFError:
            pass

    return is_elf


def sonames_in_elf_file(elf_file: str) -> list[str]:
    """
    Extract list of sonames.

    each item is full path to library
    e.g. (/usr/lib/libressl.so.56)

    Discussion:
      We use ldd rather than objdump - this will pick up shared lib
      libxxx.so.1 even if doesn't have NEEDED in private header.
      e.g. nginx has soname dep on libresolv.so.2
      but "objdump -p" shows no NEEDED header (build problem perhaps).
      So we use ldd For shared libs use instead:
        "objdump -p <shared> | grep SONAME"
    """
    sonames: list[str] = []
    if not os.path.exists(elf_file):
        return sonames

    pargs = ['/usr/bin/ldd', elf_file]
    (retc, output, _errors) = run_prog(pargs)
    if retc == 0 and output:
        rows = output.splitlines()
        for row in rows:
            if 'linux-vdso.so' in row or 'ld-linux' in row:
                continue

            srow = row.strip().split()
            if len(srow) < 3:
                continue

            #
            # check library version.
            # executable uses soname so we do as well
            # even if foo.so -> /usr/lib/lib/foo.so.NNN
            #
            soname = srow[0]
            soname_path = srow[2]
            vsplit = soname.split('.so.')
            if len(vsplit) < 2:
                continue

            if soname_path not in sonames:
                sonames.append(soname_path)
    return sonames
