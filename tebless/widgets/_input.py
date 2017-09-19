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
from tebless.devs import Widget, echo
from tebless.utils.constants import BACKSPACE, DEL

class Input(Widget):
    """Input widget with label.

    Params:
        text: str -- placeholder text
        label: str -- Desc of input
        align: styles -- center, ljust, rjust text
        fill_c: str -- blank space
        cursor: str -- pointer
        left_l: str -- left terminator
        right_l: str -- right terminator
        max_len: int -- max string lenght
        validation: regex -- a regex string to validate input
        text_style: func -- apply to text

    """
    def __init__(self, text='', label='', max_len=6, *args, **kwargs):
        params = dict(text=text, label=label, max_len=round(max_len))
        Widget.__init__(self, on_key=self._on_key, *args, **params, **kwargs)
        self._text = text
        self._label = label

        self._max_len = round(max_len)
        align = kwargs.get('align', 'left')
        self._fill_c = kwargs.get('fill_c', '_')
        self._cursor = kwargs.get('cursor', '_')

        self._left_l = kwargs.get('left_l', ' [ ')
        self._right_l = kwargs.get('right_l', ' ]')
        self._validation = kwargs.get('validation', r'.')
        self._text_style = kwargs.get('text_style', lambda x: x)

        if align == 'left':
            self._align = self.term.ljust
        elif align == 'center':
            self._align = self.term.center
        elif align == 'right':
            self._align = self.term.rjust
        else:
            raise ValueError('Only valids aligns: left, right, center')

        if self.term.length(self._text) > self._max_len:
            raise ValueError('text is too long')
        elif self.term.length(self._fill_c) > 1:
            raise ValueError('fill_c need a char')
        elif self.term.length(self._cursor) > 1:
            raise ValueError('cursor need a char')


    def _on_key(self, *_, **kwargs):
        key = kwargs.get('key')
        correct_len = len(self.value) < self._max_len
        validations = re.match(self._validation, key) and key.isprintable()

        #TODO: Add event on fail validation
        if correct_len and validations:
            self.value += key
        elif key.code in (BACKSPACE, DEL) and self.value:
            self.value = self.value[:-1]

    def paint(self):
        text = self._text_style(self.value)
        if len(self.value) < self._max_len:
            text = text + self._cursor
        text = self._align(text, fillchar=self._fill_c, width=self._max_len)

        input_field = self._left_l + text + self._right_l # [_______]

        echo(self.term.move(self.y, self.x) + self._label + input_field) # label 

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

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        if not isinstance(value, str):
            raise TypeError('Only supported string')
        self._label = value
        self.on_change()

    @value.setter
    def value(self, value):
        if not (isinstance(value, str) or isinstance(value, int)):
            raise TypeError('Only supported string or int')
        self._text = str(value)
        self.on_change()
