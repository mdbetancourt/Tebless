# Copyright (c) 2017 Michel Betancourt
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from tebless.devs import echo
from tebless.utils.constants import KEY_F1
from tebless.devs import Widget

class CheckBox(Widget):
    def __init__(self,
                 label='CheckBox',
                 key=KEY_F1,
                 state=False,
                 *args, **kwargs):
        super().__init__(on_key=self._on_key, *args, **kwargs)
        self._label = label
        self._state = state
        self._key = key

    def paint(self):
        echo(self.term.move(self.y, self.x))
        echo(self._check + self._label)

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value
        self.on_change()
