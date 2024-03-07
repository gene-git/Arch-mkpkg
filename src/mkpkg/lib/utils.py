# SPDX-License-Identifier: MIT
# Copyright (c) 2022,2024 Gene C
"""
General utilities
"""
import os

def os_scandir(tdir):
    """
    wrapper around scandir with exception handling
    """
    scan = None
    if os.path.exists(tdir) and os.path.isdir(tdir) :
        try:
            scan = os.scandir(tdir)
        except OSError as _error:
            scan = None
    return scan
