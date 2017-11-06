# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
"""Input Label.

This module contains the Label Input
"""

__all__ = ['Input']

import re
from tebless.devs import Widget, echo
from tebless.utils.keyboard import KEY_BACKSPACE, KEY_DELETE

class Input(Widget):
    """Input widget with label.

    :param text: placeholder text
    :param label: Desc of input
    :param align: center, ljust, rjust text
    :param fill_c: blank space
    :param cursor: pointer
    :param left_l: left terminator
    :param right_l: right terminator
    :param max_len: max string length
    :param validation: a regex string to validate input
    :param text_style: apply to text
    :type text: str
    :type label: str
    :type align: str
    :type fill_c: str
    :type cursor: str
    :type left_l: str
    :type right_l: str
    :type max_len: int
    :type validation: regex
    :type text_style: func

    :Example:

    >>> from tebless.widgets import Input, Window
    >>> @Window.decorator(main=True)
    ... def view(window):
    ...     window += Input(label="Insert text", cordx=2,
    ...                     cordy=2, width=10, align='center')

    """
    def __init__(self,
                 text='',
                 label='',
                 align='left',
                 max_len=6,
                 *args, **kwargs):
        params = dict(text=text, label=label, max_len=round(max_len))
        super().__init__(on_key=self._on_key, *args, **params, **kwargs)
        self._text = text
        self._label = label

        self._max_len = round(max_len)
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


    def _on_key(self, key):
        correct_len = self.term.length(self.value) < self._max_len
        validations = re.match(self._validation, key) and key.isprintable()

        #TODO: Add event on fail validation
        if correct_len and validations:
            self.value += key
        elif key.code in (KEY_BACKSPACE, KEY_DELETE) and self.value:
            self.value = self.value[:-1]

    def paint(self):
        text = self._text_style(self.value)
        if self.term.length(self.value) < self._max_len:
            text = text + self._cursor
        text = self._align(text, fillchar=self._fill_c, width=self._max_len)

        input_field = self._left_l + text + self._right_l # [_______]

        echo(self.term.move(self.y, self.x) + self._label + input_field) # label

    @property
    def width(self):
        len_widget = self.term.length(self._label) + self.term.length(self._right_l)
        len_widget += self.term.length(self._left_l) + self._max_len
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
