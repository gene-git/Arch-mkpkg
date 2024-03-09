# SPDX-License-Identifier: MIT
# Copyright (c) 2022,2023 Gene C
"""
soname tools
"""
import os
from elftools.elf.elffile import ELFFile
from elftools.common.exceptions import ELFError
from .run_prog import run_prog

def file_is_elf(filename):
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
        except ELFError :
            pass
    return is_elf

def sonames_in_elf_file(elf_file):
    """
    Extract list of sonames
      each item is full path to versioned library (path)
      e.g. (/usr/lib/libressl.so.56)
    """
    sonames = []
    if not os.path.exists(elf_file):
        return sonames

    pargs = ['/usr/bin/ldd', elf_file]
    [retc, output, _errors] = run_prog(pargs)
    if retc == 0 and output:
        rows = output.splitlines()
        for row in rows:
            if 'linux-vdso.so' in row or  'ld-linux' in row:
                continue

            srow = row.strip().split()
            if len(srow) < 3:
                continue

            #
            # check for library version - executable uses soname so we do as well
            # even if foo.so -> /usr/lib/lib/foo.so.NNN
            #
            soname = srow[0]
            libname = srow[2]
            vsplit = soname.split('.so.')
            if len(vsplit) < 2:
                continue

            if libname not in sonames:
                sonames.append(libname)
    return sonames
