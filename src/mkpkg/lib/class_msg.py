# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2022-present  Gene C <arch@sapience.com>
"""
 Screen output with indent and color
 Messages are written to stdout
 Colors are turned off if non-tty
"""
import sys
from .text import str_iter
from .color_pick import color_pick

def _txt_list_expand_newlines (txt_list):
    """
    List Elements split by newlines expand the list
    """
    new_list = []
    for item in txt_list:
        item_expanded = item.splitlines(keepends=True)
        new_list = new_list + item_expanded
    return new_list

class AscCol:
    """
    Ascii Color
    """
    # pylint: disable=R0903
    def __init__(self):
        self.color_map = {
                'blue'      : 27,
                'cyan'      : 51,
                'green'     : 10,
                'orange'    : 9,
                'pink'      : 13,
                'red'       : 196,
                'tan'       : 208,
                'yellow'    : 11,
                'white'     : 254,
                'warn'      : 11,
                'fail'      : 160,
                'error'     : 196,
                'info'      : 208,
                'hdr'       : 227,
                }
        self.col_list = list(self.color_map.keys())

    def _lookup_color_number(self, color):
        """
        Maps first letter of color name to ascii color number (256 color)
        """
        color_num = color
        if isinstance(color, str):
            # match color and retrieve it's ascii color number
            color_matched = color_pick(color, self.col_list)
            if color_matched:
                color_num = self.color_map[color_matched]
            else:
                color_num = 254     # unknown - make it white

        return color_num

    def colorize (self, txt, fg=None, bg=None, bold=False):
        """
        Colorize a string using 256 color ascii escapes
        Colors are a few names or digit from 0-255
        """
        esc = '\033['
        set_fg = '38;5;'
        set_bg = '48;5;'
        set_off = '0'
        #under = '\033[4m'

        set_bold = ''
        color_fg = ''
        color_bg = ''
        if bold:
            set_bold = ';1'

        if fg :
            color_fg = self._lookup_color_number(fg)
            color_fg = f'{set_fg}{color_fg}'

        if bg :
            color_bg = self._lookup_color_number(bg)
            color_bg = f'{set_bg}{color_bg}'

        if fg or bg or bold:
            color_txt = f'{esc}{color_fg}{color_bg}{set_bold}m{txt}{esc}{set_off}m'
        else:
            color_txt = txt

        return color_txt


class GcMsg:
    """
    GcMsg class - handles screen writes
    see msg() and companion methods
        indent sets initial indent
        indent_char provides a char to print before every text
    """
    # pylint: disable=R0903
    def __init__(self, indent=4*' '):
        self.color = AscCol()
        self.fpo = sys.stdout
        self.indent = indent
        self.tty = False
        if self.fpo.isatty():
            self.tty = True

    def _msg(self, lead, txt, fg=None, bg=None, bold=False):
        """
        Writes text (string or list of strings)
            lead  - prepended to each line.
            color - if set, then text will be colored according to its value
        """
        # pylint: disable=R0913,R0917
        for line in str_iter(txt):
            #if self.tty and fg and fg != '':
            if self.tty :
                ctxt = self.color.colorize (lead + line, fg=fg, bg=bg, bold=bold)
            else:
                ctxt = lead + line
            self.fpo.write(ctxt)
        self.fpo.flush()

    def msg(self, txt, adash=None, bdash=None, ind=0, fg=None, bold=False):
        """
        Handles the work for messages with header or footer (dashes)

        txt can be string or list of strings
        Single string can contain newlines.
            adash   : If True then add dashes on line above the text. (Default False)
            bdash   : If True then add dashes on line below the text. (Default False)
            ind     : indent amount (in steps of 4) (Default 0)
            fg      : ascii color uses first letter or use number 0-254 (Default 'w')
                      blue Bold cyan fail red green head under warn
        """
        # pylint: disable=R0913,R0917
        # always need list and we also split newlines into separate rows
        txt_list = txt
        if not isinstance(txt, list):
            txt_list = [txt]
        txt_list = _txt_list_expand_newlines(txt_list)

        dashes = ''
        if adash or bdash:
            longest = 1 + max( len(line) for line in txt_list)
            dashes = longest *  '-'

        # initial indent
        lead = ind * self.indent

        # dashes above
        if adash:
            self._msg(lead, [dashes,  '\n'], fg=fg, bold=bold)

        # body
        self._msg(lead, txt_list, fg=fg, bold=bold)

        # dashes below
        if bdash:
            self._msg(lead, [dashes, '\n'], fg=fg, bold=bold)
