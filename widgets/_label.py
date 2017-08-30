# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from tebless.utils.term import echo
from tebless.devs import Widget

class Label(Widget):
    def __init__(self, parent, **kwargs):
        Widget.__init__(self, parent, **kwargs)
        self._text = kwargs.get('text', 'Label')

    def paint(self):
        echo(self.term.move(self.y, self.x) + self.value)

    def __str__(self):
        return self._text
