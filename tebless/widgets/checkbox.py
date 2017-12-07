# Copyright (c) 2017 Michel Betancourt
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from tebless.devs import echo
from tebless.utils.keyboard import KEY_F1  # pylint: disable=E0611
from tebless.devs import Widget


class CheckBox(Widget):
    def __init__(self,
                 label='CheckBox',
                 key=KEY_F1,
                 state=False,
                 render=None,
                 check=None,
                 *args, **kwargs):
        super().__init__(on_key=self._on_key, *args, **kwargs)
        self._label = label
        self._state = state
        self._render = render or '{check} {label}'
        self._check = check or (lambda _state: '[ ]' if _state else '[X]')
        self._key = key

    def paint(self):
        echo(self.term.move(self.y, self.x))
        echo(self._render.format(check=self._check(self._state),
                                 label=self._label))

    def _on_key(self, key):
        if key.code == self._key:
            self.value = not self.value

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value
        self.on_change()  # pylint: disable=E1101

    @property
    def value(self):
        return self._state

    @value.setter
    def value(self, value):
        if not isinstance(value, bool):
            raise TypeError('Only supported boolean')
        self._state = value
        self.on_change()  # pylint: disable=E1101
