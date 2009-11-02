import os
import sys

from curses import setupterm, tigetstr, tigetnum, tigetflag, tparm

ansi_colors = 'black red green yellow blue magenta cyan white'.split()
colors = 'black blue green cyan red magenta yellow white'.split()

meta_caps = [ { 'cap': 'sgr0', 'type': 'str', 'name': 'reset' },
              { 'cap': 'cols', 'type': 'int', 'name': 'height' },
              ]

class Termcap:
    def __init__(self):
        self._init_fg_colors()
        self._init_meta_caps()

        try:
            setupterm()
            self.set_fg_colors()
            self.set_meta_caps()
        except:
            pass

    def _init_fg_colors(self):
        for color in colors:
            setattr(self, color, '')

    def set_fg_colors(self):
        if tigetstr('setaf'):
            for i, color in enumerate(ansi_colors):
                setattr(self,
                        color,
                        tparm(tigetstr('setaf'), i))
        elif curses.tigetstr('setf'):
            for i, color in enumerate(colors):
                setattr(self,
                        color,
                        tparm(tigetstr('setf'), i))

    def _init_meta_caps(self):
        for cap in meta_caps:
            setattr(self, cap['name'], '')

    def set_meta_caps(self):
        for cap in meta_caps:
            param = ''
            if cap['type'] == 'str':
                param = tigetstr(cap['cap']) or ''
            elif cap['type'] == 'int':
                param = tigetnum(cap['cap']) or ''
            elif cap['type'] == 'bool':
                param = tigetflag(cap['cap']) or ''
            setattr(self, cap['name'], param)
