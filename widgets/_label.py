# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from tebless.utils.term import echo
from tebless.devs import Widget

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

    @property
    def width(self):
        return len(self._prev)
    @property
    def height(self):
        return 1
