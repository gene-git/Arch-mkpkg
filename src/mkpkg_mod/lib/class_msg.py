# SPDX-License-Identifier: GPL-2.0-or-later
# SPDX-FileCopyrightText: © 2022-present Gene C <arch@sapience.com>
"""
 Screen output with indent and color
 Messages are written to stdout
 Colors are turned off if non-tty
"""
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments, too-many-positional-arguments
from typing import TextIO
import sys
from .color_pick import color_pick


def _txt_list_expand_newlines(txt_list: list[str]) -> list[str]:
    """
    List Elements split by newlines expand the list
    """
    new_list: list[str] = []
    for item in txt_list:
        item_expanded = item.splitlines(keepends=True)
        new_list += item_expanded
    return new_list


class _AscCol:
    """
    Ascii Colors
    """
    # pylint: disable=
    def __init__(self, theme: str = 'dark'):
        self.theme = theme
        self.color_map = {
                'blue': '27',
                'cyan': '51',
                'green': '10',
                'orange': '9',
                'pink': '13',
                'red': '196',
                'tan': '208',
                'yellow': '11',
                'white': '254',
                'warn': '11',
                'fail': '160',
                'error': '196',
                'info': '208',
                'hdr': '227',
                }
        self.col_list = list(self.color_map.keys())

    def _lookup_color_number(self, color: str) -> str:
        """
        Maps first letter of color name to ascii color number (256 color)
        """
        color_num = color
        if isinstance(color, str):
            # match color and retrieve it's ascii color number
            color_matched = color_pick(color, self.col_list)
            if color_matched:
                color_num = self.color_map[color_matched]
                return color_num

        if color.isdigit():
            return color

        # unknown and not a number
        color_num = '254'
        if self.theme and self.theme.lower().startswith('l'):
            color_num = '0'

        return color_num

    def colorize(self,
                 txt: str,
                 fg: str = '',
                 bg: str = '',
                 bold: bool = False) -> str:
        """
        Colorize a string using 256 color ascii escapes
        Colors are a few names or digit from 0-255
        """
        esc = '\033['
        a_fg = '38;5;'
        a_bg = '48;5;'
        a_off = '0'
        # under = '\033[4m'

        a_bold = ''
        col_fg = ''
        col_bg = ''
        if bold:
            a_bold = ';1'

        if fg:
            col_fg = self._lookup_color_number(fg)
            col_fg = f'{a_fg}{col_fg}'

        if bg:
            col_bg = self._lookup_color_number(bg)
            col_bg = f'{a_bg}{col_bg}'

        if fg or bg or bold:
            ctxt = f'{esc}{col_fg}{col_bg}{a_bold}m{txt}{esc}{a_off}m'
        else:
            ctxt = txt

        return ctxt


class Msg:
    """
    Msg class - handles screen writes
    see msg() and companion methods
        indent sets initial indent
        indent_char provides a char to print before every text
    """
    # pylint: disable=
    def __init__(self,
                 indent: str = 4*' ',
                 theme: str = 'dark'):
        self.color = _AscCol(theme)
        self.fpo: TextIO = sys.stdout
        self.indent: str = indent
        self.tty: bool = False

        if self.fpo.isatty():
            self.tty = True

    def _msg(self,
             lead: str,
             txt: str | list[str],
             fg: str = '',
             bg: str = '',
             bold: bool = False):
        """
        Writes text (string or list of strings)

        lead  - prepended to each line.
        color - if set, then text will be colored according to its value
        """
        if isinstance(txt, list):
            txt_list = txt
        else:
            txt_list = [txt]

        for line in txt_list:
            ctxt = lead + line
            if self.tty:
                ctxt = self.color.colorize(ctxt, fg=fg, bg=bg, bold=bold)
            self.fpo.write(ctxt)
        self.fpo.flush()

    def msg(self,
            txt: str | list[str],
            adash: bool = False,
            bdash: bool = False,
            ind: int = 0,
            fg: str = '',
            bold: bool = False):
        """
        Handles the work for messages with header or footer (dashes)

        txt can be string or list of strings
        Single string can contain newlines.

         - adash:
           If True then add dashes on line above the text. (False)
         - bdash:
           If True then add dashes on line below the text. (False)
         - ind: indent amount (in steps of 4) (0)
         - fg: ascii color uses first letter or use number 0-254 ('w')
              blue Bold cyan fail red green head under warn
        """
        # pylint: disable=
        # Make it a list and split newlines into separate rows
        txt_list: list[str]
        if isinstance(txt, list):
            txt_list = txt
        else:
            txt_list = [txt]
        txt_list = _txt_list_expand_newlines(txt_list)

        dashes = ''
        if adash or bdash:
            longest = 1 + max(len(line) for line in txt_list)
            dashes = longest * '-'

        # initial indent
        lead = ind * self.indent

        # dashes above
        if adash:
            self._msg(lead, [dashes, '\n'], fg=fg, bold=bold)

        # body
        self._msg(lead, txt_list, fg=fg, bold=bold)

        # dashes below
        if bdash:
            self._msg(lead, [dashes, '\n'], fg=fg, bold=bold)
