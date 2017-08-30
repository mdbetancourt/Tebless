# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""
    input.py



    Created by Michel Betancourt on 2017.
    Copyright (c) 2017 ACT. All rights reserved.
"""
__all__ = ['Input']

import re
from tebless.devs import Widget

from tebless.utils.term import echo

class Input(Widget):
    """ Input widget with label  """
    def __init__(self, parent, **kwargs):
        Widget.__init__(self, parent, **kwargs)

        self._label = kwargs.get('label', '')
        self._max_len = round(kwargs.get('max_len', 6))
        self._text = kwargs.get('text', '')

        if len(self._text) > self._max_len:
            raise ValueError('text is too long')

        self._text_style = kwargs.get('text_style', lambda x: x)
        self._validation = kwargs.get('validation', r'.')
        self._left_l = kwargs.get('left_l', ' [ ')
        self._right_l = kwargs.get('right_l', ' ]')
        self._fill_c = kwargs.get('fill_c', '_')
        self._cursor = kwargs.get('cursor', '_')

        align = kwargs.get('align', 'left')

        if align == 'center':
            self._align = self._term.center
        elif align == 'right':
            self._align = self._term.rjust
        elif align == 'left':
            self._align = self._term.ljust
        else:
            raise ValueError(f'No existe {align}')

    def listen(self):
        delete_keys = (self._term.KEY_BACKSPACE, self._term.KEY_DELETE)
        
        key = self._term.inkey(timeout=0.2)
        if key.isprintable() and len(self._text) < self._max_len and key != '':
            if re.match(self._validation, key) is not None:
                self._text += key
                self._on_change(self)

        elif key.code in delete_keys and len(self._text) > 0:
            self._text = self._text[:-1]
            self._on_change(self)      
        elif key.code == self._term.KEY_ESCAPE or key == chr(3):
            return -1
        elif key.code == self._term.KEY_ENTER:
            return self._on_enter(self) or 1
        return 0

    def paint(self):
        """ Print widget in the window """
        term = self._term
        text = self._text_style(self._text)
        if len(self._text) < self._max_len:
            text = text + self._cursor
        text = self._align(text, fillchar=self._fill_c, width=self._max_len)

        input_field = self._left_l + text + self._right_l

        echo(term.move(self.y, self.x) + self._label + input_field)

    @property
    def width(self):
        len_widget = len(self._label) + len(self._right_l)
        len_widget += len(self._left_l) + self._max_len
        return len_widget

    @property
    def height(self):
        return 1

    @property
    def value(self):
        return self._text

    @value.setter
    def value(self, value):
        if not isinstance(value, str):
            raise TypeError('Only supported string')
        self._text = value
