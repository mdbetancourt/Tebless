# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from blessed import Terminal
from tebless.devs import Widget, echo

class Label(Widget):
    def __init__(self, *args, **kwargs):
        Widget.__init__(self, *args, **kwargs)
        self._text = kwargs.get('text', 'Label')
        self._prev = ''

    def _paint(self):
        echo(self.term.move(self.y, self.x) + self.value)

    @property
    def value(self):
        return self._text

    @value.setter
    def value(self, text):
        self._prev = self._text
        self._text = text
        self.on_change()

    def _destroy(self):
        width = self.term.length(self._prev)
        line = (' ' * width) + '\n'
        lines = line * self.height
        echo(self.term.move(self.y, self.x) + lines)

    @property
    def width(self):
        return self.term.length(self._text)

    @property
    def height(self):
        return 1
