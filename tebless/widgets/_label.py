# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from functools import partial

from blessed import Terminal
from tebless.devs import Widget, echo

class Label(Widget):
    def __init__(self, text='Label', align='left', width=20, *args, **kwargs):
        params = dict(text=text, align=align, width=width)
        Widget.__init__(self, *args, **params, **kwargs)
        self._text = text
        self._prev = ''
        if align == 'right':
            self._align = self.term.rjust
        elif align == 'center':
            self._align = self.term.center
        elif align == 'left':
            self._align = self.term.ljust
        else:
            raise ValueError("Only align center, left, right")


    def paint(self):
        value = self._align(self.value, width=self.width)
        echo(self.term.move(self.y, self.x) + value)

    @property
    def value(self):
        return self._text

    @value.setter
    def value(self, text):
        self._prev = self._text
        self._text = text
        self.on_change()

    def destroy(self):
        width = self.term.length(self._prev)
        line = (' ' * width) + '\n'
        lines = line * self.height
        echo(self.term.move(self.y, self.x) + lines)

    @property
    def height(self):
        return 1
